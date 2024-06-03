import json
from typing import List, Union, Literal, Optional, Dict, Iterable

from openai.types.chat import ChatCompletionMessageParam, ChatCompletionToolParam, ChatCompletionToolChoiceOptionParam
from pydantic import BaseModel

from aily_code_sdk_core import action

ACTION_API_NAME = 'action:brn:cn:spring:all:all:connector_action_runtime:/spring_sdk_llm'


class Function(BaseModel):
    arguments: Optional[str] = None

    name: Optional[str] = None


class MessageToolCall(BaseModel):
    id: str

    function: Function

    type: Literal["function"]


class Usage(BaseModel):
    input_tokens: int

    output_tokens: int


class Message(BaseModel):
    content: Optional[str] = None
    role: Literal["assistant", "user", "system"]

    tool_calls: Optional[List[MessageToolCall]] = None

    usage: Optional[Usage] = None


def capitalize_keys_and_stringify_properties(tools):
    new_tools = []
    for tool in tools:
        new_tool = {k.capitalize(): v for k, v in tool.items()}
        if 'Function' in new_tool:
            function = new_tool['Function']
            function = {k.capitalize(): v for k, v in function.items()}
            function['Parameters'] = json.dumps(function['Parameters'])
            new_tool['Function'] = function
        new_tools.append(new_tool)
    return new_tools


def chat_completion(
        messages: Iterable[ChatCompletionMessageParam],
        model: Union[
            str,
            Literal[
                "BYOM-lite",
                "BYOM-plus",
                "BYOM-pro",
                "BYOM-max",
                "BYOM-ultra",
                "BYOM-4o",
                "BYOM-embedding",
                "3.5-Turbo",
                "3.5-Turbo-16K",
                "4-8K",
                "4-32k",
                "4-Turbo",
                "4o",
            ],
        ],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        # stream: bool = False,  # 当前并不支持
        tools: Iterable[ChatCompletionToolParam] = None,
        tool_choice: ChatCompletionToolChoiceOptionParam = "none",
        timeout: Optional[float] = None,
) -> Message:
    """
    Generates a response message based on the input messages and parameters.

    Args:
        messages: The list of input messages.
        model: The LLM model to use for generation.
        max_tokens: The maximum number of tokens to generate.
        temperature: The temperature value for generation.
        # stream: Whether to stream the response. Currently not supported.
        tools: The tools available for the model to use.
        tool_choice: The choice of tool usage. Can be "none", "auto", or "required".
        timeout: The timeout value for the API request.

    Returns:
        The generated response message.
    """
    action_data = {
        "llmID": model,
        "chatCompletionParameters": {
            "ChatCompletionMessages": [
                {
                    "Role": message['role'],
                    "Content": message['content'],
                }
                for message in messages
            ],
            "MaxTokens": max_tokens,
            "Temperature": temperature,
            "Tools": capitalize_keys_and_stringify_properties(tools),
            "ToolChoice": tool_choice,
        },
    }

    res = action.call_action(
        action_api_name=ACTION_API_NAME,
        action_data=action_data,
    )
    if res["Choices"]:
        choice = res["Choices"][0]
        message = choice["Message"]
        content = message.get("Content")
        role = message["Role"]
        function_call = message.get("FunctionCall")
        tool_calls = [
            MessageToolCall(
                id=tool_call["ID"],
                function=Function(
                    name=tool_call["Function"]["Name"],
                    arguments=tool_call["Function"]["Arguments"],
                ),
                type="function",
            )
            for tool_call in message.get("ToolCalls", [])
        ]
        return Message(
            content=content,
            role=role,
            function_call=function_call,
            tool_calls=tool_calls if tool_calls else None,
            usage=Usage(
                input_tokens=res.get('Usage', {}).get('PromptTokens'),
                output_tokens=res.get('Usage', {}).get('CompletionTokens'),
            )
        )
    else:
        return Message()
