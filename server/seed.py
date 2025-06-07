from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Deck, Card

# Database setup
engine = create_engine('sqlite:///tarot.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_cards():
    db_session = SessionLocal()
    
    try:
        # Create a standard Rider-Waite deck
        deck = Deck(name="Rider-Waite Tarot Deck")
        db_session.add(deck)
        db_session.commit()

        # Major Arcana (22 cards)
        major_arcana_cards = [
            {"name": "The Fool", "suit": None, "major_arcana": True, "description": "New beginnings, innocence, spontaneity", "image": "card_images/the_fool.png"},
            {"name": "The Magician", "suit": None, "major_arcana": True, "description": "Manifestation, resourcefulness, power", "image": "card_images/the_magician.png"},
            {"name": "The High Priestess", "suit": None, "major_arcana": True, "description": "Intuition, sacred knowledge, divine feminine", "image": "card_images/the_high_priestess.png"},
            {"name": "The Empress", "suit": None, "major_arcana": True, "description": "Femininity, beauty, nature, abundance", "image": "card_images/the_empress.png"},
            {"name": "The Emperor", "suit": None, "major_arcana": True, "description": "Authority, structure, control, fatherhood", "image": "card_images/the_emperor.png"},
            {"name": "The Hierophant", "suit": None, "major_arcana": True, "description": "Spiritual wisdom, religious beliefs, conformity", "image": "card_images/the_hierophant.png"},
            {"name": "The Lovers", "suit": None, "major_arcana": True, "description": "Love, harmony, relationships, values alignment", "image": "card_images/the_lovers.png"},
            {"name": "The Chariot", "suit": None, "major_arcana": True, "description": "Control, willpower, success, determination", "image": "card_images/the_chariot.png"},
            {"name": "Strength", "suit": None, "major_arcana": True, "description": "Strength, courage, persuasion, influence", "image": "card_images/strength.png"},
            {"name": "The Hermit", "suit": None, "major_arcana": True, "description": "Soul searching, introspection, inner guidance", "image": "card_images/the_hermit.png"},
            {"name": "Wheel of Fortune", "suit": None, "major_arcana": True, "description": "Good luck, karma, life cycles, destiny", "image": "card_images/wheel_of_fortune.png"},
            {"name": "Justice", "suit": None, "major_arcana": True, "description": "Justice, fairness, truth, cause and effect", "image": "card_images/justice.png"},
            {"name": "The Hanged Man", "suit": None, "major_arcana": True, "description": "Suspension, restriction, letting go", "image": "card_images/the_hanged_man.png"},
            {"name": "Death", "suit": None, "major_arcana": True, "description": "Endings, change, transformation, transition", "image": "card_images/death.png"},
            {"name": "Temperance", "suit": None, "major_arcana": True, "description": "Balance, moderation, patience, purpose", "image": "card_images/temperance.png"},
            {"name": "The Devil", "suit": None, "major_arcana": True, "description": "Bondage, addiction, sexuality, materialism", "image": "card_images/the_devil.png"},
            {"name": "The Tower", "suit": None, "major_arcana": True, "description": "Sudden change, upheaval, chaos, revelation", "image": "card_images/the_tower.png"},
            {"name": "The Star", "suit": None, "major_arcana": True, "description": "Hope, faith, purpose, renewal, spirituality", "image": "card_images/the_star.png"},
            {"name": "The Moon", "suit": None, "major_arcana": True, "description": "Illusion, fear, anxiety, subconscious, intuition", "image": "card_images/the_moon.png"},
            {"name": "The Sun", "suit": None, "major_arcana": True, "description": "Optimism, fun, warmth, success, vitality", "image": "card_images/the_sun.png"},
            {"name": "Judgement", "suit": None, "major_arcana": True, "description": "Judgement, rebirth, inner calling, absolution", "image": "card_images/judgement.png"},
            {"name": "The World", "suit": None, "major_arcana": True, "description": "Completion, integration, accomplishment, travel", "image": "card_images/the_world.png"}
        ]

        # Minor Arcana - Cups (Hearts - Emotions, love, spirituality)
        cups_cards = [
            {"name": "Ace of Cups", "suit": "Cups", "major_arcana": False, "description": "Love, new relationships, compassion, creativity", "image": "card_images/ace_of_cups.png"},
            {"name": "Two of Cups", "suit": "Cups", "major_arcana": False, "description": "Unified love, partnership, mutual attraction", "image": "card_images/two_of_cups.png"},
            {"name": "Three of Cups", "suit": "Cups", "major_arcana": False, "description": "Celebration, friendship, creativity, community", "image": "card_images/three_of_cups.png"},
            {"name": "Four of Cups", "suit": "Cups", "major_arcana": False, "description": "Meditation, contemplation, apathy, reevaluation", "image": "card_images/four_of_cups.png"},
            {"name": "Five of Cups", "suit": "Cups", "major_arcana": False, "description": "Regret, failure, disappointment, pessimism", "image": "card_images/five_of_cups.png"},
            {"name": "Six of Cups", "suit": "Cups", "major_arcana": False, "description": "Revisiting the past, childhood memories, innocence", "image": "card_images/six_of_cups.png"},
            {"name": "Seven of Cups", "suit": "Cups", "major_arcana": False, "description": "Opportunities, choices, wishful thinking, illusion", "image": "card_images/seven_of_cups.png"},
            {"name": "Eight of Cups", "suit": "Cups", "major_arcana": False, "description": "Disappointment, abandonment, withdrawal, escapism", "image": "card_images/eight_of_cups.png"},
            {"name": "Nine of Cups", "suit": "Cups", "major_arcana": False, "description": "Contentment, satisfaction, gratitude, wish fulfillment", "image": "card_images/nine_of_cups.png"},
            {"name": "Ten of Cups", "suit": "Cups", "major_arcana": False, "description": "Divine love, blissful relationships, harmony, alignment", "image": "card_images/ten_of_cups.png"},
            {"name": "Page of Cups", "suit": "Cups", "major_arcana": False, "description": "Creative opportunities, intuitive messages, curiosity", "image": "card_images/page_of_cups.png"},
            {"name": "Knight of Cups", "suit": "Cups", "major_arcana": False, "description": "Creativity, romance, charm, imagination", "image": "card_images/knight_of_cups.png"},
            {"name": "Queen of Cups", "suit": "Cups", "major_arcana": False, "description": "Compassionate, calm, comfort, serene", "image": "card_images/queen_of_cups.png"},
            {"name": "King of Cups", "suit": "Cups", "major_arcana": False, "description": "Emotional balance, compassion, diplomacy", "image": "card_images/king_of_cups.png"}
        ]

        # Minor Arcana - Pentacles (Material world, money, career)
        pentacles_cards = [
            {"name": "Ace of Pentacles", "suit": "Pentacles", "major_arcana": False, "description": "Manifestation, financial opportunity, new job", "image": "card_images/ace_of_pentacles.png"},
            {"name": "Two of Pentacles", "suit": "Pentacles", "major_arcana": False, "description": "Multiple priorities, time management, prioritization", "image": "card_images/two_of_pentacles.png"},
            {"name": "Three of Pentacles", "suit": "Pentacles", "major_arcana": False, "description": "Collaboration, learning, implementation", "image": "card_images/three_of_pentacles.png"},
            {"name": "Four of Pentacles", "suit": "Pentacles", "major_arcana": False, "description": "Saving money, security, conservatism", "image": "card_images/four_of_pentacles.png"},
            {"name": "Five of Pentacles", "suit": "Pentacles", "major_arcana": False, "description": "Financial loss, poverty, lack mindset, isolation", "image": "card_images/five_of_pentacles.png"},
            {"name": "Six of Pentacles", "suit": "Pentacles", "major_arcana": False, "description": "Giving, receiving, sharing wealth, generosity", "image": "card_images/six_of_pentacles.png"},
            {"name": "Seven of Pentacles", "suit": "Pentacles", "major_arcana": False, "description": "Perseverance, investment, effort, reward", "image": "card_images/seven_of_pentacles.png"},
            {"name": "Eight of Pentacles", "suit": "Pentacles", "major_arcana": False, "description": "Apprenticeship, skill development, quality work", "image": "card_images/eight_of_pentacles.png"},
            {"name": "Nine of Pentacles", "suit": "Pentacles", "major_arcana": False, "description": "Abundance, luxury, self-reliance, financial independence", "image": "card_images/nine_of_pentacles.png"},
            {"name": "Ten of Pentacles", "suit": "Pentacles", "major_arcana": False, "description": "Wealth, financial security, family, long-term success", "image": "card_images/ten_of_pentacles.png"},
            {"name": "Page of Pentacles", "suit": "Pentacles", "major_arcana": False, "description": "Financial opportunity, skill development, manifestation", "image": "card_images/page_of_pentacles.png"},
            {"name": "Knight of Pentacles", "suit": "Pentacles", "major_arcana": False, "description": "Hard work, productivity, routine, conservatism", "image": "card_images/knight_of_pentacles.png"},
            {"name": "Queen of Pentacles", "suit": "Pentacles", "major_arcana": False, "description": "Nurturing, practical, providing, down-to-earth", "image": "card_images/queen_of_pentacles.png"},
            {"name": "King of Pentacles", "suit": "Pentacles", "major_arcana": False, "description": "Financial security, discipline, abundance", "image": "card_images/king_of_pentacles.png"}
        ]

        # Minor Arcana - Swords (Mind, communication, conflict)
        swords_cards = [
            {"name": "Ace of Swords", "suit": "Swords", "major_arcana": False, "description": "Breakthrough, clarity, sharp mind", "image": "card_images/ace_of_swords.png"},
            {"name": "Two of Swords", "suit": "Swords", "major_arcana": False, "description": "Difficult decisions, weighing options, indecision", "image": "card_images/two_of_swords.png"},
            {"name": "Three of Swords", "suit": "Swords", "major_arcana": False, "description": "Heartbreak, emotional pain, sorrow, grief", "image": "card_images/three_of_swords.png"},
            {"name": "Four of Swords", "suit": "Swords", "major_arcana": False, "description": "Rest, relaxation, meditation, contemplation", "image": "card_images/four_of_swords.png"},
            {"name": "Five of Swords", "suit": "Swords", "major_arcana": False, "description": "Conflict, disagreements, competition, defeat", "image": "card_images/five_of_swords.png"},
            {"name": "Six of Swords", "suit": "Swords", "major_arcana": False, "description": "Transition, change, rite of passage, moving on", "image": "card_images/six_of_swords.png"},
            {"name": "Seven of Swords", "suit": "Swords", "major_arcana": False, "description": "Betrayal, deception, getting away with something", "image": "card_images/seven_of_swords.png"},
            {"name": "Eight of Swords", "suit": "Swords", "major_arcana": False, "description": "Negative thoughts, self-imposed restriction, victim mentality", "image": "card_images/eight_of_swords.png"},
            {"name": "Nine of Swords", "suit": "Swords", "major_arcana": False, "description": "Anxiety, worry, fear, depression, nightmares", "image": "card_images/nine_of_swords.png"},
            {"name": "Ten of Swords", "suit": "Swords", "major_arcana": False, "description": "Painful endings, deep wounds, betrayal, crisis", "image": "card_images/ten_of_swords.png"},
            {"name": "Page of Swords", "suit": "Swords", "major_arcana": False, "description": "New ideas, curiosity, thirst for knowledge, new ways of communicating", "image": "card_images/page_of_swords.png"},
            {"name": "Knight of Swords", "suit": "Swords", "major_arcana": False, "description": "Ambitious, action-oriented, driven to succeed", "image": "card_images/knight_of_swords.png"},
            {"name": "Queen of Swords", "suit": "Swords", "major_arcana": False, "description": "Independent, unbiased judgement, clear boundaries", "image": "card_images/queen_of_swords.png"},
            {"name": "King of Swords", "suit": "Swords", "major_arcana": False, "description": "Mental clarity, intellectual power, authority, truth", "image": "card_images/king_of_swords.png"}
        ]

        # Minor Arcana - Wands (Fire, passion, creativity, energy)
        wands_cards = [
            {"name": "Ace of Wands", "suit": "Wands", "major_arcana": False, "description": "Inspiration, new opportunities, growth", "image": "card_images/ace_of_wands.png"},
            {"name": "Two of Wands", "suit": "Wands", "major_arcana": False, "description": "Future planning, making decisions, leaving comfort zone", "image": "card_images/two_of_wands.png"},
            {"name": "Three of Wands", "suit": "Wands", "major_arcana": False, "description": "Expansion, foresight, overseas opportunities", "image": "card_images/three_of_wands.png"},
            {"name": "Four of Wands", "suit": "Wands", "major_arcana": False, "description": "Celebration, joy, harmony, relaxation, homecoming", "image": "card_images/four_of_wands.png"},
            {"name": "Five of Wands", "suit": "Wands", "major_arcana": False, "description": "Conflict, competition, tension, diversity", "image": "card_images/five_of_wands.png"},
            {"name": "Six of Wands", "suit": "Wands", "major_arcana": False, "description": "Success, public recognition, progress, self-confidence", "image": "card_images/six_of_wands.png"},
            {"name": "Seven of Wands", "suit": "Wands", "major_arcana": False, "description": "Challenge, competition, protection, perseverance", "image": "card_images/seven_of_wands.png"},
            {"name": "Eight of Wands", "suit": "Wands", "major_arcana": False, "description": "Speed, swift action, rapid results, movement", "image": "card_images/eight_of_wands.png"},
            {"name": "Nine of Wands", "suit": "Wands", "major_arcana": False, "description": "Courage, persistence, test of faith, boundaries", "image": "card_images/nine_of_wands.png"},
            {"name": "Ten of Wands", "suit": "Wands", "major_arcana": False, "description": "Burden, extra responsibility, hard work, completion", "image": "card_images/ten_of_wands.png"},
            {"name": "Page of Wands", "suit": "Wands", "major_arcana": False, "description": "Inspiration, ideas, discovery, limitless potential", "image": "card_images/page_of_wands.png"},
            {"name": "Knight of Wands", "suit": "Wands", "major_arcana": False, "description": "Energy, passion, inspired action, adventure, impulsiveness", "image": "card_images/knight_of_wands.png"},
            {"name": "Queen of Wands", "suit": "Wands", "major_arcana": False, "description": "Courage, confidence, independence, social butterfly", "image": "card_images/queen_of_wands.png"},
            {"name": "King of Wands", "suit": "Wands", "major_arcana": False, "description": "Natural-born leader, vision, entrepreneur, honour", "image": "card_images/king_of_wands.png"}
        ]

        # Combine all cards
        all_cards = major_arcana_cards + cups_cards + pentacles_cards + swords_cards + wands_cards

        # Add all cards to the deck
        for card_data in all_cards:
            card = Card(
                name=card_data["name"],
                suit=card_data["suit"],
                major_arcana=card_data["major_arcana"],
                description=card_data["description"],
                image=card_data["image"],
                deck_id=deck.id
            )
            db_session.add(card)

        db_session.commit()
        print(f"Successfully seeded {len(all_cards)} cards in the {deck.name}!")
        
    except Exception as e:
        print(f"Error seeding cards: {e}")
        db_session.rollback()
    finally:
        db_session.close()

if __name__ == "__main__":
    seed_cards()




