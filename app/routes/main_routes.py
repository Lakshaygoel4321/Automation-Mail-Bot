"""
Main Application Routes
Handles HTML page rendering
"""
from flask import Blueprint, render_template, jsonify

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Render main application page"""
    return render_template('index.html')


@main_bp.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy', 
        'message': 'AI Email Generator is running'
    }), 200


@main_bp.route('/api-info')
def api_info():
    """API information endpoint"""
    return jsonify({
        'message': 'AI Email Generator API',
        'status': 'running',
        'endpoints': {
            'generate': 'POST /api/generate',
            'feedback': 'POST /api/feedback',
            'finalize': 'POST /api/finalize',
            'send_email': 'POST /api/send-email',
            'get_session': 'GET /api/session/<session_id>'
        }
    })
