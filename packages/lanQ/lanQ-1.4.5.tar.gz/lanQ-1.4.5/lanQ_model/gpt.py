import json

from lanQ_model.base_func.openai_api import OpenAI

gpt_client = None

def check_key(data: json):
    key_list = ['score', 'error', 'reason']
    for key in key_list:
        if key not in data:
            return False

    return True

def call_api(content: str):
    global gpt_client
    if gpt_client is None:
        gpt_client = OpenAI('gpt-4', key="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")

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
    response = gpt_client.generate([general_filter % content])
    # print(response)
    try:
        response = json.loads(response[0])
        if check_key(response) is False:
            raise Exception('miss key: score, error, reason')

        return response
    except Exception:
        return {
            'score': 0,
            'error': 'API_LOSS',
            'reason': '',
        }
