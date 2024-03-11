import json

import numpy as np
from flask import Flask, request

from ai_llm_v2 import predict
from utils.com_util import extract_digits, base64_to_image
import utils.audio_array as audio_array
import mqtt_client
import os


client = mqtt_client.connect_mqtt()

app = Flask(__name__)
mqtt_send_count = 0

@app.route("/gtc/scene_detection", methods=["POST"])
def scene_detection_v2():
    try:
        global mqtt_send_count
        data = request.json  # 获取JSON数据
        scene_id = data.get('sceneId')  # 获取"audio"字段的值
        image = data.get('image')  # 获取"audio"字段的值
        img_file_path = base64_to_image(image)

        prompt1 = "What's in this picture?"
        prompt2 = "Whether Grabbed something off the table and return '1' if they fall, otherwise '0'. You can only return '1' or '0'"
        if image is None or scene_id is None:
            return {
                "code": 10001,
                "msg": "parameter passing error",
                "data": {
                }
            }
        if scene_id == 3 and image is not None:
            # FIXME: 提示词修改,应该有更好的形式
            original = predict( prompt1, img_file_path, "")
            result = predict(prompt2, img_file_path, "result only '0' or '1'")
            result = extract_digits(result)
            code = 0
            data = {
                "sceneId": 3,
                "warnStatus": int(result),
                "taskList": [
                    {
                        "action": 0,
                        "hardware": 0,
                        "params": {
                            "text": "" if int(result) == 0 else "Warning! Abnormal behavior detected!"
                        }
                    }, {
                        "action": 0,
                        "hardware": 1,
                        "params": {
                            "audio": "" if int(result) == 0 else audio_array.THIEF
                        }
                    }
                ]
            }
            mqtt_data = {
                "img": image,
                "prompt1": prompt1,
                "result1": original,
                "prompt2": prompt2,
                # "result2": original,
                "warn": int(result),
                "count": mqtt_send_count
            }
            result = client.publish("llava-result", json.dumps(mqtt_data))
            mqtt_send_count += 1
            print(result)
            
            os.remove(img_file_path)
        else:
            code = 10004
            data = {
                "sceneId": 0,
                "warnStatus": 0,
                "taskList": [
                    {
                        "action": 0,
                        "hardware": 0,
                        "params": {
                            "text": "Sorry, Combo can't handle it right now."
                        }
                    }, {
                        "action": 0,
                        "hardware": 1,
                        "params": {
                            "audio": audio_array.SORRY
                        }
                    }
                ]
            }
        return {
            "code": code,
            "msg": "",
            "data": data
        }
    except Exception as err:
        print(err, flush=True)
        return {
            "code": 10000,
            "msg": "service error",
            "data": {
            }
        }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)
