from typing import Any, Callable, Generator, Mapping, Optional, Sequence

import numpy as np
import pandas as pd
import requests
import result
from requests import Response

import lastmile_eval.rag.debugger.evaluation_lib as evaluation_lib
from lastmile_eval.rag.debugger.common import core as core
from lastmile_eval.rag.debugger.evaluation_lib import (
    BatchDownloadParams,
    clean_rag_query_tracelike_df,
)
import lastmile_eval.text.metrics as text_metrics


# lol dont ask
EPSILON = 0


def _token(lastmile_api_token: str | None) -> core.APIToken:
    return (
        core.APIToken(lastmile_api_token)
        if lastmile_api_token is not None
        else core.APIToken(core.api_token_from_dot_env("LASTMILE_API_TOKEN"))
    )


def download_rag_query_traces(
    lastmile_api_token: str | None = None,
    trace_id: str | None = None,
    project_id: str | None = None,
    batch_limit: int | None = None,
    substring_filter: str | None = None,
    creator_id: str | None = None,
    organization_id: str | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
) -> Generator[pd.DataFrame, None, None]:
    HARD_BATCH_LIMIT = 50
    if batch_limit is None:
        batch_limit = HARD_BATCH_LIMIT

    if batch_limit < 1 or batch_limit > HARD_BATCH_LIMIT:
        raise ValueError(
            f"batch_limit must be between 1 and {HARD_BATCH_LIMIT}"
        )

    base_url = "https://lastmileai.dev"
    lastmile_api_token = _token(lastmile_api_token)
    download_params = BatchDownloadParams(
        batch_limit=batch_limit,
        search=substring_filter,
        trace_id=(
            core.RAGQueryTraceID(trace_id) if trace_id is not None else None
        ),
        creator_id=(
            core.CreatorID(creator_id) if creator_id is not None else None
        ),
        project_id=(
            core.ProjectID(project_id) if project_id is not None else None
        ),
        organization_id=(
            core.OrganizationID(organization_id)
            if organization_id is not None
            else None
        ),
        start_timestamp=start_time,
        end_timestamp=end_time,
    )
    generator = evaluation_lib.download_rag_query_traces_helper(
        core.BaseURL(base_url),
        core.APIToken(lastmile_api_token),
        download_params,
    )

    for batch in generator:
        yield batch.map(clean_rag_query_tracelike_df).unwrap_or_raise(
            ValueError
        )


def download_rag_events(
    lastmile_api_token: str | None = None,
    project_id: str | None = None,
    batch_limit: int | None = None,
    substring_filter: str | None = None,
    creator_id: str | None = None,
    organization_id: str | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
    event_name: str | None = None,
) -> Generator[pd.DataFrame, None, None]:
    HARD_BATCH_LIMIT = 50
    if batch_limit is None:
        batch_limit = HARD_BATCH_LIMIT

    if batch_limit < 1 or batch_limit > HARD_BATCH_LIMIT:
        raise ValueError(
            f"batch_limit must be between 1 and {HARD_BATCH_LIMIT}"
        )

    base_url = "https://lastmileai.dev"
    lastmile_api_token = _token(lastmile_api_token)
    download_params = BatchDownloadParams(
        batch_limit=batch_limit,
        search=substring_filter,
        creator_id=(
            core.CreatorID(creator_id) if creator_id is not None else None
        ),
        project_id=(
            core.ProjectID(project_id) if project_id is not None else None
        ),
        organization_id=(
            core.OrganizationID(organization_id)
            if organization_id is not None
            else None
        ),
        start_timestamp=start_time,
        end_timestamp=end_time,
        event_name=event_name,
    )
    generator = evaluation_lib.download_rag_events_helper(
        core.BaseURL(base_url),
        core.APIToken(lastmile_api_token),
        download_params,
    )

    for batch in generator:
        yield batch.unwrap_or_raise(ValueError)


def create_test_set_from_rag_query_traces(
    df_rag_query_traces: pd.DataFrame,
    test_set_name: str,
    ground_truth: list[str] | None = None,
    lastmile_api_token: str | None = None,
) -> evaluation_lib.CreateTestSetsResult:
    base_url = "https://lastmileai.dev"
    lastmile_api_token = _token(lastmile_api_token)
    return result.do(
        evaluation_lib.create_test_set_from_rag_query_traces_helper(
            core.BaseURL(base_url),
            lastmile_api_token,
            df_rag_query_trace_ok,
            test_set_name,
            ground_truth,
        )
        for df_rag_query_trace_ok in core.df_as_df_rag_query_trace(
            df_rag_query_traces
        )
    ).unwrap_or_raise(ValueError)


