from flask import Blueprint, request, jsonify, current_app
from app.database import insert_masked_text_to_db
import logging
from datetime import datetime
from app.maskText import maskText

main_bp = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

def token_required(f):
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token or token != current_app.config['ACCESS_TOKEN']:
            logger.warning(f"Unauthorized access attempt with token: {token}")
            return jsonify({'message': 'Token is missing or invalid'}), 401

        client_ip = request.remote_addr
        # if client_ip not in current_app.config['ALLOWED_IPS']:
        #     logger.warning(f"Access blocked for IP: {client_ip}")
        #     return jsonify({'message': 'Access denied for this IP address'}), 403

        logger.info(f"Authorized access with token: {token} from IP: {client_ip}")
        return f(*args, **kwargs)
    return decorated

@main_bp.route('/domask', methods=['POST'])
@token_required
def submit():
    data = request.get_json()
    if not data or 'text' not in data or 'date' not in data:
        logger.warning('Invalid request:　Incorrect JSON value')
        return jsonify({'message': 'Invalid request:　Incorrect JSON value'}), 400
    elif data['text'] is None or data['date'] is None:
        logger.warning('Invalid request:　Incorrect JSON value')
        return jsonify({'message': 'Invalid request'}), 400
    id = data.get('id')
    if id is not None:
        id = int(id)
    else:
        id = None
    text = data['text']
    recive_date = data['date']
    # 現在の日時を取得
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:00:00')
    masked_text = maskText.get_mask_text(text)
    insert_tuple_data = [(id, str(masked_text), str(formatted_datetime), str(formatted_datetime), str(recive_date))]
    try:
        logger.info(f"Insert text: {insert_tuple_data}")
        insert_masked_text_to_db(insert_tuple_data)
        return jsonify({'message': 'Text submitted successfully'}), 201
    except Exception as e:
        logger.error(f"Error inserting data: {e}")
        return jsonify({'message': 'Failed to add text' }), 500
    
@main_bp.route('/test', methods=['POST'])
@token_required
def submit():
    data = request.get_json()
    if not data or 'text' not in data or 'date' not in data:
        logger.warning('Invalid request:　Incorrect JSON value')
        return jsonify({'message': 'Invalid request:　Incorrect JSON value'}), 400
    elif data['text'] is None or data['date'] is None:
        logger.warning('Invalid request:　Incorrect JSON value')
        return jsonify({'message': 'Invalid request'}), 400
    id = data.get('id')
    if id is not None:
        id = int(id)
    else:
        id = None
    text = data['text']
    recive_date = data['date']
    # 現在の日時を取得
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:00:00')
    masked_text = maskText.get_mask_text(text)
    insert_tuple_data = [(id, str(masked_text), str(formatted_datetime), str(formatted_datetime), str(recive_date))]
    logger.info(f"データベースへ登録するタプルデータ: {insert_tuple_data}")
    try:
        logger.info(f"Insert text: {insert_tuple_data}")
        # insert_masked_text_to_db(insert_tuple_data)
        return jsonify({'message': 'Text submitted successfully'}), 201
    except Exception as e:
        logger.error(f"Error inserting data: {e}")
        return jsonify({'message': 'Failed to add text' }), 500
