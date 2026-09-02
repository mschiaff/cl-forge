# CL Forge

<figure markdown="span">
  ![CL Forge banner](assets/banner.png)
</figure>

<p align="center">
  <strong>Fast, typed Python tools for Chilean data and public APIs.</strong>
</p>

<div align="center" markdown="1">
  [Get started](install.md){ .md-button .md-button--primary }
  [API reference](api/CmfClient.md){ .md-button }
</div>

<div align="center" markdown="1">
  [![PyPI version](https://img.shields.io/pypi/v/cl-forge)](https://pypi.org/project/cl-forge/)
  [![Supported Python versions](https://img.shields.io/pypi/pyversions/cl-forge)](https://pypi.org/project/cl-forge/)
  [![Test status](https://img.shields.io/github/actions/workflow/status/mschiaff/cl-forge/python-package.yml?logo=github&label=tests)](https://github.com/mschiaff/cl-forge/actions/workflows/python-package.yml)
  [![License](https://img.shields.io/github/license/mschiaff/cl-forge)](https://github.com/mschiaff/cl-forge/blob/main/LICENSE)
</div>

CL Forge combines Rust-backed validation utilities with a clean Python interface for the [CMF](https://api.cmfchile.cl/) and [Mercado Público](https://api.mercadopublico.cl/) APIs. It includes synchronous and asynchronous clients, typed responses, configurable HTTP behavior, and flexible credential providers.

## Install

CL Forge supports Python 3.12–3.14.

=== ":simple-python: pip"

    ```bash
    pip install cl-forge
    ```

=== ":simple-astral: uv"

    ```bash
    uv add cl-forge
    ```

See the [installation guide](install.md) for source installs and optional dependencies.

## Quick start

### Validate Chilean identifiers

```python
from cl_forge import Ppu, calculate_verifier, validate_rut

validate_rut(12_345_678, "5")     # True
calculate_verifier(12_345_678)    # "5"

plate = Ppu("PHZF55")
plate.complete                    # "PHZF55-K"
plate.numeric                     # 69455
```

### Query CMF indicators

```python
from cl_forge import CmfClient

cmf = CmfClient("your-cmf-api-key")

latest_uf = cmf.uf.latest()
ipc_2025 = cmf.ipc.year(2025)
usd_for_day = cmf.usd.day(2025, 12, 1)
```

The [CMF client](api/CmfClient.md) provides resources for `ipc`, `uf`, `utm`, `usd`, `eur` (also `euro`), `tip`, and `tmc`, plus `raw` JSON and XML access.

!!! note "CMF credentials"

    CMF requests require an API key. You can request one through the [CMF API portal](https://api.cmfchile.cl/api_cmf/contactanos.jsp).

### Query Mercado Público

```python
from cl_forge import MarketClient

market = MarketClient("your-mercado-publico-ticket")

active_tenders = market.tender.active()
today_orders = market.order.today()
suppliers = market.supplier.search("70.017.820-K")
```

The [Mercado Público client](api/MarketClient.md) includes typed resources for tenders, purchase orders, suppliers, and buyers, plus raw v1 and v2 access.

!!! note "Mercado Público credentials"

    Mercado Público requests require an API ticket. See the [Mercado Público API portal](https://api.mercadopublico.cl/modules/api.aspx) for access details.

### Use async clients

The asynchronous clients mirror the synchronous resource interface:

```python
from cl_forge import AsyncCmfClient

cmf = AsyncCmfClient("your-cmf-api-key")
latest_uf = await cmf.uf.latest()
```

## Credentials and configuration

Pass a credential directly, load it from the environment, or read it from a dotenv file:

```bash
export CLFORGE_CMF_API_KEY="your-cmf-api-key"
export CLFORGE_MARKET_API_KEY="your-mercado-publico-ticket"
```

```python
from cl_forge import ClientConfig, CmfClient, DotEnvCredentials, EnvCredentials

cmf = CmfClient(
    credentials=EnvCredentials(),
    config=ClientConfig(timeout=20, http2=True, retries=5),
)

cmf_from_dotenv = CmfClient(DotEnvCredentials(".env"))
```

## API at a glance

| Area | Public API |
| --- | --- |
| CMF | [`CmfClient`](api/CmfClient.md) · [`AsyncCmfClient`](api/AsyncCmfClient.md) |
| Mercado Público | [`MarketClient`](api/MarketClient.md) · [`AsyncMarketClient`](api/AsyncMarketClient.md) |
| Credentials | [`EnvCredentials`](api/EnvCredentials.md) · [`DotEnvCredentials`](api/DotEnvCredentials.md) |
| HTTP configuration | [`ClientConfig`](api/ClientConfig.md) |
| RUT/RUN | [`validate_rut`](api/validate_rut.md) · [`calculate_verifier`](api/calculate_verifier.md) |
| License plates | [`Ppu`](api/Ppu.md) |

## Contributing

Contributions are welcome. Please read the [contributing guide](contributing.md) before opening a pull request.

## License

CL Forge is available under the [Apache License 2.0](https://github.com/mschiaff/cl-forge/blob/main/LICENSE).
