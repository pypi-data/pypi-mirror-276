import random
import time

import pytest
from loguru import logger

from jamaibase import JamAI
from jamaibase.protocol import (
    ColumnSchemaCreate,
    GenConfigUpdateRequest,
    RowAddRequest,
    RowRegenRequest,
    TableSchemaCreate,
    TableType,
)

GEN_TYPES = ["REGEN"]


@pytest.fixture
def jamai_client():
    yield JamAI()


def _create_table(
    jamai_client: JamAI,
    table_type: TableType,
    cols_info: tuple[dict[str, str], dict[str, str]] = None,
):
    table_id = f"{table_type.value}_{random.randint(10000, 99999)}"
    schema = TableSchemaCreate(
        id=table_id,
        cols=(
            [
                ColumnSchemaCreate(id="article 1", dtype="str"),
                ColumnSchemaCreate(id="summary", dtype="str"),
            ]
            if cols_info is None
            else (
                [ColumnSchemaCreate(id=k, dtype=v) for k, v in cols_info[0].items()]
                + [ColumnSchemaCreate(id=k, dtype=v) for k, v in cols_info[1].items()]
            )
        ),
    )
    if table_type == TableType.action:
        table = jamai_client.create_action_table(schema)
    else:
        raise ValueError(f"Invalid table type: {table_type}")
    return table, table_id


def _update_gen_config(
    jamai_client: JamAI, table_type: TableType, gen_config: GenConfigUpdateRequest
):
    jamai_client.update_gen_config(table_type, gen_config)


# ---------------------------------------------------------
# Test Cases for concurrent Execution
# ---------------------------------------------------------
def column_map_prompt(content: str, max_tokens: int):
    return {
        "id": "",
        # "model": "openai/gpt-3.5-turbo",
        # "model": "openai/gpt-4-turbo",
        "model": "openai/gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": "You are a concise assistant.",
            },
            {
                "role": "user",
                "content": content,
            },
        ],
        "functions": [],
        "function_call": "auto",
        "temperature": 0.01,
        "top_p": 0.1,
        "stream": False,
        "stop": [],
        "max_tokens": max_tokens,
    }


