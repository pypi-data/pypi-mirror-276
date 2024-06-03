import logging
import os
import signal
from typing import Annotated, Any, Callable, Dict, Optional, Union

import uvicorn
import uvicorn.config
from fastapi import Depends, FastAPI, Header, HTTPException, status

from .webhook_dto import WebhookData


class GreenAPIWebhookServer:
    """
    GreenAPI webhooks handler server class (based on `FastAPI`)

    Init args:
        - `host`: target host for receiving events
        - `port`: target port for receiving events
        - `event_handler`: callable object for handling events. Must receive two args:
        `webhook_type: str` & `webhook_data: dict`
        - `webhook_auth_header`: Your GreenAPI auth header key
        - `return_keys_by_alias: bool = False`: if this value is set to `True`,
        webhook keys will be returned in camelCase,
        otherwise in snake_case. Default `False` (snake_case)
        - `enable_info_logs: bool = False`: if this value is set to `True`,
        INFO logs from server will be enabled, otherwise - only ERROR.
        Default `False` (ERROR)

    call `.start()` method for starting server
    """

    def __init__(
        self,
        event_handler: Callable[[str, Dict[str, Any]], None],
        host: str = "0.0.0.0",
        port: int = 8080,
        webhook_auth_header: Optional[str] = None,
        return_keys_by_alias: bool = False,
        enable_info_logs: bool = False,
    ):
        self._host = host
        self._port = port
        self._event_handler = event_handler
        self._webhook_auth_header = webhook_auth_header
        self._return_keys_by_alias = return_keys_by_alias
        self._enable_info_logs = enable_info_logs

        self._init_server()

    def _handle_webhook(self, webhook_data: WebhookData, handler_func: Callable):
        """
        Handles the incoming webhook data by calling the event handler function
        """
        parsed_data = webhook_data.model_dump(
            exclude_none=True,
            by_alias=self._return_keys_by_alias,
        )
        handler_func(webhook_data.type_webhook, parsed_data)

    def _init_server(self):
        """
        Init webhooks listener server with provided data
        """

        self._server_app = FastAPI(docs_url=None)

        @self._server_app.post("/", status_code=status.HTTP_204_NO_CONTENT)
        def webhook_endpoint(
            webhook_data: WebhookData,
            authorization: Annotated[Union[str, None], Header()] = None,
            webhook_handler_func: Callable = Depends(lambda: self._event_handler),
            webhook_auth_header: Optional[str] = Depends(
                lambda: self._webhook_auth_header
            ),
        ):
            """
            Endpoint for receiving webhooks from GreenAPI

            If `WEBHOOK_AUTH_TOKEN` env provided, request's `authorization`
            header must be in format `Bearer {WEBHOOK_AUTH_TOKEN}`
            """
            if webhook_auth_header and authorization != f"Bearer {webhook_auth_header}":
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

            self._handle_webhook(webhook_data, webhook_handler_func)

        self._server_app.state.WEBHOOK_HANDLER_FUNC = self._event_handler
        self._server_app.state.WEBHOOK_AUTH_HEADER = self._webhook_auth_header

    def start(self):
        """
        Starts the FastAPI server and handles graceful shutdown.
        """
        try:
            uvicorn.run(
                app=self._server_app,
                host=self._host,
                port=self._port,
                reload=False,
                log_level=logging.INFO if self._enable_info_logs else logging.ERROR,
            )
        except KeyboardInterrupt:
            os.kill(os.getpid(), signal.SIGTERM)
