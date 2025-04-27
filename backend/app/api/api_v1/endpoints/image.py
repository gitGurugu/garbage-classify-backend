from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()
@router.get("/index", summary="首页图片")
async def upload_home_image():
    return {
    "code": 0,
    "data": {
        "pageImg": [
            "http://image.curryking123.online/%E9%A6%96%E9%A1%B5/index1.png",
            "http://image.curryking123.online/%E9%A6%96%E9%A1%B5/index2.png",
            "http://image.curryking123.online/%E9%A6%96%E9%A1%B5/indexsub1.png",
            "http://image.curryking123.online/%E9%A6%96%E9%A1%B5/indexsub2.png",
            "http://image.curryking123.online/%E9%A6%96%E9%A1%B5/indexsub3.png",
            "http://image.curryking123.online/%E9%A6%96%E9%A1%B5/indexsub4.png",
            "http://image.curryking123.online/%E9%A6%96%E9%A1%B5/indexsubact1.png",
            "http://image.curryking123.online/%E9%A6%96%E9%A1%B5/indexsubact2.png",
            "http://image.curryking123.online/%E9%A6%96%E9%A1%B5/indexsubact3.png",
            "http://image.curryking123.online/%E9%A6%96%E9%A1%B5/indexsubact4.png",
        ],
        "classifyImg": {
            "recyclable": "http://image.curryking123.online/%E9%A6%96%E9%A1%B5/sub1_recycle.png",
            "other": "http://image.curryking123.online/%E9%A6%96%E9%A1%B5/sub1_other.png",
            "hazardous": "http://image.curryking123.online/%E9%A6%96%E9%A1%B5/sub1_harm.png",
            "kitchen": "http://image.curryking123.online/%E9%A6%96%E9%A1%B5/sub1_kitchen.png"
        },
        "policyImg": [
            "http://image.curryking123.online/%E9%A6%96%E9%A1%B5/sub2_3.png",
            "http://image.curryking123.online/%E9%A6%96%E9%A1%B5/sub2_3.png",
            "http://image.curryking123.online/%E9%A6%96%E9%A1%B5/sub2_3.png"
        ],
        "activityImg": [
            "http://image.curryking123.online/%E9%A6%96%E9%A1%B5/sub2_3.png",
            "http://image.curryking123.online/%E9%A6%96%E9%A1%B5/sub2_3.png",
            "http://image.curryking123.online/%E9%A6%96%E9%A1%B5/sub2_3.png"
        ],
        "exchange": [
            "http://image.curryking123.online/%E9%A6%96%E9%A1%B5/sub4_1.png",
            "http://image.curryking123.online/%E9%A6%96%E9%A1%B5/sub4_2.png",
            "http://image.curryking123.online/%E9%A6%96%E9%A1%B5/sub4_3.png",
            "http://image.curryking123.online/%E9%A6%96%E9%A1%B5/sub4_4.png",
           
        ]
    },
    "msg": "success"
}
    
@router.get("/classify", summary="垃圾分类图片")
async def upload_classify_image():
    return {
    "code": 0,
    "data": {
        "pageImg": [
            "http://image.curryking123.online/%E5%9E%83%E5%9C%BE%E5%88%86%E7%B1%BB%E9%A1%B5%E9%9D%A2/classify1.png",
            "http://image.curryking123.online/%E5%9E%83%E5%9C%BE%E5%88%86%E7%B1%BB%E9%A1%B5%E9%9D%A2/classify2.png",
            "http://image.curryking123.online/%E5%9E%83%E5%9C%BE%E5%88%86%E7%B1%BB%E9%A1%B5%E9%9D%A2/classify3.png",
            "http://image.curryking123.online/%E5%9E%83%E5%9C%BE%E5%88%86%E7%B1%BB%E9%A1%B5%E9%9D%A2/classifyback.png",
        ],
        "classifyImg": {
            "recyclable": "http://image.curryking123.online/%E5%9E%83%E5%9C%BE%E5%88%86%E7%B1%BB%E9%A1%B5%E9%9D%A2/classify_recycle.png",
            "other": "http://image.curryking123.online/%E5%9E%83%E5%9C%BE%E5%88%86%E7%B1%BB%E9%A1%B5%E9%9D%A2/classify_other.png",
            "hazardous": "http://image.curryking123.online/%E5%9E%83%E5%9C%BE%E5%88%86%E7%B1%BB%E9%A1%B5%E9%9D%A2/classify_harm.png",
            "kitchen": "http://image.curryking123.online/%E5%9E%83%E5%9C%BE%E5%88%86%E7%B1%BB%E9%A1%B5%E9%9D%A2/classify_kitchen.png",
        }
    },
    "msg": "success"
}

@router.get("/mine", summary="个人主页的图片")
async def upload_mine_image():
    return{
        
    "code": 0,
    "data": {
        "pageImg": [
            "http://image.curryking123.online/%E6%88%91%E7%9A%84/mine1.png",
            "http://image.curryking123.online/%E6%88%91%E7%9A%84/minesub1.png",
            "http://image.curryking123.online/%E6%88%91%E7%9A%84/minesub2.png",
            "http://image.curryking123.online/%E6%88%91%E7%9A%84/minesub3.png",
            "http://image.curryking123.online/%E6%88%91%E7%9A%84/minesub4.png",
            "http://image.curryking123.online/%E6%88%91%E7%9A%84/mine6.png",
            "http://image.curryking123.online/%E6%88%91%E7%9A%84/1.png",
            "http://image.curryking123.online/%E6%88%91%E7%9A%84/2.png",
            "http://image.curryking123.online/%E6%88%91%E7%9A%84/3.png",
            "http://image.curryking123.online/%E6%88%91%E7%9A%84/4.png",
            "http://image.curryking123.online/%E6%88%91%E7%9A%84/5.png",
            "http://image.curryking123.online/%E6%88%91%E7%9A%84/arrow1.png",
            "http://image.curryking123.online/%E6%88%91%E7%9A%84/arrow2.png",
            "http://image.curryking123.online/%E6%88%91%E7%9A%84/arrow3.png",

            

        ]
    },
    "msg": "success"
}

@router.get("/feedback", summary="反馈页面的图片")
async def upload_feedback_image():
    return{
    "code": 0,
    "data": {
        "pageImg": [
            "http://image.curryking123.online/%E5%8F%8D%E9%A6%88/act-star.png",
            "http://image.curryking123.online/%E5%8F%8D%E9%A6%88/feedback.png",
            "http://image.curryking123.online/%E5%8F%8D%E9%A6%88/star.png",
        ]
    },
    "msg": "success"
}
    