import aiofiles
import asyncio
import logging

from python_compute_module.api import ConnectionInformation

log = logging.getLogger(__name__)
READ_POLL_DELAY_SECONDS = 0.5
MAX_READ_ATTEMPTS = 100


async def read_connection_file(path: str) -> ConnectionInformation:
    log.info(
        f"Attempting reading connection file from {path} [Poll interval {READ_POLL_DELAY_SECONDS}s]"
    )
    start_time = asyncio.get_event_loop().time()
    attempt_count = 0

    while attempt_count < MAX_READ_ATTEMPTS:
        try:
            async with aiofiles.open(path, "r") as f:
                blob = await f.read()
            log.info(
                f"Successfully read connection file from {path} after {(asyncio.get_event_loop().time() - start_time):.2f}s"
            )
            log.info(f"connection file blob looks like: {blob}")
            return ConnectionInformation.parse_raw(blob)
        except Exception as e:
            log.error(f"Error reading connection file: {e}")
            # The file can take a while to appear, so we retry a few times
            # logger.error(f"Error reading connection file: {e}")
            await asyncio.sleep(READ_POLL_DELAY_SECONDS)
            attempt_count += 1

    raise ValueError(
        f"Failed to read connection file after {MAX_READ_ATTEMPTS} attempts"
    )
