from flask import Flask
from flask import render_template
from datetime import time
from backend import search

app = Flask(__name__)


@app.route("/<query>")
def chart(query):
    res = search(query)
    titles = []
    pos = []
    neu = []
    neg = []
    for k, v in res.items():
        titles.append(k)
        pos.append(v['pos'])
        neg.append(v['neg'])
        neu.append(v['neu'])
    return render_template('chart.html', query=query, titles=titles, pos=pos, neg=neg, neu=neu)

if __name__ == "__main__":
    app.run(debug=True)
