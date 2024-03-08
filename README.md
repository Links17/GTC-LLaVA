# GTC-LLaVA

GTC Demo

## 说明

使用local_llm+llava形式,传输图片解析,返回tasklist 给设备,并且推送MQTT消息(topic:“llava-result”)
```bash
├── Dockerfile
├── README.md
├── ai_llm_v2.py
├── main.py
├── mqtt_client.py
└── utils
    ├── audio_array.py
    └── com_util.py
```

## 使用方法

1. 修改mqtt url,port 改为node-red mqtt-broker
2. 构建docker 镜像

```bash
docker build -f Dockerfile . -t hi_combo
```

3. 启动

```bash
docker run -d --runtime nvidia  --network host  -v /etc/enctune.conf:/etc/enctune.conf   -v /etc/nv_tegra_release:/etc/nv_tegra_release  -v /mnt/ssd/workspace/jetson-containers/data:/data  --name hi_combo  --device /dev/snd --device /dev/bus/usb hi_combo:latest
```
4. 测试
```bash
curl --location 'http://127.0.0.1:8888/ai/scene_detection' \
--header 'Content-Type: application/json' \
--data '{
    "sceneId":1,
    "image":"base64 image"
    }'
```