from typing import Any
from clients_core.service_clients import E360ServiceClient
from .models import TDBundleImportModel, TDBundleImportResponseModel


class TDImportServiceClient(E360ServiceClient):
    service_endpoint = ""
    extra_headers = {"accept": "application/json", "Content-Type": "application/json"}

    def create(
        self, model: TDBundleImportModel, **kwargs: Any
    ) -> TDBundleImportResponseModel:

        response = self.client.post(
            "",
            json=model.dict(by_alias=True),
            headers=self.service_headers,
            raises=True,
            **kwargs,
        )
        # There is no json response, however one is created to follow the convention
        response_json = {
            "status": str(response.status_code),
            "message": response.reason,
        }
        return TDBundleImportResponseModel.parse_obj(response_json)
