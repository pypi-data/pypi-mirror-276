from functools import partial
import json
import os
from dataclasses import dataclass
import re
from typing import (
    Any,
    Callable,
    Generator,
    Sequence,
    cast,
)
from urllib.parse import urlencode

import lastmile_utils.lib.core.api as core_utils
import pandas as pd
import requests
import result
from result import Err, Ok

from lastmile_eval.rag.debugger.api.core_utils_todo_move_out import (
    res_reduce_list_all_ok,
)
from lastmile_eval.rag.debugger.common import core as core


@dataclass
class CreateEvaluationsResult:
    success: bool
    message: str
    df_metrics_trace: core.DFRAGQueryTraceEvaluations | None = None
    df_metrics_dataset: core.DFRAGQueryDatasetEvaluations | None = None


@dataclass
class CreateTestSetsResult:
    success: bool
    message: str
    ids: list[core.TestSetID]


@dataclass
class CreateInputSetsResult:
    success: bool
    message: str
    ids: list[core.InputSetID]


@dataclass
class BatchDownloadParams:
    batch_limit: int
    search: str | None = None
    trace_id: core.RAGQueryTraceID | None = None
    creator_id: core.CreatorID | None = None
    project_id: core.ProjectID | None = None
    organization_id: core.OrganizationID | None = None
    start_timestamp: str | None = None
    end_timestamp: str | None = None
    event_name: str | None = None


def _http_get(
    base_url: str, endpoint: str, headers: dict[str, str]
) -> core.Res[requests.Response]:
    raw = requests.get(
        os.path.join(base_url, "api", endpoint), headers=headers
    )
    if raw.status_code != 200:
        return Err(ValueError(f"LastMile website returned error:\n{raw.text}"))
    return Ok(raw)


def _http_post_json(
    base_url: str, endpoint: str, headers: dict[str, str], data: dict[str, Any]
):
    return requests.post(
        os.path.join(base_url, "api", endpoint), headers=headers, json=data
    )


def _auth_header(lastmile_api_token: core.APIToken):
    return {
        "Authorization": f"Bearer {lastmile_api_token}",
    }


def _get_test_set_ids_by_name(
    base_url: core.BaseURL,
    test_set_name: str,
    lastmile_api_token: core.APIToken,
) -> core.Res[list[core.TestSetID]]:
    endpoint_without_args = "evaluation_test_sets/list"
    params = {"name": test_set_name}
    encoded_params = urlencode(params)
    endpoint = f"{endpoint_without_args}?{encoded_params}"
    headers = _auth_header(lastmile_api_token)
    response = _http_get(base_url, endpoint, headers)

    def _parse_response(
        response: requests.Response,
    ) -> core.Res[list[core.TestSetID]]:
        if response.status_code != 200:
            return Err(
                ValueError(
                    f"LastMile website returned error:\n{response.text}"
                )
            )

        if "evaluationTestSets" not in response.json():
            return Err(
                ValueError(f"Expected 'evaluationTestSets' in response.")
            )

        test_sets = response.json()["evaluationTestSets"]

        return Ok([core.TestSetID(test_set["id"]) for test_set in test_sets])

    return response.and_then(_parse_response)


