from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Deck, Card, Spread, Session
from sqlalchemy_serializer import SerializerMixin

app = Flask(__name__)

# Database setup
engine = create_engine('sqlite:///tarot.db')  # or your PostgreSQL connection string
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.route('/')
def home():
    return {"message": "Tarot API is running!"}



@app.route('/decks')
def decks():
    decks = Deck.query.all
    return jsonify(decks)

@app.route('/cards')
def cards():
    cards = Card.query.all
    return jsonify(cards)

app.route('/<int:session_id>/spreads')
def spreads(session_id):
    spread = Spread.query(spread_id = session_id).first()
    return jsonify(spread)

@app.route('/<int:session_id>/spreads')
def new_spread(session_id):

    data = request.get_json()
    new_spread = Spread(name=data['name'])

    if data['id'] != session_id:
        return {'message': 'the fuck you doing here'}
    
    try:
        db_session = SessionLocal()
        db_session.add(new_spread)
        db_session.commit()

        return jsonify({
            'id': new_spread.id,
            'name': new_spread.name,
            'layout': new_spread.layout,
            'layout_cards': new_spread.cards
        }), 201

    except Exception as e:
        return jsonify({
            'error': 'your dick is too small'
        }), 400

    finally:
        db_session.close()    

@app.route('/sessions', methods=['POST'])
def create_session():
    try:
        data = request.get_json()

        new_session = Session(name=data['name'])
        if not new_session:
            return {"Error": 'This session is empty'}, 402
        db_session = SessionLocal()
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



@app.route('/session/<int:session_id>')
def sessions(session_id):
    session = Session.query(session_id = session_id).first()
    return jsonify(session)


if __name__ == '__main__':
    app.run(debug=True)

