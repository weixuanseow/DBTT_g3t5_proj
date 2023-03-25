import numpy as np
import pickle
from preprocessing import preprocess_text

with open('count_vectorizer.pkl', 'rb') as f:
    count_vectorizer = pickle.load(f)
with open("topic_model.pkl", "rb") as f:
    lda_model = pickle.load(f)

def classify_text(text):
    # preprocess text
    preprocessed_text = preprocess_text(text)
    # convert preprocessed text into a bag of words matrix
    text_bow = count_vectorizer.transform([preprocessed_text])
    # compute probabilities of input text belonging to each topic
    topic_probs = lda_model.transform(text_bow)
    
    # sort topics by probability and return the most likely topic
    most_likely_topic = np.argmax(topic_probs)
    
    topic_labels = {
        0: "Immigration",
        1: "Legal Practice Management",
        2: "Commercial & Corporate"
    }
    topic_label = topic_labels[most_likely_topic]

    return topic_label