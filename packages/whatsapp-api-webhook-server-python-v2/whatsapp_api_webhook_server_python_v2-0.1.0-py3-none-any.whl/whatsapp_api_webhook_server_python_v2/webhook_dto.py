from typing import List, Optional

from pydantic import BaseModel, Field


class InstanceData(BaseModel):

    id_instance: Optional[int] = Field(None, alias="idInstance")
    wid: Optional[str] = Field(None, alias="wid")
    type_instance: Optional[str] = Field(None, alias="typeInstance")


class SenderData(BaseModel):

    chat_id: Optional[str] = Field(None, alias="chatId")
    sender: Optional[str] = Field(None, alias="sender")
    chat_name: Optional[str] = Field(None, alias="chatName")
    sender_name: Optional[str] = Field(None, alias="senderName")
    sender_contact_name: Optional[str] = Field(None, alias="senderContactName")


class TextMessageData(BaseModel):

    text_message: Optional[str] = Field(None, alias="textMessage")


class ExtendedTextMessageData(BaseModel):

    text: Optional[str] = Field(None, alias="text")
    description: Optional[str] = Field(None, alias="description")
    title: Optional[str] = Field(None, alias="title")
    jpeg_thumbnail: Optional[str] = Field(None, alias="jpegThumbnail")
    forwarding_score: Optional[int] = Field(None, alias="forwardingScore")
    is_forwarded: Optional[bool] = Field(None, alias="isForwarded")
    stanza_id: Optional[str] = Field(None, alias="stanzaId")
    participant: Optional[str] = Field(None, alias="participant")


class Contact(BaseModel):

    display_name: Optional[str] = Field(None, alias="displayName")
    vcard: Optional[str] = Field(None, alias="vcard")


class Location(BaseModel):

    name_location: Optional[str] = Field(None, alias="nameLocation")
    address: Optional[str] = Field(None, alias="address")
    jpeg_thumbnail: Optional[str] = Field(None, alias="jpegThumbnail")
    latitude: Optional[float] = Field(None, alias="latitude")
    longitude: Optional[float] = Field(None, alias="longitude")


class ExtendedTextMessage(BaseModel):

    description: Optional[str] = Field(None, alias="description")
    title: Optional[str] = Field(None, alias="title")
    preview_type: Optional[str] = Field(None, alias="previewType")
    jpeg_thumbnail: Optional[str] = Field(None, alias="jpegThumbnail")


class QuotedMessage(BaseModel):

    stanza_id: Optional[str] = Field(None, alias="stanzaId")
    participant: Optional[str] = Field(None, alias="participant")
    type_message: Optional[str] = Field(None, alias="typeMessage")
    text_message: Optional[str] = Field(None, alias="textMessage")
    download_url: Optional[str] = Field(None, alias="downloadUrl")
    caption: Optional[str] = Field(None, alias="caption")
    jpeg_thumbnail: Optional[str] = Field(None, alias="jpegThumbnail")
    contact: Optional[Contact] = Field(None, alias="contact")
    location: Optional[Location] = Field(None, alias="location")
    extended_text_message: Optional[ExtendedTextMessage] = Field(
        None, alias="extendedTextMessage"
    )


class FileMessageData(BaseModel):

    download_url: Optional[str] = Field(None, alias="downloadUrl")
    caption: Optional[str] = Field(None, alias="caption")
    file_name: Optional[str] = Field(None, alias="fileName")
    jpeg_thumbnail: Optional[str] = Field(None, alias="jpegThumbnail")
    is_animated: Optional[bool] = Field(None, alias="isAnimated")
    mime_type: Optional[str] = Field(None, alias="mimeType")
    forwarding_score: Optional[int] = Field(None, alias="forwardingScore")
    is_forwarded: Optional[bool] = Field(None, alias="isForwarded")


class LocationMessageData(BaseModel):

    nameLocation: Optional[str] = Field(None, alias="nameLocation")
    address: Optional[str] = Field(None, alias="address")
    jpeg_thumbnail: Optional[str] = Field(None, alias="jpegThumbnail")
    latitude: Optional[float] = Field(None, alias="latitude")
    longitude: Optional[float] = Field(None, alias="longitude")
    forwarding_score: Optional[int] = Field(None, alias="forwardingScore")
    is_forwarded: Optional[bool] = Field(None, alias="isForwarded")


class ContactMessageData(BaseModel):

    display_name: Optional[str] = Field(None, alias="displayName")
    vcard: Optional[str] = Field(None, alias="vcard")
    forwarding_score: Optional[int] = Field(None, alias="forwardingScore")
    is_forwarded: Optional[bool] = Field(None, alias="isForwarded")


