from django.core.exceptions import ValidationError


def validate_image_size(image):
    max_size_kb = 200
    if image.size > max_size_kb * 1024:
        raise ValidationError(f"Image file size should not exceed {max_size_kb} KB.")
