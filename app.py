from flask import Flask, render_template, request, jsonify
import mysql.connector
import requests
import wikipedia
import json
from datetime import datetime
import os # keep for Deployment

app = Flask(__name__)


# ================= DATABASE CONFIG =================
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'amir'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

def save_chat_to_db(user_message, bot_response, user_id='default_user'):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO chat_history (user_id, user_message, bot_response)
        VALUES (%s, %s, %s)
        """

        values = (user_id, user_message, bot_response)
        cursor.execute(query, values)

        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print("Database Error:", e)
        return False

# ================= WEATHER =================
WEATHER_API_KEY = 'e82b0fcf2c88d6f069b778a824fc79ac'
WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather'
WEATHER_FORECAST_URL = 'http://api.openweathermap.org/data/2.5/forecast'


def get_weather(city_name):
    try:
        params = {
            'q': city_name,
            'appid': WEATHER_API_KEY,
            'units': 'metric'
        }

        response = requests.get(WEATHER_API_URL, params=params)

        if response.status_code == 200:
            data = response.json()

            return f"""
🌤️ Weather in {data['name']}:
🌡 Temperature: {data['main']['temp']}°C
🤔 Feels like: {data['main']['feels_like']}°C
💧 Humidity: {data['main']['humidity']}%
☁️ Condition: {data['weather'][0]['description']}
            """

        return "❌ City not found."
    except:
        return "❌ Weather error."

def get_weather_forecast(city_name):
    try:
        params = {
            'q': city_name,
            'appid': WEATHER_API_KEY,
            'units': 'metric'
        }
        response = requests.get(WEATHER_FORECAST_URL, params= params)

        if response.status_code == 200:
            data = response.json()
            forecast_text = f"📅 5-Day Forecast for {data['city']['name']}:\n\n"

            for i in range(0, 40, 8):
                item = data['list'][i]
                date = item['dt_txt'].split(" ")[0]
                temp = item['main']['temp']
                desc = item['weather'][0]['description']

                forecast_text += f"📆 {date}\n"
                forecast_text += f"🌡 {temp}°C\n"
                forecast_text += f"☁️ {desc}\n\n"

            return forecast_text

        return "❌ Forecast not available."
    except:
        return "❌ Forecast error."

# ================= WIKIPEDIA =================
def search_wikipedia(query, sentences=4):
    try:
        wikipedia.set_lang("en")

        # Search for best results
        results = wikipedia.search(query)

        if not results:
            return "❌ No results found."

        # Try to find a biography-style result first
        for result in results:
            if "(" in result and any(word in result.lower() for word in ["born", "actor", "president", "singer", "football", "politician"]):
                page = wikipedia.page(result)
                summary = wikipedia.summary(result, sentences=sentences)
                return format_wiki_response(page.title, summary, page.url)

        # Otherwise use first result
        best_match = results[0]
        page = wikipedia.page(best_match)
        summary = wikipedia.summary(best_match, sentences=sentences)

        return format_wiki_response(page.title, summary, page.url)

    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options[:5]
        return "🔍 Multiple results found:\n\n" + "\n".join(options)

    except wikipedia.exceptions.PageError:
        return "❌ No page found."

    except Exception as e:
        return f"❌ Wikipedia Error: {str(e)}"


def format_wiki_response(title, summary, url):
    return f"""
📚 {title}

{summary}

🔗 Read more:
{url}
"""
# ================= BOT RESPONSE =================
def get_bot_response(user_message):
    msg = user_message.lower().strip()

    words = user_message.strip().split()

    if 1 <= len(words) <= 4:
        skip_words = ['weather', 'forecast', 'time', 'date', 'help']
        if not any(word in  msg for word in skip_words):
            return search_wikipedia(user_message)



    if "forecast" in msg:
        if "in" in msg:
            city = msg.split("in")[-1].strip()
            return get_weather_forecast(city)
            return "Please say: forecast in london"

    # ---- Weather ----
    if "weather" in msg:
        if "in" in msg:
            city = msg.split("in")[-1].strip()
            return get_weather(city)
        return "Please say: weather in London"

    # ---- Time ----
    if "time" in msg:
        return f"🕐 {datetime.now().strftime('%I:%M %p')}"

    # ---- Date ----
    if "date" in msg:
        return f"📅 {datetime.now().strftime('%B %d, %Y')}"

    # ---- Wikipedia ----
    wiki_keywords = ['who is', 'what is', 'tell me about', 'define', 'meaning of']
    if any(keyword in msg for keyword in wiki_keywords):
        for keyword in wiki_keywords:
            if keyword in msg:
                query = msg.replace(keyword, '').strip()
                return search_wikipedia(query)

    # ---- Greeting ----
    if msg in ['hello', 'hi', 'hey']:
        return "👋 Hello! Ask me about weather or Wikipedia."

    return "🤔 Ask me about weather or say: who is Elon Musk"

# ================= ROUTES =================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        user_id = data.get('user_id', 'default_user')

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        bot_response = get_bot_response(user_message)

        save_chat_to_db(user_message, bot_response, user_id)

        return jsonify({
            'response': bot_response,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history')
def history():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM chat_history ORDER BY created_at DESC LIMIT 50")
        history = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(history)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clear_history', methods=['POST'])
def clear_history():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM chat_history")
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'History cleared'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ================= RUN =================
if __name__ == '__main__':
    port = 
    print("🚀 AmirBot Running on {port}")
    app.run(host= '0.0.0.0',port= port,debug=False)
