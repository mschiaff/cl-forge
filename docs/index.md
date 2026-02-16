# Welcome to CL Forge!

<img src="https://github.com/mschiaff/cl-forge/blob/main/docs/assets/banner.png?raw=true" align="center" style="border-radius: 25px;" alt="banner"/>

<h2 align="center">Simple yet powerful Chilean tools written in Rust and Python.</h2>

<figure markdown="1">

[![PyPI - Version](https://img.shields.io/pypi/v/cl-forge)](https://pypi.org/project/cl-forge/)
[![GitHub Release](https://img.shields.io/github/v/release/mschiaff/cl-forge)](https://github.com/mschiaff/cl-forge/releases/latest)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cl-forge)](https://pypi.org/project/cl-forge/)
[![GH Pages - Docs](https://img.shields.io/badge/Pages-Docs-blue?logo=github)](https://mschiaff.github.io/cl-forge/)

</figure>

<figure markdown="1">

![PyPI - Status](https://img.shields.io/pypi/status/cl-forge)
![PyPI - Types](https://img.shields.io/pypi/types/cl-forge)
[![GitHub License](https://img.shields.io/github/license/mschiaff/cl-forge)](https://github.com/mschiaff/cl-forge/blob/main/LICENSE)

</figure>

<figure markdown="1">

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/mschiaff/cl-forge/python-package.yml?logo=github&label=Tests)](https://github.com/mschiaff/cl-forge/actions/workflows/python-package.yml)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/mschiaff/cl-forge/release-python.yml?logo=github&label=Release)](https://github.com/mschiaff/cl-forge/actions/workflows/release-python.yml)
[![pages-build-deployment](https://github.com/mschiaff/cl-forge/actions/workflows/pages/pages-build-deployment/badge.svg?branch=gh-pages)](https://github.com/mschiaff/cl-forge/actions/workflows/pages/pages-build-deployment)

</figure>


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

!!! important
   
    To use the CMF API, you need an API key. You can request one at [Contact CMF](https://api.cmfchile.cl/api_cmf/contactanos.jsp).

See the [API Reference](https://mschiaff.github.io/cl-forge/api/cmf/base_client/) for endpoint-specific clients, and the [CMF API documentation](https://api.cmfchile.cl/documentacion/index.html) for details about all the available endpoints.

The Public Market API client also allows you to easily interact with the [Mercado Público](https://api.mercadopublico.cl) API.

```python
from cl_forge.market import MarketClient

client = MarketClient(ticket='your-api-ticket')

tenders_data = client.get(path="/licitaciones")

print(tenders_data)
#{'Cantidad': 463,
# 'FechaCreacion': '2026-02-12T16:07:58.813315Z',
# 'Version': 'v1',
# 'Listado': [{'CodigoExterno': '1057049-30-B226',
#   'Nombre': 'CSP- SERVICIO DE INMUNOHISTOQUÍMICA Y CISH',
#   'CodigoEstado': 5,
#   'FechaCierre': '2026-02-23T15:30:00'},
#  {'CodigoExterno': '1057374-8-L126',
# ...}
```

!!! important

    To use the Mercado Público API, you need an API ticket. You can request one at [Contact Mercado Público](https://api.mercadopublico.cl/modules/IniciarSesion.aspx). To request this API ticket, you will also have to request and activate your [ClaveÚnica](https://claveunica.gob.cl).

See the [Mercado Público API documentation](https://api.mercadopublico.cl/modules/api.aspx) for details about all the available endpoints. **Endpoint-specific clients coming soon in future updates.**

## Contributing

Pull requests are welcome. For changes and reporting bugs, please open an issue first to discuss it. Read our [Contributing Guide](contributing.md) for more details.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](https://github.com/mschiaff/cl-forge/blob/main/LICENSE) file for details.