def create_input_set(
    inputs: Sequence[str],
    input_set_name: str,
    ground_truth: list[str] | None = None,
    lastmile_api_token: str | None = None,
):
    """
    Create an input set from a list of inputs.

    Args:
        inputs: The list of inputs.
        input_set_name: The name of the input set.
        ground_truth: The list of ground truth values. The default is None.
        lastmile_api_token: The API token for the LastMile API. If not provided,
            will try to get the token from the LASTMILE_API_TOKEN
            environment variable.
            You can create a token from the "API Tokens" section from this website:
            https://lastmileai.dev/settings?page=tokens

    Returns:
        A dictionary containing the input set.
    """
    base_url = "https://lastmileai.dev"
    lastmile_api_token = _token(lastmile_api_token)

    return evaluation_lib.create_input_set_helper(
        core.BaseURL(base_url),
        core.APIToken(lastmile_api_token),
        inputs,
        ground_truth,
        input_set_name,
    ).unwrap_or_raise(ValueError)


def create_input_set_from_rag_query_traces(
    df_rag_query_traces: pd.DataFrame,
    input_set_name: str,
    ground_truth: list[str] | None = None,
    lastmile_api_token: str | None = None,
) -> evaluation_lib.CreateInputSetsResult:
    """
    The same as create_test_set_from_rag_query_traces, but for input sets.
    An input set is inputs and ground_truth (optional).
    The intention is to represent a traditional "test set",
    i.e. just the inputs to the RAG system and corresponding ground truth.

    In contrast, TestSet also contains intermediate trace results as well as outputs.
    """
    base_url = "https://lastmileai.dev"
    lastmile_api_token = _token(lastmile_api_token)
    return result.do(
        evaluation_lib.create_input_set_from_rag_query_traces_helper(
            core.BaseURL(base_url),
            lastmile_api_token,
            df_rag_query_trace_ok,
            input_set_name,
            ground_truth,
        )
        for df_rag_query_trace_ok in core.df_as_df_rag_query_trace(
            df_rag_query_traces
        )
    ).unwrap_or_raise(ValueError)


def create_test_set_from_rag_events(
    df_rag_events: pd.DataFrame,
    test_set_name: str,
    ground_truth: list[str] | None = None,
    lastmile_api_token: str | None = None,
) -> evaluation_lib.CreateTestSetsResult:
    base_url = "https://lastmileai.dev"
    lastmile_api_token = _token(lastmile_api_token)
    return result.do(
        evaluation_lib.create_test_set_from_rag_events_helper(
            core.BaseURL(base_url),
            lastmile_api_token,
            df_rag_events_ok,
            test_set_name,
            ground_truth,
        )
        for df_rag_events_ok in core.df_as_df_rag_events(df_rag_events)
    ).unwrap_or_raise(ValueError)


def download_test_set(
    test_set_id: str | None = None,
    test_set_name: str | None = None,
    lastmile_api_token: str | None = None,
) -> pd.DataFrame:
    base_url = "https://lastmileai.dev"
    lastmile_api_token = _token(lastmile_api_token)

    raw = evaluation_lib.download_test_sets_helper(
        core.BaseURL(base_url),
        core.APIToken(lastmile_api_token),
        core.TestSetID(test_set_id) if test_set_id is not None else None,
        test_set_name,
    )

    return raw.map(clean_rag_query_tracelike_df).unwrap_or_raise(ValueError)


def download_input_set(
    input_set_id: str | None = None,
    input_set_name: str | None = None,
    lastmile_api_token: str | None = None,
) -> pd.DataFrame:
    base_url = "https://lastmileai.dev"
    lastmile_api_token = _token(lastmile_api_token)

    # Since input sets are currently implemented as TestSets,
    # We just treat the input_set_id as a test set ID.
    test_set_id = (
        core.TestSetID(input_set_id) if input_set_id is not None else None
    )

    raw = evaluation_lib.download_test_sets_helper(
        core.BaseURL(base_url),
        core.APIToken(lastmile_api_token),
        test_set_id,
        input_set_name,
    )

    def _convert_df_test_set_to_input_set(df: pd.DataFrame) -> pd.DataFrame:
        return (
            df.drop(columns=["testCaseId"], errors="ignore")  # type: ignore[pandas]
            .dropna(axis=1, how="all")
            .rename(
                columns={
                    "testSetId": "inputSetId",
                    "testSetName": "inputSetName",
                }
            )
        )

    return (
        raw.map(clean_rag_query_tracelike_df)
        .map(_convert_df_test_set_to_input_set)
        .unwrap_or_raise(ValueError)
    )


