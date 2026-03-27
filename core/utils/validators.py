from rest_framework.exceptions import ValidationError

def validate_image(file):
    if file.size > 2 * 1024 * 1024:
        raise ValidationError("Max file size is 2MB")

    if not file.content_type.startswith("image/"):
        raise ValidationError("Invalid image type")