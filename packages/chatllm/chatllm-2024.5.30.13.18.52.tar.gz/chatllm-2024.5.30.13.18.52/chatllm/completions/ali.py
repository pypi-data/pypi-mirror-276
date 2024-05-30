#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ali
# @Time         : 2024/5/24 11:11
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
from asgiref.sync import sync_to_async

from meutils.pipe import *

from dashscope import Application, Generation

from chatllm.schemas.openai_api_protocol import ChatCompletionRequest, UsageInfo
from chatllm.schemas.openai_types import chat_completion, chat_completion_chunk


class Completions(object):
    def __init__(self, api_key=None):
        self.api_key = api_key

    @sync_to_async
    def acreate(self, request: ChatCompletionRequest):
        return self.create(request)

    def create(self, request: ChatCompletionRequest):
        if request.model.startswith("qwen-"):
            response = Generation.call(
                model=request.model,  # app当做一个模型
                messages=request.messages,  # Message
                api_key=self.api_key,
                stream=request.stream,
                temperature=request.temperature,
                # incremental_output=True,
            )
        else:

            response = Application.call(
                app_id=request.model,  # app当做一个模型
                prompt=request.last_content,
                api_key=self.api_key,
                stream=request.stream,
                temperature=request.temperature,
            )

        if request.stream:
            content = ''
            for chunk in response:
                if chunk.status_code != 200:
                    logger.error(chunk)
                    chat_completion_chunk.choices[0].delta.content = chunk
                    chat_completion_chunk.choices[0].finish_reason = 'stop'
                    yield chat_completion_chunk
                    return

                output = chunk.get("output", {})

                _content = output.get("text")
                if _content:
                    chat_completion_chunk.choices[0].delta.content = _content.replace(content, '')
                    yield chat_completion_chunk
                    chat_completion_chunk.choices[0].finish_reason = output.get("finish_reason")
                    content = _content
                else:
                    _ = output.get("choices")[0]
                    finish_reason = _.get("finish_reason")
                    _content = _.get("message").get("content")

                    chat_completion_chunk.choices[0].delta.content = _content.replace(content, '')
                    if finish_reason != 'stop':
                        chat_completion_chunk.choices[0].finish_reason = finish_reason
                    yield chat_completion_chunk
                    content = _content
        else:
            if response.status_code != 200:
                logger.error(response)
                chat_completion.choices[0].message.content = response
                yield chat_completion
                return

            chat_completion.choices[0].message.content = response.get("output", {}).get("text")

            if "models" in (usage := response.get("usage")):
                usage = response.get("usage").get("models")[0]

            prompt_tokens = usage.get("input_tokens")
            completion_tokens = usage.get("output_tokens")
            total_tokens = prompt_tokens + completion_tokens
            chat_completion.usage = UsageInfo(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens
            )

            # logger.debug(chat_completion)

            yield chat_completion


if __name__ == '__main__':
    app_id = '3e27fc43adf5410c919cc4aaae03c88d'
    prompt = '你是谁'
    api_key = 'sk-4e6489ba597541dfa7a51f43e3912ca2'
    api_key = 'sk-9c519f1bffd4486f8c3c308ac3d89b66	'


    # model = "farui-plus"
    model = "qwen-max"

    client = Completions(api_key=api_key)
    # print(client.get_and_update_api_key(resource_ids=list(client.endpoint_map.values())))

    r = client.create(ChatCompletionRequest(stream=False, model=app_id))
    r = client.create(ChatCompletionRequest(stream=False, model='qwen-max'))
    r = client.create(
        ChatCompletionRequest(stream=True, model=model, messages=[{'role': 'user', 'content': '你是谁'}]))

    for i in r:
        print(i)