def list_test_sets(
    take: int = 10,
    lastmile_api_token: Optional[str] = None,
    # TODO: Create macro for default timeout value
    timeout: int = 60,
) -> dict[str, Any]:  # TODO: Define eplicit typing for JSON response return
    """
    Get a list of test sets from the LastMile API.

    Args:
        take: The number of test sets to return. The default is 10.
        lastmile_api_token: The API token for the LastMile API. If not provided,
            will try to get the token from the LASTMILE_API_TOKEN
            environment variable.
            You can create a token from the "API Tokens" section from this website:
            https://lastmileai.dev/settings?page=tokens
        timeout: The maximum time in seconds to wait for the request to complete.
            The default is 60.

    Returns:
        A dictionary containing the test sets.
    """
    lastmile_api_token = _token(lastmile_api_token)
    lastmile_endpoint = f"https://lastmileai.dev/api/evaluation_test_sets/list?pageSize={str(take)}"

    response: Response = requests.get(
        lastmile_endpoint,
        headers={"Authorization": f"Bearer {lastmile_api_token}"},
        timeout=timeout,
    )
    # TODO: Handle response errors
    return response.json()


def get_latest_test_set_id(
    lastmile_api_token: Optional[str] = None,
) -> str:
    """
    Convenience function to get the latest test set id. You can pass this id
    into these methods to build your offline evaluator data:
        - download_test_set
        - run_and_store_evaluations

    @param lastmile_api_token Optional(str): Used for authentication. If not
        defined, will try to get the token from the LASTMILE_API_TOKEN
        environment variable.
        You can create a token from the "API Tokens" section from this website:
        https://lastmileai.dev/settings?page=tokens

    @return str: The test set id corresponding to latest test set
    """
    test_sets: dict[str, Any] = list_test_sets(
        take=1, lastmile_api_token=lastmile_api_token
    )
    # TODO: Handle errors
    test_set_id: str = test_sets["evaluationTestSets"][0]["id"]
    return test_set_id


def run_and_store_evaluations(
    test_set_id: str,
    project_id: str,
    trace_level_evaluators: Mapping[
        str, Callable[[pd.DataFrame], Sequence[float]]
    ],
    dataset_level_evaluators: Mapping[
        str, Callable[[pd.DataFrame], Sequence[float]]
    ],
    lastmile_api_token: str | None = None,
    evaluation_set_name: str | None = None,
) -> evaluation_lib.CreateEvaluationsResult:
    base_url = "https://lastmileai.dev"
    lastmile_api_token = _token(lastmile_api_token)

    (
        trace_evaluators_typed,
        dataset_evaluators_typed,
    ) = evaluation_lib.user_provided_evaluators_to_all_typed_evaluators(
        trace_level_evaluators,  # type: ignore[deliberate ignore]
        dataset_level_evaluators,  # type: ignore[deliberate ignore]
    )

    return evaluation_lib.run_and_store_evaluations_helper(
        core.BaseURL(base_url),
        core.APIToken(lastmile_api_token),
        core.TestSetID(test_set_id),
        evaluation_set_name or "Evaluation Set",
        core.ProjectID(project_id),
        trace_evaluators_typed,
        dataset_evaluators_typed,
    ).unwrap_or_raise(ValueError)


def run_evaluations(
    df_test_set: pd.DataFrame,
    trace_level_evaluators: Mapping[
        str, Callable[[pd.DataFrame], Sequence[float]]
    ],
    dataset_level_evaluators: Mapping[
        str, Callable[[pd.DataFrame], Sequence[float]]
    ],
) -> tuple[pd.DataFrame | None, pd.DataFrame | None]:
    """
    In: test set (everything needed to directly run evaluators)
    evaluators: two mappings from name to function.
    Each function should calculate a metric, i.e. return a batch of floats.

    The first mapping is trace-level, i.e. row-by-row.
    The second mapping should aggregate over traces, grouping by test set.

    NOTE: For every trace-level metric, if you do not provide the corresponding
    dataset-level metric, we will fill in defaults.

    Out: (trace-level evaluations, dataset-level evaluations)"""
    (
        trace_evaluators_typed,
        dataset_evaluators_typed,
    ) = evaluation_lib.user_provided_evaluators_to_all_typed_evaluators(
        trace_level_evaluators,  # type: ignore[deliberate ignore]
        dataset_level_evaluators,  # type: ignore[deliberate ignore]
    )

    df_test_set_typed = core.df_as_df_test_set(df_test_set)

    return result.do(
        evaluation_lib.run_evaluations_helper(
            df_test_set_ok,
            trace_evaluators_typed,
            dataset_evaluators_typed,
        )
        for df_test_set_ok in df_test_set_typed
    ).unwrap_or_raise(ValueError)


