from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-pro')

MEDICAL_PROMPT = """You are a knowledgeable medical assistant. Provide clear, structured advice for the following medical query:

CONCERN: {user_input}

For symptoms/conditions, format your response like this:

BRIEF EXPLANATION:
• What is it?
• What typically causes it?
• How common/serious is it?

COMMON REMEDIES AND TREATMENTS:
• First-line treatment:
  [Primary recommended treatment]

• Self-care steps:
  [What to do at home]

• Medications:
  [Relevant medications if applicable]

• Lifestyle changes:
  [If relevant]

WHEN TO SEEK MEDICAL HELP:
• Urgent signs:
  [List immediate warning signs]

• General indicators:
  [When to see a doctor]

For medication/treatment queries, format like this:

MEDICATION/TREATMENT INFO:
• Purpose:
  [What it's used for]

• Usage:
  [How to use/take it]

• Common side effects:
  [List main side effects]

• Important notes:
  [Key warnings or interactions]

For general health queries, format appropriately with clear bullet points and line breaks. Keep responses concise and easy to understand.

Note: This is general information only. Always consult healthcare professionals for personal medical advice."""

HEALTH_RECOMMENDATION_PROMPT = """Create a personalized health plan based on the following profile:

Age: {age} years
Height: {height}cm
Weight: {weight}kg
Activity Level: {activity_level}
Medical Conditions: {conditions}
Goals: {goals}

Format your response with clear headers and bullet points:

PERSONALIZED HEALTH PLAN

CURRENT STATUS:
• BMI calculation and category
• Overall health assessment

DIET RECOMMENDATIONS:
• Daily caloric needs
• Macronutrient breakdown
• Key foods to include
• Meal timing suggestions

EXERCISE PLAN:
• Cardio recommendations
• Strength training suggestions
• Weekly schedule outline
• Activity modifications if needed

LIFESTYLE RECOMMENDATIONS:
• Sleep guidelines
• Stress management
• Other health considerations

Note: Format with clear sections, no asterisks, use bullet points for lists."""

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('message', '')
        if not user_input:
            return jsonify({'error': 'No message provided'}), 400

        # Generate response using Gemini
        prompt = MEDICAL_PROMPT.format(user_input=user_input)
        response = model.generate_content(prompt)
        
        return jsonify({'response': response.text})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Failed to process request'}), 500

@app.route('/api/health-recommendations', methods=['POST'])
def get_health_recommendations():
    try:
        data = request.json
        
        required_fields = ['height', 'weight', 'age', 'activity_level']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        bmi = calculate_bmi(float(data['weight']), float(data['height']))
        
        # Format prompt for health recommendations
        prompt = HEALTH_RECOMMENDATION_PROMPT.format(
            age=data.get('age'),
            height=data.get('height'),
            weight=data.get('weight'),
            activity_level=data.get('activity_level'),
            conditions=data.get('conditions', 'None'),
            goals=data.get('goals', 'General health improvement')
        )
        
        # Get recommendations from Gemini
        response = model.generate_content(prompt)
        
        return jsonify({
            'bmi': bmi,
            'bmi_category': get_bmi_category(bmi),
            'recommendations': {
                'overview': f"Your BMI is {bmi} ({get_bmi_category(bmi)})",
                'details': response.text
            }
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Failed to process request'}), 500

def get_bmi_category(bmi):
    if bmi < 18.5: return "underweight"
    elif bmi < 25: return "healthy weight"
    elif bmi < 30: return "overweight"
    else: return "obese"

def calculate_bmi(weight, height):
    height_m = height / 100
    return round(weight / (height_m ** 2), 1)

if __name__ == '__main__':
    app.run(debug=True) 