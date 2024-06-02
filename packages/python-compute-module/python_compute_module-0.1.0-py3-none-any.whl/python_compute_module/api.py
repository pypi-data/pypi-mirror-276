import json
import logging
from typing import Any, List, Optional

import httpx
from python_compute_module.schema import Schema
from pydantic import BaseModel

log = logging.getLogger(__name__)

CONNECT_TIMEOUT_SECONDS = 60
READ_TIMEOUT_SECONDS = 60


class ConnectionInformation(BaseModel):
    host: str
    port: int
    getJobPath: str
    postResultPath: str
    basePath: str
    trustStorePath: Optional[str]
    moduleAuthToken: str


class JobRequest(BaseModel):
    type: str
    computeModuleJobV1: dict


class ComputeModuleApi:
    def __init__(self, connection_information: ConnectionInformation):
        self.connection_information = connection_information
        trust_store_path = connection_information.trustStorePath

        self.client = httpx.AsyncClient(
            base_url=f"https://{connection_information.host}:{connection_information.port}",
            headers={
                "Module-Auth-Token": connection_information.moduleAuthToken,
            },
            http2=True,
            verify=trust_store_path,
            timeout=(CONNECT_TIMEOUT_SECONDS, READ_TIMEOUT_SECONDS),
        )

    async def get_job_request(self) -> Optional[JobRequest]:
        response = await self.client.get(self.connection_information.getJobPath)
        log.debug(f"received job request response {response.status_code}")
        if response.status_code == 204:
            return None
        else:
            return JobRequest.parse_obj(response.json())

    async def post_result(self, job_id: str, response: Any) -> httpx.Response:
        log.debug(f"posting result: {response}")
        return await self.client.post(
            f"{self.connection_information.postResultPath}/{job_id}",
            content=json.dumps(response),
            headers={
                "Content-Type": "application/octet-stream",
            },
        )

    async def post_schema(self, schemas: List[Schema]) -> httpx.Response:
        return await self.client.post(
            f"{self.connection_information.basePath}/schemas",
            json=[schema.dict() for schema in schemas],
        )