def download_test_set_by_id(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,  # "Explicit is better than implicit." - The Zen of Python
    test_set_id: core.TestSetID | None = None,
) -> core.Res[core.DFTestSet]:
    # api/evaluation_test_sets/list doesn't return the underlying test cases

    query_args: dict[str, str] = {}
    if test_set_id is not None:
        query_args["testSetId"] = test_set_id
    endpoint = f"evaluation_test_cases/list?{urlencode(query_args)}"

    headers = _auth_header(lastmile_api_token)
    response = _http_get(base_url, endpoint, headers)
    match response:
        case Err(e):
            return Err(e)
        case Ok(response_ok):
            raw_test_cases = response_ok.json()["evaluationTestCases"]

            def _extract_record(
                record: dict[str, Any]
            ) -> dict[str, str | None]:
                return record

            df_records = (
                pd.DataFrame.from_records(  # type: ignore
                    map(_extract_record, raw_test_cases)
                )
                .rename(
                    columns={
                        "id": "testCaseId",
                    }
                )
                .reset_index()
            )

            if test_set_id is not None and "testSetId" in df_records.columns:
                df_records = df_records.query(f"testSetId == '{test_set_id}'")  # type: ignore[pandas]

            if len(df_records) == 0:
                return Err(
                    ValueError(
                        f"No test cases found for {test_set_id=}.\n"
                        f"If you provided a test_set_id filter, "
                        "Please check whether the ID exists "
                        "and you have permission to view it.\n"
                        f"\nLastmile website returned {response_ok.text}."
                    )
                )

            return core.df_as_df_test_set(df_records)


def download_test_sets_helper(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    test_set_id: core.TestSetID | None = None,
    test_set_name: str | None = None,
) -> core.Res[core.DFTestSet]:
    def _concat(res: list[core.DFTestSet]) -> core.Res[core.DFTestSet]:
        df_all = pd.concat(res)  # type: ignore
        return core.df_as_df_test_set(df_all)

    def _assign_name(
        df: core.DFTestSet, test_set_name: str | None
    ) -> core.Res[core.DFTestSet]:
        if test_set_name is None:
            test_set_name = "<unknown>"
        out = df.assign(testSetName=test_set_name)  # type: ignore
        return core.df_as_df_test_set(out)

    def _get_ids_allowed(
        test_set_name: str | None,
        test_set_id: core.TestSetID | None,
    ) -> core.Res[list[core.TestSetID]]:
        # Supports 3 cases (at least input is not None).
        if test_set_id is None and test_set_name is not None:
            # Just test_set_name filter given. Simply look up the IDs.
            # (No other filtering)
            return _get_test_set_ids_by_name(
                base_url, test_set_name, lastmile_api_token
            )
        elif test_set_id is not None and test_set_name is None:
            # Just test_set_id filter given. Simply return it.
            # (No other filtering)
            return Ok([test_set_id])
        elif test_set_id is not None and test_set_name is not None:
            # Both filters given. Look up the IDs by name, then intersect them
            # with the given set ID.
            ids_by_name = _get_test_set_ids_by_name(
                base_url, test_set_name, lastmile_api_token
            )
            # Intersect the ID list corresponding to the name with the given ID
            # (If the ID list was looked up successfully).
            return result.do(
                Ok(list(set(ids_by_name_ok) & set({test_set_id})))
                for ids_by_name_ok in ids_by_name
            )
        else:
            # The only not-allowed case.
            return Err(
                ValueError(
                    "Either test_set_id or test_set_name must be provided."
                )
            )

    def _download_all_test_sets_by_id(
        ids: list[core.TestSetID],
        lastmile_api_token: core.APIToken,
        base_url: core.BaseURL,
    ) -> list[core.Res[core.DFTestSet]]:
        # TODO (@jll): abstract out do_list
        return [
            download_test_set_by_id(
                base_url,
                lastmile_api_token,
                test_set_id_,
            ).and_then(partial(_assign_name, test_set_name=test_set_name))
            for test_set_id_ in ids
        ]

    list_dfs_downloaded = result.do(
        res_reduce_list_all_ok(
            _download_all_test_sets_by_id(
                ids_allowed_ok, lastmile_api_token, base_url
            )
        )
        for ids_allowed_ok in _get_ids_allowed(test_set_name, test_set_id)
    )

    df_all = list_dfs_downloaded.and_then(_concat)

    return df_all


