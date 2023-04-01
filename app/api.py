import json
from flask import Flask, request
import html_parser

app = Flask(__name__)


@app.route('/post/item', methods=['POST'])
def get_url():
    data = requests.get_json()
    url = data['url']
    token = data['token']
    return json.dumps(data)

app.listen
if __name__ == '__main__':
    app.run()

