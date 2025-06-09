import os
import openai
from dotenv import load_dotenv
import json
from typing import List, Dict

# Load environment variables
load_dotenv()

# Initialize OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY environment variable is required")

def get_tarot_reading(cards: List[Dict], spread_type: str = "general", question: str = ""):
    """
    Generate a tarot reading using OpenAI based on the drawn cards
    
    Args:
        cards: List of card dictionaries with name, suit, description, etc.
        spread_type: Type of spread (e.g., "three_card", "celtic_cross", "general")
        question: Optional question from the user
    
    Returns:
        Dict with the reading interpretation
    """
    
    # Format cards for the prompt
    card_descriptions = []
    for i, card in enumerate(cards, 1):
        position = f"Position {i}"
        card_info = f"{position}: {card['name']}"
        if card.get('suit'):
            card_info += f" of {card['suit']}"
        card_info += f" - {card['description']}"
        card_descriptions.append(card_info)
    
    cards_text = "\n".join(card_descriptions)
    
    # Define position meanings for different spreads
    position_meanings = {
        "three-card-spread": ["Past/Situation", "Present/Action", "Future/Outcome"],
        "celtic-cross": [
            "Present Situation", "Challenge/Cross", "Distant Past/Foundation", 
            "Possible Future", "Conscious Thoughts", "Unconscious Influences",
            "Your Approach", "External Influences", "Hopes and Fears", "Final Outcome"
        ],
        "chakra-spread": [
            "Crown Chakra (Spirituality)", "Third Eye (Intuition)", "Throat Chakra (Communication)",
            "Heart Chakra (Love)", "Solar Plexus (Power)", 
            "Sacral Chakra (Creativity)", "Root Chakra (Security)"
        ],
        "single-card": ["Core Message"]
    }
    
    # Create the prompt
    system_prompt = """You are a professional tarot reader with deep knowledge of tarot symbolism and interpretation. 
    Provide insightful, thoughtful readings that help people gain perspective on their situations. 
    Be encouraging while being honest about challenges. Focus on personal growth and empowerment.
    
    IMPORTANT: Always mention the specific cards by name in your interpretations. Reference how each card relates to its position meaning and connects to other cards in the spread.
    
    Format your response as a JSON object with the following structure:
    {
        "overall_message": "A general interpretation mentioning specific cards by name",
        "advice": "Practical advice referencing the specific cards drawn",
        "theme": "The main theme or energy of the reading"
    }"""
    
    # Add position context to the prompt
    spread_positions = position_meanings.get(spread_type, [f"Position {i+1}" for i in range(len(cards))])
    
    user_prompt = f"""Please provide a tarot reading for the following cards:

{cards_text}

Spread Type: {spread_type}
Position Meanings: {', '.join(spread_positions)}
"""
    
    if question:
        user_prompt += f"User's Question: {question}\n"
        user_prompt += """
IMPORTANT INSTRUCTIONS:
- This reading must specifically answer the user's question above
- Interpret each card in relation to their question
- Mention each card by name (e.g., "The Three of Cups", "Death", "King of Wands") in your interpretation
- Explain what each card means in its specific position and how it relates to their question
- Describe how the cards relate to each other to answer their question
- Reference specific cards when giving advice (e.g., "The Hermit suggests you need time for reflection regarding your question")
- Make the reading feel personal and specific to both their question and these exact cards drawn
- Focus the entire reading on providing insight and guidance for their specific question

Please interpret these cards specifically to answer the user's question and provide guidance that directly addresses what they asked."""
    else:
        user_prompt += """
IMPORTANT INSTRUCTIONS:
- Mention each card by name (e.g., "The Three of Cups", "Death", "King of Wands") in your interpretation
- Explain what each card means in its specific position 
- Describe how the cards relate to each other and tell a story together
- Reference specific cards when giving advice (e.g., "The Hermit suggests you need time for reflection")
- Make the reading feel personal and specific to these exact cards drawn

Please interpret these cards in relation to each other and provide guidance that specifically references the cards by name."""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        
        # Parse the JSON response
        reading_text = response['choices'][0]['message']['content']
        
        try:
            reading_data = json.loads(reading_text)
            return {
                "success": True,
                "reading": reading_data
            }
        except json.JSONDecodeError:
            # If JSON parsing fails, return the raw text
            return {
                "success": True,
                "reading": {
                    "overall_message": reading_text,
                    "card_interpretations": [],
                    "advice": "",
                    "theme": "General Reading"
                }
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to generate reading: {str(e)}"
        }

def get_card_meaning(card_name: str, context: str = "general"):
    """
    Get a detailed explanation of a specific tarot card
    
    Args:
        card_name: Name of the tarot card
        context: Context for the interpretation (e.g., "love", "career", "general")
    
    Returns:
        Dict with card meaning and interpretation
    """
    
    system_prompt = """You are a tarot expert. Provide detailed, insightful explanations of tarot cards.
    Include traditional meanings, symbolism, and practical applications.
    
    Format your response as JSON:
    {
        "card_name": "Card Name",
        "upright_meaning": "Traditional upright meaning",
        "reversed_meaning": "Traditional reversed meaning",
        "symbolism": "Key symbols and their significance",
        "context_interpretation": "Interpretation in the given context",
        "keywords": ["keyword1", "keyword2", "keyword3"]
    }"""
    
    user_prompt = f"""Please provide a detailed explanation of the tarot card: {card_name}
    
Context: {context}

Include both traditional meanings and how this card might be interpreted in the context of {context}."""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=800,
            temperature=0.6
        )
        
        meaning_text = response['choices'][0]['message']['content']
        
        try:
            meaning_data = json.loads(meaning_text)
            return {
                "success": True,
                "meaning": meaning_data
            }
        except json.JSONDecodeError:
            return {
                "success": True,
                "meaning": {
                    "card_name": card_name,
                    "upright_meaning": meaning_text,
                    "reversed_meaning": "",
                    "symbolism": "",
                    "context_interpretation": meaning_text,
                    "keywords": []
                }
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get card meaning: {str(e)}"
        }

def get_daily_guidance(question: str = ""):
    """
    Get daily spiritual guidance or answer a specific question
    
    Args:
        question: Optional specific question
    
    Returns:
        Dict with guidance message
    """
    
    system_prompt = """You are a wise spiritual guide offering daily inspiration and guidance.
    Provide uplifting, practical wisdom that helps people navigate their day with intention and positivity.
    Be encouraging, insightful, and focus on personal empowerment and growth."""
    
    if question:
        user_prompt = f"Please provide guidance for this question: {question}"
    else:
        user_prompt = "Please provide general daily spiritual guidance and inspiration."
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=400,
            temperature=0.8
        )
        
        guidance = response['choices'][0]['message']['content']
        
        return {
            "success": True,
            "guidance": guidance
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get guidance: {str(e)}"
        }








