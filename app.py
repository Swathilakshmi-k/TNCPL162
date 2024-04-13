from flask import jsonify, Flask, render_template, request
import pickle
from transformers import pipeline
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime
import jinja2
import emoji
from langdetect import detect
from googletrans import Translator
from deep_translator import GoogleTranslator
translator = Translator()

# Add the zip function to the Jinja2 environment

def predict_emotion(input_text):
    # Detect the language of the input text
    language = detect(input_text)
    input_text=convert_emojis_to_text(input_text)
    # Translate the text to English if it's in Tamil
    if language == 'ta'or language == 'tanglish':
        translator = GoogleTranslator(source='ta', target='en')
        input_text = translator.translate(input_text)
    if language == 'hi':
        translator = GoogleTranslator(source='hi', target='en')
        input_text = translator.translate(input_text)
    if language == 'ben':
        translator = GoogleTranslator(source='ben', target='en')
        input_text = translator.translate(input_text)
    if language == 'pa':
        translator = GoogleTranslator(source='pa', target='en')
        input_text = translator.translate(input_text)
    if language == 'ml':
        translator = GoogleTranslator(source='ml', target='en')
        input_text = translator.translate(input_text)
    if language == 'mr':
        translator = GoogleTranslator(source='mr', target='en')
        input_text = translator.translate(input_text)
    if language == 'kn':
        translator = GoogleTranslator(source='kn', target='en')
        input_text = translator.translate(input_text)
    if language == 'gu':
        translator = GoogleTranslator(source='gu', target='en')
        input_text = translator.translate(input_text)
    if language == 'ur':
        translator = GoogleTranslator(source='ur', target='en')
        input_text = translator.translate(input_text)

  
    response = classifier(input_text)
    prediction = response[0][0]['label']
    accuracy = round(response[0][0]['score'] * 100, 2)
    alter = response[0][1]["label"]

    return prediction, accuracy, alter
def get_dd_mm_yy_time():
    # Get the current date and time
    current_time = datetime.now()
    
    # Format the date and time as DD/MM/YY HH:MM:SS
    formatted_time = current_time.strftime("%d/%m/%y %H:%M:%S")
    
    return formatted_time

# Fetch the service account key JSON file contents
cred = credentials.Certificate('cred.json')

# Initialize the Firebase app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://hope-be2dc-default-rtdb.firebaseio.com'
})

# Add new fields to the Firebase database
ref = db.reference('analytics')
#ref.set({
 #   'total_predictions': 0,
  #  'positive_emotions': 0,
   # 'negative_emotions': 0
#})

# Function to save data to Firebase and update analytics fields
def save_messages(name, emotion, index, time):
    # Get a reference to the 'userData' node in the database
    ref = db.reference('userData')

    # Create a new child node under 'userData' with an auto-generated key
    new_node = ref.push({
        'Text': name,
        'Emotion': emotion,
        'Index': index,
        'Time': time
    })
    print(f"Data saved successfully with key: {new_node.key}")

    # Update analytics fields
    update_analytics(emotion)

# Function to update analytics fields
def update_analytics(emotion):
    ref = db.reference('analytics')
    analytics = ref.get()

    total_predictions = analytics['total_predictions'] + 1
    positive_emotions = analytics['positive_emotions']
    negative_emotions = analytics['negative_emotions']

    positive_emotions_list = [
        "amusement", "approval", "caring", "curiosity", "desire", "excitement",
        "gratitude", "joy", "love", "optimism", "pride", "realization", "relief",
        "satisfaction", "surprise", "trust", "neutral"
    ]

    if emotion in positive_emotions_list:
        positive_emotions += 1
    else:
        negative_emotions += 1

    ref.update({
        'total_predictions': total_predictions,
        'positive_emotions': positive_emotions,
        'negative_emotions': negative_emotions
    })

classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)