def store_evaluation_set_results(
    project_id: str,
    df_metrics_trace_level: pd.DataFrame | None = None,
    df_metrics_dataset_level: pd.DataFrame | None = None,
    lastmile_api_token: str | None = None,
    evaluation_set_name: str | None = None,
) -> evaluation_lib.CreateEvaluationsResult:
    base_url = core.BaseURL("https://lastmileai.dev")
    lastmile_api_token = _token(lastmile_api_token)

    return evaluation_lib.store_evaluation_set_results_helper(
        base_url,
        core.APIToken(lastmile_api_token),
        df_metrics_trace_level=(
            core.DFRAGQueryTraceEvaluations(df_metrics_trace_level)
            if df_metrics_trace_level is not None
            else None
        ),
        df_metrics_dataset_level=(
            core.DFRAGQueryDatasetEvaluations(df_metrics_dataset_level)
            if df_metrics_dataset_level is not None
            else None
        ),
        evaluation_set_name=evaluation_set_name or "Evaluation Set",
        project_id=core.ProjectID(project_id),
    ).unwrap_or_raise(ValueError)


def run_rag_query_function(
    rag_query_fn: Callable[[str], str],
    inputs: Sequence[str] | pd.DataFrame,
) -> list[str]:
    def _get_seq(inputs: Sequence[str] | pd.DataFrame) -> Sequence[str]:
        if isinstance(inputs, pd.DataFrame):
            col = None
            if "input" in inputs.columns:
                col = "input"
            elif "query" in inputs.columns:
                col = "query"

            if col is None:
                raise ValueError(
                    "Input set must have an 'input' or 'query' column"
                )
            return inputs[col].tolist()  # type: ignore[pandas]

        else:
            return inputs

    input_seq = _get_seq(inputs)
    return list(map(rag_query_fn, input_seq))


def run_and_evaluate_outputs(
    trace_level_evaluators: Mapping[
        str,
        Callable[
            [Sequence[str], Sequence[str], Sequence[str]],
            Sequence[float],
        ],
    ],
    dataset_level_evaluators: Mapping[
        str,
        Callable[
            [Sequence[str], Sequence[str], Sequence[str]],
            Sequence[float],
        ],
    ],
    rag_query_fn: Callable[[str], str],
    inputs: Sequence[str],
    ground_truth: Sequence[str],
    project_id: Optional[str] = None,
    lastmile_api_token: str | None = None,
    test_set_name: str | None = None,
    evaluation_set_name: str | None = None,
    n_trials: int = 1,
) -> evaluation_lib.CreateEvaluationsResult:
    """
    Special case of evaluation where
        - The rag query path can be run in a single function (rag_query_fn)
        - Evaluators take 3 inputs: outputs, ground truth, inputs
    """
    base_url = "https://lastmileai.dev"
    lastmile_api_token = _token(lastmile_api_token)

    inputs = list(inputs) * n_trials
    ground_truth = list(ground_truth) * n_trials

    outputs = evaluation_lib.run_rag_query_fn(rag_query_fn, inputs)

    def evaluator_with_df_input(
        evaluator: Callable[
            [Sequence[str], Sequence[str], Sequence[str]],
            Sequence[float],
        ]
    ):
        def _evaluator(df: pd.DataFrame) -> Sequence[float]:
            inputs: list[str] = df["query"].tolist()
            output: list[str] = df["output"].tolist()
            ground_truth: list[str] = (
                df["groundTruth"].tolist()
                if "groundTruth" in df.columns
                else [""] * len(df)
            )
            return evaluator(output, ground_truth, inputs)

        return _evaluator

    trace_level_evaluators_from_df = {
        name: evaluator_with_df_input(evaluator)
        for name, evaluator in trace_level_evaluators.items()
    }

    dataset_level_evaluators_from_df = {
        name: evaluator_with_df_input(evaluator)
        for name, evaluator in dataset_level_evaluators.items()
    }

    (
        trace_evaluators_typed,
        dataset_evaluators_typed,
    ) = evaluation_lib.user_provided_evaluators_to_all_typed_evaluators(
        trace_level_evaluators_from_df,  # type: ignore[deliberate ignore]
        dataset_level_evaluators_from_df,  # type: ignore[deliberate ignore]
    )

    def _make_df(
        inputs: Sequence[str],
        outputs: Sequence[str],
        ground_truth: Sequence[str],
    ):
        df = pd.DataFrame(
            {"query": inputs, "output": outputs, "groundTruth": ground_truth}
        )

        return df

    output = result.do(
        evaluation_lib.evaluate_rag_outputs_helper(
            core.BaseURL(base_url),
            core.APIToken(lastmile_api_token),
            _make_df(inputs, outputs_ok, ground_truth),
            (
                core.ProjectID(project_id) if project_id else None
            ),  # Just a type cast
            trace_evaluators_typed,
            dataset_evaluators_typed,
            test_set_name=(test_set_name or "Test Set"),
            evaluation_set_name=(evaluation_set_name or "Evaluation Set"),
        )
        for outputs_ok in outputs
    )

    return output.unwrap_or_raise(ValueError)


