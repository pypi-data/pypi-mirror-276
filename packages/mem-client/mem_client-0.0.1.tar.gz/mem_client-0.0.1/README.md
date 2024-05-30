# Mem API Client

A Python client for interacting with the Mem API, including support for Mem's unique Markdown format.

## Features

- Create mems with custom content
- Upload mems from Markdown files
- Batch create mems
- Append content to existing mems
- Automatically convert standard Markdown to Mem's Markdown format

## Installation

You can install the `mem-client` package via pip:

```bash
pip install mem-client
```

Or via conda (once published):

```bash
conda install -c conda-forge mem-client
```

## Usage

### Initialization

```python
from mem_client import Client

api_token = "your_api_access_token_here"
client = Client(api_token)
```

### Create a Simple Mem

```python
response = client.create_mem(content="Hello there! I am a new mem.")
print(response)
```

### Create a Mem with Additional Parameters

```python
response = client.create_mem(
    content="Hello there! I am a new mem.",
    is_read=True,
    is_archived=True,
    scheduled_for="2032-08-02T08:15:30-05:00",
    created_at="1994-11-05T08:15:30-05:00"
)
print(response)
```

### Create a Mem from a Markdown File

```python
response = client.create_mem_from_file(file_path="./path/to/filename.md")
print(response)
```

### Batch Create Mems

```python
batch_mems = [
    {"content": "Hello there! I am a new mem."},
    {"content": "I am another new mem!"}
]
response = client.batch_create_mems(batch_mems)
print(response)
```

### Append to an Existing Mem

```python
mem_id = "10000000-0000-4000-a000-000000000000"
response = client.append_to_mem(mem_id, content="This will be appended to the end of the mem!")
print(response)
```

## Command Line Interface (CLI)

### Create a Simple Mem

```bash
python -m mem_client.cli create-mem "Hello there! I am a new mem."
```

### Create a Mem with Additional Parameters

```bash
python -m mem_client.cli create-mem "Hello there! I am a new mem." --is-read --is-archived --scheduled-for "2032-08-02T08:15:30-05:00" --created-at "1994-11-05T08:15:30-05:00"
```

### Create a Mem from a Markdown File

```bash
python -m mem_client.cli create-mem-from-file ./path/to/filename.md
```

### Batch Create Mems

```bash
python -m mem_client.cli batch-create-mems ./path/to/mems.json
```

### Append to an Existing Mem

```bash
python -m mem_client.cli append-to-mem 10000000-0000-4000-a000-000000000000 "This will be appended to the end of the mem!"
```

## Documentation Links

- [Create a Mem](https://docs.mem.ai/docs/api/mems/create)
- [Batch Create Mems](https://docs.mem.ai/docs/api/mems/batch-create)
- [Append to a Mem](https://docs.mem.ai/docs/api/mems/append)
- [Authentication](https://docs.mem.ai/docs/general/authentication)
- [Error Handling](https://docs.mem.ai/docs/general/handling-errors)
- [Mem Markdown Format Information](https://docs.mem.ai/docs/general/mem-markdown-format)

## Error Handling

The client raises appropriate exceptions for various error conditions, such as invalid requests, unauthorized access, and server errors. For more details, refer to the [Error Handling documentation](https://docs.mem.ai/docs/general/handling-errors).

## License

This project is licensed under the MIT License.
- Append content to existing mems
- Automatically convert standard Markdown to Mem's Markdown format

## Installation

You can install the `mem-client` package via pip:

```bash
pip install mem-client
```

Or via conda (once published):

```bash
conda install -c conda-forge mem-client
```

## Usage

### Initialization

```python
from mem_client import Client

api_token = "your_api_access_token_here"
client = Client(api_token)
```

### Create a Simple Mem

```python
response = client.create_mem(content="Hello there! I am a new mem.")
print(response)
```

### Create a Mem with Additional Parameters

```python
response = client.create_mem(
    content="Hello there! I am a new mem.",
    is_read=True,
    is_archived=True,
    scheduled_for="2032-08-02T08:15:30-05:00",
    created_at="1994-11-05T08:15:30-05:00"
)
print(response)
```

### Create a Mem from a Markdown File

```python
response = client.create_mem_from_file(file_path="./path/to/filename.md")
print(response)
```

### Batch Create Mems

```python
batch_mems = [
    {"content": "Hello there! I am a new mem."},
    {"content": "I am another new mem!"}
]
response = client.batch_create_mems(batch_mems)
print(response)
```

### Append to an Existing Mem

```python
mem_id = "10000000-0000-4000-a000-000000000000"
response = client.append_to_mem(mem_id, content="This will be appended to the end of the mem!")
print(response)
```

## Command Line Interface (CLI)

### Create a Simple Mem

```bash
python -m mem_client.cli create-mem "Hello there! I am a new mem."
```

### Create a Mem with Additional Parameters

```bash
python -m mem_client.cli create-mem "Hello there! I am a new mem." --is-read --is-archived --scheduled-for "2032-08-02T08:15:30-05:00" --created-at "1994-11-05T08:15:30-05:00"
```

### Create a Mem from a Markdown File

```bash
python -m mem_client.cli create-mem-from-file ./path/to/filename.md
```

### Batch Create Mems

```bash
python -m mem_client.cli batch-create-mems ./path/to/mems.json
```

### Append to an Existing Mem

```bash
python -m mem_client.cli append-to-mem 10000000-0000-4000-a000-000000000000 "This will be appended to the end of the mem!"
```

## Documentation Links

- [Create a Mem](https://docs.mem.ai/docs/api/mems/create)
- [Batch Create Mems](https://docs.mem.ai/docs/api/mems/batch-create)
- [Append to a Mem](https://docs.mem.ai/docs/api/mems/append)
- [Authentication](https://docs.mem.ai/docs/general/authentication)
- [Error Handling](https://docs.mem.ai/docs/general/handling-errors)
- [Mem Markdown Format Information](https://docs.mem.ai/docs/general/mem-markdown-format)

## Error Handling

The client raises appropriate exceptions for various error conditions, such as invalid requests, unauthorized access, and server errors. For more details, refer to the [Error Handling documentation](https://docs.mem.ai/docs/general/handling-errors).

## License

This project is licensed under the MIT License.