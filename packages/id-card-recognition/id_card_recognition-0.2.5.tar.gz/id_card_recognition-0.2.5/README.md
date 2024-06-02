1、创建 .env 文件，并添加以下内容：
API_KEY= 你的moonshot AI 秘钥
IMAGE_DIRECTORY= 需要识别的身份证照片存放路径，默认为 ./images
RESULT_FILE_NAME= 识别结果文件名称，默认为 result.txt
CHOSEN_MODEL_NAME= 选择的模型名称，默认为 "moonshot-v1-8k"

2、添加引用
from id_card_recognition.recognition import do_recognition

3、调用识别方法
调用do_recognition()，返回识别结果。识别结果将保存在 RESULT_FILE_NAME 指定的文件中。