def run_evaluations_helper(
    df_test_cases: core.DFTestSet,
    trace_level_evaluators: list[core.RAGQueryTraceLevelEvaluator],
    dataset_level_evaluators: list[core.DatasetLevelEvaluator],
) -> core.Res[
    tuple[
        core.DFRAGQueryTraceEvaluations | None,
        core.DFRAGQueryDatasetEvaluations | None,
    ]
]:
    df_trace_level = None
    df_dataset_level = None

    dfs_evaluations_trace_level: list[core.DFRAGQueryTraceEvaluations] = []
    for evaluator in trace_level_evaluators:
        df_trace_level_ = evaluator(df_test_cases)
        dfs_evaluations_trace_level.append(df_trace_level_)

    if len(dfs_evaluations_trace_level) > 0:
        df_trace_level = cast(
            core.DFRAGQueryTraceEvaluations, pd.concat(dfs_evaluations_trace_level)  # type: ignore
        )

    dfs_dataset_level: list[core.DFRAGQueryDatasetEvaluations] = []
    test_sets_found: list[str] = df_test_cases.testSetId.unique()  # type: ignore
    for evaluator in dataset_level_evaluators:
        if len(test_sets_found) > 1:  # type: ignore
            return Err(
                ValueError(
                    "Dataset-level evaluators were given, but "
                    f"multiple test sets were found: {','.join(test_sets_found)}"
                    "\nCurrently, only one test set per dataframe "
                    "is supported."
                )
            )
        df_dataset_level_ = evaluator(df_test_cases)

        dfs_dataset_level.append(df_dataset_level_)

    if len(dfs_dataset_level) > 0:
        df_dataset_level = cast(
            core.DFRAGQueryDatasetEvaluations, pd.concat(dfs_dataset_level)  # type: ignore
        )

    return Ok((df_trace_level, df_dataset_level))


def evaluate_rag_outputs_helper(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    df: pd.DataFrame,
    project_id: core.ProjectID | None,
    trace_level_evaluators: list[core.RAGQueryTraceLevelEvaluator],
    dataset_level_evaluators: list[core.DatasetLevelEvaluator],
    test_set_name: str,
    evaluation_set_name: str,
) -> core.Res[CreateEvaluationsResult]:
    create_test_set_result = create_test_set_from_df(
        base_url,
        lastmile_api_token,
        df,
        test_set_name,
    )

    out = result.do(
        run_and_store_evaluations_helper(
            core.BaseURL(base_url),
            core.APIToken(lastmile_api_token),
            core.TestSetID(create_test_set_result_ok.ids[0]),
            evaluation_set_name,
            project_id,
            trace_level_evaluators,
            dataset_level_evaluators,
        )
        for create_test_set_result_ok in create_test_set_result
    )

    return out


def run_and_store_evaluations_helper(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    test_set_id: core.TestSetID,
    evaluation_set_name: str,
    project_id: core.ProjectID | None,
    trace_level_evaluators: list[core.RAGQueryTraceLevelEvaluator],
    dataset_level_evaluators: list[core.DatasetLevelEvaluator],
) -> core.Res[CreateEvaluationsResult]:
    base_url = core.BaseURL("https://lastmileai.dev")
    df_test_cases = download_test_set_by_id(
        base_url,
        lastmile_api_token,
        test_set_id,
    )

    dfs_metrics = result.do(
        run_evaluations_helper(
            df_test_cases_ok,
            trace_level_evaluators,
            dataset_level_evaluators,
        )
        for df_test_cases_ok in df_test_cases
    )

    def _store_results(
        dfs_metrics: tuple[
            core.DFRAGQueryTraceEvaluations | None,
            core.DFRAGQueryDatasetEvaluations | None,
        ]
    ) -> core.Res[CreateEvaluationsResult]:
        df_metrics_trace_level, df_metrics_dataset_level = dfs_metrics

        return store_evaluation_set_results_helper(
            base_url,
            lastmile_api_token,
            evaluation_set_name,
            project_id,
            df_metrics_trace_level=df_metrics_trace_level,
            df_metrics_dataset_level=df_metrics_dataset_level,
        )

    return dfs_metrics.and_then(_store_results)


