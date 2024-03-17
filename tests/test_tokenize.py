import pytest
from typer.testing import CliRunner

from prepembd.bin.tokenize import app

runner = CliRunner()


class TestTokenize:
    @pytest.mark.e2e
    def test_tokenize_tiktoken(self):
        result = runner.invoke(
            app, ["tokenize", "--exclude-dirs", "test,bla", "tests/resources/md"]
        )
        # print(result.stdout)
        assert result.exit_code == 0
        assert "rust.md:1" in result.stdout
        assert "r1.md:0" in result.stdout

    def test_tokenize_help(self):
        result = runner.invoke(
            app,
            [
                "tokenize",
                "--help",
            ],
        )
        # print(result.stdout)
        assert result.exit_code == 0
