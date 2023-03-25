from flask import Flask, request, jsonify, render_template
from classification import classify_text
from flask_cors import CORS
from twilio.rest import Client
import os
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('../app/pages/contact.html')

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    message = request.form.get('message')

    # Classify the message
    topic_label = classify_text(message)

    # Construct the confirmation message
    confirmation_message = f"Thank you {name} for contacting us. Our {topic_label} department will get back to you soon."

    # Load environment variables from .env file
    load_dotenv()

    if phone and all(k in os.environ for k in ('TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'TWILIO_PHONE_NUMBER')) :
        # Send an SMS to the client
        twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        twilio_phone_number = os.environ.get('TWILIO_PHONE_NUMBER')
        
        account_sid = twilio_account_sid
        auth_token = twilio_auth_token
        client = Client(account_sid, auth_token)
        
        sms_body = f"Hi {name}! Thank you for contacting us. Your request has been processed and our {topic_label} department will get back to you shortly. Have a nice day ahead!"
        client.messages.create(
            body= sms_body,
            from_= twilio_phone_number,
            to=phone
        )
    else:
        print("Missing Twilio credentials.")


    return jsonify({'confirmation_message': confirmation_message})


@app.route('/classify_incoming', methods=['POST'])
def classify_incoming():
    text = request.form['text']
    result = classify_text(text)

    confirmation_message = f"The document has been classified under the {result} Law.\nIt has been assigned to the {result} Department."
    
    return jsonify({'confirmation_message': confirmation_message})


@app.route('/summarize', methods=['POST'])
def summarize(percentage=0.08):
    nlp = spacy.load("en_core_web_sm")
    stopwords = set(STOP_WORDS)
    
    text = request.form['text']
    # build nlp object
    doc = nlp(text)
    freq_of_word = dict()

    # Text cleaning and vectorization 
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            freq_of_word[word.text] = freq_of_word.get(word.text, 0) + 1

    # Maximum frequency of word
    max_freq = max(freq_of_word.values())

    # Normalization of word frequency
    for word in freq_of_word.keys():
        freq_of_word[word] = freq_of_word[word] / max_freq

    # Weigh each sentence based on how often it contains the token
    sent_tokens = [sent for sent in doc.sents]
    sent_scores = dict()
    for sent in sent_tokens:
        for word in sent:
            if word.text.lower() in freq_of_word:
                sent_scores.setdefault(sent, 0)
                sent_scores[sent] += freq_of_word[word.text.lower()]

    len_tokens = int(len(sent_tokens) * percentage)

    # Summary for the sentences with maximum score
    summary = nlargest(n=len_tokens, iterable=sent_scores, key=sent_scores.get)
    
    final_summary = [word.text for word in summary]
    summary = " ".join(final_summary)

    return jsonify({'summary': summary})


if __name__ == '__main__':
    app.run(debug=True)