def data():
    input_dict = {"xx": "str", "yy": "str", "zz": "str"}
    # output_dict = {
    #     "aa": "str",
    #     "bb": "str",
    #     "cc": "str",
    #     "dd": "str",
    #     "ee": "str",
    #     "ff": "str",
    # }
    output_dict2 = {
        "aa": "str",
        "bb": "str",
        "cc": "str",
        # ---
        "dd": "str",
        "ee": "str",
        "ff": "str",
        "dd2": "str",
        "ee2": "str",
        "ff2": "str",
        # ---
        "aa3": "str",
        "bb3": "str",
        "cc3": "str",
        "dd3": "str",
        "ee3": "str",
        "ff3": "str",
        "dd23": "str",
        "ee23": "str",
        "ff23": "str",
    }
    row = {"xx": "1", "yy": "2", "zz": "3"}
    # inv_nodes = [  # map - end: (start, expected_gen_output)
    #     # {
    #     #     "aa": (["xx"], "<xx:1>"),
    #     #     "bb": (["yy"], "<yy:2>"),
    #     #     "cc": (["zz"], "<zz:3>"),
    #     #     # "dd": (["xx"], "<xx:1>"),
    #     #     # "ee": (["yy"], "<yy:2>"),
    #     #     # "ff": (["zz"], "<zz:3>"),
    #     # },
    #     {
    #         "aa": (["xx"], "<xx:1>"),
    #         "bb": (["yy"], "<yy:2>"),
    #         "cc": (["zz"], "<zz:3>"),
    #         "dd": (["aa"], "<aa:<xx:1>>"),
    #         "ee": (["bb"], "<bb:<yy:2>>"),
    #         "ff": (["cc"], "<cc:<zz:3>>"),
    #     },
    #     # {
    #     #     "aa": (["xx"], "<xx:1>"),
    #     #     "bb": (["yy"], "<yy:2>"),
    #     #     "cc": (["zz"], "<zz:3>"),
    #     #     "dd": (["aa", "bb"], "(<aa:<xx:1>> & <bb:<yy:2>>)"),
    #     #     "ee": (["cc"], "<cc:<zz:3>>"),
    #     #     "ff": (
    #     #         ["dd", "ee"],
    #     #         "(<dd:(<aa:<xx:1>> & <bb:<yy:2>>)> & <ee:<cc:<zz:3>>>)",
    #     #     ),
    #     # },
    #     # {
    #     #     "aa": (["xx"], "<xx:1>"),
    #     #     "bb": (["yy"], "<yy:2>"),
    #     #     "cc": (["zz"], "<zz:3>"),
    #     #     "dd": (["aa", "bb"], "(<aa:<xx:1>> & <bb:<yy:2>>)"),
    #     #     "ee": (["cc", "dd"], "(<cc:<zz:3>> & <dd:(<aa:<xx:1>> & <bb:<yy:2>>)>)"),
    #     #     "ff": (
    #     #         ["dd", "ee"],
    #     #         "(<dd:(<aa:<xx:1>> & <bb:<yy:2>>)> & <ee:(<cc:<zz:3>> & <dd:(<aa:<xx:1>> & <bb:<yy:2>>)>)>)",
    #     #     ),
    #     # },
    #     # {
    #     #     "aa": (["xx", "yy"], "(<xx:1> & <yy:2>)"),
    #     #     "bb": (["aa"], "<aa:(<xx:1> & <yy:2>)>"),
    #     #     "cc": (["zz", "bb"], "(<zz:3> & <bb:<aa:(<xx:1> & <yy:2>)>>)"),
    #     #     "dd": (["cc"], "<cc:(<zz:3> & <bb:<aa:(<xx:1> & <yy:2>)>>)>"),
    #     #     "ee": (
    #     #         ["cc", "dd"],
    #     #         "(<cc:(<zz:3> & <bb:<aa:(<xx:1> & <yy:2>)>>)> & <dd:<cc:(<zz:3> & <bb:<aa:(<xx:1> & <yy:2>)>>)>>)",
    #     #     ),
    #     #     "ff": (
    #     #         ["aa", "bb", "cc", "dd", "ee"],
    #     #         "(<aa:(<xx:1> & <yy:2>)> & <bb:<aa:(<xx:1> & <yy:2>)>> & <cc:(<zz:3> & <bb:<aa:(<xx:1> & <yy:2>)>>)> & <dd:<cc:(<zz:3> & <bb:<aa:(<xx:1> & <yy:2>)>>)>> & <ee:(<cc:(<zz:3> & <bb:<aa:(<xx:1> & <yy:2>)>>)> & <dd:<cc:(<zz:3> & <bb:<aa:(<xx:1> & <yy:2>)>>)>>)>)",
    #     #     ),
    #     # },
    #     # {
    #     #     "aa": (["xx", "yy", "zz"], "(<xx:1> & <yy:2> & <zz:3>)"),
    #     #     "bb": (["aa"], "<aa:(<xx:1> & <yy:2> & <zz:3>)>"),
    #     #     "cc": (["bb"], "<bb:<aa:(<xx:1> & <yy:2> & <zz:3>)>>"),
    #     #     "dd": (["cc"], "<cc:<bb:<aa:(<xx:1> & <yy:2> & <zz:3>)>>>"),
    #     #     "ee": (["yy", "zz"], "(<yy:2> & <zz:3>)"),
    #     #     "ff": (
    #     #         ["dd", "ee"],
    #     #         "(<dd:<cc:<bb:<aa:(<xx:1> & <yy:2> & <zz:3>)>>>> & <ee:(<yy:2> & <zz:3>)>)",
    #     #     ),
    #     # },
    #     # {
    #     #     "aa": (["xx"], "<xx:1>"),
    #     #     "bb": (["yy"], "<yy:2>"),
    #     #     "cc": (["zz"], "<zz:3>"),
    #     #     "dd": (["xx"], "<xx:1>"),
    #     #     "ee": (["yy"], "<yy:2>"),
    #     #     "ff": (["zz"], "<zz:3>"),
    #     # },
    # ]
    inv_nodes2 = [  # map - end: (start, expected_gen_output)
        {
            "aa": (["xx"], "<xx:1>"),
            "bb": (["yy"], "<yy:2>"),
            "cc": (["zz"], "<zz:3>"),
            # ---
            "dd": (["aa"], "<aa:<xx:1>>"),
            "ee": (["bb"], "<bb:<yy:2>>"),
            "ff": (["cc"], "<cc:<zz:3>>"),
            "dd2": (["aa"], "<aa:<xx:1>>"),
            "ee2": (["bb"], "<bb:<yy:2>>"),
            "ff2": (["cc"], "<cc:<zz:3>>"),
            # ---
            "aa3": (["dd2"], "<dd2:<aa:<xx:1>>>"),
            "bb3": (["ee2"], "<ee2:<bb:<yy:2>>>"),
            "cc3": (["ff2"], "<ff2:<cc:<zz:3>>>"),
            "dd3": (["dd2"], "<dd2:<aa:<xx:1>>>"),
            "ee3": (["ee2"], "<ee2:<bb:<yy:2>>>"),
            "ff3": (["ee2"], "<ee2:<bb:<yy:2>>>"),
            "dd23": (["dd2"], "<dd2:<aa:<xx:1>>>"),
            "ee23": (["ee2"], "<ee2:<bb:<yy:2>>>"),
            "ff23": (["ee2"], "<ee2:<bb:<yy:2>>>"),
        },
        # {
        #     "aa": (["xx"], "<xx:1>"),
        #     "bb": (["xx"], "<xx:1>"),
        #     "cc": (["xx"], "<xx:1>"),
        #     # ---
        #     "dd": (["xx"], "<xx:1>"),
        #     "ee": (["xx"], "<xx:1>"),
        #     "ff": (["xx"], "<xx:1>"),
        #     "dd2": (["xx"], "<xx:1>"),
        #     "ee2": (["xx"], "<xx:1>"),
        #     "ff2": (["xx"], "<xx:1>"),
        #     # ---
        #     "aa3": (["xx"], "<xx:1>"),
        #     "bb3": (["xx"], "<xx:1>"),
        #     "cc3": (["xx"], "<xx:1>"),
        #     "dd3": (["xx"], "<xx:1>"),
        #     "ee3": (["xx"], "<xx:1>"),
        #     "ff3": (["xx"], "<xx:1>"),
        #     "dd23": (["xx"], "<xx:1>"),
        #     "ee23": (["xx"], "<xx:1>"),
        #     "ff23": (["xx"], "<xx:1>"),
        # }
    ]

    def get_nodes_data(inv_nodes, output_dict, content_postfix, max_tokens):
        nodes_data = []
        for inv_node in inv_nodes:
            column_map = {}
            expected_column_gen = {}
            for end, (starts, expected_gen) in inv_node.items():
                sub_contents = [f"<{start}:${{{start}}}>" for start in starts]
                if len(sub_contents) > 1:
                    sub_content = "(" + " & ".join(sub_contents) + ")"
                else:
                    sub_content = sub_contents[0]
                logger.info(end, starts)
                logger.info(sub_content)
                content = f"{sub_content} \n\n{content_postfix}"
                column_map[end] = column_map_prompt(content, max_tokens)
                expected_column_gen[end] = expected_gen
            nodes_data.append((input_dict, output_dict, column_map, row, expected_column_gen))
        return nodes_data

    content_postfix = "Output exactly the content above, don't include any other information."
    # content_postfix2 = "Output exactly the content above, don't include any other information. Then create a story."
    # all_nodes_data = get_nodes_data(inv_nodes2, output_dict2, content_postfix2, max_tokens=5)
    # all_nodes_data = get_nodes_data(inv_nodes2, output_dict2, content_postfix2, max_tokens=1000)
    # all_nodes_data = get_nodes_data(inv_nodes2, output_dict2, content_postfix2, max_tokens=500)
    # all_nodes_data = get_nodes_data(inv_nodes2, output_dict2, content_postfix2, max_tokens=300)
    all_nodes_data = get_nodes_data(inv_nodes2, output_dict2, content_postfix, max_tokens=100)
    # all_nodes_data = get_nodes_data(inv_nodes, output_dict, content_postfix, max_tokens=100)
    # all_nodes_data = get_nodes_data(inv_nodes, output_dict, content_postfix2, max_tokens=300)
    return all_nodes_data


