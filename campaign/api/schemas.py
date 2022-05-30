import datetime
import typing

from ninja.schema import Schema


class BaseSchema(Schema):
    guid: str
    created: datetime.datetime
    updated: datetime.datetime


class SubscriberSchema(Schema):
    name: str
    gender: str
    date_of_birth: typing.Union[str, datetime.date]
    parent_names: str
    address: str
    phone: str
    parent_email: str
    player_email: str
    health_card_number: str
    medications: str
    allergies: str
    injuries: str
    emergency_contact_number: str


class SubscriberPostInSchema(SubscriberSchema):
    package_guid: str


class SubscriberInSchema(SubscriberSchema, BaseSchema):
    pass


class PaymentIntentPostOutSchema(Schema):
    subscriber: SubscriberInSchema
    package_guid: str
    package_name: str
    charge_id: str
    price: str


class ClientSecretDataSchema(Schema):
    client_secret: str
    transaction_guid: str


class SubscriberPostOutSchema(SubscriberPostInSchema, BaseSchema):
    client_secret: str
    price: float
    transaction_guid: str
    publishable_key: str


class PaymentIntentPostInSchema(Schema):
    intent: typing.Dict[str, typing.Any]
