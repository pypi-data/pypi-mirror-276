"""Ask a question to GPT."""
import re
import time

import json5 as json
import openai

from . import getLogger
from .config import baseConf
from .conversation import Conversation
from .OwegaFun import connectLTS, existingFunctions, functionlist_to_toollist


def convert_invalid_json(invalid_json):
    """
    Try converting invalid json to valid json.

    Sometimes, GPT will give back invalid json.
    This function tries to make it valid.
    """
    def replace_content(match):
        content = match.group(1)
        content = (
            content
            .replace('"', '\\"')
            .replace("\n", "\\n")
        )
        return f'"{content}"'
    valid_json = re.sub(r'`([^`]+)`', replace_content, invalid_json)
    return valid_json


# Ask a question via OpenAI or Mistral based on the model.
# TODO: comment a lot more
def ask(
    prompt: str = "",
    messages: Conversation = Conversation(),
    model=baseConf.get("model", ""),
    temperature=baseConf.get("temperature", 0.8),
    max_tokens=baseConf.get("max_tokens", 3000),
    function_call="auto",
    temp_api_key="",
    temp_organization="",
    top_p=baseConf.get("top_p", 1.0),
    frequency_penalty=baseConf.get("frequency_penalty", 0.0),
    presence_penalty=baseConf.get("presence_penalty", 0.0),
):
    """Ask a question via OpenAI or Mistral based on the model."""
    logger = getLogger.getLogger(__name__, debug=baseConf.get("debug", False))

    bc = baseConf.copy()
    bc["api_key"] = "REDACTED"
    bc["mistral_api"] = "REDACTED"
    bc["chub_api"] = "REDACTED"
    logger.debug(f"{bc}")

    connectLTS(
        messages.add_memory, messages.remove_memory, messages.edit_memory)
    if (prompt):
        messages.add_question(prompt)
    else:
        prompt = messages.last_question()

    # Determine if we're using Mistral based on the model name
    is_mistral = False
    is_chub = False
    if model.startswith('chub-'):
        model = model[5:]
        is_chub = True
    elif ("mistral" in model) or ("mixtral" in model):
        is_mistral = True

    try:
        client = openai.OpenAI()
    except openai.OpenAIError:
        # fix for key not set by $OPENAI_API_KEY
        client = openai.OpenAI(api_key='')

    if (baseConf.get('api_key', '')):
        client.api_key = baseConf.get('api_key', '')

    if is_chub:
        logger.info(f"Using Chub's API for model: {model}")
        if model in ["mars", "asha"]:
            model = "asha"
            client.base_url = 'https://mars.chub.ai/chub/asha/v1'
        elif model in ["mercury", "mythomax"]:
            model = "mythomax"
            client.base_url = 'https://mercury.chub.ai/mythomax/v1'
        elif model in ["mistral", "mixtral"]:
            model = "mixtral"
            client.base_url = 'https://mars.chub.ai/mixtral/v1'
        client.api_key = baseConf.get('chub_api', '')
    elif is_mistral:
        logger.info(f"Using Mistral API for model: {model}")
        client.base_url = 'https://api.mistral.ai/v1'
        client.api_key = baseConf.get('mistral_api', '')

    if isinstance(function_call, bool):
        if function_call:
            function_call = "auto"
        else:
            function_call = "none"
    response = False
    while (not response):
        try:
            if (temp_api_key):
                client.api_key = temp_api_key
            if (temp_organization):
                client.organization = temp_organization

            if "vision" in model:
                # if model is base vision model (not accepting tools/functions)
                response = client.chat.completions.create(
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty,
                    messages=messages.get_messages_vision(),
                )
            elif "gpt-4o" in model:
                # if model is derivative of gpt-4o (omni: vision+functions)
                response = client.chat.completions.create(
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty,
                    messages=messages.get_messages_vision(),
                    tools=functionlist_to_toollist(
                        existingFunctions.getEnabled()),
                    tool_choice=function_call,
                )
            else:
                if is_mistral:
                    # if model is a mistral model
                    try:
                        response = client.chat.completions.create(
                            model=model,
                            temperature=temperature,
                            max_tokens=max_tokens,
                            top_p=top_p,
                            messages=messages.get_messages(),
                            tools=functionlist_to_toollist(
                                existingFunctions.getEnabled()),
                            tool_choice=function_call,
                        )
                    except Exception as e:
                        if 'function calling is not enabled' in str(e).lower():
                            # if not compatible with functions:
                            response = client.chat.completions.create(
                                model=model,
                                temperature=temperature,
                                max_tokens=max_tokens,
                                top_p=top_p,
                                messages=messages.get_messages(),
                            )
                        else:
                            openai.BadRequestError
                elif is_chub:
                    # if model is a chub.ai model
                    try:
                        response = client.chat.completions.create(
                            model=model,
                            temperature=temperature,
                            max_tokens=max_tokens,
                            top_p=top_p,
                            frequency_penalty=frequency_penalty,
                            presence_penalty=presence_penalty,
                            messages=messages.get_messages(),
                        )
                    except Exception as e:
                        logger.exception(e)
                else:
                    # else (supposedly GPT model from openAI, without vision)
                    response = client.chat.completions.create(
                        model=model,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        top_p=top_p,
                        frequency_penalty=frequency_penalty,
                        presence_penalty=presence_penalty,
                        messages=messages.get_messages(),
                        tools=functionlist_to_toollist(
                            existingFunctions.getEnabled()),
                        tool_choice=function_call,
                    )
        except openai.BadRequestError:
            try:
                messages.shorten()
            except Exception as e:
                lf = getLogger.getLoggerFile()
                logger.critical("Critical error... Aborting request...")
                logger.critical(f"Please, send {lf} to @darkgeem on discord")
                logger.critical("Along with a saved .json of your request.")
                logger.exception(e)
                return messages
        except openai.InternalServerError:
            logger.error("Service unavailable...")
            time.sleep(1)
            logger.error("Retrying now...")
    # do something with the response
    message = response.choices[0].message
    while message.tool_calls is not None:
        try:
            for tool_call in message.tool_calls:
                tool_function = tool_call.function
                function_name = tool_function.name
                try:
                    kwargs = json.loads(tool_function.arguments)
                except json.decoder.JSONDecodeError:
                    unfixed = tool_function.arguments
                    fixed = convert_invalid_json(unfixed)
                    kwargs = json.loads(fixed)
                function_response = \
                    existingFunctions.getFunction(function_name)(**kwargs)
                messages.add_function(function_name, function_response)
            response2 = False
            while not (response2):
                try:
                    if (temp_api_key):
                        client.api_key = temp_api_key
                    if (temp_organization):
                        client.organization = temp_organization
                    response2 = client.chat.completions.create(
                        model=model,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        top_p=top_p,
                        frequency_penalty=frequency_penalty,
                        presence_penalty=presence_penalty,
                        messages=messages.get_messages(),
                        tools=functionlist_to_toollist(
                            existingFunctions.getEnabled()),
                        tool_choice=function_call,
                    )
                except (
                    openai.BadRequestError,
                    openai.UnprocessableEntityError
                ):
                    messages.shorten()
                except (
                    openai.RateLimitError,
                    openai.InternalServerError,
                    openai.APIConnectionError,
                ):
                    logger.error("Service unavailable...")
                    time.sleep(1)
                    logger.error("Retrying now...")
                message = response2.choices[0].message
        except Exception as e:
            logger.exception(e)
            logger.error(message.tool_calls[0].function.name)
            logger.error(message.tool_calls[0].function.arguments)
            break
    try:
        messages.add_answer(message.content.strip())
    except Exception as e:
        logger.exception(e)
    return messages
