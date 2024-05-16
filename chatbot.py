from flask import Flask, request, jsonify, render_template

app = Flask(__name__, static_folder="static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    bot_response = get_bot_response(user_message)
    return jsonify({"message": bot_response})

def get_bot_response(message):
    message = message.lower()
    if "hello" in message:
        return "Hello! How can I assist you today?"
    elif "how are you" in message:
        return "I'm just a bot, but I'm doing great! How about you?"
    elif "weather" in message:
        return "I'm sorry, I cannot provide real-time weather updates at the moment."
    elif "thank you" in message or "thanks" in message:
        return "You're welcome!"
    elif "goodbye" in message or "goodbye" in message:
        return "Goodbye! Have a great day!"
    elif "order" in message:
        return "Sure, what would you like to order?"
    elif "menu" in message:
        return "Here is our menu:\n1. Pizza\n2. Burger\n3. Pasta\n4. Salad\nPlease let me know what you would like to order."
    elif "I would Like To have Pizza" in message:
        return "Great choice! What size would you like? We have small, medium, and large."
    elif "burger" in message:
        return "Sure! Would you like a regular burger or a cheeseburger?"
    elif "pasta" in message:
        return "Excellent choice! Would you like spaghetti or penne?"
    elif "i like eat salad" in message:
        return "Healthy choice! Would you like a garden salad or a Caesar salad?"
    elif "small" in message or "medium" in message or "large" in message:
        return "Perfect! Your {} pizza will be ready in 20 minutes. Can I help you with anything else?".format(message)
    elif "regular" in message or "cheeseburger" in message:
        return "Delicious choice! Your {} burger will be ready in 15 minutes. Can I help you with anything else?".format(message)
    elif "spaghetti" in message or "penne" in message:
        return "Yummy! Your {} pasta will be ready in 15 minutes. Can I help you with anything else?".format(message)
    elif "garden" in message or "caesar" in message:
        return "Great! Your {} salad will be ready in 10 minutes. Can I help you with anything else?".format(message)
    elif "dessert" in message:
        return "We have a variety of desserts available. Would you like to see the dessert menu?"
    elif "dessert menu" in message:
        return "Here is our dessert menu:\n1. Chocolate cake\n2. Cheesecake\n3. Tiramisu\nPlease let me know what you would like to order."
    elif "chocolate cake" in message:
        return "Great choice! Would you like to add ice cream or whipped cream?"
    elif "cheesecake" in message:
        return "Delicious choice! Would you like to add berries or caramel sauce?"
    
    elif "What is 10 + 10" in message:
        return "It's Equal with = 20!"
    
    elif "tiramisu" in message:
        return "Classic choice! Would you like to add extra cocoa powder or chocolate shavings?"
    elif "ice cream" in message or "whipped cream" in message:
        return "Perfect! Your {} chocolate cake will be ready in 10 minutes. Can I help you with anything else?".format(message)
    elif "berries" in message or "caramel sauce" in message:
        return "Delicious! Your {} cheesecake will be ready in 10 minutes. Can I help you with anything else?".format(message)
    elif "cocoa powder" in message or "chocolate shavings" in message:
        return "Great choice! Your {} tiramisu will be ready in 10 minutes. Can I help you with anything else?".format(message)
    elif "no" in message:
        return "Alright. Is there anything else I can assist you with?"
    else:
        return "I'm sorry, I didn't understand that."

if __name__ == "__main__":
    app.run(debug=True)










# from flask import Flask, request, jsonify, render_template
# import openai

# app = Flask(__name__, static_folder="static")

# # Set your OpenAI API key here
# openai.api_key = 'OPen_Api_KEy'

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/api/chat", methods=["POST"])
# def chat():
#     user_message = request.json["message"]
#     bot_response = get_bot_response(user_message)
#     return jsonify({"message": bot_response})

# def get_bot_response(message):
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=message,
#         temperature=0.7,
#         max_tokens=150
#     )
#     return response.choices[0].text.strip()

# if __name__ == "__main__":
#     app.run(debug=True)

