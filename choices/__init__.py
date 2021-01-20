import enum


MEMBER_TYPE_CHOICES = (
    ('INSTRUCTOR', 'INSTRUCTOR'),
    ('CEO', 'CEO'),
    ('POSTER', 'POSTER'),
    ('MEMBER', 'MEMBER')
)

USER_PROFILE_TYPE_CHOICES = (
    ('PLAYER', 'PLAYER'),
    ('COACH', 'COACH'),
)

CYCLE_TYPE_CHOICES = (
    ('MONTHLY', 'MONTHLY'),
    ('ANNUALLY', 'ANNUALLY'),
    ('DAILY', 'DAILY'),
    ('WEEKLY', 'WEEKLY')
)

SUBSCRIPTION_STATUS_CHOICES = (
    ('PENDING', 'PENDING'),
    ('ACTIVE', 'ACTIVE'),
    ('PAST_DUE', 'PAST_DUE'),
    ('CANCELED', 'CANCELED'),
    ('EXPIRED', 'EXPIRED')
)


class SubscriptionStatusName(enum.Enum):
    ACTIVE = 'ACTIVE'
    PENDING = 'PENDING'
    PAST_DUE = 'PAST_DUE'
    CANCELED = 'CANCELED'
    EXPIRED = 'EXPIRED'
    SUCCESSFUL = True
    UNSUCCESSFUL = False
    IN_TRIAL = True
    NOT_IN_TRIAL = False
