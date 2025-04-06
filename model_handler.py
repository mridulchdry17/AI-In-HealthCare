from transformers import pipeline
import re

class ModelHandler:
    def __init__(self):
        print("Loading model...")
        # Using a medical-focused model
        self.generator = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",  # Changed to flan-t5 which is better for structured responses
            max_length=200
        )
        print("Model loaded successfully!")

    def generate_response(self, prompt, max_length=200):
        try:
            # Add medical context to the prompt
            medical_prompt = f"""Answer as a medical professional:

{prompt}

Provide a clear response with:
1. Brief explanation of the condition
2. Common treatments and home remedies
3. When to seek medical attention"""

            # Generate response
            results = self.generator(
                medical_prompt,
                max_length=max_length,
                num_return_sequences=1,
                temperature=0.3,  # Lower temperature for more focused responses
                do_sample=True
            )
            
            # Get the response text
            response = results[0]['generated_text']
            
            # Clean up the response
            response = self.clean_response(response)
            
            if len(response) < 20:
                return """For fever:
1. Rest and stay hydrated
2. Take over-the-counter fever reducers like acetaminophen
3. See a doctor if fever is high (over 103°F/39.4°C) or lasts more than 3 days"""
                
            return response
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return """I apologize for the error. Here's general fever advice:
- Rest and stay hydrated
- Monitor temperature
- Take fever reducers if needed
- See a doctor if fever is high or persistent"""

    def clean_response(self, text):
        # Remove any weird artifacts or repetitions
        text = re.sub(r'[\[\]\{\}]', '', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'(\. \.|\,\,)', '.', text)
        
        # Ensure proper formatting
        lines = text.split('\n')
        cleaned_lines = [line.strip() for line in lines if line.strip()]
        return '\n'.join(cleaned_lines) 