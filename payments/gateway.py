import braintree
from django.conf import settings
import os


GATEWAY = getattr(settings, 'GATEWAY', None)


BRAINTREE_MERCHANT_ID = getattr(settings, 'BRAINTREE_MERCHANT_ID', os.environ.get('MID'))
BRAINTREE_PRIVATE_KEY = getattr(settings, 'BRAINTREE_PRIVATE_KEY', os.environ.get('PRK'))
BRAINTREE_PUBLIC_KEY = getattr(settings, 'BRAINTREE_PUBLIC_KEY', os.environ.get('PBK'))
BRAINTREE_ENVIRONMENT = getattr(settings, 'BRAINTREE_ENVIRONMENT', braintree.Environment.Sandbox)

if BRAINTREE_MERCHANT_ID is None:
    raise AttributeError("BRAINTREE_MERCHANT_ID not found in settings")

if BRAINTREE_PRIVATE_KEY is None:
    raise AttributeError("BRAINTREE_PRIVATE_KEY not found in settings")

if BRAINTREE_PUBLIC_KEY is None:
    raise AttributeError("BRAINTREE_PUBLIC_KEY not found in settings")

TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        BRAINTREE_ENVIRONMENT,
        merchant_id=BRAINTREE_MERCHANT_ID,
        public_key=BRAINTREE_PUBLIC_KEY,
        private_key=BRAINTREE_PRIVATE_KEY
    )
)


def generate_client_token(customer_id):
    return gateway.client_token.generate({
        "customer_id": customer_id
    })


def generate_empty_client_token():
    return gateway.client_token.generate()


def make_transaction(options):
    return gateway.transaction.sale(options)


def find_transaction(trx_id):
    return gateway.transaction.find(trx_id)


def create_new_customer(customer_id, first_name, last_name, email, phone):
    return gateway.customer.create({
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "id": customer_id
    })


def update_customer(options):
    return gateway.customer.update(options)


def get_customer(customer_id):
    return gateway.customer.find(customer_id)


def delete_customer(customer_id):
    return gateway.customer.delete(customer_id)


def create_payment_method(customer_id, payment_method_nonce, make_default=False):
    return gateway.payment_method.create({
        "customer_id": customer_id,
        "payment_method_nonce": payment_method_nonce,
        "options": {
            "make_default": make_default,
            "verify_card": True
        }
    })


def get_payment_method(payment_method_token):
    return gateway.payment_method.find(payment_method_token)


def delete_payment_method(payment_method_token):
    return gateway.payment_method.delete(payment_method_token)


def create_subscription(payment_method_token, plan_id):
    return gateway.subscription.create({
        "payment_method_token": payment_method_token,
        "plan_id": plan_id
    })


def update_subscription(subscription_id, plan_id):
    return gateway.subscription.update(subscription_id, {
        "plan_id": plan_id,
    })


def update_subscription_payment_method(subscription_id, new_payment_method_token):
    return gateway.subscription.update(subscription_id, {
        "payment_method_token": new_payment_method_token,
    })


def cancel_subscription(subscription_id):
    return gateway.subscription.cancel(subscription_id)


def find_subscription(subscription_id):
    return gateway.subscription.find(subscription_id)
