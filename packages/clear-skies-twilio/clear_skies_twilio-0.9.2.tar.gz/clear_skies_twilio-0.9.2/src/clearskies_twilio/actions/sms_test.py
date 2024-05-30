import unittest
from unittest.mock import MagicMock, call
from .sms import SMS
import clearskies
class SMSTest(unittest.TestCase):
    def setUp(self):
        self.di = clearskies.di.StandardDependencies()
        self.twilio = MagicMock()
        self.twilio.messages = MagicMock()
        self.twilio.messages.create = MagicMock()
        self.di.bind("twilio", self.twilio)

    def test_send(self):
        sms = SMS(self.twilio, self.di)
        sms.configure(
            from_number='1 (555) 123-4567', to_number='phone', message=lambda model: f"Welcome {model.name}!"
        )

        model = MagicMock()
        model.name = 'asdf'
        model.columns = MagicMock(return_value=["phone"])
        model.get = MagicMock(return_value="5551236789")
        sms(model)
        expected_call = {
            "to": "+15551236789",
            "from_": "+15551234567",
            "body": "Welcome asdf!",
        }
        self.twilio.messages.create.assert_called_once()
        assert expected_call == self.twilio.messages.create.call_args_list[0].kwargs
        model.get.assert_has_calls([call('phone')])

    def test_send_with_callable_number(self):
        sms = SMS(self.twilio, self.di)
        sms.configure(
            from_number=lambda model: "5551234567", to_number='phone', message="Welcome!"
        )

        model = MagicMock()
        model.name = 'asdf'
        model.columns = MagicMock(return_value=["phone"])
        model.get = MagicMock(return_value="5551236789")
        sms(model)
        expected_call = {
            "to": "+15551236789",
            "from_": "+15551234567",
            "body": "Welcome!",
        }
        self.twilio.messages.create.assert_called_once()
        assert expected_call == self.twilio.messages.create.call_args_list[0].kwargs
        model.get.assert_has_calls([call('phone')])

    def test_when(self):
        sms = SMS(self.twilio, self.di)
        sms.configure(
            from_number=lambda model: "5551234567", to_number='phone', message="Welcome!", when=lambda model: False,
        )

        model = MagicMock()
        model.name = 'asdf'
        model.columns = MagicMock(return_value=["phone"])
        model.get = MagicMock(return_value="5551236789")
        sms(model)
        expected_call = {
            "to": "+15551236789",
            "from_": "+15551234567",
            "body": "Welcome!",
        }
        self.twilio.messages.create.assert_not_called()