@pytest.mark.parametrize("gen_type", GEN_TYPES)
@pytest.mark.parametrize("input_dict, output_dict, column_map, row, expected_column_gen", data())
def test_nonstream_concurrent_execution(
    jamai_client: JamAI, gen_type, input_dict, output_dict, column_map, row, expected_column_gen
):
    """
    Tests concurrent execution in non-streaming mode with dependencies.
    """
    meta, table_id = _create_table(
        jamai_client,
        TableType.action,
        cols_info=(
            input_dict,
            output_dict,
        ),
    )
    gen_config = GenConfigUpdateRequest(table_id=table_id, column_map=column_map)
    _update_gen_config(jamai_client, TableType.action, gen_config)

    response = jamai_client.add_table_rows(
        TableType.action,
        RowAddRequest(table_id=table_id, data=[row], stream=False, concurrent=True),
    )

    # Verify all output columns were executed
    for response in response.rows:
        for output_column_name in output_dict.keys():
            assert output_column_name in response.columns

    if gen_type == "REGEN":
        rows = jamai_client.list_table_rows(TableType.action, table_id)
        row_id = rows.items[0]["ID"]
        response = jamai_client.regen_table_rows(
            TableType.action,
            RowRegenRequest(table_id=table_id, row_ids=[row_id], stream=False, concurrent=True),
        )

    # Get rows
    rows = jamai_client.list_table_rows(TableType.action, table_id)
    for i in range(len(response.rows)):
        row_id = rows.items[i]["ID"]
        row = jamai_client.get_table_row(TableType.action, table_id, row_id)

        # Compare generated outputs with expected outputs
        for output_column_name in output_dict.keys():
            expected_gen = expected_column_gen[output_column_name]
            column_gen = row[output_column_name]["value"]
            len_expected_gen = len(expected_gen)
            len_column_gen = len(column_gen)
            if len_column_gen >= len_expected_gen:
                assert column_gen[:len_expected_gen] == expected_gen
            else:
                assert column_gen == expected_gen[:len_column_gen]

    jamai_client.delete_table(TableType.action, table_id)


