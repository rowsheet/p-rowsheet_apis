from django.conf import settings
import stripe
stripe.api_key = settings.STRIPE_API_SK

def create_customer(description, name, email):
    customer = stripe.Customer.create(
        name=name,
        email=email,
        description=description,
    )
    return customer

def create_checkout_session(plan_id):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        subscription_data={
            'items': [{
                'plan': plan_id,
            }],
        },
        success_url=settings.STRIPE_SUCCESS_URL,
        cancel_url=settings.STRIPE_CANCEL_URL,
    )
    import json
    print(json.dumps(session, indent=4, sort_keys=True))
    return {
        "session_id": session.id,
        "amount": session.display_items[0].amount,
        "currency": session.display_items[0].currency,
        "product_id": session.display_items[0].plan.product,
        "interval": session.display_items[0].plan.interval,
    }

def get_subscription_id_by_session_id(session_id):
    session = stripe.checkout.Session.retrieve(session_id)
    return session.subscription
