import json
from pydantic import BaseModel

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class Item(BaseModel):
    content: str

model_path = "/mnt/140/llama3/Meta-Llama-3-8B-Instruct"

model = None
tokenizer = None

def generate_words(item: Item):
    global model,tokenizer
    if model is None and tokenizer is None:
        # 加载模型
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )

        # 加载分词器
        tokenizer = AutoTokenizer.from_pretrained(model_path)

    messages = [
        {"role": "system", "content": item.content},
    ]

    input_ids = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(model.device)

    terminators = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    outputs = model.generate(
        input_ids,
        max_new_tokens=256,
        eos_token_id=terminators,
        do_sample=True,
        temperature=0.6,
        top_p=0.9,
    )
    response = outputs[0][input_ids.shape[-1]:]
    # print(tokenizer.decode(response, skip_special_tokens=True))
    return json.loads(tokenizer.decode(response, skip_special_tokens=True))

def check_key(data: json):
    key_list = ['score', 'error', 'reason']
    for key in key_list:
        if key not in data:
            return False

    return True

def call_api(content: str):
    general_filter = """
        请从内容的流畅性、完整性、重复程度，为下面的句子打分，分数从低到高表示句子的质量从低到高，值为一个0-10之间的整数，并给出原因。请提供一个JSON格式的回复，包含指定的键和值。
        要求：
        - 返回的内容必须是JSON格式，不要有多余的内容。
        - 返回的第一个键是score，值是0-10之间的整数。
        - 返回的第二个键是error，值是内容不流畅、内容不完整、内容重复中的一个，如果句子没有问题这个值为空。
        - 返回的第三个键是reason，值是打分的原因。
        - 如果句子是空的请打0分。


        %s

        """
    try:
        item = Item(content=general_filter % content)
        response = generate_words(item)
        if check_key(response) is False:
            raise Exception('miss key: score, error, reason')

        return response
    except Exception:
        return {
            'score': 0,
            'error': 'MODEL_LOSS',
            'reason': '',
        }

# if __name__ == '__main__':
#     res = call_api('�I am 8 years old. I love apple because:')
#     print(res)