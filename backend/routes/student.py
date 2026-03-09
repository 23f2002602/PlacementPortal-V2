from flask import Blueprint, jsonify

student_bp = Blueprint('student', __name__)

@student_bp.route('/test')
def student_test():
    return jsonify({"message": "Student route working"})