from flask import Flask, request, jsonify, render_template
import os
import logging
from datetime import datetime

app = Flask(__name__)

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

        # Log the submission
        logger.info(f"Code submission received - Language: {language}, Length: {len(code)}")

        # Here you would typically:
        # 1. Save the code to submissions folder
        # 2. Run it in a sandboxed environment
        # 3. Return results

        return jsonify({
            'message': 'Code submitted successfully',
            'language': language,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Error processing submission: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