def store_evaluation_set_results_helper(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    evaluation_set_name: str,
    project_id: core.ProjectID | None,
    df_metrics_trace_level: core.DFRAGQueryTraceEvaluations | None = None,
    df_metrics_dataset_level: core.DFRAGQueryDatasetEvaluations | None = None,
) -> core.Res[CreateEvaluationsResult]:
    """
    Upload evaluations results for persistence and analysis in UI.

    Metrics can be either trace-level or dataset-level.
    Both are optional, at least one is required.

    """
    if df_metrics_trace_level is None and df_metrics_dataset_level is None:
        raise ValueError(
            "At least one of trace_level or dataset_level must be provided"
        )

    def _get_all_test_set_ids(
        df_metrics_trace_level: core.DFRAGQueryTraceEvaluations | None,
        df_metrics_dataset_level: core.DFRAGQueryDatasetEvaluations | None,
    ) -> set[core.TestSetID]:
        test_set_ids_trace_level = (  # type: ignore
            set(df_metrics_trace_level.testSetId.unique())  # type: ignore
            if df_metrics_trace_level is not None
            else set()
        )
        test_set_ids_dataset_level = (  # type: ignore
            set(df_metrics_dataset_level.testSetId.unique())  # type: ignore
            if df_metrics_dataset_level is not None
            else set()
        )
        return set(test_set_ids_trace_level) | set(test_set_ids_dataset_level)  # type: ignore

    all_test_set_ids = _get_all_test_set_ids(
        df_metrics_trace_level, df_metrics_dataset_level
    )

    all_results: list[CreateEvaluationsResult] = []

    for test_set_id in all_test_set_ids:
        result_for_set = _store_evaluations_for_test_set(
            base_url,
            lastmile_api_token,
            evaluation_set_name,
            test_set_id,
            project_id,
            df_metrics_trace_level,
            df_metrics_dataset_level,
        )

        all_results.append(result_for_set)

    is_success = all(result_.success for result_ in all_results)
    message = ", ".join(result_.message for result_ in all_results)
    return Ok(
        CreateEvaluationsResult(
            success=is_success,
            message=message,
            df_metrics_trace=df_metrics_trace_level,
            df_metrics_dataset=df_metrics_dataset_level,
        )
    )


def _store_evaluations_for_test_set(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    evaluation_set_name: str,
    test_set_id: core.TestSetID,
    project_id: core.ProjectID | None,
    df_metrics_trace_level: core.DFRAGQueryTraceEvaluations | None,
    df_metrics_dataset_level: core.DFRAGQueryDatasetEvaluations | None,
) -> CreateEvaluationsResult:
    endpoint = "evaluation_sets/create"
    headers = _auth_header(lastmile_api_token)

    trace_level_metrics = []
    dataset_level_metrics = []

    if df_metrics_trace_level is not None:
        df_trace = (
            df_metrics_trace_level.query(  # type: ignore[fixme]
                f"testSetId == '{test_set_id}'"
            )
            .rename(columns={"value": "metricValue"})
            .drop(
                columns=["testSetId"],
            )
        ).dropna()

        trace_level_metrics = df_trace.to_dict("records")  # type: ignore[fixme]

    if df_metrics_dataset_level is not None:
        df_dataset = (
            df_metrics_dataset_level.query(  # type: ignore[fixme]
                f"testSetId == '{test_set_id}'"
            )
            .rename(columns={"value": "metricValue"})
            .drop(
                columns=["testSetId"],
            )
        ).dropna()

        dataset_level_metrics = df_dataset.to_dict("records")  # type: ignore[fixme]

    data: dict[str, Any] = {
        "testSetId": test_set_id,
        "name": evaluation_set_name,
        "evaluationMetrics": trace_level_metrics,
        "evaluationSetMetrics": dataset_level_metrics,
        "projectId": project_id,
    }
    response = _http_post_json(base_url, endpoint, headers, data)
    return CreateEvaluationsResult(
        success=response.status_code == 200,
        message=response.text,
    )