class ContactsArrayMessage(BaseModel):

    contacts: Optional[List[Contact]] = Field(None, alias="contacts")
    forwarding_score: Optional[int] = Field(None, alias="forwardingScore")
    is_forwarded: Optional[bool] = Field(None, alias="isForwarded")


class Button(BaseModel):

    button_id: Optional[str] = Field(None, alias="buttonId")
    button_text: Optional[str] = Field(None, alias="buttonText")


class ButtonsMessage(BaseModel):

    content_text: Optional[str] = Field(None, alias="contentText")
    footer: Optional[str] = Field(None, alias="footer")
    buttons: Optional[List[Button]] = Field(None, alias="buttons")
    forwarding_score: Optional[int] = Field(None, alias="forwardingScore")
    is_forwarded: Optional[bool] = Field(None, alias="isForwarded")


class ListMessageRow(BaseModel):

    title: Optional[str] = Field(None, alias="title")
    row_id: Optional[str] = Field(None, alias="rowId")
    description: Optional[str] = Field(None, alias="description")


class ListMessageSection(BaseModel):

    title: Optional[str] = Field(None, alias="title")
    rows: Optional[List[ListMessageRow]] = Field(None, alias="rows")


class ListMessage(BaseModel):

    content_text: Optional[str] = Field(None, alias="contentText")
    title: Optional[str] = Field(None, alias="title")
    footer: Optional[str] = Field(None, alias="footer")
    button_text: Optional[str] = Field(None, alias="buttonText")
    sections: Optional[List[ListMessageSection]] = Field(None, alias="sections")


class TemplateMessageButtonUrlButton(BaseModel):

    display_text: Optional[str] = Field(None, alias="displayText")
    url: Optional[str] = Field(None, alias="url")


class TemplateMessageButtonCallButton(BaseModel):

    display_text: Optional[str] = Field(None, alias="displayText")
    phone_number: Optional[str] = Field(None, alias="phoneNumber")


class TemplateMessageButtonQuickReplyButton(BaseModel):

    display_text: Optional[str] = Field(None, alias="displayText")
    id: Optional[str] = Field(None, alias="id")


class TemplateMessageButton(BaseModel):

    index: Optional[int] = Field(None, alias="index")
    url_button: Optional[TemplateMessageButtonUrlButton] = Field(
        None, alias="urlButton"
    )
    call_button: Optional[TemplateMessageButtonCallButton] = Field(
        None, alias="callButton"
    )
    quick_reply_button: Optional[TemplateMessageButtonQuickReplyButton] = Field(
        None, alias="quickReplyButton"
    )


class TemplateMessage(BaseModel):

    content_text: Optional[str] = Field(None, alias="contentText")
    footer: Optional[str] = Field(None, alias="footer")
    buttons: Optional[List[TemplateMessageButton]] = Field(None, alias="buttons")
    forwarding_score: Optional[int] = Field(None, alias="forwardingScore")
    is_forwarded: Optional[bool] = Field(None, alias="isForwarded")


class GroupInviteMessageDataExpiration(BaseModel):

    low: Optional[int] = Field(None, alias="low")
    high: Optional[int] = Field(None, alias="high")
    unsigned: Optional[bool] = Field(None, alias="unsigned")


class GroupInviteMessageData(BaseModel):

    group_jid: Optional[str] = Field(None, alias="groupJid")
    invite_code: Optional[str] = Field(None, alias="inviteCode")
    invite_expiration: Optional[GroupInviteMessageDataExpiration] = Field(
        None, alias="inviteExpiration"
    )
    group_name: Optional[str] = Field(None, alias="groupName")
    caption: Optional[str] = Field(None, alias="caption")
    name: Optional[str] = Field(None, alias="name")
    jpeg_thumbnail: Optional[str] = Field(None, alias="jpegThumbnail")


class PollMessageOption(BaseModel):

    option_name: Optional[str] = Field(None, alias="optionName")


class PollMessageVote(BaseModel):

    option_name: Optional[str] = Field(None, alias="optionName")
    option_voters: Optional[List[str]] = Field(None, alias="optionVoters")


class PollMessageData(BaseModel):

    stanza_id: Optional[str] = Field(None, alias="stanzaId")
    name: Optional[str] = Field(None, alias="name")
    options: Optional[List[PollMessageOption]] = Field(None, alias="options")
    votes: Optional[List[PollMessageVote]] = Field(None, alias="votes")
    multiple_answers: Optional[bool] = Field(None, alias="multipleAnswers")


