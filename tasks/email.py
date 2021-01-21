from typing import List, Union, Tuple
from app.utils import get_logger, celery_app
from vendor import Mail, Message

logger = get_logger(__name__)


def get_config() -> Tuple[str, int, bool, bool, str, str, str]:
    from app import config

    server: str = getattr(config, "MAIL_SERVER")
    port: int = getattr(config, "MAIL_PORT")
    use_ssl: bool = getattr(config, "MAIL_USE_SSL")
    use_tls: bool = getattr(config, "MAIL_USE_TLS")
    username: str = getattr(config, "MAIL_USERNAME")
    password: str = getattr(config, "MAIL_PASSWORD")
    sender = getattr(config, "MAIL_DEFAULT_SENDER")
    return (server, port, use_ssl, use_tls, username, password, sender)


@celery_app.task(name="web_task.send_email")
def send_email(
    subject: str,
    recipients: List[str],
    sender: Union[str, None] = None,
    html: Union[None, str] = None,
    body: Union[None, str] = None,
):
    (server, port, use_ssl, use_tls, username, password,
     config_sender) = get_config()
    sender = sender or config_sender
    mail_client = Mail(
        server,
        username,
        password,
        port,
        use_ssl,
        use_tls,
        sender,
        None,
    )
    message = Message(subject, recipients, html=html, sender=sender, body=body)
    with mail_client.connect() as connect:
        message.send(connect)


def send_email_message(message: Message):
    (server, port, use_ssl, use_tls, username, password,
     config_sender) = get_config()
    sender = message.sender or config_sender
    if not message.sender:
        message.sender = sender

    mail_client = Mail(
        server,
        username,
        password,
        port,
        use_ssl,
        use_tls,
        sender,
        None,
    )
    mail_client.send(message)
