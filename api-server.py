#!/usr/bin/env python3
"""
Simple in-memory polling API server
No database - stores answers in memory (lost on restart)
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# In-memory storage
answers = []

@app.route('/api/answers', methods=['POST'])
def submit_answer():
    """Submit a new answer"""
    data = request.json

    if not data or 'question_id' not in data or 'answer_text' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    answer = {
        'id': str(uuid.uuid4()),
        'question_id': int(data['question_id']),
        'answer_text': data['answer_text'],
        'created_at': datetime.utcnow().isoformat() + 'Z'
    }

    answers.append(answer)
    print(f"✅ New answer for Q{answer['question_id']}: {answer['answer_text'][:50]}...")

    return jsonify(answer), 201

@app.route('/api/answers', methods=['GET'])
def get_answers():
    """Get answers for a question"""
    question_id = request.args.get('question_id', type=int)
    limit = request.args.get('limit', 300, type=int)

    if question_id is None:
        filtered = answers
    else:
        filtered = [a for a in answers if a['question_id'] == question_id]

    # Sort by created_at descending
    filtered.sort(key=lambda x: x['created_at'], reverse=True)

    return jsonify(filtered[:limit])

@app.route('/api/answers/clear', methods=['POST'])
def clear_answers():
    """Clear all answers (for testing)"""
    global answers
    answers = []
    print("🗑️  All answers cleared")
    return jsonify({'message': 'All answers cleared'}), 200

@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'ok',
        'total_answers': len(answers)
    })

if __name__ == '__main__':
    print("🚀 Starting polling API server...")
    print("📝 Endpoints:")
    print("   POST   /api/answers          - Submit answer")
    print("   GET    /api/answers?question_id=1  - Get answers")
    print("   POST   /api/answers/clear    - Clear all answers")
    print("   GET    /api/health           - Health check")
    print()
    app.run(host='0.0.0.0', port=5000, debug=True)
