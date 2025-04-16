from openai import AsyncOpenAI
from app.core.config import settings
import logging
from fastapi import HTTPException

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AIAssistant:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL
        )
        
        self.system_prompt = """
        你是一个垃圾分类助手，可以帮助用户:
        1. 识别垃圾类别
        2. 解答垃圾分类相关问题
        3. 提供垃圾处理建议
        请用简短、清晰的语言回答。
        """

    async def get_response(self, message: str) -> str:
        try:
            # 检查是否配置了API密钥
            if not settings.OPENAI_API_KEY:
                raise ValueError("未配置OpenAI API密钥")

            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            # 确保异常包含具体信息
            raise Exception(f"OpenAI API调用失败: {str(e)}") from e