class ButtonsResponseMessage(BaseModel):

    stanza_id: Optional[str] = Field(None, alias="stanzaId")
    selected_button_id: Optional[str] = Field(None, alias="selectedButtonId")
    selected_button_text: Optional[str] = Field(None, alias="selectedButtonText")


class TemplateButtonReplyMessage(BaseModel):

    stanza_id: Optional[str] = Field(None, alias="stanzaId")
    selected_index: Optional[int] = Field(None, alias="selectedIndex")
    selected_id: Optional[str] = Field(None, alias="selectedId")
    selected_display_text: Optional[str] = Field(None, alias="selectedDisplayText")


class ListResponseMessage(BaseModel):

    stanza_id: Optional[str] = Field(None, alias="stanzaId")
    title: Optional[str] = Field(None, alias="title")
    list_type: Optional[int] = Field(None, alias="listType")
    single_select_reply: Optional[str] = Field(None, alias="singleSelectReply")


class MessageData(BaseModel):

    type_message: Optional[str] = Field(None, alias="typeMessage")
    text_message_data: Optional[TextMessageData] = Field(None, alias="textMessageData")
    extended_text_message_data: Optional[ExtendedTextMessageData] = Field(
        None, alias="extendedTextMessageData"
    )
    quoted_message: Optional[QuotedMessage] = Field(None, alias="quotedMessage")
    file_message_data: Optional[FileMessageData] = Field(None, alias="fileMessageData")
    location_message_data: Optional[LocationMessageData] = Field(
        None, alias="locationMessageData"
    )
    message_data: Optional[ContactsArrayMessage] = Field(None, alias="messageData")
    buttons_message: Optional[ButtonsMessage] = Field(None, alias="buttonsMessage")
    list_message: Optional[ListMessage] = Field(None, alias="listMessage")
    template_message: Optional[TemplateMessage] = Field(None, alias="templateMessage")
    group_invite_message_data: Optional[GroupInviteMessageData] = Field(
        None, alias="groupInviteMessageData"
    )
    poll_message_data: Optional[PollMessageData] = Field(None, alias="pollMessageData")
    button_response_message: Optional[ButtonsResponseMessage] = Field(
        None, alias="buttonsResponseMessage"
    )
    template_button_reply_message: Optional[TemplateButtonReplyMessage] = Field(
        None, alias="templateButtonReplyMessage"
    )
    list_response_message: Optional[ListResponseMessage] = Field(
        None, alias="ListResponseMessage"
    )


class DeviceData(BaseModel):

    platform: Optional[str] = Field(None, alias="platform")
    device_manufacturer: Optional[str] = Field(None, alias="deviceManufacturer")
    device_model: Optional[str] = Field(None, alias="deviceModel")
    os_version: Optional[str] = Field(None, alias="osVersion")
    wa_version: Optional[str] = Field(None, alias="waVersion")
    battery: Optional[int] = Field(None, alias="battery")


class AvatarInfo(BaseModel):

    chat_id: Optional[str] = Field(None, alias="chatId")
    url_avatar: Optional[str] = Field(None, alias="urlAvatar")


class QuotaData(BaseModel):

    method: Optional[str] = Field(None, alias="method")
    used: Optional[int] = Field(None, alias="used")
    total: Optional[int] = Field(None, alias="total")
    status: Optional[str] = Field(None, alias="status")
    description: Optional[str] = Field(None, alias="description")


class WebhookData(BaseModel):

    type_webhook: Optional[str] = Field(None, alias="typeWebhook")
    instance_data: Optional[InstanceData] = Field(None, alias="instanceData")
    timestamp: Optional[int] = Field(None, alias="timestamp")
    avatar_info: Optional[AvatarInfo] = Field(None, alias="avatarInfo")
    device_data: Optional[DeviceData] = Field(None, alias="deviceData")
    id_message: Optional[str] = Field(None, alias="idMessage")
    status: Optional[str] = Field(None, alias="status")
    description: Optional[str] = Field(None, alias="description")
    send_by_api: Optional[bool] = Field(None, alias="sendByApi")
    sender_data: Optional[SenderData] = Field(None, alias="senderData")
    message_data: Optional[MessageData] = Field(None, alias="messageData")
    state_instance: Optional[str] = Field(None, alias="stateInstance")
    status_instance: Optional[str] = Field(None, alias="statusInstance")
    status: Optional[str] = Field(None, alias="status")
    chat_id: Optional[str] = Field(None, alias="chatId")
    chat_state: Optional[str] = Field(None, alias="chatState")
    quota_data: Optional[QuotaData] = Field(None, alias="quotaData")
