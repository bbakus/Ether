from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Column, Boolean, Integer, String, Float, ForeignKey, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import date

# Create the base class
Base = declarative_base()

# Association tables for different many-to-many relationships
deck_session_association = Table(
    'deck_sessions', Base.metadata,
    Column('deck_id', Integer, ForeignKey('decks.id'), primary_key=True),
    Column('session_id', Integer, ForeignKey('sessions.id'), primary_key=True)
)

card_session_association = Table(
    'card_sessions', Base.metadata,
    Column('card_id', Integer, ForeignKey('cards.id'), primary_key=True),
    Column('session_id', Integer, ForeignKey('sessions.id'), primary_key=True)
)

spread_session_association = Table(
    'spread_sessions', Base.metadata,
    Column('spread_id', Integer, ForeignKey('spreads.id'), primary_key=True), 
    Column('session_id', Integer, ForeignKey('sessions.id'), primary_key=True)
)

layout_cards_association = Table(
    'layout_cards', Base.metadata,
    Column('spread_id', Integer, ForeignKey('spreads.id'), primary_key=True),
    Column('card_id', Integer, ForeignKey('cards.id'), primary_key=True)
)

class Deck(Base, SerializerMixin):

    __tablename__ = 'decks'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # One-to-many: Deck has many cards
    cards = relationship('Card', back_populates='deck')
    # Many-to-many: Deck can be used in many sessions
    sessions = relationship('Session', secondary=deck_session_association, back_populates='decks')


class Card(Base, SerializerMixin):

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


class Spread(Base, SerializerMixin):

    __tablename__='spreads'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    layout = Column(String)
    session_id = Column(Integer, ForeignKey('sessions.id'))

    # Many-to-many: Spread can be used in many sessions
    sessions = relationship('Session', secondary=spread_session_association, back_populates='spreads')
    cards = relationship('Card', secondary=layout_cards_association, back_populates='spreads')


class Session(Base, SerializerMixin):

    __tablename__='sessions'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Many-to-many relationships
    decks = relationship('Deck', secondary=deck_session_association, back_populates='sessions')
    cards = relationship('Card', secondary=card_session_association, back_populates='sessions') 
    spreads = relationship('Spread', secondary=spread_session_association, back_populates='sessions')


