import clearskies

from typing import Callable, Union, Callable, Optional

from .sms import SMS
def sms(
    from_number: Optional[Union[str, Callable]] = "",
    to_number: Optional[Union[str, Callable]] = "",
    message: Optional[Union[str, Callable]] = "",
    when: Optional[Callable] = None,
):
    return clearskies.BindingConfig(
        SMS,
        from_number=from_number,
        to_number=to_number,
        message=message,
        when=when,
    )
__all__ = ["sms", "SMS"]
