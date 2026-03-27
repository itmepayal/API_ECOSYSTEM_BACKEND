import cloudinary.uploader
import cloudinary.uploader
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class CloudinaryService:

    @staticmethod
    def upload_image(file, folder="uploads"):
        try:
            if not file:
                raise ValueError("No file provided")

            response = cloudinary.uploader.upload(
                file,
                folder=folder,
                resource_type="image",
                transformation=[
                    {"width": 500, "height": 500, "crop": "limit"},
                    {"quality": "auto", "fetch_format": "auto"}
                ]
            )

            return {
                "url": response.get("secure_url"),
                "public_id": response.get("public_id"),
                "format": response.get("format"),
                "width": response.get("width"),
                "height": response.get("height")
            }

        except Exception as e:
            logger.error(f"Cloudinary image upload failed: {str(e)}")
            raise


    @staticmethod
    def upload_file(file, folder="files"):
        try:
            if not file:
                raise ValueError("No file provided")

            response = cloudinary.uploader.upload(
                file,
                folder=folder,
                resource_type="auto"
            )

            return {
                "url": response.get("secure_url"),
                "public_id": response.get("public_id"),
                "format": response.get("format")
            }

        except Exception as e:
            logger.error(f"Cloudinary file upload failed: {str(e)}")
            raise


    @staticmethod
    def delete_file(public_id):
        try:
            if not public_id:
                raise ValueError("public_id is required")

            response = cloudinary.uploader.destroy(public_id)

            return response

        except Exception as e:
            logger.error(f"Cloudinary delete failed: {str(e)}")
            raise