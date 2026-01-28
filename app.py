from flask import Flask, render_template, request
from google import genai

# -------------------------------
# Flask App
# -------------------------------
app = Flask(__name__)

# -------------------------------
# Gemini Client
# -------------------------------
client = genai.Client(
    api_key="your api key"
)

# -------------------------------
# AI Logic - Diet Recommendation
# -------------------------------
def generate_recommendations(diet, goal, lifestyle, restrictions, health):
    prompt = f"""
You are a diet and fitness expert.

User Profile:
Dietary Preference: {diet}
Fitness Goal: {goal}
Lifestyle: {lifestyle}
Dietary Restrictions: {restrictions}
Health Conditions: {health}

Give output in this format:

Diet Recommendations:
- item

Workout Recommendations:
- item

Breakfast Suggestions:
- item

Dinner Suggestions:
- item

Additional Tips:
- item
"""

    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=prompt
    )
    return response.text

# -------------------------------
# AI Logic - Chatbot
# -------------------------------
def chat_with_ai(user_question):
    prompt = f"""
You are a friendly AI nutrition and fitness assistant.
Answer clearly, briefly, and safely.

User Question:
{user_question}
"""

    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=prompt
    )
    return response.text

# -------------------------------
# Routes
# -------------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    result = generate_recommendations(
        request.form["diet_pref"],
        request.form["fitness_goal"],
        request.form["lifestyle"],
        request.form["restrictions"],
        request.form["health"]
    )
    return render_template("index.html", result=result)

@app.route("/chat", methods=["POST"])
def chat():
    user_question = request.form["chat_input"]
    reply = chat_with_ai(user_question)
    return render_template("index.html", chat_reply=reply)

# -------------------------------
# Run
# -------------------------------
if __name__ == "__main__":
    app.run(debug=False)

