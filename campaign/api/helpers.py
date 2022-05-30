import json
import math
import typing

from django.conf import settings

import stripe

from campaign.models import CampaignPackage, CampaignSubscriber
from campaign.api.schemas import SubscriberPostInSchema, ClientSecretDataSchema
from payments.models import OneTimeTransaction


def get_subscriber(guid: str) -> typing.Union[CampaignSubscriber, None]:
    return CampaignSubscriber.objects.filter(guid=guid).first()


def get_package(guid) -> typing.Union[CampaignPackage, None]:
    return CampaignPackage.objects.filter(guid__exact=guid).first()


def get_transaction(payment_intent_id: str) -> typing.Union[OneTimeTransaction, None]:
    return OneTimeTransaction.objects.filter(payment_intent_id=payment_intent_id).first()


def update_transaction(transaction: OneTimeTransaction,
                       payment_intent_json_object: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    stripe.api_key = settings.STRIPE_SECRET_KEY
    intent = stripe.PaymentIntent.retrieve(
        payment_intent_json_object.get('id'),
    )
    charge_id = intent.get('charges').get('data')[0].get('id')
    transaction.charge_id = charge_id
    transaction.payment_intent_json_object_after = json.dumps(intent)
    transaction.confirmed = True
    transaction.save()

    return intent


def generate_client_secret(package: typing.Union[CampaignPackage, None], subscriber: CampaignSubscriber) -> \
typing.Union[ClientSecretDataSchema, None]:
    if package is None:
        return None

    stripe.api_key = settings.STRIPE_SECRET_KEY

    price = math.ceil(package.get_price * 100)
    intent = stripe.PaymentIntent.create(
        amount=price,
        currency="cad",
        payment_method_types=["card"],
        metadata={'subscriber_guid': subscriber.guid, 'package_guid': package.guid}
    )

    transaction = OneTimeTransaction.objects.create(
        payment_intent_id=intent.get('id'),
        amount=price,
        payment_intent_json_object_before=json.dumps(intent)
    )

    if intent:
        return ClientSecretDataSchema(
            client_secret=intent['client_secret'],
            transaction_guid=transaction.guid
        )

    return None


def create_subscriber(package: typing.Union[CampaignPackage, None], data: SubscriberPostInSchema) -> CampaignSubscriber:
    values = data.dict()
    values.pop('package_guid')

    subscriber = CampaignSubscriber.objects.create(**values, campaign_package=package)

    return subscriber
