#
<img style="border-radius: 25px;" alt="logo" src="assets/banner.png"/>

<h2 style="text-align: center;">
   Simple yet powerful Chilean tools written in Rust and Python.
</h2>

<br>

<div style="text-align: center;">
   <a href="https://pypi.org/project/cl-forge/" style="text-decoration: none;">
      <img src="https://img.shields.io/pypi/v/cl-forge.svg" alt="pypi">
   </a>
   <a href="https://github.com/mschiaff/cl-forge/actions/workflows/python-package.yml" style="text-decoration: none;">
      <img src="https://github.com/mschiaff/cl-forge/actions/workflows/python-package.yml/badge.svg?branch=main" alt="python package">
   </a>
   <a href="https://github.com/mschiaff/cl-forge/actions/workflows/release-python.yml" style="text-decoration: none;">
      <img src="https://github.com/mschiaff/cl-forge/actions/workflows/release-python.yml/badge.svg" alt="python release">
   </a>
</div>

`cl-forge` provides a collection of high-performance utilities for common Chilean data formats and API integrations. The core logic is implemented in Rust for maximum speed, with a clean and easy-to-use Python interface.

## Features

- **High Performance**: Core logic written in Rust.
- **Verify**: Efficiently validate Chilean RUT/RUN and PPU (License Plates).
- **API Integrations**: Simple clients to interact with the [CMF](https://api.cmfchile.cl) and [Public Market](https://api.mercadopublico.cl) APIs.
- **Type Safety**: Full type hints and `.pyi` stubs for excellent IDE support.

## Examples

### Validate

You can validate if a verifier digit is correct for a given numeric part of a RUT/RUN.

```python
from cl_forge import verify

is_valid = verify.validate_rut(8750720, "3")

print(f"RUT is valid: {is_valid}")
# RUT is valid: True
```

... Or you can calculate the verifier digit yourself.

```python
from cl_forge import verify

dv = verify.calculate_verifier(8750720)

print(f"Verifier digit: {dv}")
# Verifier digit: 3
```

### Generate

Need to generate a bunch of random, unique and valid RUTs? No problem! And you can even specify a random seed, so you can reproduce the same results every time.

```python
from cl_forge import verify

ruts = verify.generate(
   n=100,
   min=1_000_000,
   max=20_000_000,
   seed=42
)

print(ruts)
# [{'correlative': 8750720, 'verifier': '3'}, ...]
```

### API Clients

The CMF API client allows you to easily interact with the [CMF](https://api.cmfchile.cl) API.

```python
from cl_forge.cmf import CmfClient

client = CmfClient(api_key="your-api-key")

# Get latest IPC data
ipc_data = client.get(path="/ipc")

print(ipc_data)
# {'IPCs': [{'Valor': '-0,2', 'Fecha': '2025-12-01'}]}
```

!!! note
   
    To use the CMF API, you need an API key. You can request one at [CMF Chile](https://api.cmfchile.cl/api_cmf/contactanos.jsp).

See the [CMF API documentation](https://api.cmfchile.cl/documentacion/index.html) for details about the available endpoints.

## Contributing

Pull requests are welcome. For changes and reporting bugs, please open an issue first to discuss it. Read our [Contributing Guide](contributing.md) for more details.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](https://github.com/mschiaff/cl-forge/blob/main/LICENSE) file for details.