def run_and_evaluate_outputs_with_input_set(
    trace_level_evaluators: Mapping[
        str,
        Callable[
            [Sequence[str], Sequence[str], Sequence[str]],
            Sequence[float],
        ],
    ],
    dataset_level_evaluators: Mapping[
        str,
        Callable[
            [Sequence[str], Sequence[str], Sequence[str]],
            Sequence[float],
        ],
    ],
    rag_query_fn: Callable[[str], str],
    input_set_id: str,
    project_id: str | None = None,
    lastmile_api_token: str | None = None,
    create_test_set_name: str | None = None,
    evaluation_set_name: str | None = None,
    n_trials: int = 1,
):
    df_input_set = download_input_set(input_set_id, lastmile_api_token)
    return run_and_evaluate_outputs(
        trace_level_evaluators,
        dataset_level_evaluators,
        rag_query_fn,
        df_input_set["query"].tolist(),  # type: ignore[pandas]
        df_input_set["groundTruth"].tolist(),  # type: ignore[pandas]
        project_id=project_id,
        lastmile_api_token=lastmile_api_token,
        test_set_name=create_test_set_name,
        evaluation_set_name=evaluation_set_name,
        n_trials=n_trials,
    )


def evaluate_rag_outputs(
    project_id: str,
    trace_level_evaluators: Mapping[
        str, Callable[[pd.DataFrame], Sequence[float]]
    ],
    dataset_level_evaluators: Mapping[
        str, Callable[[pd.DataFrame], Sequence[float]]
    ],
    df: pd.DataFrame,
    lastmile_api_token: str | None = None,
    test_set_name: str | None = None,
    evaluation_set_name: str | None = None,
) -> evaluation_lib.CreateEvaluationsResult:
    base_url = "https://lastmileai.dev"
    lastmile_api_token = _token(lastmile_api_token)

    (
        trace_evaluators_typed,
        dataset_evaluators_typed,
    ) = evaluation_lib.user_provided_evaluators_to_all_typed_evaluators(
        trace_level_evaluators,  # type: ignore[deliberate ignore]
        dataset_level_evaluators,  # type: ignore[deliberate ignore]
    )

    output = evaluation_lib.evaluate_rag_outputs_helper(
        core.BaseURL(base_url),
        core.APIToken(lastmile_api_token),
        df,
        core.ProjectID(project_id),
        trace_evaluators_typed,
        dataset_evaluators_typed,
        test_set_name=(test_set_name or "Test Set"),
        evaluation_set_name=(evaluation_set_name or "Evaluation Set"),
    )
    return output.unwrap_or_raise(ValueError)


def assert_is_close(
    evaluation_result: evaluation_lib.CreateEvaluationsResult,
    metric_name: str,
    value: float,
):
    df_metrics_agg = evaluation_result.df_metrics_dataset
    metric = df_metrics_agg.set_index(["testSetId", "metricName"]).value.unstack("metricName")[metric_name].iloc[0]  # type: ignore[pandas]
    assert np.isclose(metric, value), f"Expected: {value}, Got: {metric}"  # type: ignore[fixme]


