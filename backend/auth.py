import jwt
from flask import request, jsonify, current_app
from functools import wraps

def create_token(user_id, role):
    payload = {
        'user_id': user_id,
        'role': role
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        # Get token from  "Authorization: Bearer <token>"
        auth_header = request.headers.get('Authorization', '')
        token = auth_header.replace('Bearer ', '').strip()

        if not token:
            return jsonify({'error': 'Token missing. Please login.'}), 401

        try:
            # Decode the token → get user_id and role back
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            # Attach to request so route functions can read them
            request.user_id = data['user_id']
            request.role    = data['role']
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid or expired token.'}), 401

        return f(*args, **kwargs)
    return decorated

def require_auth(*roles):
    def decorator(f):
        @wraps(f)
        @token_required  # always verify token first
        def wrapped(*args, **kwargs):
            if request.role not in roles:
                return jsonify({'error': 'Access denied. Wrong role.'}), 403
            
            from models.models import User
            user = User.query.get(request.user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404
                
            return f(user, *args, **kwargs)
        return wrapped
    return decorator