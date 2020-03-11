#!/usr/bin/env python
import os
import sys

from django.conf import settings

import stripe

def test_basic():
    stripe.api_key = settings.STRIPE_API_KEY
    resp = stripe.Customer.create(
        description="My First Test Customer (created for API docs)",
    )
    import pprint as pp
    pp.pprint(resp)

def test_create_session_id():
    plan_id = "plan_GtHMSytV6dBI4w"
    session = stripe_util.create_checkout_session(plan_id)
    import pprint as pp
    pp.pprint(session)

def test_get_subscription_id_by_session_id():
    session_id = "cs_test_1UpJ6OmAdiiYaKAGqkClAliWrx18fZhPAdwshbtIqSg9akf7mTucMoEo"
    subscription_id = stripe_util.get_subscription_id_by_session_id(session_id)
    import pprint as pp
    pp.pprint(subscription_id)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    print(settings.ADMIN_SITE_HEADER)
    import stripe_util
    # test_basic()
    # test_create_session_id()
    test_get_subscription_id_by_session_id()
