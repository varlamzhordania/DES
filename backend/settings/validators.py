import os
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions


def image_validator(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.svg']

    if not ext in valid_extensions:
        raise ValidationError(
            'Only .jpg, .jpeg, .png, and .svg files are allowed.'
        )

    # try:
    #     # Additional checks for image dimensions if needed
    #     width, height = get_image_dimensions(value)
    #     # Add your specific dimension requirements here if necessary
    # except Exception as e:
    #     raise ValidationError('Invalid image format.')

    # # Additional checks for image size if needed
    # max_size_kb = 1024  # set your maximum size limit in kilobytes
    # if value.size > max_size_kb * 1024:
    #     raise ValidationError('File size must be no more than {} KB.'.format(max_size_kb))
