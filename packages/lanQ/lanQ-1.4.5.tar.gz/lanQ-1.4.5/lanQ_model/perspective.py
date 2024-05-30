import pprint
from googleapiclient import discovery

KEY_LOOP = 0
API_KEYS = [
    'AIzaSyCBmZuYLUpXjIvc0B73e6WG6dorXhzU7Kk',
    # 'AIzaSyCK9teFVz_GYSxrsVYnJX42-HFEYDPpeJE',
    # 'AIzaSyBFt3rQrj001AsIrFniz8lqynt2CkqpMMA',
    # 'AIzaSyC3kEyahFUw9hCgW3_M2ogz0B0TlBOoPeg',
    # 'AIzaSyCm4F0FjFU006fvrOSVemGaaZHBLvbVCI4',
    # 'AIzaSyCg1PLPvJxsshmS1AMRYpjGR7VJou2ZYGU',
    # 'AIzaSyBcsMnmKB3okX4tjli881pyexkqraqsZjU',
    # 'AIzaSyAXuiKRJ41XgTngmR9YTEKpbLRBChUu5Is',
    # 'AIzaSyCBeRUdEmY4jK3DtR16P1ECA3Y4r5s0PN8',
    # 'AIzaSyC_wKcLvXWptGbsQqnU-xxm04i_fAbRrnA',
]

CLIENT_LIST = []

def call_api(content):
    if CLIENT_LIST == []:
        for api_key in API_KEYS:
            client = discovery.build(
                "commentanalyzer",
                "v1alpha1",
                developerKey=api_key,
                discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
                static_discovery=False,
            )
            CLIENT_LIST.append(client)

    global KEY_LOOP
    client = CLIENT_LIST[0]
    KEY_LOOP = (KEY_LOOP + 1) % 10

    analyze_request = {
        'comment': {'text': content},
        'requestedAttributes': {
            'TOXICITY': {},
            'SEVERE_TOXICITY': {},
            'IDENTITY_ATTACK': {},
            'INSULT': {},
            'PROFANITY': {},
            'THREAT': {},
            # 'SEXUALLY_EXPLICIT': {},
            # 'FLIRTATION': {},
        }
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        # print(type(response))
        # pprint.pprint(response)
        result = {'score':10, 'error':'', 'reason':[]}
        for e in response['attributeScores']:
            value = response['attributeScores'][e]['summaryScore']['value']
            if value > 0.6:
                result['score'] = 0
                result['error'] = 'ERROR_PERSPECTIVE'
                result['reason'].append(e)
        return result
    except Exception:
        return {
            'score': 0,
            'error': 'API_LOSS',
            'reason': '',
        }
