import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_service import AIAssistant

logger = logging.getLogger(__name__)

router = APIRouter()
ai_assistant = AIAssistant()

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    code: int = 0
    data: dict
    msg: str = "success"

@router.post("/speech", response_model=ChatResponse)
async def chat_with_ai(chat_message: ChatMessage):
    """与AI助手对话"""
    try:
        result = await ai_assistant.get_response(chat_message.message)
        return ChatResponse(
            code=0,
            data={"result": result},
            msg="success"
        )
    except Exception as e:
        # 添加日志记录
        logger.error(f"AI聊天出错: {str(e)}", exc_info=True)
        return ChatResponse(
            code=1,
            data={},
            msg=f"AI服务出错: {str(e) or '未知错误'}"  # 如果错误消息为空则显示"未知错误"
        )




