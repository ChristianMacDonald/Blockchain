import sys
import requests
from uuid import uuid4
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')
backend_node = 'http://localhost:5000'

@app.route('/', methods=['GET'])
def root():
    return jsonify('Hello, world!'), 200

@app.route('/wallet/<id>', methods=['GET'])
def wallet(id):
    wallet_total = 0
    r = requests.get(url=backend_node + '/chain')
    data = r.json()
    chain = data['chain']
    transactions_involving_id = []
    for block in chain:
        for transaction in block['transactions']:
            if transaction['recipient'] == id:
                transactions_involving_id.append(transaction)
                wallet_total += transaction['amount']
            elif transaction['sender'] == id:
                transactions_involving_id.append(transaction)
                wallet_total -= transaction['amount']
    return render_template('index.html', id=id, transactions=transactions_involving_id, total=wallet_total)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)