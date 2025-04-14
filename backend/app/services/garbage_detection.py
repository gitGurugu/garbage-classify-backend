from ultralytics import YOLO
import cv2
import numpy as np
from pathlib import Path
import uuid #生成唯一识别码
import os
from fastapi import UploadFile #用于处理上传的文件
from gtts import gTTS #导入gTTS类
from app.core.config import settings
from typing import List
class GarbageDetectionService:
    def __init__(self):
        Path(settings.PROCESSED_IMAGES_DIR).mkdir(parents=True, exist_ok=True) #如果 settings.PROCESSED_IMAGES_DIR 指定的目录不存在，则创建该目录。
        Path(settings.AUDIO_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
        
        # 使用 ultralytics YOLO
        self.model = YOLO(settings.YOLO_MODEL_PATH)

    async def process_image(self, image_file: UploadFile):
        # 读取图片
        contents = await image_file.read() #读取上传的文件内容，返回一个字节串（bytes）对象。这个对象包含了文件的二进制数据。
        nparr = np.frombuffer(contents, np.uint8) #这行代码将二进制数据 contents 转换为一个 NumPy 数组 nparr，其中每个元素的数据类型为 uint8（无符号8位整数）
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR) #从上传的文件中读取图像内容，将其转换为 NumPy 数组，然后使用 OpenCV 将其解码为图像。
        #cv2.IMREAD_COLOR 是一个标志，指定解码时的模式。它表示将图像解码为彩色图像（BGR 格式）。

        # 执行检测
        #results 通常是一个对象，它包含了检测结果和原始图像的引用
        results = self.model(img)[0]  # 只取第一张图片的结果
        #在深度学习中，尤其是使用现代框架（如 PyTorch、TensorFlow 等）时，模型的输入和输出通常是批量（batch）数据。这意味着即使你只处理一张图像，模型也会将其视为一个批量中的一个元素。
        # 在图片上绘制检测框和标签
        annotated_img = results.plot()  # 使用 YOLO 内置的绘图功能
        #边界框坐标：通常是 [x_min, y_min, x_max, y_max] 或 [x_center, y_center, width, height]。类别标签：检测到的目标的类别。置信度：模型对检测结果的置信度分数。
       
        
       
       
        # 保存处理后的图片
        image_filename = f"{uuid.uuid4()}.jpg"
        #uuid4() 是 uuid 模块中的一个函数，用于生成一个随机的 UUID。
        #UUID 是一个 128 位的数字，通常表示为 32 个十六进制数字，分为 5 组，形式为 xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx。
        image_path = os.path.join(settings.PROCESSED_IMAGES_DIR, image_filename)
        #os.path.join 是 Python 的 os 模块提供的一个函数，用于安全地连接路径组件
        cv2.imwrite(image_path, annotated_img)
        


        # 获取检测结果
        detected_categories = []
        for r in results.boxes.data: #results.boxes.data 是一个张量（Tensor），其中每一行表示一个检测结果。
            #boxes就是检测到的边界框，data就是边界框的坐标和置信度等信息。
            cls = int(r[5]) #[x_min, y_min, x_max, y_max, confidence, class_id]
            conf = float(r[4])
            if conf > 0.5 and settings.GARBAGE_CATEGORIES[cls] not in detected_categories:
                detected_categories.append(settings.GARBAGE_CATEGORIES[cls])

        # 生成语音提示
        audio_text = self.generate_audio_text(detected_categories)
        audio_filename = f"{uuid.uuid4()}.mp3"
        audio_path = os.path.join(settings.AUDIO_OUTPUT_DIR, audio_filename)
        
        tts = gTTS(text=audio_text, lang='zh-cn')
        tts.save(audio_path)

        return {
            "image_url": f"/static/processed_images/{image_filename}",
            "audio_url": f"/static/audio/{audio_filename}",
            "categories": detected_categories
        }
        """
        class ProcessedFilesResponse(TypedDict):
            image_url: str
            audio_url: str
            categories: List[str]
        """




    def generate_audio_text(self, categories: List[str]) -> str:
        if not categories:
            return "未能识别出垃圾类别，请重新拍摄。"
        
        text = "识别结果：\n"
        for category in categories:
            text += f"{category}，{settings.CATEGORY_DESCRIPTIONS[category]}。\n"
        return text
    



    """results = [
    {
        'class': 0,  # 物体类别标签，例如 0 代表 'cat'，1 代表 'dog' 等
        'confidence': 0.85,  # 置信度，范围从0到1
        'bbox': [50, 150, 200, 300],  # 边界框坐标，格式为[x_min, y_min, x_max, y_max]
        'mask': ...,  # 掩码图，表示物体在图像中的具体位置
        'image_id': 0  # 图像 ID，用于追踪图像中物体
    },
    {
        'class': 1,
        'confidence': 0.75,
        'bbox': [100, 200, 250, 350],
        'mask': ...,
        'image_id': 0
    },
    {
        'class': 2,
        'confidence': 0.9,
        'bbox': [30, 80, 180, 230],
        'mask': ...,
        'image_id': 0
    }
]"""