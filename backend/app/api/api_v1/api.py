from fastapi import APIRouter

from app.api.api_v1.endpoints import wechat ,garbage,ai,garbage_item,history,image



api_router = APIRouter()

# api_router.include_router(login.router, prefix="/login", tags=["login"])
# api_router.include_router(users.router, prefix="/users", tags=["users"]) 
api_router.include_router(ai.router, prefix="/ecosort", tags=["ai"])
# api_router.include_router(article.router, prefix="/article", tags=["articles"])
api_router.include_router(wechat.router, prefix="/user", tags=["user"])
api_router.include_router(garbage.router,prefix="/ecosort",tags=["garbage_detect"])
api_router.include_router(garbage_item.router,prefix="/ecosort",tags=["garbage_item"])
api_router.include_router(history.router,prefix="/ecosort",tags=["history"])
api_router.include_router(image.router,prefix="/img",tags=["image"])


