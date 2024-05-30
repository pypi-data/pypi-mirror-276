import re
from typing import Callable, Optional, Union

import clearskies

class SMS:
    def __init__(self, twilio, di) -> None:
        self.twilio = twilio
        self.di = di

    def configure(
        self,
        from_number: Optional[Union[str, Callable]] = None,
        to_number: Optional[Union[str, Callable]] = None,
        message: Optional[Union[str, Callable]] = None,
        when: Optional[Callable] = None,
    ) -> None:
        """Configure the rules for this SMS notification."""
        self._required_str_or_callable_check(message, "message")
        self._required_str_or_callable_check(from_number, "from_number")
        self._required_str_or_callable_check(to_number, "to_number")

        if when and not callable(when):
            raise ValueError("Config 'when' for twilio.actions.sms should be a callable, but isn't.")

        self.when = when
        self.message = message
        self.from_number = from_number
        self.to_number = to_number

    def _required_str_or_callable_check(self, item: Union[str, Callable], label: str) -> None:
        if not item:
            raise ValueError(f"Config '{label}' for twilio.actions.sms is required, but was not provided.")

        if not isinstance(item, str) and not callable(item):
            bad_type = item.__class__.__name__
            raise ValueError(
                f"Config '{label}' for twilio.actions.sms should be a string or a callable, but instead is a '{bad_type}'"
            )
        return

    def __call__(self, model: clearskies.Model) -> None:
        """Send a notification as configured."""
        if self.when and not self.di.call_function(self.when, model=model):
            return

        from_number = self._resolve_number(self.from_number, "from_number", model)
        to_number = self._resolve_number(self.to_number, "to_number", model)
        if not from_number or not to_number:
            return
        message = self._resolve_message(self.message, model)
        self.twilio.messages.create(**{
            "to":to_number,
            "from":from_number,
            "body":message,
        })

    def _resolve_number(self, number: Union[str, Callable], label: str, model: clearskies.Model) -> str:
        """
        Convert self.from_number or self.to_number to an actual phone number.

        We can receive a few things:

         1. A phone number
         2. The name of a column from the model
         3. A callable that returns a phone number

        Note that the actual phone numbers may not be in the correct format expected by twilio.
        """
        model_label = model.id_column_name + ": " + model.get(model.id_column_name)
        if callable(number):
            number = self.di.call_function(number, model=model)
            if not number:
                return None
            if not isinstance(number, str):
                raise ValueError(f"Error with clearskies_twilio.actions.sms: I executed the callable attached to '{label}' but it did not return a string.  The callable must return a phone number as a string.")
        else:
            # do we have a column name?
            if number in model.columns():
                number = model.get(number)
            if not number:
                return None
            if not isinstance(number, str):
                raise ValueError(f"Error with clearskies_twilio.actions.sms: I fetched a column called '{label}' for model {model_label}, hoping for a phone number, but it returned a non-string.  The column must return a phone number as a string.")


        # now make sure we have a twilio friendly number
        number = re.sub(r"\D", "", number)
        if not number:
            raise ValueError(f"Error with clearskies.twilio.actions.sms: while fetching the '{label}' for model {model_label} I ended up with something that just doesn't look like a phone number.")
        if len(number) == 10:
            number = f"1{number}"
        return f"+{number}"

    def _resolve_message(self, message: Union[Callable, str], model: clearskies.Model) -> str:
        """Build the string for the message given the model."""
        if callable(message):
            message = self.di.call_function(message, model=model)
            if not message:
                raise ValueError(f"Error with clearskies.twilio.actions.sms: I executed the callable attached to 'message' but it returned a non-value.  The callable must return a message as a string.  In case this helps, you can provide a callable to 'when' and have it return false in csaes where you don't want a message sent.")
            if not isinstance(message, str):
                raise ValueError(f"Error with clearskies_twilio.actions.sms: I executed the callable attached to 'message' but it did not return a string.  The callable must return a message as a string.")

        return message
