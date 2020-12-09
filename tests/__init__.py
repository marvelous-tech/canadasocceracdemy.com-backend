import os
import dotenv
import braintree

dotenv.read_dotenv()

BRAINTREE_MERCHANT_ID = os.environ.get('MID')
BRAINTREE_PRIVATE_KEY = os.environ.get('PRK')
BRAINTREE_PUBLIC_KEY = os.environ.get('PBK')
BRAINTREE_ENVIRONMENT = braintree.Environment.Sandbox

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        BRAINTREE_ENVIRONMENT,
        merchant_id=BRAINTREE_MERCHANT_ID,
        public_key=BRAINTREE_PUBLIC_KEY,
        private_key=BRAINTREE_PRIVATE_KEY
    )
)


def test_webhook():
    sample_notification = gateway.webhook_testing.sample_notification(
        braintree.WebhookNotification.Kind.SubscriptionChargedSuccessfully,
        "my_id"
    )

    webhook_notification = gateway.webhook_notification.parse(
        sample_notification['bt_signature'],
        sample_notification['bt_payload']
    )

    print(webhook_notification.subscription)
    return


test_webhook()
