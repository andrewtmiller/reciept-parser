from flask import Blueprint, request, jsonify
from .categorizer import categorize_receipt

receipts_bp = Blueprint("receipts", __name__)

@receipts_bp.route("/parse", methods=["POST"])
def parse_receipt():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    html_content = file.read().decode("utf-8")

    try:
        parsed_items = categorize_receipt(html_content)
        print(parsed_items)
        return jsonify(parsed_items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