@pytest.mark.parametrize("gen_type", GEN_TYPES)
@pytest.mark.parametrize("input_dict, output_dict, column_map, row, expected_column_gen", data())
def test_stream_concurrent_execution(
    jamai_client: JamAI, gen_type, input_dict, output_dict, column_map, row, expected_column_gen
):
    """
    Tests concurrent execution in streaming mode with dependencies.
    """
    meta, table_id = _create_table(
        jamai_client,
        TableType.action,
        cols_info=(
            input_dict,
            output_dict,
        ),
    )
    gen_config = GenConfigUpdateRequest(table_id=table_id, column_map=column_map)
    _update_gen_config(jamai_client, TableType.action, gen_config)

    response = jamai_client.add_table_rows(
        TableType.action,
        RowAddRequest(table_id=table_id, data=[row], stream=True, concurrent=True),
    )

    # Collect streaming response
    chunks = []
    for chunk in response:
        chunks.append(chunk)

    if gen_type == "REGEN":
        rows = jamai_client.list_table_rows(TableType.action, table_id)
        # logger.info(f"rows.items: {rows.items}")
        row_id = rows.items[0]["ID"]
        total_start_time = time.time()
        response = jamai_client.regen_table_rows(
            TableType.action,
            RowRegenRequest(table_id=table_id, row_ids=[row_id], stream=True, concurrent=True),
        )
        # Collect streaming response
        chunks = []
        for chunk in response:
            chunks.append(chunk)
        logger.info(f"> Total Regen Rows Time: {time.time() - total_start_time}")

    # Get first rows
    rows = jamai_client.list_table_rows(TableType.action, table_id)
    row_id = rows.items[0]["ID"]
    row = jamai_client.get_table_row(TableType.action, table_id, row_id)

    # Compare generated outputs with expected outputs
    for output_column_name in output_dict.keys():
        expected_gen = expected_column_gen[output_column_name]
        column_gen = row[output_column_name]["value"]
        len_expected_gen = len(expected_gen)
        len_column_gen = len(column_gen)
        if len_column_gen >= len_expected_gen:
            assert column_gen[:len_expected_gen] == expected_gen
        else:
            assert column_gen == expected_gen[:len_column_gen]

    jamai_client.delete_table(TableType.action, table_id)


