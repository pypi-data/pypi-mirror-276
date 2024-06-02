import pytest
from aws_s3.list_objects_async import ListObjectsAsync


@pytest.mark.asyncio
async def test_list_objects(mock_s3_structure):
    walker = ListObjectsAsync("mock-bucket")
    keys = sorted([object["Key"] for object in await walker.list_objects(prefix="root/")])

    expected_keys = sorted([
        'root/data01/image01.png',
        'root/data01/images/img11.jpg',
        'root/data01/docs/doc12.pdf',
        'root/data01/archives/archive13a.zip',
        'root/data01/archives/archive13b.zip',
        'root/data02/report02.docx',
        'root/data02/reports/report21.docx',
        'root/data02/logs/log22.txt',
        'root/data02/scripts/script23.py',
        'root/data03/video03a.mp4',
        'root/data03/video03b.mp4',
        'root/data03/video03c.mp4'
    ])

    assert sorted(keys) == sorted(expected_keys)
