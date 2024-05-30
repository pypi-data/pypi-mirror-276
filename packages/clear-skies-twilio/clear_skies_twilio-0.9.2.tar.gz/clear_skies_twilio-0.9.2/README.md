# clearskies-twilio

clearskies bindings for working with [Twilio](https://twilio.com/).  At the moment it's just an action to send an SMS.

# Installation

To install:

```
pip install clear-skies-twilio
```

# Usage

## Authentication

Before you can use this you need to setup authentication to Twilio.  This only works with [API keys](https://www.twilio.com/docs/iam/api-keys/api-key) from Twilio - **not** your auth token(s). Also, this module assumes that your authentication details are stored in your secret manager, so you provide paths to secrets in your secret manager.

**IMPORTANT**: This module is designed to fetch your Twilio credentials only when needed and will automatically re-fetch them from the secrets manager in the event of an authentication failure.  As a result, you can rotate your Twilio credentials at anytime: just drop the new credentials in your secret manager and your running processes will automatically find it and use it without needing to restart/rebuild/relaunch the application.  There are three "pieces" to authentication with Twilio:

 1. API Key
 2. API Secret
 3. Account SID

You have to tell the twilio module where these live in the secret manager.  We do that in the below example and also point clearskies to AWS Secrets Manager:

```
import clearskies
import clearskies_twilio
import clearskies_aws

application = clearskies.Application(
    SomeHandler,
    {
        "your": "application config",
    },
    bindings={
        "twilio": clearskies_twilio.di.twilio(
            path_to_api_key="/path/to/twilio/api_key",
            path_to_api_secret="/path/to/twilio/api_secret",
            path_to_account_sid="/path/to/twilio/account_sid",
        ),
        "secrets": clearskies_aws.secrets.SecretsManager,
    },
)
```

## Actions

Currently the only option available is an Action for sending SMS messages.  It accepts a message that should be a string or a callable that returns the SMS message and which can accept `model` (the model that triggered the action) as well as any other configured dependencies.  You must provide `from_number` and `to_number` which can be either a phone number, the name of one of the columns in the model, or callables which return the phone number.  Simple example:

```
import clearskies
from clearskies.column_types import uuid, string, created
from collections import OrderedDict
from clearskies_twilio.actions import sms

class User(clearskies.Model):
    def __init__(self, cursor_backend, columns):
        super().__init__(cursor_backend, columns)

    def columns_configuration(self):
        return OrderedDict(
            [
                uuid("id"),
                string("phone"),
                string("name"),
                created(
                    "created_at",
                    on_change=[
                        sms(
                            from_number="+15551234567",
                            to_number="phone",
                            message=lambda model: f"Welcome {model.name}!"
                        ),
                    ],
                ),
            ]
        )

```
