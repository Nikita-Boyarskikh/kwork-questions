from datetime import date

from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.core.files.uploadedfile import UploadedFile
from django.core.validators import MaxValueValidator
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext as _


# TODO: use class-based validators
def max_value_current_year_validator(value):
    current = date.today().year
    validator = MaxValueValidator(current)
    return validator(value)


def content_type_validator(content_type, allowed=('jpeg', 'pjpeg', 'gif', 'png')):
    main, sub = content_type.split('/')
    if not (main == 'image' and sub in allowed):
        raise ValidationError(
            message=_('Please use one of %(allowed)s image.'),
            params={
                'allowed': ', '.join(allowed),
            },
            code='wrong_content_type',
        )


def max_dimensions_validator(wh, max_wh=(1000, 1000)):
    w, h = wh
    max_w, max_h = max_wh
    if w > max_w or h > max_h:
        raise ValidationError(
            message=_('Please use an image that is %(max_width)s x %(max_height)s pixels or smaller.'),
            params={
                'max_width': max_w,
                'max_height': max_h,
            },
            code='max_dimensions',
        )


def size_validator(size, max_size=20 * 1024):
    if size > max_size:
        raise ValidationError(
            message=_('Avatar file size may not exceed %(limit)s.'),
            params={
                'message': filesizeformat(max_size),
            },
            code='max_size',
        )


def avatar_validator(avatar):
    if isinstance(avatar, UploadedFile):
        w, h = get_image_dimensions(avatar)
        max_dimensions_validator((w, h))
        size_validator(avatar.size)
        content_type_validator(avatar.content_type)
