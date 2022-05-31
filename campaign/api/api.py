from django.conf import settings
from django.template.loader import render_to_string
from ninja.router import Router

from campaign.api.schemas import \
    SubscriberPostOutSchema, \
    SubscriberPostInSchema, PaymentIntentPostInSchema, PaymentIntentPostOutSchema
from campaign.api.helpers import \
    create_subscriber, \
    generate_client_secret, \
    get_package, \
    get_transaction, \
    update_transaction, \
    get_subscriber
from mt_utils import email_raw

router = Router()


@router.post('/create_subscriber', response=SubscriberPostOutSchema)
def create_subscriber_api(request, data: SubscriberPostInSchema):
    package = get_package(data.package_guid)
    if package is None:
        return router.api.create_response(request, {
            'error_code': 101,
        }, status=400)
    subscriber = create_subscriber(package, data.copy())
    secret = generate_client_secret(package, subscriber)
    pk = settings.STRIPE_PUBLISHABLE_KEY
    response_data = SubscriberPostOutSchema(
        **(data.dict()),
        client_secret=secret.client_secret,
        guid=subscriber.guid,
        created=subscriber.created,
        updated=subscriber.updated,
        price=package.get_price,
        transaction_guid=secret.transaction_guid,
        publishable_key=pk
    )
    return response_data


@router.post('/post_payment_intent', response=PaymentIntentPostOutSchema)
def post_payment_intent(request, data: PaymentIntentPostInSchema):
    transaction = get_transaction(data.intent.get('id'))
    if transaction is None:
        return router.api.create_response(request, {
            'error_code': 102,
        }, status=400)
    intent = update_transaction(transaction, data.intent)
    subscriber = get_subscriber(intent.get('metadata')['subscriber_guid'])
    subscriber.stripe_transaction_id = transaction.id
    subscriber.save()

    email_raw(
        from_email=settings.NO_REPLY_MAIL_ADDRESS,
        from_name='Canada Soccer Academy',
        to=[
            {
                "Email": "eroberts1055@gmail.com",
                "Name": "Eddie Roberts"
            },
            {
                "Email": subscriber.player_email,
                "Name": subscriber.name
            }
        ],
        subject='Canada Soccer Academy 2022 Spain ID Campaign Registration Receipt',
        text=f'{subscriber.campaign_package.name} Registration was successful',
        html=render_to_string('campaign/spain_id_camp/email.html', {'subscriber': subscriber})
    )

    return PaymentIntentPostOutSchema(
        subscriber=subscriber,
        package_guid=subscriber.campaign_package.guid,
        package_name=subscriber.campaign_package.name,
        charge_id=transaction.charge_id,
        price=transaction.amount / 100
    )
