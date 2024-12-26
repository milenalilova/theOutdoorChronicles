# from django.core.exceptions import ValidationError
# from django.utils import timezone
#
#
# def validate_date_not_in_future(date):
#     if date > timezone.now().date():
#         raise ValidationError("Date cannot be in the future")

from django.core.exceptions import ValidationError
from datetime import date


def validate_date_not_in_future(value):
    today = date.today()

    if value > today:
        raise ValidationError("Date cannot be in the future.")
