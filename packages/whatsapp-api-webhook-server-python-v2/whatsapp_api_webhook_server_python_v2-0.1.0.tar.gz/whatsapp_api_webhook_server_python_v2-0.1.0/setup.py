from setuptools import setup

setup(
    name="whatsapp_api_webhook_server_python_v2",
    version="0.1.0",
    description=(
        "This library helps you easily create"
        " a Python server endpoint to receive"
        " WhatsApp message webhooks."
    ),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="GREEN API",
    author_email="support@green-api.com",
    url="https://github.com/green-api/whatsapp-api-webhook-server-python-v2",
    packages=["whatsapp_api_webhook_server_python_v2"],
    install_requires=[
        "fastapi==0.110.0",
        "uvicorn[standard]==0.30.0",
        "pydantic==2.7.1",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Natural Language :: English",
        "Natural Language :: Russian",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Communications",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    license=(
        "Creative Commons Attribution-NoDerivatives 4.0 International" " (CC BY-ND 4.0)"
    ),
)
