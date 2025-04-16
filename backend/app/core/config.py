import os
import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "拉风侠-垃圾检测系统"
    
    # 数据库设置
    USE_SQLITE: bool = os.getenv("USE_SQLITE", "").lower() in ("true", "1", "t")
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "123456"
    POSTGRES_DB: str = "garbage"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None


    # ai_key_settings
    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str = "https://xiaoai.plus/v1/"
    OPENAI_MODEL: str = "gpt-3.5-turbo"  # 默认使用 gpt-3.5-turbo 模型

    # 微信登录授权
    WECHAT_APP_ID: str = ""  # 你的小程序 AppID
    WECHAT_APP_SECRET: str = ""  # 你的小程序 AppSecret
    
    # @validator("WECHAT_APP_ID", "WECHAT_APP_SECRET", pre=True)
    # def validate_wechat_config(cls, v: str) -> str:
    #     if not v:
    #         raise ValueError("请在.env文件中配置微信小程序相关信息")
    #     return v
     # 图片处理和语音配置
    PROCESSED_IMAGES_DIR: str = "static/processed_images"
    AUDIO_OUTPUT_DIR: str = "static/audio"
    GARBAGE_CATEGORIES: Dict[int, str] = {
        0: "可回收物",
        1: "有害垃圾",
        2: "厨余垃圾",
        3: "其他垃圾"
    }
    CATEGORY_DESCRIPTIONS: Dict[str, str] = {
        "可回收物": "请投放到可回收物收集容器",
        "有害垃圾": "请投放到有害垃圾收集点",
        "厨余垃圾": "请投放到厨余垃圾收集容器",
        "其他垃圾": "请投放到其他垃圾收集容器"
    }
    YOLO_MODEL_PATH: str = "best.pt"  # YOLOv11模型的路径

    # 七牛云配置
    QINIU_ACCESS_KEY: str = ""
    QINIU_SECRET_KEY: str = ""
    QINIU_BUCKET_NAME: str = ""
    QINIU_DOMAIN: str = ""  # 你的七牛云域名，例如 http://cdn.example.com

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        
        # 如果设置了使用 SQLite，则返回 SQLite 连接字符串
        if values.get("USE_SQLITE"):
            return "sqlite:///./garbage.db"
            
        # 否则使用 PostgreSQL
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        case_sensitive = True
        env_file = ".env"
        # 因为下载了python-dotenv包，才可以使用.env文件

settings = Settings()

