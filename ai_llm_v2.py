import os

from local_llm import LocalLM, ChatHistory
from local_llm.utils import ArgParser

# see utils/args.py for options
parser = ArgParser()
args = parser.parse_args()

# 加载模型（首次运行加载就行）
model = LocalLM.from_pretrained(
    "liuhaotian/llava-v1.5-13b",
    quant=args.quant,
    api="mlc",
    vision_model=args.vision_model,
)

JSON_TEMPLATE_0 = """Answer the question based only on the input question, except the answer content as json, parameters:(question, description , result), 'result:0' means No,'result:1' means Yes, Do not anwser other content, just json data,
example:
    { 
        "question": "input question",
        "result": 0 or 1,
        "description": "the compelte anwser content"
    }
"""


# 推理（每次请求去调用，图片应该要先存到本地，暂时不知道怎么按其他格式处理）
def predict(user_text, image_path, system_prompt):
    chat_history = ChatHistory(model, chat_template=None, system_prompt=system_prompt)
    # add image to the chat history
    entry = chat_history.append(role="user", msg=image_path)
    # add the latest user prompt to the chat history
    entry = chat_history.append(role="user", msg=user_text)
    # images should be followed by text prompts
    if "image" in entry and "text" not in entry:
        return "only image message, waiting for user prompt"
    # get the latest embeddings from the chat
    embedding, position = chat_history.embed_chat()
    # generate bot reply
    reply = model.generate(
        embedding,
        streaming=False,
        max_new_tokens=args.max_new_tokens,
        min_new_tokens=args.min_new_tokens,
        do_sample=args.do_sample,
        repetition_penalty=args.repetition_penalty,
        temperature=args.temperature,
        top_p=args.top_p,
    )
    os.remove(image_path)
    return str(reply)