def get_default_rag_trace_level_metrics(
    names: set[str], lastmile_api_token: str | None = None
) -> dict[
    str,
    Callable[
        [Sequence[str], Sequence[str], Sequence[str]],
        Sequence[float],
    ],
]:
    lastmile_api_token = _token(lastmile_api_token)

    def epsilonify(
        fn: Callable[
            [Sequence[str], Sequence[str], Sequence[str]], Sequence[float]
        ]
    ) -> Callable[
        [Sequence[str], Sequence[str], Sequence[str]], Sequence[float]
    ]:
        """LOL dont ask"""

        def _fn(
            outputs: Sequence[str],
            ground_truth: Sequence[str],
            inputs: Sequence[str],
        ) -> list[float]:
            return [elt + EPSILON for elt in fn(outputs, ground_truth, inputs)]

        return _fn

    @epsilonify
    def _wrap_bleu(
        outputs: Sequence[str],
        ground_truth: Sequence[str],
        inputs: Sequence[str],
    ):
        return text_metrics.calculate_bleu_score(outputs, ground_truth)

    @epsilonify
    def _wrap_rouge1(
        outputs: Sequence[str],
        ground_truth: Sequence[str],
        inputs: Sequence[str],
    ):
        return text_metrics.calculate_rouge1_score(outputs, ground_truth)

    @epsilonify
    def _wrap_exact_match(
        outputs: Sequence[str],
        ground_truth: Sequence[str],
        inputs: Sequence[str],
    ):
        return text_metrics.calculate_exact_match_score(outputs, ground_truth)

    @epsilonify
    def _wrap_relevance(
        outputs: Sequence[str],
        ground_truth: Sequence[str],
        inputs: Sequence[str],
    ):
        return text_metrics.calculate_relevance_score(outputs, ground_truth)

    def _wrap_faithfulness(
        lastmile_api_token: str,
    ):
        @epsilonify
        def _inner(
            outputs: Sequence[str],
            ground_truth: Sequence[str],
            inputs: Sequence[str],
        ):
            return text_metrics.calculate_faithfulness_score(
                outputs, ground_truth, inputs, lastmile_api_token
            )

        return _inner

    @epsilonify
    def _wrap_toxicity(
        outputs: Sequence[str],
        ground_truth: Sequence[str],
        inputs: Sequence[str],
    ):
        return text_metrics.calculate_toxicity_score(outputs)

    @epsilonify
    def _wrap_qa(
        outputs: Sequence[str],
        ground_truth: Sequence[str],
        inputs: Sequence[str],
    ):
        return text_metrics.calculate_qa_score(outputs, ground_truth, inputs)

    @epsilonify
    def _wrap_summarization(
        outputs: Sequence[str],
        ground_truth: Sequence[str],
        inputs: Sequence[str],
    ):
        return text_metrics.calculate_summarization_score(
            outputs, ground_truth
        )

    @epsilonify
    def _wrap_human_vs_ai(
        outputs: Sequence[str],
        ground_truth: Sequence[str],
        inputs: Sequence[str],
    ):
        return text_metrics.calculate_human_vs_ai_score(
            outputs, ground_truth, inputs
        )

    @epsilonify
    def _wrap_sentiment(
        outputs: Sequence[str],
        ground_truth: Sequence[str],
        inputs: Sequence[str],
    ):
        return text_metrics.calculate_custom_llm_metric_example_sentiment(
            outputs
        )

    @epsilonify
    def _wrap_similarity(
        outputs: Sequence[str],
        ground_truth: Sequence[str],
        inputs: Sequence[str],
    ):
        return text_metrics.calculate_custom_llm_metric_example_semantic_similarity(
            outputs, ground_truth
        )

    all_wrappers = {
        "bleu": _wrap_bleu,
        "exact_match": _wrap_exact_match,
        "rouge1": _wrap_rouge1,
        "relevance": _wrap_relevance,
        "faithfulness": _wrap_faithfulness(lastmile_api_token),
        "toxicity": _wrap_toxicity,
        "qa": _wrap_qa,
        "summarization": _wrap_summarization,
        "human_vs_ai": _wrap_human_vs_ai,
        "sentiment": _wrap_sentiment,
        "similarity": _wrap_similarity,
    }
    return {name: all_wrappers[name] for name in names}
