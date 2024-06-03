"""Example of multi-LLM routing"""

from dataclasses import dataclass
import os
import uuid
from typing import List, Optional

from fixpoint_sdk import openapi_client, FixpointClient


@dataclass
class ApiKeys:
    """Various API keys"""

    fixpoint: str
    openai: str


def main(apikeys: ApiKeys) -> None:
    """Example of A/B routing

    When you make an A/B routing request, you must specify the experiment ID for
    your A/B experiment and the user ID that you are routing. For that
    experiment and user ID, we make sure that they are assigned to one of the
    arms of the experiment, and every subsequent inference request for that user
    goes to the same experiment arm.
    """
    client = FixpointClient(
        fixpoint_api_key=apikeys.fixpoint,
        openai_api_key=apikeys.openai,
    )

    # This is optional, but it lets you set tracing info on your requests.
    trace = new_trace(session_id=str(uuid.uuid4()))

    # For the same combination of (experiment_id, user_id), we will always route
    # to the same model arm.
    experiment_id = "ab_exp_123"
    user_id = "dylan-000"

    ab_llm_chat_req = openapi_client.V1CreateABChatCompletionRequest(
        mode=openapi_client.V1Mode.MODE_TEST,
        experiment_id=experiment_id,
        user_id=user_id,
        tracing=trace,
        # Here you specify the different model arms that are part of your A/B
        # experiment. You need to pass the API key in for each model arm.
        models=[
            openapi_client.V1Model(
                name="openai/ft:gpt-3.5-turbo-1106:fixpoint::9QJrlP1n",
                api_key=apikeys.openai,
            ),
            openapi_client.V1Model(
                name="openai/gpt-3.5-turbo-1106", api_key=apikeys.openai
            ),
        ],
        messages=[
            openapi_client.V1InputMessage(
                role="user",
                content="Was Paris always the capital of France?",
            ),
        ],
        # if you want to record additional attributes on the logs, specify them
        # here
        log_attributes=[
            openapi_client.V1LogAttribute(
                key="prompt-version",
                value="v0.1.0",
            ),
        ],
    )

    print("")
    print("Making an A/B ChatCompletion request with models:\n")
    print("\n".join(get_model_info(ab_llm_chat_req)))
    print("\nUser:", user_id)
    print("Experiment:", experiment_id)
    print("\nTracing info:")
    print(f"Session ID: {trace.session_id}")
    print(f"Trace ID: {trace.trace_id}")
    print("")
    print("\nWaiting for inference...\n\n")

    ab_completion = client.fixpoint.api.fixpoint_create_ab_chat_completion(
        ab_llm_chat_req
    )

    completion_id = ab_completion.id
    # This is the identifier from your inference provider
    external_id = ab_completion.primary_external_id
    print("Made AbChatCompletion with:")
    print(f"ID: {completion_id}")
    print(f"External ID: {external_id}")
    print(f"Model: {ab_completion.model.name}\n")
    choice = ab_completion.completion.choices[0]
    role = choice.message.role
    content = choice.message.content
    print(f"{role}: {content}")


def new_trace(
    session_id: str, parent_span_id: Optional[str] = None
) -> openapi_client.V1Tracing:
    """Generate a new trace with random IDs."""
    return openapi_client.V1Tracing(
        # All children inference requests (one for each model above) will share
        # this session ID.
        session_id=session_id,
        # All children inference requests share this trace ID.
        trace_id=str(uuid.uuid4()),
        # All children inference requests have `parent_span_id` set to this.
        # Aka if the span_id for the CreateMultiLLMChatCompletion request is
        # "A", then all of the actual inference requests will have
        # parent_span_ids that are equal to "A", and completely new individual
        # span IDs.
        span_id=str(uuid.uuid4()),
        # If the rest of your app instruments tracing, you can set the parent
        # span ID here.
        parent_span_id=parent_span_id,
    )


def get_model_info(
    req: openapi_client.V1CreateABChatCompletionRequest,
) -> List[str]:
    """Return a list of model info strings"""
    if req.models is None:
        return []
    return [f"- {m.name} (temperature {m.temperature})" for m in req.models]


if __name__ == "__main__":
    main(
        ApiKeys(
            fixpoint=os.environ["FIXPOINT_API_KEY"],
            openai=os.environ["OPENAI_API_KEY"],
        )
    )
