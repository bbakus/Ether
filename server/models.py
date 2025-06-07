from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Column, Boolean, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import date

# Association tables for different many-to-many relationships
deck_session_association = Table(
    'deck_sessions',
    Column('deck_id', Integer, ForeignKey('decks.id'), primary_key=True),
    Column('session_id', Integer, ForeignKey('sessions.id'), primary_key=True)
)

card_session_association = Table(
    'card_sessions', 
    Column('card_id', Integer, ForeignKey('cards.id'), primary_key=True),
    Column('session_id', Integer, ForeignKey('sessions.id'), primary_key=True)
)

spread_session_association = Table(
    'spread_sessions',
    Column('spread_id', Integer, ForeignKey('spreads.id'), primary_key=True), 
    Column('session_id', Integer, ForeignKey('sessions.id'), primary_key=True)
)

layout_cards_association = Table(
    'layout_cards',
    Column('spread_id', Integer, ForeignKey('spreads.id'), primary_key=True),
    Column('card_id', Integer, ForeignKey('cards.id'), primary_key=True)
)

class Deck(SerializerMixin):

    __tablename__ = 'decks'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # One-to-many: Deck has many cards
    cards = relationship('Card', back_populates='deck')
    # Many-to-many: Deck can be used in many sessions
    sessions = relationship('Session', secondary=deck_session_association, back_populates='decks')


class Card(SerializerMixin):

    __tablename__='cards'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    suit = Column(String)
    major_arcana = Column(Boolean, default=False)
    description = Column(String)
    image = Column(String)

    # Foreign key to deck (card belongs to one deck)
    deck_id = Column(Integer, ForeignKey('decks.id'))

    # Many-to-one: Card belongs to one deck
    deck = relationship('Deck', back_populates='cards')
    # Many-to-many: Card can appear in many sessions
    sessions = relationship('Session', secondary=card_session_association, back_populates='cards')
    spreads = relationship('Spread', secondary=layout_cards_association, back_populates='cards')


class Spread(SerializerMixin):

    __tablename__='spreads'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    layout = Column(String)

    # Many-to-many: Spread can be used in many sessions
    sessions = relationship('Session', secondary=spread_session_association, back_populates='spreads')
    cards = relationship('Card', secondary=layout_cards_association, back_populaes='spreads')


class Session(SerializerMixin):

    __tablename__='sessions'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Many-to-many relationships
    decks = relationship('Deck', secondary=deck_session_association, back_populates='sessions')
    cards = relationship('Card', secondary=card_session_association, back_populates='sessions') 
    spreads = relationship('Spread', secondary=spread_session_association, back_populates='sessions')


