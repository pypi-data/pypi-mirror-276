import os
import pathlib
import subprocess
import time
from unittest.mock import patch

import pytest
import yaml

import boto3
import aiobotocore
import aiobotocore.session


def create_s3_folder(bucket_name, structure, s3_client, parent_path=""):
    if isinstance(structure, list):
        for item in structure:
            for key, value in item.items():
                create_s3_objects(key, value, bucket_name, s3_client, parent_path)
    else:
        for key, value in structure.items():
            create_s3_objects(key, value, bucket_name, s3_client, parent_path)


def create_s3_objects(key, value, bucket_name, s3_client, parent_path):
    if isinstance(value, list):
        for item in value:
            if isinstance(item, str) and item == "EMPTY":
                folder_path = os.path.join(parent_path, key)
                s3_client.put_object(Bucket=bucket_name, Key=(folder_path + "/"))
            elif isinstance(item, str):
                file_path = os.path.join(parent_path, key, item)
                s3_client.put_object(Bucket=bucket_name, Key=file_path, Body="")
            elif isinstance(item, dict):
                folder_path = os.path.join(parent_path, key)
                create_s3_folder(bucket_name, item, s3_client, folder_path)
    elif isinstance(value, dict):
        folder_path = os.path.join(parent_path, key)
        create_s3_folder(bucket_name, value, s3_client, folder_path)


def wait_for_moto_server(s3_client, moto_server_process, retries=5, delay=1):
    for _ in range(retries):
        try:
            s3_client.list_buckets()
            return True
        except Exception:
            stderr_output = moto_server_process.stderr.readline()
            if stderr_output:
                print(stderr_output.decode(), end="")
            time.sleep(delay)
    return False


@pytest.fixture(scope="session")
def fake_s3_server():
    """Starts a Moto server.

    Moto does not support mocking async clients, so we have to use fake server.

    Returns (<S3 client>, <factory for async S3 clients>).
    """
    moto_server_process = subprocess.Popen(
        ["moto_server", "-p3000"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    s3_client = boto3.client("s3", region_name="us-east-1", endpoint_url="http://localhost:3000")

    if not wait_for_moto_server(s3_client, moto_server_process):
        print("Failed to start the Moto server.")
        moto_server_process.terminate()
        moto_server_process.wait()
        pytest.fail("Failed to start Moto server")

    session = aiobotocore.session.get_session()
    yield (
        s3_client,
        lambda: session.create_client(
            "s3", region_name="us-east-1", endpoint_url="http://localhost:3000"
        ),
    )

    # Teardown
    moto_server_process.terminate()
    moto_server_process.wait()


@pytest.fixture(scope="session")
def mock_s3_structure(fake_s3_server):
    s3_client, s3_async_client_factory = fake_s3_server
    HERE = pathlib.Path(__file__).parent
    with (HERE / "resources" / "bucket_keys.yml").open("r") as file:
        structure = yaml.safe_load(file)
    bucket_name = "mock-bucket"
    s3_client.create_bucket(Bucket=bucket_name)
    create_s3_folder(bucket_name, structure, s3_client)
    with patch("aws_s3.list_objects_async.get_s3_client") as mock_client:
        mock_client.side_effect = s3_async_client_factory
        yield
