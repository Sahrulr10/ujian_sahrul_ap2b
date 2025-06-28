import flask
from flask import Flask, jsonify, request
import time
import random

app = Flask(__name__)

mock_order_status = {
    "ORD-101": {"customer": "Budi", "status": "Baking", "estimated_delivery": "19:30"},
    "ORD-102": {"customer": "Ani", "status": "Out for Delivery", "estimated_delivery": "19:25"},
    "ORD-103": {"customer": "Cici", "status": "Preparing", "estimated_delivery": "19:45"},
    "ORD-104": {"customer": "Dedi", "status": "Delivered", "estimated_delivery": "19:10"},
    "ORD-105": {"customer": "Eka", "status": "Baking", "estimated_delivery": "19:50"},
}
valid_orders = list(mock_order_status.keys())

@app.route('/get_order_status', methods=['GET'])
def get_order_status():
    order_id_param = request.args.get('order_id')
    delay = random.uniform(0.3, 0.8)
    time.sleep(delay)
    if order_id_param:
        order_id = order_id_param.upper()
        if order_id in mock_order_status:
            data = mock_order_status[order_id]
            data["order_id"] = order_id
            print(f"[SERVER] Sending status for {order_id}: {data} (after {delay:.2f}s delay)")
            return jsonify(data)
        else:
            error_msg = {"error": "order_not_found", "message": f"Order ID '{order_id}' not found."}
            print(f"[SERVER] Order ID {order_id} not found (after {delay:.2f}s delay)")
            return jsonify(error_msg), 404
    else:
        error_msg = {"error": "bad_request", "message": "Parameter 'order_id' is required."}
        return jsonify(error_msg), 400

if __name__ == '__main__':
    print("Simple Pizza Order API Server running on http://127.0.0.1:5000")
    print("Endpoint: GET /get_order_status?order_id=ORD-101")
    app.run(debug=False, threaded=True, use_reloader=False)