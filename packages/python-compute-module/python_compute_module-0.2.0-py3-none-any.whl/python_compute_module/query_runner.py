import asyncio
import logging
import os
from typing import Any, Callable, List

from python_compute_module.api import ComputeModuleApi
from python_compute_module.read_connection_file import read_connection_file
from python_compute_module.schema import Schema, generate_schema

log = logging.getLogger(__name__)


class QueryRunner:
    JOB_POLL_DELAY_SECONDS = 0.5
    CONNECTION_ENV_VAR = "CONNECTION_TO_RUNTIME"

    def __init__(self, *funcs: List[Callable[..., Any]]):
        schemas_by_function = {f: generate_schema(f) for f in funcs}
        self.query_functions = {schemas_by_function[f].name: f for f in funcs}
        schemas = list(schemas_by_function.values())
        connection_path = os.environ.get(QueryRunner.CONNECTION_ENV_VAR)
        if not connection_path:
            raise ValueError(
                "Connection path not found in environment variables, please set CONNECTION_TO_RUNTIME to the path of the connection file."
            )
        asyncio.run(self.initialize(connection_path, schemas))

    async def initialize(self, connection_path: str, schemas: List[Schema]):
        self.connection_information = await read_connection_file(connection_path)
        self.compute_module_api = ComputeModuleApi(self.connection_information)
        await self.compute_module_api.post_schema(schemas)
        await self.run()

    async def run(self):
        while True:
            try:
                job_request = await self.compute_module_api.get_job_request()

                if job_request is None:
                    log.debug("No job requests, sleeping")
                    await asyncio.sleep(QueryRunner.JOB_POLL_DELAY_SECONDS)
                    continue

                query_type = job_request.type
                query = job_request.computeModuleJobV1
                job_id = query["jobId"]
                query_name = query["queryType"]
                query_data = query["query"]
                log.debug(
                    f"Received query: {query_name}, {query_type}, {query_data}, {job_id}"
                )

                if query_name in self.query_functions:
                    query_function = self.query_functions[query_name]
                    result = query_function(**query_data)
                    log.debug(f"Invoked query function {query_name}: {result}")
                    await self.compute_module_api.post_result(job_id, result)
                else:
                    log.warn(
                        f"Could not find a matching query function for {query_name}"
                    )
                    await self.compute_module_api.post_result(
                        job_id, "No matching query function found"
                    )
            except Exception as e:
                log.error(f"Error processing job: {e}")
                await self.compute_module_api.post_result(job_id, f"error {e}")
