# -*- coding: utf-8 -*- 

from openai import AsyncOpenAI, OpenAI
from openai.types.chat.chat_completion import ChatCompletion
import httpx

from app.config.setting import settings
from app.core.logger import logger


class AIClient:

    def __init__(self):
        self.model = settings.OPENAI_MODEL
        # 创建一个不带冲突参数的httpx客户端
        self.http_client = httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True
        )
        
        # 使用自定义的http客户端
        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL,
            http_client=self.http_client
        )

    async def process(self, query: str):
        """处理查询并返回流式响应"""
        system_prompt = """你是一个有用的AI助手，可以帮助用户回答问题和提供帮助。请用中文回答用户的问题。"""

        try:
            # 使用 await 调用异步客户端
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                stream=True
            )
            
            # 流式返回响应
            async for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            logger.error(f"AI处理查询失败: {str(e)}")
            yield f"抱歉，处理您的请求时出现了错误: {str(e)}"

    async def close(self):
        """关闭客户端连接"""
        if hasattr(self, 'client'):
            await self.client.close()
        if hasattr(self, 'http_client'):
            await self.http_client.aclose()