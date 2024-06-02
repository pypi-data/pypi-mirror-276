# id_card_recognition/recognition.py
import os
from pathlib import Path
from openai import OpenAI
import json
import time
from natsort import natsorted
from dotenv import load_dotenv
from .utils import get_headers, make_request, calculate_cost

# 加载环境变量
load_dotenv()

# 从环境变量中获取API密钥
api_key = os.getenv("API_KEY")

# 指定使用的模型
chosen_model = os.getenv("CHOSEN_MODEL_NAME")

# 指定图像目录
image_directory = os.getenv("IMAGE_DIRECTORY")  # 替换为实际的目录名
result_file_name = os.getenv("RESULT_FILE_NAME")

# 初始化OpenAI客户端
client = OpenAI(
    api_key=api_key,
    base_url="https://api.moonshot.cn/v1",
)


def get_balance(api_key):
    url = "https://api.moonshot.cn/v1/users/me/balance"
    headers = get_headers(api_key)
    return make_request(url, headers)


def estimate_token_count(api_key, messages, model):
    url = "https://api.moonshot.cn/v1/tokenizers/estimate-token-count"
    headers = get_headers(api_key)
    data = {
        "model": model,
        "messages": messages
    }
    return make_request(url, headers, method="POST", data=data)


def process_id_card(image_file, file_content, model):
    messages = [
        {
            "role": "system",
            "content": "你是身份证检查员。"
        },
        {
            "role": "user",
            "content": (
                "请从以下图像内容中提取身份证信息，并以JSON格式输出。"
                "请确保包含以下字段：姓名、性别、民族、出生日期、住址、公民身份号码。\n\n"
                "图像内容如下：\n" + file_content
            )
        }
    ]

    token_response = estimate_token_count(api_key, messages, model)
    if not token_response:
        return None, 0

    tokens_used = token_response['data']['total_tokens']

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.3,
    )

    response_content = completion.choices[0].message.content

    try:
        id_info = json.loads(response_content)
        result = {
            "file": str(image_file),
            "result": {
                "姓名": id_info.get('姓名', '未知'),
                "性别": id_info.get('性别', '未知'),
                "民族": id_info.get('民族', '未知'),
                "出生日期": id_info.get('出生日期', '未知'),
                "住址": id_info.get('住址', '未知'),
                "公民身份号码": id_info.get('公民身份号码', '未知')
            }
        }
    except json.JSONDecodeError:
        result = {
            "file": str(image_file),
            "result": "无法解析的结果: " + response_content
        }

    return result, tokens_used


def delete_all_files():
    file_list = client.files.list()
    for file in file_list.data:
        client.files.delete(file_id=file.id)


def do_recognition():
    model_prices = {
        "moonshot-v1-8k": 12.0,
        "moonshot-v1-32k": 24.0,
        "moonshot-v1-128k": 60.0
    }
    model_price_per_million_tokens = model_prices[chosen_model]

    image_files = natsorted([Path(image_directory) / file_name for file_name in os.listdir(image_directory) if
                             file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))])

    total_start_time = time.time()
    total_cost = 0.0
    total_tokens = 0
    results = []

    for image_file in image_files:
        try:
            start_time = time.time()

            print(f"开始识别文件{image_file}......")

            file_object = client.files.create(file=image_file, purpose="file-extract")
            file_content = client.files.content(file_id=file_object.id).text

            result, tokens_used = process_id_card(image_file, file_content, chosen_model)

            if not result:
                continue

            end_time = time.time()
            recognition_time = end_time - start_time

            cost_per_image = calculate_cost(tokens_used, model_price_per_million_tokens)
            total_cost += cost_per_image
            total_tokens += tokens_used

            result["recognition_time"] = f"{recognition_time:.2f} 秒"
            result["cost"] = f"¥{cost_per_image:.6f}"
            result["tokens_used"] = tokens_used

            results.append(result)
            print(f"文件{image_file}识别完成，耗时{recognition_time:.2f}秒。")

        except Exception as e:
            error_result = {
                "file": str(image_file),
                "result": f"处理文件时出错: {e}"
            }
            results.append(error_result)
            continue

    total_end_time = time.time()
    total_time_message = f"文件全部处理完成，总处理时间: {total_end_time - total_start_time:.2f} 秒"
    print(total_time_message)

    results.append({"total_time": total_time_message, "total_cost": f"¥{total_cost:.6f}", "total_tokens": total_tokens})

    final_balance_info = get_balance(api_key)
    results.append({"balance_info": final_balance_info})

    with open(result_file_name, 'w', encoding='utf-8') as result_file:
        json.dump(results, result_file, ensure_ascii=False, indent=4)

    return results


if __name__ == "__main__":
    delete_all_files()
    do_recognition()
