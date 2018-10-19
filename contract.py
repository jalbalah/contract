

import sys
import json
import requests
from flask import Flask, request
app = Flask(__name__)

def main(argv):
    if not argv:
        for i in range(0, 1):
            print(POST({'data': 1.0}))
    elif argv[0].lower().strip() == 'run':
        app.run(port=1337)


@app.route('/', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        return str(request.json)
    elif request.method == 'GET':
        with open('contract.json') as rf:
            explain_str = 'Send a POST request with the following schema:<br/>{}<br/>'
            return explain_str.format(rf.read())


def validate(json_args):

    def get_keys(js, x):
        if isinstance(js, dict):
            for k in sorted(js.keys()):
                if k:
                    x = [x] + [k]
                    get_keys(js[k], k)
        return x

    def get_values(node):
        return [x for x in r_get_values(node)]

    def r_get_values(node):
        if isinstance(node, dict):
            for item in sorted(node.values(), key=lambda x: hash(str(x))):
                yield from r_get_values(item)
        elif any(isinstance(node, x) for x in (list, tuple)):
            for item in node:
                yield from r_get_values(item)
        else:
            yield node

    try:
        with open('contract.json') as rf:
            json_real = json.loads(rf.read().replace("'", '"'))
        l_real = get_keys(json_args, [])
        l_args = get_keys(json_real, [])
        if l_real != l_args:
            raise Exception('{} != {}'.format(l_real, l_args))
        t_real = [type(x) for x in get_values(json_real)]
        t_args = [type(x) for x in get_values(json_args)]
        if t_real != t_args:
            raise Exception('{} != {}'.format(t_real, t_args))
        return json_args
    except Exception as e:
        print(e)
        return json_args


def POST(json_data):
    validate(json_data)
    URL = 'http://localhost:1337'
    return requests.post(URL, json=json_data).text


if __name__ == '__main__':
    main(sys.argv[1::])