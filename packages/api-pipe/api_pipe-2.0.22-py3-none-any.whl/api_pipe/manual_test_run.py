'''
    Manual test run

    (Entry Point)
'''
import os
import logging
import httpx
import asyncio
import json
from pathlib import Path
from copy import deepcopy

from api_pipe.api import ApiPipe
from api_pipe import config
from api_pipe.url import Url
from api_pipe.params import ApiParams

DUMMY_TEST_GROUP_ID = 79866152

gitlab_url = Url("https://gitlab.com/api/v4")

common_params = ApiParams(
    headers={
        "PRIVATE-TOKEN": os.environ["TOKEN"]
    },
    timeout=(5.0, 5.0),
    retries={
        "initial_delay": 0.5,
        "backoff_factor": 3,
        "max_retries": 7,
    },
    logs={
        "unique_name": "__TO_BE_REPLACED__",
        "log_dir": Path("../logs"),
        "level": logging.DEBUG,
        "words_to_highlight": config.logger_words_to_highlight
    }
)

def main():
    asyncio.run(async_main())

async def async_main():
    '''
        Main
    '''
    async with httpx.AsyncClient() as client:
        await test_fetch_async(client)

    with httpx.Client() as client:
        test_fetch(client)
        test_fetch_all(client)

async def test_fetch_async(client: httpx.AsyncClient):
    '''
        Test run fetch async
    '''
    params = deepcopy(common_params)
    params.logs["unique_name"] = "test_run_fetch_async"

    api = ApiPipe(
        gitlab_url / "groups" / DUMMY_TEST_GROUP_ID / "members",
        client,
        params
    )

    await api.fetch_async()

    api.to_python()    \
        .to_json(indent=2)

    #print(api.data)

def test_fetch(client: httpx.Client):
    '''
        Test run fetch
    '''
    params = deepcopy(common_params)
    params.logs["unique_name"] = "test_gitlab_read_var"

    api = ApiPipe(
        gitlab_url / "groups" / DUMMY_TEST_GROUP_ID / "variables",
        client,
        params
    )

    api                         \
        .fetch()                \
        .to_python()            \
        .select([
            "key",
            "value",
            "masked",
        ])                      \
        .filter(
            lambda item: item["key"] == "Var2"
        )                       \
        .to_json(indent=2)

    #print(api.data)


def test_fetch_all(client: httpx.Client):
    '''
        Test fetch all
    '''
    params = deepcopy(common_params)
    page_number = 1
    results: list = []

    while True:

        url = gitlab_url                    \
            / "groups"                      \
            / DUMMY_TEST_GROUP_ID           \
            / "variables"                   \
            / f"?page={page_number}&per_page=1"

        params.logs["unique_name"] = f"test_run_fetch_all_{page_number}"

        api = ApiPipe(
            url,
            client,
            params
        )
        api                         \
            .fetch()                \
            .to_python()        \
            .select([
                "key",
                "value",
                "masked",
            ])

        if api.data:
            results += api.data
        else:
            break

        page_number += 1

    # print(
    #     "Number of calls made: ", page_number, " (last one was empty)"
    # )

    # print(
    #     json.dumps(results, indent=2)
    # )
