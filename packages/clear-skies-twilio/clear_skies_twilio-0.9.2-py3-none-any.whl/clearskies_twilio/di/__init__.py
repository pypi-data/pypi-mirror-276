import clearskies
from .twilio import Twilio

def twilio(
    path_to_api_key: str = "",
    path_to_api_secret: str = "",
    path_to_account_sid: str = "",
) -> clearskies.BindingConfig:
    return clearskies.BindingConfig(
        Twilio,
        path_to_api_key=path_to_api_key,
        path_to_api_secret=path_to_api_secret,
        path_to_account_sid=path_to_account_sid,
    )

__all__ = [
    "twilio",
    "Twilio",
]