def default_dataset_aggregators(
    trace_level_evaluator: core.RAGQueryTraceLevelEvaluator,
) -> list[core.DatasetLevelEvaluator]:
    def _agg(
        df: core.DFTestSet, stat: str
    ) -> core.DFRAGQueryDatasetEvaluations:
        trace_evals = trace_level_evaluator(df)
        aggregated = (  # type: ignore
            trace_evals.groupby(["testSetId", "metricName"])[["value"]]  # type: ignore
            .agg(stat)
            .reset_index()
            .drop(
                columns=[
                    "ragQueryTraceId",
                ],
                errors="ignore",
            )
        )
        renamed = aggregated.assign(  # type: ignore
            metricName=lambda df: df.metricName + "_" + stat  # type: ignore
        )

        # vscode can infer more about pandas than cli pyright
        # vscode thinks cast is redundant
        # CLI needs the cast otherwise reports:
        # "Argument type is partially unknown..."
        renamed = cast(pd.DataFrame, renamed)  # type: ignore[fixme]

        return core.df_as_df_dataset_evaluations(renamed)

    return [partial(_agg, stat=stat) for stat in ["mean", "std", "count"]]


def user_provided_evaluators_to_all_typed_evaluators(
    trace_level_evaluators: dict[str, Callable[..., core.T_inv]],
    dataset_level_evaluators: dict[str, Callable[..., core.T_inv]],
) -> tuple[
    list[core.RAGQueryTraceLevelEvaluator], list[core.DatasetLevelEvaluator]
]:
    trace_evaluators_typed = [
        core.callable_as_trace_level_evaluator(metric_name, evaluator)
        for metric_name, evaluator in trace_level_evaluators.items()
    ]

    given_dataset_evaluators_typed = [
        core.callable_as_dataset_level_evaluator(metric_name, evaluator)
        for metric_name, evaluator in dataset_level_evaluators.items()
    ]

    trace_evaluators_for_missing_dataset_evaluators = [
        core.callable_as_trace_level_evaluator(metric_name, evaluator)
        for metric_name, evaluator in trace_level_evaluators.items()
    ]

    default_dataset_evaluators_for_missing_names = [
        default_dataset_aggregators(trace_evaluator)
        for trace_evaluator in trace_evaluators_for_missing_dataset_evaluators
    ]

    dataset_evaluators_typed = (
        given_dataset_evaluators_typed
        + core_utils.flatten_list(default_dataset_evaluators_for_missing_names)
    )
    return trace_evaluators_typed, dataset_evaluators_typed


def _post_filter_rag_tracelike(
    df: core.T_RAGTracelike, params: BatchDownloadParams
) -> core.T_RAGTracelike:
    if params.trace_id is not None:
        df = df.query(f"traceId == '{params.trace_id}'")  # type: ignore[pandas]
    if params.creator_id is not None:
        df = df.query(f"creatorId == '{params.creator_id}'")  # type: ignore[pandas]
    if params.project_id is not None:
        df = df.query(f"projectId == '{params.project_id}'")  # type: ignore[pandas]
    if params.organization_id is not None:
        df = df.query(f"organizationId == '{params.organization_id}'")  # type: ignore[pandas]
    if params.event_name is not None and "eventName" in df.columns:
        df = df.query(f"eventName == '{params.event_name}'")  # type: ignore[pandas]

    start_timestamp = params.start_timestamp
    if start_timestamp is None:
        # 3 months ago
        start_timestamp = pd.Timestamp.now() - pd.DateOffset(months=3)

    df = df.query(f"createdAt >= '{start_timestamp}'")  # type: ignore
    if params.end_timestamp is not None:
        df = df.query(f"createdAt <= '{params.end_timestamp}'")  # type: ignore

    return df


def download_rag_query_traces_helper(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    batch_download_params: BatchDownloadParams,
) -> Generator[core.Res[core.DFRAGQueryTrace], None, None]:
    should_continue = True
    cursor: str | None = None
    while should_continue:
        batch = _download_rag_query_trace_batch(
            base_url,
            lastmile_api_token,
            batch_download_params.batch_limit,
            cursor,
            batch_download_params.search,
        )
        match batch:
            case Ok((df, cursor, has_more)):
                df = _post_filter_rag_tracelike(df, batch_download_params)
                cursor = cursor
                should_continue = has_more
                if len(df) == 0:
                    continue
                yield Ok(df)
            case Err(e):
                yield Err(e)


