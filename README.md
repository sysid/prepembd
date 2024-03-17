# prepembd

[![PyPi](https://img.shields.io/pypi/v/inka2)](https://pypi.org/project/prepembd)
[![Tests CI](https://img.shields.io/github/actions/workflow/status/sysid/prepembd/test.yml?branch=main)](https://github.com/sysid/inka2/actions/workflows/prepembd.yml)
[![Codecov](https://codecov.io/gh/sysid/prepembd/branch/main/graph/badge.svg?token=8IL9MN4FK5)](https://codecov.io/gh/sysid/prepembd)


## Installation

Install **prepembd**:

```shell
python3 -m pip install prepembd --upgrade
```

### Requirements

- [Python](https://www.python.org/) >= 3.10

## Why

I've been using markdown now for a long time to take notes in every possible scenario. I even manage my Anki cards with markdown ([inka2](https://github.com/sysid/inka2)) so finding relevant information again is paramount.
With the advent of semantic search via Embeddings search became so much more powerfull. However, to create the
embeddings out of markdown the files have to be prepared in order to reduce noice and create the correct chunk sizes.

This Python script automates the process and creates a json representation of all the markdown files which then can be fed into an embedding model. It is basically just a thin wrapper aroung LangChain combined with some bespoke filter to eliminated noise.


## Usage
```bash
prepembd tokenize --prefix '$VIMWIKI_PATH/' <directory> | tee -a output.ndjson

# cat output.ndjson:
{
  "id": "$VIMWIKI_PATH/help/qk/quarkus.md:0",
  "content": "..."
}
{
  "id": "$VIMWIKI_PATH/help/qk/quarkus.md:1",
  "content": "..."
}
{
  "id": "$VIMWIKI_PATH/help/qk/quarkus.md:2",
  "content": "..."
}
```

This script integrates particularly well with [bkmr](https://github.com/sysid/bkmr).
