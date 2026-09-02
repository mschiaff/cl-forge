# CL Forge

<p align="center">
  <img src="https://github.com/mschiaff/cl-forge/blob/main/docs/assets/banner.png?raw=true" alt="CL Forge banner">
</p>

<p align="center">
  <strong>Fast, typed Python tools for Chilean data and public APIs.</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/cl-forge/"><img src="https://img.shields.io/pypi/v/cl-forge" alt="PyPI version"></a>
  <a href="https://pypi.org/project/cl-forge/"><img src="https://img.shields.io/pypi/pyversions/cl-forge" alt="Supported Python versions"></a>
  <a href="https://github.com/mschiaff/cl-forge/actions/workflows/python-package.yml"><img src="https://img.shields.io/github/actions/workflow/status/mschiaff/cl-forge/python-package.yml?logo=github&label=tests" alt="Test status"></a>
  <a href="https://github.com/mschiaff/cl-forge/blob/main/LICENSE"><img src="https://img.shields.io/github/license/mschiaff/cl-forge" alt="License"></a>
  <a href="https://mschiaff.github.io/cl-forge/"><img src="https://img.shields.io/badge/docs-GitHub%20Pages-blue?logo=github" alt="Documentation"></a>
</p>

CL Forge combines Rust-backed validation utilities with a clean Python interface for the [CMF](https://api.cmfchile.cl/) and [Mercado Público](https://api.mercadopublico.cl/) APIs. It includes synchronous and asynchronous clients, typed responses, configurable HTTP behavior, and flexible credential providers.

## Install

CL Forge supports Python 3.12–3.14.

```bash
pip install cl-forge
```

Using `uv`:

```bash
uv add cl-forge
```

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

The CMF client provides resources for `ipc`, `uf`, `utm`, `usd`, `eur` (also `euro`), `tip`, and `tmc`, plus `raw` JSON and XML access.

> [!NOTE]
> CMF requests require an API key. You can request one through the [CMF API portal](https://api.cmfchile.cl/api_cmf/contactanos.jsp).

### Query Mercado Público

```python
from cl_forge import MarketClient

market = MarketClient("your-mercado-publico-ticket")

active_tenders = market.tender.active()
today_orders = market.order.today()
suppliers = market.supplier.search("70.017.820-K")
```

The Mercado Público client includes typed resources for tenders, purchase orders, suppliers, and buyers, plus raw v1 and v2 access.

> [!NOTE]
> Mercado Público requests require an API ticket. See the [Mercado Público API portal](https://api.mercadopublico.cl/modules/api.aspx) for access details.

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

## API reference

| Area | Public API |
| --- | --- |
| CMF | [`CmfClient`](https://mschiaff.github.io/cl-forge/api/CmfClient/) · [`AsyncCmfClient`](https://mschiaff.github.io/cl-forge/api/AsyncCmfClient/) |
| Mercado Público | [`MarketClient`](https://mschiaff.github.io/cl-forge/api/MarketClient/) · [`AsyncMarketClient`](https://mschiaff.github.io/cl-forge/api/AsyncMarketClient/) |
| Credentials | [`EnvCredentials`](https://mschiaff.github.io/cl-forge/api/EnvCredentials/) · [`DotEnvCredentials`](https://mschiaff.github.io/cl-forge/api/DotEnvCredentials/) |
| HTTP configuration | [`ClientConfig`](https://mschiaff.github.io/cl-forge/api/ClientConfig/) |
| RUT/RUN | [`validate_rut`](https://mschiaff.github.io/cl-forge/api/validate_rut/) · [`calculate_verifier`](https://mschiaff.github.io/cl-forge/api/calculate_verifier/) |
| License plates | [`Ppu`](https://mschiaff.github.io/cl-forge/api/Ppu/) |

Explore the [full documentation](https://mschiaff.github.io/cl-forge/) for installation details and the complete API reference.

## Contributing

Contributions are welcome. Please read the [contributing guide](CONTRIBUTING.md) before opening a pull request.

## License

CL Forge is available under the [Apache License 2.0](LICENSE).
