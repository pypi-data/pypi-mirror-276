# used https://github.com/simonw/llm/blob/main/llm/default_plugins/openai_models.py as a template

import llm
from llm.utils import remove_dict_none_values
from typing import List, Optional
from pydantic import Field
import requests
import uuid
import json


@llm.hookimpl
def register_models(register):
    register(GigaChat())


class SharedOptions(llm.Options):
    temperature: Optional[float] = Field(
        description=(
            "What sampling temperature to use, between 0 and 2. Higher values like "
            "0.8 will make the output more random, while lower values like 0.2 will "
            "make it more focused and deterministic."
        ),
        ge=0,
        le=100,
        default=1,
    )
    max_tokens: Optional[int] = Field(
        description="Maximum number of tokens to generate.", default=1024
    )
    top_p: Optional[float] = Field(
        description=(
            "An alternative to sampling with temperature, called nucleus sampling, "
            "where the model considers the results of the tokens with top_p "
            "probability mass. So 0.1 means only the tokens comprising the top "
            "10% probability mass are considered. Recommended to use top_p or "
            "temperature but not both."
        ),
        ge=0,
        le=1,
        default=0.4,
    )


class GigaChat(llm.Model):
    model_id = "gigachat"
    needs_key = "gigachat"
    key_env_var = "GIGA_AUTH"

    can_stream = False
    default_max_tokens = None

    class Options(SharedOptions):
        json_object: Optional[bool] = Field(
            description="Output a valid JSON object {...}. Prompt must mention JSON.",
            default=None,
        )

    def __str__(self):
        return "GigaChat: {}".format(self.model_id)

    def execute(self, prompt, stream, response, conversation=None):
        messages = []
        current_system = None
        if conversation is not None:
            for prev_response in conversation.responses:
                if (
                    prev_response.prompt.system
                    and prev_response.prompt.system != current_system
                ):
                    messages.append(
                        {"role": "system", "content": prev_response.prompt.system}
                    )
                    current_system = prev_response.prompt.system
                messages.append(
                    {"role": "user", "content": prev_response.prompt.prompt}
                )
                messages.append({"role": "assistant", "content": prev_response.text()})
        if prompt.system and prompt.system != current_system:
            messages.append({"role": "system", "content": prompt.system})
        messages.append({"role": "user", "content": prompt.prompt})
        response._prompt_json = {"messages": messages}
        kwargs = self.build_kwargs(prompt)
        token = get_giga_auth(self.get_key())
        
        if stream:
            print('Streaming not implemented')
            pass
        else:
            completion = giga_send(
                msgs=messages,
                token=token,
                **kwargs
            )
            response.response_json = remove_dict_none_values(completion.json())
            yield completion.json()['choices'][0]['message']['content']

    def build_kwargs(self, prompt):
        kwargs = dict(not_nulls(prompt.options))
        json_object = kwargs.pop("json_object", None)
        if "max_tokens" not in kwargs and self.default_max_tokens is not None:
            kwargs["max_tokens"] = self.default_max_tokens
        if json_object:
            kwargs["response_format"] = {"type": "json_object"}
        return kwargs


def not_nulls(data) -> dict:
    return {key: value for key, value in data if value is not None}


def combine_chunks(chunks: List) -> dict:
    content = ""
    role = None
    finish_reason = None

    for item in chunks:
        for choice in item.choices:

            if not hasattr(choice, "delta"):
                content += choice.text
                continue
            role = choice.delta.role
            if choice.delta.content is not None:
                content += choice.delta.content
            if choice.finish_reason is not None:
                finish_reason = choice.finish_reason

    combined = {
        "content": content,
        "role": role,
        "finish_reason": finish_reason,
    }
    for key in ("id", "object", "model", "created", "index"):
        value = getattr(chunks[0], key, None)
        if value is not None:
            combined[key] = value

    return combined


def get_giga_auth(GIGA_AUTH, corp = False):
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    rquid = str(uuid.uuid4())
    payload = "scope=GIGACHAT_API_CORP" if corp else "scope=GIGACHAT_API_PERS"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": rquid,
        "Authorization": "Basic " + GIGA_AUTH,
    }
    response = requests.request(
        "POST",
        url,
        headers=headers,
        data=payload,
        verify="/etc/ssl/certs/ca-certificates.crt",
        # verify=False
    )

    return response.json()['access_token']


def giga_send(
    msgs,
    token,
    model = 'GigaChat-Pro',
    url="https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
    temperature=0.7,
    top_p=0.6,
    n=1,
    max_tokens=512,
):
    payload = json.dumps(
        {
            "model": model,
            "messages": msgs,
            "temperature": temperature,
            "top_p": top_p,
            "n": n,
            "stream": False,
            "max_tokens": max_tokens,
            "repetition_penalty": 1,
            "update_interval": 0,
        }
    )
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    }
    response = requests.request(
        "POST",
        url,
        headers=headers,
        data=payload,
        verify="/etc/ssl/certs/ca-certificates.crt",
        # verify=False
    )
    if response.status_code != 200:
        print(response.status_code)
        print(response.json())
    return response
