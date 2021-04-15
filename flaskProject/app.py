from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
import requests

app = Flask(__name__)
es = Elasticsearch()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if 'BM25' in request.form:
            index_model = "est_bm25"
        elif 'DFR' in request.form:
            index_model = "est_dfr"
        elif 'IB' in request.form:
            index_model = "est_ib"
        else:
            index_model = "est_bm25"
        q = request.form.get("q")
        if q is not None:
            if es.ping():
                resp = es.search(index=index_model, doc_type="books", body={"query": {"multi_match": {"query": q}}})
                return render_template('index.html', q=q, response=resp, model=index_model)
            else:
                url = 'https://hooks.slack.com/services/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'
                payload = "{\"channel\": \"#ir-search-engine\", \"username\": \"webhookbot\", \"text\": \":rotating_light: Elasticsearch down :rotating_light:\", \"icon_emoji\": \":ghost:\"}"
                headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
                requests.post(url, data=payload, headers=headers)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
