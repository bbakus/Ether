from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Deck, Card, Spread, Session
from openAI import get_tarot_reading, get_card_meaning, get_daily_guidance
import random
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database setup
engine = create_engine('sqlite:///tarot.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Serve static files (card images)
@app.route('/card_images/<filename>')
def serve_card_image(filename):
    return send_from_directory('card_images', filename)

@app.route('/')
def home():
    return {"message": "Tarot API is running!"}

@app.route('/decks')
def decks():
    db_session = SessionLocal()
    try:
        decks = db_session.query(Deck).all()
        return jsonify([{
            'id': deck.id,
            'name': deck.name,
            'card_count': len(deck.cards)
        } for deck in decks])
    finally:
        db_session.close()

@app.route('/cards')
def cards():
    db_session = SessionLocal()
    try:
        cards = db_session.query(Card).all()
        return jsonify([{
            'id': card.id,
            'name': card.name,
            'suit': card.suit,
            'major_arcana': card.major_arcana,
            'description': card.description,
            'image': card.image
        } for card in cards])
    finally:
        db_session.close()

@app.route('/cards/random/<int:count>')
def random_cards(count):
    """Draw random cards from the deck"""
    if count < 1 or count > 10:
        return jsonify({'error': 'Count must be between 1 and 10'}), 400
    
    db_session = SessionLocal()
    try:
        all_cards = db_session.query(Card).all()
        if len(all_cards) < count:
            return jsonify({'error': 'Not enough cards in deck'}), 400
        
        selected_cards = random.sample(all_cards, count)
        return jsonify([{
            'id': card.id,
            'name': card.name,
            'suit': card.suit,
            'major_arcana': card.major_arcana,
            'description': card.description,
            'image': card.image
        } for card in selected_cards])
    finally:
        db_session.close()

@app.route('/reading', methods=['POST'])
def create_reading():
    """Generate an AI-powered tarot reading"""
    data = request.get_json()
    
    if not data or 'cards' not in data:
        return jsonify({'error': 'Cards are required'}), 400
    
    cards = data['cards']
    spread_type = data.get('spread_type', 'general')
    question = data.get('question', '')
    
    # Generate the reading using OpenAI
    reading_result = get_tarot_reading(cards, spread_type, question)
    
    if not reading_result['success']:
        return jsonify({'error': reading_result['error']}), 500
    
    return jsonify({
        'cards': cards,
        'spread_type': spread_type,
        'question': question,
        'reading': reading_result['reading']
    })

@app.route('/card/<card_name>/meaning')
def card_meaning(card_name):
    """Get detailed meaning of a specific card"""
    context = request.args.get('context', 'general')
    
    meaning_result = get_card_meaning(card_name, context)
    
    if not meaning_result['success']:
        return jsonify({'error': meaning_result['error']}), 500
    
    return jsonify(meaning_result['meaning'])

@app.route('/guidance', methods=['GET', 'POST'])
def daily_guidance():
    """Get daily spiritual guidance"""
    question = ""
    
    if request.method == 'POST':
        data = request.get_json()
        question = data.get('question', '') if data else ''
    else:
        question = request.args.get('question', '')
    
    guidance_result = get_daily_guidance(question)
    
    if not guidance_result['success']:
        return jsonify({'error': guidance_result['error']}), 500
    
    return jsonify({
        'question': question if question else 'Daily guidance',
        'guidance': guidance_result['guidance']
    })

@app.route('/session/<int:session_id>/spreads', methods=['GET'])
def spreads(session_id):
    db_session = SessionLocal()
    try:
        spreads = db_session.query(Spread).filter(Spread.session_id == session_id).all()
        return jsonify([{
            'id': spread.id,
            'name': spread.name,
            'layout': spread.layout,
            'cards': spread.cards
        } for spread in spreads])
    finally:
        db_session.close()

@app.route('/session/<int:session_id>/spreads', methods=['POST'])
def new_spread(session_id):
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Spread name is required'}), 400
    
    try:
        db_session = SessionLocal()
        new_spread = Spread(
            name=data['name'],
            session_id=session_id,
            layout=data.get('layout', ''),
            cards=data.get('cards', [])
        )
        
        db_session.add(new_spread)
        db_session.commit()

        return jsonify({
            'id': new_spread.id,
            'name': new_spread.name,
            'layout': new_spread.layout,
            'cards': new_spread.cards,
            'session_id': new_spread.session_id
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        db_session.close()

@app.route('/sessions', methods=['POST'])
def create_session():
    try:
        data = request.get_json()
        
        if not data or 'name' not in data:
            return jsonify({'error': 'Session name is required'}), 400

        db_session = SessionLocal()
        new_session = Session(name=data['name'])
        db_session.add(new_session)
        db_session.commit()

        return jsonify({
            'id': new_session.id,
            'name': new_session.name,
            'message': 'Session started!'
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        db_session.close()

@app.route('/sessions')
def get_sessions():
    db_session = SessionLocal()
    try:
        sessions = db_session.query(Session).all()
        return jsonify([{
            'id': session.id,
            'name': session.name,
            'created_at': session.created_at.isoformat() if hasattr(session, 'created_at') else None
        } for session in sessions])
    finally:
        db_session.close()

@app.route('/session/<int:session_id>')
def get_session(session_id):
    db_session = SessionLocal()
    try:
        session = db_session.query(Session).filter(Session.id == session_id).first()
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        return jsonify({
            'id': session.id,
            'name': session.name,
            'created_at': session.created_at.isoformat() if hasattr(session, 'created_at') else None
        })
    finally:
        db_session.close()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)