def download_rag_events_helper(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    batch_download_params: BatchDownloadParams,
) -> Generator[core.Res[core.DFRAGEvent], None, None]:
    should_continue = True
    cursor: str | None = None
    while should_continue:
        batch = _download_rag_event_batch(
            base_url,
            lastmile_api_token,
            batch_download_params.batch_limit,
            cursor,
            batch_download_params.search,
        )
        match batch:
            case Ok((df, cursor, has_more)):
                df = _post_filter_rag_tracelike(df, batch_download_params)
                cursor = cursor
                should_continue = has_more
                if len(df) == 0:
                    continue
                yield Ok(df)
            case Err(e):
                yield Err(e)


def _download_rag_tracelike_batch(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    batch_limit: int,
    endpoint_without_args: str,
    parse_http_response_fn: Callable[
        [core.Res[requests.Response]], core.Res[core.T_RAGTracelike]
    ],
    cursor: str | None,
    search: str | None = None,
) -> core.Res[tuple[core.T_RAGTracelike, str, bool]]:
    params = {
        "search": search,
        "pageSize": batch_limit,
        "cursor": cursor,
    }
    params = {key: value for key, value in params.items() if value is not None}
    encoded_params = urlencode(params)
    endpoint = f"{endpoint_without_args}?{encoded_params}"
    headers = _auth_header(lastmile_api_token)
    raw_response = _http_get(base_url, endpoint, headers)
    response = raw_response

    df = parse_http_response_fn(response)

    def _get_cursor(response: dict[str, Any]) -> core.Res[str]:
        if "cursor" not in response:
            return Err(ValueError(f"Expected 'cursor' in response"))
        return Ok(response["cursor"])

    def _get_has_more(response: dict[str, Any]) -> core.Res[bool]:
        if "hasMore" not in response:
            return Err(ValueError(f"Expected 'hasMore' in response"))
        return Ok(response["hasMore"])

    out: core.Res[tuple[core.T_RAGTracelike, str, bool]] = result.do(
        Ok((df_ok, cursor_ok, has_more_ok))
        for df_ok in df
        for response_ok in response
        for cursor_ok in _get_cursor(response_ok.json())
        for has_more_ok in _get_has_more(response_ok.json())
    )

    return out


def _download_rag_query_trace_batch(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    batch_limit: int,
    cursor: str | None,
    search: str | None = None,
) -> core.Res[tuple[core.DFRAGQueryTrace, str, bool]]:
    endpoint_without_args = "rag_query_traces/list"

    def _parse_http_response(
        response: core.Res[requests.Response],
    ) -> core.Res[core.DFRAGQueryTrace]:
        match response:
            case Err(e):
                return Err(e)
            case Ok(response_ok):
                if (
                    "queryTraces" not in response_ok.json()
                    or len(response_ok.json()["queryTraces"]) == 0
                ):
                    return Err(
                        ValueError(f"No query traces found. {response=}")
                    )

        df = result.do(
            core.df_as_df_rag_query_trace(
                pd.DataFrame.from_records(  # type: ignore[pandas]
                    response_ok.json()["queryTraces"]
                ).rename(columns={"id": "ragQueryTraceId"})
            )
            for response_ok in response
        )
        return df

    return _download_rag_tracelike_batch(
        base_url,
        lastmile_api_token,
        batch_limit,
        endpoint_without_args,
        _parse_http_response,
        cursor,
        search,
    )


