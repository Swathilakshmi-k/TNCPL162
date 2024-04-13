# Emotion Detection and Analysis App

This is a web application built with Flask that uses a pre-trained transformer model to detect emotions in text input by users. The app also stores user data and analytics in a Firebase Realtime Database and provides visualizations for the data.

## Features

- Emotion detection: The app can detect up to 27 different emotions, including positive emotions like joy, love, and gratitude, and negative emotions like anger, sadness, and fear.
- Language support: The app can handle text input in English, Tamil, and French. It automatically detects the language and translates non-English text to English before processing.
- Data storage: All user input text, detected emotions, and timestamps are stored in a Firebase Realtime Database.
- Analytics: The app tracks the total number of predictions made, as well as the counts of positive and negative emotions detected. This data is also stored in the Firebase database.
- Data visualization: The app provides a line chart that shows the trend of the user's emotional state over time, based on the detected emotions and an "emotion index" calculated from the data.
- Memes and motivational quotes: The app includes pages for displaying memes and motivational quotes to uplift the user's mood.
- Feedback form: Users can submit feedback about the app through a feedback form.

## Technologies Used

- Python
- Flask
- Firebase Realtime Database
- Transformers (Hugging Face)
- Google Translate API
- Jinja2
- HTML/CSS/JavaScript

## Setup

1. Clone the repository:
git clone https://github.com/your-repo/emotion-detection-app.git


Copy code

2. Create a virtual environment and activate it:
python -m venv env
source env/bin/activate  # On Windows, use env\Scripts\activate


Copy code

3. Install the required dependencies:
pip install -r requirements.txt


Copy code

4. Set up a Firebase project and download the service account key JSON file. Place the file in the project directory and rename it to `cred.json`.

5. Run the Flask app:
python app.py


Copy code

6. Open your web browser and visit `http://localhost:5000` to access the app.

## Usage

1. Enter some text in the input field on the home page.
2. The app will detect the emotion(s) expressed in the text and display the primary emotion, its confidence score, and an alternative emotion.
3. The user's input, detected emotion, and timestamp will be stored in the Firebase database.
4. Visit the `/record` route to see a table of all user inputs, detected emotions, and timestamps.
5. Visit the `/analytics` route to view visualizations of the emotion data, including a line chart showing the trend of the user's emotional state over time.
6. Explore the `/memes` and `/motivate` routes for uplifting content.
7. Use the `/feedback` route to submit feedback about the app.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

###Enjoy the App###