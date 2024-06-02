from aws_s3 import __version__
from aws_s3.main import aws_s3
from click.testing import CliRunner


def test_version():
    assert __version__


def test_version_option():
    runner = CliRunner()
    result = runner.invoke(aws_s3, ['--version'])
    assert result.exit_code == 0
    assert __version__ in result.output