def _download_rag_event_batch(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    batch_limit: int,
    cursor: str | None,
    search: str | None = None,
) -> core.Res[tuple[core.DFRAGEvent, str, bool]]:
    endpoint_without_args = "rag_events/list"

    def _parse_http_response(
        response: core.Res[requests.Response],
    ) -> core.Res[core.DFRAGEvent]:
        match response:
            case Err(e):
                return Err(e)
            case Ok(response_ok):
                if (
                    "events" not in response_ok.json()
                    or len(response_ok.json()["events"]) == 0
                ):
                    return Err(
                        ValueError(f"No query traces found. {response=}")
                    )

        df = result.do(
            core.df_as_df_rag_events(
                pd.DataFrame.from_records(  # type: ignore[pandas]
                    response_ok.json()["events"]
                ).rename(columns={"id": "ragEventId"})
            )
            for response_ok in response
        )
        return df

    return _download_rag_tracelike_batch(
        base_url,
        lastmile_api_token,
        batch_limit,
        endpoint_without_args,
        _parse_http_response,
        cursor,
        search,
    )


def create_test_set_from_inputs_outputs(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    queries: Sequence[str],
    outputs: Sequence[str],
    test_set_name: str,
    ground_truth: Sequence[str] | None = None,
) -> core.Res[CreateTestSetsResult]:
    df = core.DFTestSet(
        pd.DataFrame(
            {"query": queries, "output": outputs, "groundTruth": ground_truth}
        )
    )

    return create_test_set_from_df(
        base_url,
        lastmile_api_token,
        df,
        test_set_name,
    )


def create_test_set_from_rag_query_traces_helper(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    df_rag_query_traces: core.DFRAGQueryTrace,
    test_set_name: str,
    ground_truth: list[str] | None = None,
) -> core.Res[CreateTestSetsResult]:
    df = core.DFTestSet(df_rag_query_traces.copy())
    if ground_truth is not None:
        df["groundTruth"] = ground_truth

    return create_test_set_from_df(
        base_url,
        lastmile_api_token,
        df,
        test_set_name,
    )


def create_test_set_from_rag_events_helper(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    df_rag_events: core.DFRAGEvent,
    test_set_name: str,
    ground_truth: list[str] | None = None,
) -> core.Res[CreateTestSetsResult]:
    df = core.DFTestSet(df_rag_events.copy())
    if ground_truth is not None:
        df["groundTruth"] = ground_truth

    return create_test_set_from_df(
        base_url,
        lastmile_api_token,
        df,
        test_set_name,
    )


def _test_set_create_res_to_input_set_create_res(
    test_set_create_res: CreateTestSetsResult,
) -> CreateInputSetsResult:
    return CreateInputSetsResult(
        success=test_set_create_res.success,
        message=test_set_create_res.message,
        ids=list(map(core.InputSetID, test_set_create_res.ids)),
    )


def create_input_set_from_rag_query_traces_helper(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    df_rag_query_traces: core.DFRAGQueryTrace,
    input_set_name: str,
    ground_truth: list[str] | None = None,
) -> core.Res[CreateInputSetsResult]:
    df = core.DFTestSet(df_rag_query_traces.copy())
    for c in df:
        if c not in [
            "ragQueryTraceId",
            "createdAt",
            "updatedAt",
            "paramSet",
            "query",
            "eventName",
            "metadata",
            "traceId",
            "ragIngestionTraceId",
            "creatorId",
            "projectId",
            "organizationId",
            "visibility",
            "active",
            "ragIngestionTrace",
            "annotations",
        ]:
            df[c] = "<undefined> (inputs only)"

    # TODO: currently, having the trace ID shows trace stuff in the UI which is
    # not what we want because the input set is supposed to be inputs only.
    # As a short-term solution, set it to None so we only see the inputs and GT.
    df["ragQueryTraceId"] = None

    if ground_truth is not None:
        df["groundTruth"] = ground_truth

    # Currently, input sets are implemented as test sets
    # that have empty values for intermediate values and outputs.
    # Later, we need to make a real distinct entity type.
    test_set_res = create_test_set_from_df(
        base_url,
        lastmile_api_token,
        df,
        f"Input Set {input_set_name}",
    )

    return test_set_res.map(_test_set_create_res_to_input_set_create_res)


