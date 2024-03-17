import json
import logging
from pathlib import Path

import typer

"""
jina-embeddings-v2-small-en is an English, monolingual embedding model supporting 8192 sequence length. It is based on a Bert architecture
 text-embedding-ada-002 model: 8191
"""

app = typer.Typer(name="tokenize")


@app.command()
def tokenize(
    directory: Path = typer.Argument(..., help="directory to scan for markdown files"),
    exclude_dirs: str = typer.Option("", help="list of strings, relative to scan dir"),
    prefix: str = typer.Option(
        "", help="prefix path for output id, e.g. '$VIMWIKIPATH/'"
    ),
):
    # directory = Path("/Users/Q187392/dev/s/private/vimwiki")
    excluded_dirs_list = exclude_dirs.split(",") if exclude_dirs else []
    md_files = scan_directory(directory, excluded_dirs=excluded_dirs_list)

    for md_file in md_files:
        process_md_file(md_file, directory, prefix=prefix)


def process_md_file(
    md_file: Path, directory: Path, max_chunk_size: int = 8191, prefix: str = ""
) -> None:
    """
    Process a single markdown file: convert to HTML, remove code blocks, split into chunks, and handle output.
    Unicode escape sequences are to be expected in output (ok for JSON and LLMs).
    Args:
        md_file: Path object for the markdown file.
        directory: Base directory for the markdown files.
        max_chunk_size: Maximum size of each text chunk.
        prefix: prefix for id (path).
    """
    if (directory / md_file).is_symlink():  # skip duplicated files
        return
    html_content = parse_markdown_to_html(directory / md_file)
    text_without_code = remove_code_blocks(html_content)
    chunks = split_into_chunks_with_tiktoken(
        text_without_code, max_chunk_size=max_chunk_size
    )

    for i, chunk in enumerate(chunks):
        id_ = f"{prefix}{str(md_file)}:{i}"
        json_output = json.dumps({"id": id_, "content": chunk}, ensure_ascii=True)
        print(json_output)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    verbose: bool = typer.Option(False, "-v", "--verbose", help="verbosity"),
    version: bool = typer.Option(False, "-V", "--version", help="show version"),
):
    log_fmt = r"%(asctime)-15s %(levelname)-7s %(message)s"
    if verbose:
        logging.basicConfig(
            format=log_fmt, level=logging.DEBUG, datefmt="%m-%d %H:%M:%S"
        )
    else:
        logging.basicConfig(
            format=log_fmt, level=logging.INFO, datefmt="%m-%d %H:%M:%S"
        )
    logging.getLogger("botocore").setLevel(logging.INFO)
    logging.getLogger("boto3").setLevel(logging.INFO)
    logging.getLogger("urllib3").setLevel(logging.INFO)

    if ctx.invoked_subcommand is None and version:
        ctx.invoke(print_version)
    if ctx.invoked_subcommand is None and not version:
        typer.echo(ctx.get_help())


@app.command("version", help="Show version", hidden=True)
def print_version() -> None:
    typer.secho("0.1.0", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()
