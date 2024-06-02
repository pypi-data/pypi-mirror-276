import asyncio
import functools
from typing import Iterable, Any, Dict

import aiobotocore.session
import aiobotocore.client
from botocore.config import Config


@functools.lru_cache()
def create_session() -> aiobotocore.session.AioSession:
    """Create a session object."""
    return aiobotocore.session.get_session()


def get_s3_client() -> aiobotocore.client.AioBaseClient:
    """Get S3 client."""
    session = create_session()
    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
    )
    return session.create_client("s3", config=config)


class ListObjectsAsync:
    def __init__(self, bucket: str) -> None:
        self._bucket = bucket

    async def _list_objects(
        self, s3_client: aiobotocore.client.AioBaseClient, prefix: str
    ) -> Dict[str, Any]:
        paginator = s3_client.get_paginator("list_objects_v2")
        objects = []
        prefixes = []

        async for page in paginator.paginate(Bucket=self._bucket, Prefix=prefix, Delimiter="/"):
            for obj in page.get("Contents", []):
                key: str = obj["Key"]
                if key.endswith("/"):
                    continue  # Omit "directories"

                objects.append(obj)

            prefixes.extend(page.get("CommonPrefixes", []))  # add "subdirectories"

        return {"Objects": objects, "CommonPrefixes": prefixes}

    async def list_objects(
        self,
        prefix: str = "/",
    ) -> Iterable[Dict[str, Any]]:
        """List all objects in the bucket with given prefix."""
        objects = []
        tasks = set()

        async with get_s3_client() as s3_client:
            tasks.add(asyncio.create_task(self._list_objects(s3_client, prefix)))

            while tasks:
                done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                tasks = pending

                for task in done:
                    result = await task
                    objects.extend(result["Objects"])

                    for common_prefix in result["CommonPrefixes"]:
                        tasks.add(
                            asyncio.create_task(
                                self._list_objects(s3_client, common_prefix["Prefix"])
                            )
                        )

        return objects