def create_input_set_helper(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    inputs: Sequence[str],
    ground_truth: Sequence[str] | None,
    input_set_name: str,
) -> core.Res[CreateInputSetsResult]:
    df = core.DFTestSet(
        pd.DataFrame({"query": inputs, "groundTruth": ground_truth})
    )

    test_set_res = create_test_set_from_df(
        base_url,
        lastmile_api_token,
        df,
        input_set_name,
    )

    return test_set_res.map(_test_set_create_res_to_input_set_create_res)


def create_test_set_from_df(
    base_url: core.BaseURL,
    lastmile_api_token: core.APIToken,
    df: pd.DataFrame,
    test_set_name: str,
) -> core.Res[CreateTestSetsResult]:
    endpoint = "evaluation_test_sets/create"
    headers = _auth_header(lastmile_api_token)

    allowed_columns = [
        c
        for c in [
            "query",
            "context",
            "fullyResolvedPrompt",
            "output",
            "groundTruth",
            "ragQueryTraceId",
        ]
        if c in df.columns
    ]

    data = {  # type: ignore[fixme]
        "name": test_set_name,
        "testCases": df[allowed_columns].to_dict("records"),  # type: ignore
    }
    response = _http_post_json(base_url, endpoint, headers, data)  # type: ignore[fixme]
    response_json = response.json()
    if "id" not in response_json:
        return Err(ValueError(f"Expected 'id' in response. {response_json=}"))

    ids = [core.TestSetID(response_json["id"])]
    return Ok(
        CreateTestSetsResult(
            success=response.status_code == 200, message=response.text, ids=ids
        )
    )


def run_rag_query_fn(
    rag_query_fn: Callable[[str], str], queries: Sequence[str]
) -> core.Res[list[str]]:
    try:
        # TODO: timeout
        return Ok(list(map(rag_query_fn, queries)))
    except Exception as e:
        return Err(e)


def clean_rag_query_tracelike_df(df: pd.DataFrame) -> pd.DataFrame:
    def _unpack_all(df: pd.DataFrame) -> pd.DataFrame:
        cols_unpack = {
            "query": "query",
            "context": "context",
            "output": "llm_output",
        }

        def _unpack_value(x: Any, key: str):
            try:
                return json.loads(x)[key]
            except Exception:
                return x

        def _unpack(df: pd.DataFrame, col: str, key: str) -> pd.Series:  # type: ignore
            try:
                out = df[col].apply(partial(_unpack_value, key=key))  # type: ignore
                return out  # type: ignore
            except Exception:
                return df[col]  # type: ignore

        def _extract_frp(s: pd.Series) -> pd.Series:  # type: ignore
            def _extract_frp_value(x: Any) -> str:
                try:
                    x = json.loads(x)["fully_resolved_prompt"]
                    m = re.search(r"'content': '([^']*)'", x)
                    if m:
                        return list(m.groups())[-1]
                    else:
                        return x
                except:
                    return x

            return s.apply(_extract_frp_value)  # type: ignore

        df_input_exploded = None

        def _value_to_series(x: Any) -> pd.Series | Any:  # type: ignore
            try:
                return pd.Series(x)  # type: ignore
            except Exception:
                return x

        try:
            df_input_exploded = df["input"].apply(_value_to_series)  # type: ignore
        except Exception:
            pass

        if df_input_exploded is not None:
            for c in df_input_exploded:
                if c not in df:
                    df[c] = df_input_exploded

        df = df.assign(  # type: ignore
            **{
                col: partial(_unpack, col=col, key=key)
                for col, key in cols_unpack.items()
            },
        ).drop(columns=["index", "input"], errors="ignore")

        if "fullyResolvedPrompt" in df.columns:
            df["fullyResolvedPrompt"] = _extract_frp(df["fullyResolvedPrompt"])

        return df

    try:
        return _unpack_all(df)
    except Exception:
        return df
