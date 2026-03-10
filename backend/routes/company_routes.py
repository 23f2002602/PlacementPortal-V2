from flask import Blueprint, jsonify

company_bp = Blueprint('company', __name__)

@company_bp.route('/test')
def company_test():
    return jsonify({"message": "Company route working"})