@pytest.mark.parametrize("gen_type", GEN_TYPES)
@pytest.mark.parametrize("input_dict, output_dict, column_map, row, expected_column_gen", data())
def test_multirows_nonstream_concurrent_execution(
    jamai_client: JamAI, gen_type, input_dict, output_dict, column_map, row, expected_column_gen
):
    """
    Tests concurrent execution in non-streaming mode with dependencies.
    """
    meta, table_id = _create_table(
        jamai_client,
        TableType.action,
        cols_info=(
            input_dict,
            output_dict,
        ),
    )
    gen_config = GenConfigUpdateRequest(table_id=table_id, column_map=column_map)
    _update_gen_config(jamai_client, TableType.action, gen_config)

    total_start_time = time.time()
    response = jamai_client.add_table_rows(
        TableType.action,
        RowAddRequest(
            table_id=table_id,
            data=[row, row, row],
            stream=False,
            concurrent=True,
        ),
    )
    logger.debug(f"> Non-Stream Total Rows Time: {time.time() - total_start_time}")

    # Verify all output columns were executed
    for response in response.rows:
        for output_column_name in output_dict.keys():
            assert output_column_name in response.columns

    if gen_type == "REGEN":
        total_start_time = time.time()
        rows = jamai_client.list_table_rows(TableType.action, table_id)
        response = jamai_client.regen_table_rows(
            TableType.action,
            RowRegenRequest(
                table_id=table_id,
                row_ids=[row_item["ID"] for row_item in rows.items],
                stream=False,
                concurrent=True,
            ),
        )
        logger.debug(f"> Non-Stream Total Regen Rows Time: {time.time() - total_start_time}")

    # Get rows
    rows = jamai_client.list_table_rows(TableType.action, table_id)
    for i in range(len(response.rows)):
        row_id = rows.items[i]["ID"]
        row = jamai_client.get_table_row(TableType.action, table_id, row_id)

        # Compare generated outputs with expected outputs
        for output_column_name in output_dict.keys():
            expected_gen = expected_column_gen[output_column_name]
            column_gen = row[output_column_name]["value"]
            len_expected_gen = len(expected_gen)
            len_column_gen = len(column_gen)
            if len_column_gen >= len_expected_gen:
                assert column_gen[:len_expected_gen] == expected_gen
            else:
                assert column_gen == expected_gen[:len_column_gen]

    jamai_client.delete_table(TableType.action, table_id)


@pytest.mark.parametrize("gen_type", GEN_TYPES)
@pytest.mark.parametrize("input_dict, output_dict, column_map, row, expected_column_gen", data())
def test_multirows_stream_concurrent_execution(
    jamai_client: JamAI, gen_type, input_dict, output_dict, column_map, row, expected_column_gen
):
    """
    Tests concurrent execution in streaming mode with dependencies.
    """
    meta, table_id = _create_table(
        jamai_client,
        TableType.action,
        cols_info=(
            input_dict,
            output_dict,
        ),
    )
    gen_config = GenConfigUpdateRequest(table_id=table_id, column_map=column_map)
    _update_gen_config(jamai_client, TableType.action, gen_config)

    total_start_time = time.time()
    response = jamai_client.add_table_rows(
        TableType.action,
        RowAddRequest(
            table_id=table_id,
            data=[row, row, row],
            stream=True,
            concurrent=True,
        ),
    )

    # Collect streaming response
    chunks = []
    for chunk in response:
        chunks.append(chunk)
    logger.debug(f"> Stream Total Rows Time: {time.time() - total_start_time}")

    if gen_type == "REGEN":
        rows = jamai_client.list_table_rows(TableType.action, table_id)
        logger.info(f"rows.items: {rows.items}")
        total_start_time = time.time()
        response = jamai_client.regen_table_rows(
            TableType.action,
            RowRegenRequest(
                table_id=table_id,
                row_ids=[row_item["ID"] for row_item in rows.items],
                stream=True,
                concurrent=True,
            ),
        )
        # Collect streaming response
        chunks = []
        for chunk in response:
            chunks.append(chunk)
        logger.debug(f"> Stream Total Regen Rows Time: {time.time() - total_start_time}")

    # Get first rows
    rows = jamai_client.list_table_rows(TableType.action, table_id)
    row_id = rows.items[0]["ID"]
    row = jamai_client.get_table_row(TableType.action, table_id, row_id)

    # Compare generated outputs with expected outputs
    for output_column_name in output_dict.keys():
        expected_gen = expected_column_gen[output_column_name]
        column_gen = row[output_column_name]["value"]
        len_expected_gen = len(expected_gen)
        len_column_gen = len(column_gen)
        if len_column_gen >= len_expected_gen:
            assert column_gen[:len_expected_gen] == expected_gen
        else:
            assert column_gen == expected_gen[:len_column_gen]

    jamai_client.delete_table(TableType.action, table_id)
