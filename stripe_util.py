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
    return {
        "session_id": session.id,
        "amount": session.display_items[0].amount,
        "currency": session.display_items[0].currency,
        "product_id": session.display_items[0].plan.product,
        "interval": session.display_items[0].plan.interval,
    }

def create_driver_donation_checkout_session_id(name, amount):
    session = stripe.checkout.Session.create(
	payment_method_types=['card'],
	line_items=[{
	    'name': name,
	    # 'description': 'Comfortable cotton t-shirt',
	    # 'images': ['https://example.com/t-shirt.png'],
	    'amount': int(float(amount) * 100),
	    'currency': 'usd',
	    'quantity': 1,
	}],
        success_url=settings.STRIPE_SUCCESS_URL,
        cancel_url=settings.STRIPE_CANCEL_URL,
    )
    return {
        "session_id": session.id,
        "amount": session.display_items[0].amount,
        "currency": session.display_items[0].currency,
	"donation_id": session.payment_intent,
    }

def get_subscription_id_by_session_id(session_id):
    session = stripe.checkout.Session.retrieve(session_id)
    return session.subscription

def cancel_subscription_by_subscription_id(subscription_id):
    result = stripe.Subscription.delete(subscription_id)
    return {
        "start_timestamp": result.get("current_period_start"),
        "end_timestamp": result.get("current_period_end"),
    }
