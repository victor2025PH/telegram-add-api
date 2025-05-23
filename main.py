import os
import json
import base64
from flask import Flask, request, jsonify
import gspread

# 解码 base64 到 json
sa_json = base64.b64decode(os.environ["SERVICE_ACCOUNT_JSON"]).decode("utf-8")
gc = gspread.service_account_from_dict(json.loads(sa_json))
sheet = gc.open_by_key('1U8nBZz7j91G3Ek1kONWp4zPmUNuQpxPQmPktyw1WvbA').sheet1

app = Flask(__name__)

@app.route('/get_id', methods=['GET'])
def get_id():
    rows = sheet.get_all_values()
    for idx, row in enumerate(rows[1:], start=2):
        if len(row) < 2 or not row[1]:
            return jsonify({"row": idx, "id": row[0]})
    return jsonify({"row": None, "id": None})

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.json
    row = int(data['row'])
    status = data['status']
    sheet.update_cell(row, 2, status)
    return jsonify({"result": "ok"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7860)
