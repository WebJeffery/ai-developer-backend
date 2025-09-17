# -*- coding: utf-8 -*- 

import asyncio
import httpx, aiofiles
import numpy as np
from openai import AsyncOpenAI

from app.core.logger import logger


class AIClient:
    def __init__(self, kb_filepath=None, model="qwen3:4b", embedding_model="nomic-embed-text"):
        # AI模型配置
        self.model = model
        self.embedding_model = embedding_model
        
        # 创建HTTP客户端
        self.http_client = httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True
        )
        
        # 初始化OpenAI客户端（用于与Ollama交互）
        self.client = AsyncOpenAI(
            api_key="ollama",
            base_url="http://127.0.0.1:11434/v1",
            http_client=self.http_client
        )
        
        # 知识库相关属性
        self.docs = []
        self.embeds = None
        
        # 如果提供了知识库文件路径，则加载知识库
        self.kb_loaded = False
        self.kb_filepath = kb_filepath
        
        # RAG提示词模板
        self.prompt_template = """
        基于以下知识回答用户的问题:
        1: %s
        2: %s
        3: %s
        4: %s
        5: %s
        
        用户的问题: %s
        
        请根据提供的知识，用中文简洁准确地回答问题。如果提供的知识不足以回答，请说明这一点。
        """

    # 知识库相关异步方法
    async def load_kb(self):
        """异步加载知识库文件"""
        if not self.kb_filepath or self.kb_loaded:
            return
            
        try:
            # 异步读取文件
            async with aiofiles.open(self.kb_filepath, 'r', encoding='utf-8') as f:
                content = await f.read()
            
            self.docs = self.split_content(content)
            self.embeds = await self.encode(self.docs)
            self.kb_loaded = True
            logger.info(f"成功加载知识库，包含 {len(self.docs)} 个文档片段")
        except Exception as e:
            logger.error(f"加载知识库失败: {str(e)}")
            raise

    @staticmethod
    def split_content(content):
        """将内容分割成文档块"""
        chunks = []
        # 按换行符分割成行
        lines = content.splitlines()
        for line in lines:
            stripped_line = line.strip()
            if stripped_line:
                chunks.append(stripped_line)
        return chunks

    async def encode(self, texts):
        """异步使用Ollama生成嵌入向量"""
        embeds = []
        for text in texts:
            try:
                # 使用AsyncOpenAI客户端异步生成嵌入
                response = await self.client.embeddings.create(
                    model=self.embedding_model,
                    input=text
                )
                embeds.append(response.data[0].embedding)
            except Exception as e:
                logger.error(f"生成嵌入向量失败 for text: {text[:30]}...: {str(e)}")
                # 对于失败的嵌入，添加一个零向量
                embeds.append([0.0] * 768)  # 假设nomic-embed-text生成768维向量
        return np.array(embeds)

    @staticmethod
    def similarity(e1, e2):
        """计算余弦相似度"""
        dot_product = np.dot(e1, e2)
        norm_e1 = np.linalg.norm(e1)
        norm_e2 = np.linalg.norm(e2)
        
        if norm_e1 == 0 or norm_e2 == 0:
            return 0.0  # 避免除以零
        
        return dot_product / (norm_e1 * norm_e2)

    async def search(self, text, top_k=5):
        """异步在知识库中搜索相似文本"""
        # 确保知识库已加载
        if not self.kb_loaded:
            await self.load_kb()
            
        if not self.embeds.any():
            logger.warning("知识库为空，无法进行搜索")
            return []
            
        # 生成查询文本的嵌入向量
        query_embed = (await self.encode([text]))[0]
        
        # 计算与所有文档的相似度
        sims = [(idx, self.similarity(query_embed, doc_embed)) 
                for idx, doc_embed in enumerate(self.embeds)]
        
        # 按相似度排序
        sims.sort(key=lambda x: x[1], reverse=True)
        
        # 返回前top_k个匹配结果
        top_matches = [self.docs[idx] for idx, _ in sims[:top_k]]
        return top_matches

    # RAG相关异步方法
    async def build_rag_prompt(self, query):
        """异步构建RAG提示词"""
        # 搜索知识库获取相关上下文
        context = await self.search(query)
        
        # 确保上下文有5个元素，不足的用空字符串填充
        context += [""] * (5 - len(context))
        
        # 构建提示词
        return self.prompt_template % (
            context[0], context[1], context[2], context[3], context[4], query
        )

    # AI处理相关方法
    async def process(self, query: str, use_rag=True):
        """处理查询并返回流式响应，支持RAG模式"""
        system_prompt = """你是一个有用的AI助手，可以帮助用户回答问题和提供帮助。请用中文回答用户的问题。"""
        
        # 如果启用RAG，构建增强提示词
        if use_rag and self.kb_filepath:
            user_query = await self.build_rag_prompt(query)
        else:
            user_query = query

        try:
            # 使用 await 调用异步客户端
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
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


async def chat_query(message: str, kb_filepath=None):
    """处理聊天查询的异步函数"""
    # 创建AI客户端实例，传入知识库文件路径
    # message = message + "/no_think"
    ai_client = AIClient(kb_filepath=kb_filepath)
    try:
        # 处理消息，启用RAG
        async for response in ai_client.process(message, use_rag=True):
            print(response, end='', flush=True)
    finally:
        # 确保关闭客户端连接
        await ai_client.close()


if __name__ == "__main__":
    # 在异步事件循环中运行聊天查询
    asyncio.run(chat_query("帕金森氏症介绍，怎么治疗", kb_filepath='帕金森氏症en.txt'))
