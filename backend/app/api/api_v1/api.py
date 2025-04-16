from fastapi import APIRouter

from app.api.api_v1.endpoints import wechat ,garbage,ai



api_router = APIRouter()

# api_router.include_router(login.router, prefix="/login", tags=["login"])
# api_router.include_router(users.router, prefix="/users", tags=["users"]) 
api_router.include_router(ai.router, prefix="/ecosort", tags=["ai"])
# api_router.include_router(article.router, prefix="/article", tags=["articles"])
api_router.include_router(wechat.router, prefix="/user", tags=["user"])
api_router.include_router(garbage.router,prefix="/ecosort",tags=["garbage"])




