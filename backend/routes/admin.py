from flask import Blueprint, request, jsonify
from models import db, User, Company, Student, PlacementDrive, Application
from auth import role_required
import json

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/test')
def test_admin():
    return jsonify({"message": "Admin route working"})