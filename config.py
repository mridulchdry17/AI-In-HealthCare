import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    HUGGINGFACE_API_KEY = "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"
    
    # Medical chat prompt template
    MEDICAL_CHAT_TEMPLATE = """Medical Question: {user_input}

Please provide:
1. Brief explanation of symptoms and causes
2. Recommended home care and treatment
3. Warning signs that require medical attention

Response:"""

    # Health recommendation template
    HEALTH_RECOMMENDATION_TEMPLATE = """Create health recommendations for:
AGE: {age}
HEIGHT: {height}cm
WEIGHT: {weight}kg
ACTIVITY: {activity_level}
CONDITIONS: {conditions}
GOALS: {goals}

Please provide specific recommendations for diet and exercise.""" 