from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import logging
import uuid
from datetime import datetime
from sandbox_worker import SandboxWorker

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'submissions'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize sandbox worker
sandbox_worker = SandboxWorker()

# In-memory storage for submissions (in production, use a database)
submissions = {}

@app.route('/')
def index():
    """Serve the main page"""
    return jsonify({
        'message': 'CodeShield Backend API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health',
            'submit': '/api/submit'
        }
    })

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'CodeShield Backend'
    })

@app.route('/api/submit', methods=['POST'])
def submit_code():
    """Handle code submission"""
    try:
        data = request.get_json()

        if not data or 'code' not in data:
            return jsonify({'error': 'No code provided'}), 400

        code = data['code']
        language = data.get('language', 'python')
        stdin = data.get('stdin', '')

        # Generate unique submission ID
        submission_id = str(uuid.uuid4())

        # Log the submission
        logger.info(f"Code submission received - ID: {submission_id}, Language: {language}, Length: {len(code)}")

        # Execute code in sandbox
        result = sandbox_worker.execute_code(code, language, stdin)

        # Store result
        submissions[submission_id] = {
            'id': submission_id,
            'code': code,
            'language': language,
            'stdin': stdin,
            'result': result,
            'timestamp': datetime.now().isoformat(),
            'status': 'completed'
        }

        return jsonify({
            'submission_id': submission_id,
            'status': 'completed',
            'result': result,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Error processing submission: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/status/<submission_id>', methods=['GET'])
def get_submission_status(submission_id):
    """Get submission status and results"""
    if submission_id not in submissions:
        return jsonify({'error': 'Submission not found'}), 404
    
    submission = submissions[submission_id]
    return jsonify({
        'submission_id': submission_id,
        'status': submission['status'],
        'result': submission['result'],
        'timestamp': submission['timestamp']
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
