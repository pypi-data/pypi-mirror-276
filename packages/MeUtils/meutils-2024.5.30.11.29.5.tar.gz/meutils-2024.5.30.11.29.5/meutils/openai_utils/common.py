#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : commom
# @Time         : 2024/5/30 11:20
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from openai import AsyncOpenAI, OpenAI


def ppu(model='ppu', api_key: Optional[str] = None):
    client = OpenAI(api_key=api_key)
    return client.chat.completions.create(messages=[{'role': 'user', 'content': 'hi'}], model=model)


async def appu(model='ppu', api_key: Optional[str] = None):
    client = AsyncOpenAI(api_key=api_key)
    return await client.chat.completions.create(messages=[{'role': 'user', 'content': 'hi'}], model=model)


if __name__ == '__main__':
    # print(ppu())
    print(appu())
    print(arun(appu()))
