import asyncio
import json
from typing import Dict

import websockets

from .model_config import ModelConfig
from .utils import load_json_buffer, begin_task_execution


async def interact_with_websocket(uri: str, query_payload: Dict[str, str], qid: int):
    end_of_stream = "<EOS>"
    payload = {qid: {"response": ""}}

    async with websockets.connect(uri) as websocket:
        # Send the user-provided message to the WebSocket server
        await websocket.send(json.dumps(query_payload))

        # Loop to receive messages until the server is finished
        while True:
            try:
                response = await websocket.recv()
                parsed_response = load_json_buffer(response)

                if isinstance(parsed_response, dict):
                    # Case: json/text response and user is denied entry
                    if 'message' in parsed_response.keys():
                        if parsed_response['message'] == 'Forbidden':
                            # Embed entire Forbidden message payload and leave response blank.
                            payload[qid].update(parsed_response)
                            break
                        else:
                            raise RuntimeWarning(f"Unknown ASU LLM endpoint edge case detected: `message` as key in "
                                                 f"parsed response: {parsed_response}.")

                    # Case: json response and user is not denied entry
                    elif 'response' in parsed_response.keys():
                        payload[qid]["response"] += (parsed_response["response"].replace(end_of_stream, ""))
                        if 'metadata' in parsed_response.keys() or end_of_stream in parsed_response['response']:
                            payload[qid]["metadata"] = parsed_response["metadata"]
                            break
                    # Edge case: user gets a message to contact the administrator after an error
                    elif 'error' in parsed_response.keys():
                        payload[qid]["error"] = parsed_response["error"]
                    # Unknown edge case: json getting returned that is not a `message`, `response`, `error`
                    # (not observed yet)
                    else:
                        raise RuntimeWarning(f"Unknown ASU LLM endpoint edge case detected: JSON parsed but data "
                                             f"does not contain a message or response field.")

                # Intended case: user asked for a response type of `text` and was not denied entry.
                else:
                    payload[qid]["response"] += response.replace(end_of_stream, "")
                    if end_of_stream in response:
                        break

            except websockets.ConnectionClosed:
                print(f"Question {qid} connection closed by the server")
                break
        print(f"......Question {qid} response sent by the WebSocket server.")
        return payload


async def limited_task(semaphore: asyncio.Semaphore, task):
    async with semaphore:
        return await task


@begin_task_execution
async def batch_query_llm_socket(model: ModelConfig, queries: Dict[int, str], max_concurrent_tasks: int = 3):
    tasks = []
    for qid, message in queries.items():
        tmp_payload = model.compute_payload(message)
        tasks.append(interact_with_websocket(model.api_url, tmp_payload, qid))
    semaphore = asyncio.Semaphore(max_concurrent_tasks)
    limited_tasks = [limited_task(semaphore, task) for task in tasks]

    # Gather all tasks to run them concurrently and collect results
    results = await asyncio.gather(*limited_tasks)
    final_results = {}
    # Desired format: {1: {"response": ..., "metadata": ...}, 2: {...}}
    for result_dict in results:
        final_results.update(result_dict)
    return final_results


@begin_task_execution
async def query_llm_socket(model: ModelConfig, query: str):
    tmp_payload = model.compute_payload(query=query)
    result = await interact_with_websocket(model.api_url, tmp_payload, qid=0)
    return result
