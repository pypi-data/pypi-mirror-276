from typing import List
from clearskies.secrets.secrets import Secrets
from twilio.rest import Client
import twilio

class Twilio:
    """
    A wrapper around the twilio library to manage authentication.
    """
    def __init__(self, secrets: Secrets):
        self.secrets = secrets
        self._twilio = None

    def configure(
        self,
        path_to_api_key: str = "",
        path_to_api_secret: str = "",
        path_to_account_sid: str = "",
    ):
        self.path_to_api_key = path_to_api_key
        self.path_to_api_secret = path_to_api_secret
        self.path_to_account_sid = path_to_account_sid

    def __getattr__(self, name: str):
        return TwilioWrapper(self, [name])

    def get_twilio(self, cache=True):
        if self._twilio is not None and cache:
            return self._twilio

        self._twilio = Client(
            self.secrets.get(self.path_to_api_key),
            self.secrets.get(self.path_to_api_secret),
            self.secrets.get(self.path_to_account_sid),
        )
        return self._twilio

class TwilioWrapper:
    def __init__(self, twilio_auth: Twilio, path: List[str]=[]):
        self.twilio_auth = twilio_auth
        self.path = path

    def __getattr__(self, name):
        return TwilioWrapper(self.twilio_auth, [*self.path, name])

    def __call__(self, *args, **kwargs):
        cache = True
        if cache in kwargs:
            cache = kwargs[cache]
            del kwargs[cache]

        chain = self.twilio_auth.get_twilio(cache=cache)
        for name in self.path:
            chain = getattr(chain, name, None)
            if chain is None:
                raise ValueError("Requested non-existent function from twilio: twilio." + ".".join(self.name))

        try:
            response = chain(*args, **kwargs)
        except twilio.base.exceptions.TwilioRestException as e:
            # see if we can separate out auth errors from other kinds of errors.  Also, if the cache
            # flag was set to false, then we already fetched new credentials, which means that we
            # already retried, so we can't retry again.
            if "authentication" not in e.msg.lower() or not cache:
                raise e

            return self.__call__(*args, **kwargs, cache=False)

        return response
