<!-- docs_start -->

# Superblocks Python SDK

[![Python version](https://img.shields.io/badge/python-%3E=_3.10-teal.svg)](https://www.python.org/downloads/)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```sh
pip install superblocks-agent
```

## Quickstart

### Run an API

```python3
import asyncio

from superblocks_agent.api import Api, Config as ApiConfig
from superblocks_agent.client import Client, Config


# configure client
client = Client(
    config=Config(
        endpoint="some.agent.host:8081", token="my-token-here"
    )
)

# specify api to run
api = Api("my-api-id-here", config=ApiConfig(profile="staging"))

# run with client in context manager
with client as c:
    # run syncronously (default)
    sync_result = api.run(client=c)
    # run asyncronously by passing in `run_async=True`
    async_result = asyncio.run(api.run(client=c, run_async=True))

# run and manually close client after
sync_result = api.run(client=client)
async_result = asyncio.run(api.run(client=client, run_async=True))
client.close()

# get api output
print(sync_result.get_result())
print(async_result.get_result())
# get block output by name
print(sync_result.get_block_result("Step1"))
print(async_result.get_block_result("Step1"))
```

### Run an API with inputs

```python3
from superblocks_agent.api import Api
from superblocks_agent.api import Config as ApiConfig
from superblocks_agent.client import Client, Config


client = Client(
    config=Config(
        endpoint="some.agent.host:8081", token="my-token-here"
    )
)

api = Api("my-api-id-here", config=ApiConfig(profile="staging"))


with client as c:
    # specify inputs for api run
    sync_result = api.run(client=c, inputs={"input1": "foo", "input2": 5})
```

### Run an API and Mock a Step

```python3
from superblocks_agent.api import Api,Config as ApiConfig
from superblocks_agent.client import Client, Config
from superblocks_agent.testing.step import on, Params

client = Client(
    config=Config(
        endpoint="some.agent.host:8081", token="my-token-here"
    )
)

api = Api("my-api-id-here", config=ApiConfig(profile="staging"))

# create a mock for any step named "Step1" and have it return {"im": "mocked"}
mock = on(params=Params(step_name="Step1")).return_({"im": "mocked"})

with client as c:
    # pass in mocks
    sync_result = api.run(client=c, mocks=[mock])
```

<!-- docs_stop -->
