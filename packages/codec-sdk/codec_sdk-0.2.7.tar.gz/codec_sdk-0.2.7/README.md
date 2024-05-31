# Codec Python Library

The Codec Python library provides convenient access to the Codec API from applications written in Python 3.

## Documentation

See the [Codec docs](https://docs.codec.io).

## Installation

You don't need this source code unless you want to modify the package. If you just want to use the package, just run:

```python
pip install --upgrade codec-sdk
```

### Requirements
Python 3.8+


## Usage

The library needs to be configured with your team's API key which is available in the [Codec Dashboard](https://codec.io/dashboard). Instantiate the Codec client with it:

```python
from codec import Codec

codec = Codec("pk_xxx...")

# Get a collection
collection = codec.collections.get("col_xxx...")

# Search within videos in a collection
query = "trump wearing a red hat and talking about north korea"
results = codec.search(
    query=query,
    search_types=["visual", "speech"],
    collection=collection.uid,
    max_results=5
)
```

### Handling exceptions
Unsuccessful requests raise exceptions. The class of the exception will reflect the sort of error that occurred, and the error message will provide more context. See the [API reference](https://docs.codec.io) for a description of the error classes you should handle.


## Support
For support, reach out to [support@codec.io](mailto:support@codec.io).
