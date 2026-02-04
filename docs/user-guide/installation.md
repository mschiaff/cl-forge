CL Forge is a Python librarie available on [PyPI](https://pypi.org/project/cl-forge/) and can be installed using
`pip`, `uv` or any other Python package manager.

## From PyPI

Using `uv`:

```shell
uv add cl-forge
```

Or using `pip`:

```shell
pip install cl-forge
```

## From Source

!!! info

    Building from source requires a Rust toolchain installed on your system. See [Install Rust](https://rust-lang.
    org/tools/install/) for more information. 

### Using `uv` (Recommended)

```shell
uv add "git+https://github.com/mschiaff/cl-forge.git@<version-tag>"
```

Including optional dependencies:

```shell
uv add "git+https://github.com/mschiaff/cl-forge.git@<version-tag>[dep1, ...]"
```

### Using `pip`

```shell
pip install "git+https://github.com/mschiaff/cl-forge.git@<version-tag>"
```

Including optional dependencies:

```shell
pip install "git+https://github.com/mschiaff/cl-forge.git@<version-tag>[dep1, ...]"
```

## Dependencies

### Required Dependencies

CL Forge requires the following dependencies:

| Package    | Version    |
|------------|------------|
| `orjson`   | `>=3.11.7` |
| `pydantic` | `>=2.12.5` |

### Optional Dependencies

CL Forge has several optional dependencies, although none are actually required to support any functionality. They 
are more of a convenience to support likely uses.

???+ tip "Analytics Recommendations"

    If you are planning on using CL Forge to get, manipulate and export data from API clients, we strongly 
    recommend installing the `analytics` tag. If you're working on a Jupyter Notebook environment, we encourage 
    you to also include the `notebook` tag.
    
    Using `uv`:
    ```shell
    uv add "cl-forge[analytics, notebook]"
    ```
    
    Or using `pip`:
    ```shell
    pip install "cl-forge[analytics, notebook]"
    ```
    ??? note "Why?"

        Polars is a fast and memory efficient dataframe library that stands out for its performance. Furthermore, 
        parsing lists of `Pydantic` models into polars dataframes is quite straightforward:
        
        ```python
        import polars as pl
        
        data: list[BaseModel] = ...
        df = pl.DataFrame(data)
        ```

#### Interoperability

| Tag       | Description                                       |
|-----------|---------------------------------------------------|
| `polars`  | Convert data to and from polars dataframes/series |
| `pandas`  | Convert data to and from pandas dataframes/series |
| `pyarrow` | Convert data to and from pyarrow tables/arrays    |
| `interop` | Installs all interoperability dependencies        |

#### Excel
| Tag          | Description                                      |
|--------------|--------------------------------------------------|
| `calamine`   | Read from Excel files using the calamine engine  |
| `openpyxl`   | Read from Excel files using the openpyxl engine  |
| `xlsxwriter` | Write to Excel files using the xlsxwriter engine |
| `excel`      | Installs all Excel dependencies                  |

#### Others

| Tag         | Description                                                      |
|-------------|------------------------------------------------------------------|
| `notebook`  | Installs Jupyter Notebook support dependencies                   |
| `analytics` | Installs data analytics suggested dependencies                   |
| `all`       | Installs all optional dependencies but the ones from development |

### Dependency Groups

!!! info

    These aren't extras you can install, but rather dependency groups defined in the `uv` configuration for development
    purposes.
    ??? example

        ```shell
        git clone https://github.com/mschiaff/cl-forge.git
        cd cl-forge
        uv sync --group build
        ```

#### Development

| Tag     | Description                           |
|---------|---------------------------------------|
| `build` | Installs build dependencies           |
| `docs`  | Installs documentation dependencies   |
| `test`  | Installs test dependencies            |
| `dev`   | Installs all development dependencies |