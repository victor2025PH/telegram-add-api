import os, json
from flask import Flask, request, jsonify
import gspread

gc = gspread.service_account_from_dict(json.loads(os.environ["SERVICE_ACCOUNT_JSON"]))
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