app = Flask(__name__)
app.jinja_env.globals.update(zip=zip)
def emotion_to_index(emotion, index):
    positive_emotions = [
        "amusement", "approval", "caring", "curiosity", "desire", "excitement",
        "gratitude", "joy", "love", "optimism", "pride", "realization", "relief",
        "satisfaction", "surprise", "trust", "neutral"
    ]

    negative_emotions = [
        "anger", "annoyance", "confusion", "disappointment", "disapproval",
        "disgust", "embarrassment", "fear", "grief", "nervousness", "remorse",
        "sadness"
    ]

    if index is None:
        index = 0

    if emotion in positive_emotions:
        index += 1
    else:
        index -= 1

    return index

def get_last_entry_from_firebase():
    ref = db.reference('userData')
    last_entry_query = ref.order_by_key().limit_to_last(1)
    last_entry_snapshot = last_entry_query.get()

    if last_entry_snapshot:
        for key, value in last_entry_snapshot.items():
            index = value.get('Index', 0)
        return index
    else:
        return None
def get_data_from_firebase():
    ref = db.reference('userData')
    data = ref.get()

    emotions = []
    indices = []
    times = []
    texts = []

    for key, value in data.items():
        emotion = value['Emotion']
        index = value.get('Index', 0)
        time_str = value.get('Time', '')
        text = value['Text']

        # Truncate the text if it's longer than 20 words
        words = text.split()
        if len(words) > 20:
            text = ' '.join(words[:20]) + '...'

        emotions.append(emotion)
        indices.append(index)
        times.append(time_str)
        texts.append(text)

    return emotions, indices, times, texts
# Function to get analytics data from Firebase
def get_analytics_from_firebase():
    ref = db.reference('analytics')
    data = ref.get()

    total_predictions = data['total_predictions']
    positive_emotions = data['positive_emotions']
    negative_emotions = data['negative_emotions']

    return total_predictions, positive_emotions, negative_emotions



def convert_emojis_to_text(input_text):
    # Convert emojis to text descriptions
    text_with_emojis_converted = emoji.demojize(input_text)
    return text_with_emojis_converted

def list_to_sentence(word_list):
    # Join the words in the list into a sentence
    sentence = ' '.join(word_list)
    return sentence
@app.route('/record')
def record():
    emotions, indices, times, texts = get_data_from_firebase()
    return render_template('record.html', emotions=emotions, indices=indices, times=times, texts=texts)

@app.route('/analytics')
def analytics():
    emotions, indices, times, texts = get_data_from_firebase()
    total_predictions, positive_emotions, negative_emotions = get_analytics_from_firebase()

    # Calculate the emotion index
    index = get_last_entry_from_firebase() - 1

    # Create the data for the Google Line Chart
    chart_data = [['Time', 'Index']]
    for time, ind in zip(times, indices):
        chart_data.append([time, ind])

    return render_template('Analytics.html', chart_data=chart_data, total_predictions=total_predictions, positive_emotions=positive_emotions, negative_emotions=negative_emotions, index=index)
@app.get("/")
def index_get():
    return render_template("test.html")

@app.route('/memes')
def memes():
    return render_template('memes.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/motivate')
def motivate():
    return render_template('motivate.html')
@app.route('/chat')
def chat():
    return render_template('chat.html')
@app.route('/feedback')
def feedback():
    return render_template('feedback.html')
@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        text = [str(x) for x in request.form.values()]
        #emoji
        #text=convert_emojis_to_text(text)
        prediction, accuracy, alter = predict_emotion(text[0])
        stmt = list_to_sentence(text)
        
      
        
        # emotion index calculation
        index = get_last_entry_from_firebase()
        index = emotion_to_index(prediction, index)

        save_messages(stmt, prediction, index, get_dd_mm_yy_time())
        return render_template('index.html', input_text=text[0], prediction=prediction, accuracy=str(accuracy), alter=alter)
    return render_template('index.html')

# Add a new route to get analytics data
@app.route('/get_stats', methods=['GET'])
def get_stats():
    total_predictions, positive_emotions, negative_emotions = get_analytics_from_firebase()
    emotions, indices, times, text = get_data_from_firebase()

    stats = {
        'total_predictions': total_predictions,
        'positive_emotions': positive_emotions,
        'negative_emotions': negative_emotions,
    }

    return jsonify(stats)

if __name__ == "__main__":
    app.run(debug=True)