import json
import logging
from pathlib import Path

import tiktoken
import typer
from langchain_text_splitters import MarkdownTextSplitter

from prepembd.lib.helper import remove_excessive_dots, strip_quote_prefixes
from prepembd.lib.path import scan_directory

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

    md_content = (directory / md_file).read_text(encoding="utf-8", errors="ignore")
    md_content = strip_quote_prefixes(md_content)
    md_content = remove_excessive_dots(md_content)

    markdown_splitter = MarkdownTextSplitter.from_tiktoken_encoder(
        "cl100k_base", chunk_size=max_chunk_size, chunk_overlap=200
    )
    encoding = tiktoken.get_encoding("cl100k_base")
    docs = markdown_splitter.create_documents([md_content])

    for doc in docs:
        word_tokens = encoding.encode(doc.page_content)
        word_token_length = len(word_tokens)
        assert word_token_length < max_chunk_size

    for i, doc in enumerate(docs):
        assert (
            len(encoding.encode(doc.page_content)) < max_chunk_size
        ), f"Chunk {i} too large: {len(encoding.encode(doc.page_content))} tokens."
        id_ = f"{prefix}{str(md_file)}:{i}"
        # json_output = json.dumps({"id": id_, "content": chunk.page_content}, ensure_ascii=True)
        json_output = json.dumps({"id": id_, "content": doc.page_content})
        print(json_output)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    verbose: bool = typer.Option(False, "-v", "--verbose", help="verbosity"),
    version: bool = typer.Option(False, "-V", "--version", help="show version"),
):
    log_fmt = (
        r"%(asctime)-15s %(levelname)s %(name)s %(funcName)s:%(lineno)d %(message)s"
    )
    # log_fmt = r"%(asctime)-15s %(levelname)-7s %(message)s"
    if verbose:
        logging.basicConfig(
            format=log_fmt, level=logging.DEBUG, datefmt="%m-%d %H:%M:%S"
        )
    else:
        logging.basicConfig(
            format=log_fmt, level=logging.INFO, datefmt="%m-%d %H:%M:%S"
        )
    logging.getLogger("unstructured").setLevel(logging.WARN)

    if ctx.invoked_subcommand is None and version:
        ctx.invoke(print_version)
    if ctx.invoked_subcommand is None and not version:
        typer.echo(ctx.get_help())


@app.command("version", help="Show version", hidden=True)
def print_version() -> None:
    typer.secho("0.1.0", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()
