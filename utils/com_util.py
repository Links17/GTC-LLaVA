import base64
import tempfile
import os


def base64_to_image(base64_data):
    # 将 Base64 编码的字符串解码为字节数据
    image_bytes = base64.b64decode(base64_data)

    # 创建临时文件
    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    temp_file.write(image_bytes)
    temp_file.close()

    # 返回临时文件的路径
    return temp_file.name


def image_to_base64(image_file):
    image_data = image_file.read()
    base64_data = base64.b64encode(image_data).decode("utf-8")
    return base64_data



def check_taking(taking):
    lowerString = taking.lower()
    if "yes" in lowerString:
        return 1
    else:
        return 0

def extract_digits(string):
    result = ""
    for char in string:
        if char.isdigit():
            result += char
    return result if result else "0"
