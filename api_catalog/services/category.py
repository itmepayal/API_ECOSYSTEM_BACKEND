# =========================================================
# API Catalog Models
# =========================================================
from api_catalog.models import APICategory

# =========================================================
# API CATEGORY SERVICE
# =========================================================
class APICategoryService:
    # =====================================================
    # QUERYSET HANDLER
    # =====================================================
    @staticmethod
    def get_queryset():
        return APICategory.objects.all()

    # =====================================================
    # LIST RESPONSE HANDLER
    # =====================================================
    @staticmethod
    def extract_list_data(response):
        if isinstance(response.data, dict):
            data = response.data.get("results", [])
            meta = {
                "count": response.data.get("count"),
                "next": response.data.get("next"),
                "previous": response.data.get("previous"),
            }
        else:
            data = response.data
            meta = None

        return data, meta

    # =====================================================
    # SUCCESS PAYLOAD BUILDER
    # =====================================================
    @staticmethod
    def build_success_payload(message, data=None, meta=None, status_code=200):
        return {
            "message": message,
            "data": data,
            "meta": meta,
            "status_code": status_code
        }

    # =====================================================
    # LIST RESPONSE BUILDER
    # =====================================================
    @staticmethod
    def build_list_response(response, message):
        data, meta = APICategoryService.extract_list_data(response)
        return APICategoryService.build_success_payload(
            message=message,
            data=data,
            meta=meta
        )