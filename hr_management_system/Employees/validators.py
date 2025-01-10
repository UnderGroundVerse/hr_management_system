from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_phone(num):
    phone_len = len(num)
    if (phone_len != 11) or (not num.isdigit()):
        raise ValidationError(_('Not a valid phone number'), params={'num': num})


def validate_id(num):
    id_len = len(num)
    if (id_len>9) or (id_len<8) or (not num.isdigit()):
        raise ValidationError(_('Not a valid ID'), params={'num': num})


def validate_name(name):
    if len(name) < 3:
        raise ValidationError(_('Not a valid name'), params={'name': name})
