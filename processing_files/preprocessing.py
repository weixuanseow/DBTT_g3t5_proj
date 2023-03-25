import re
from gensim.parsing.preprocessing import preprocess_string

# clean, tokenize, and stem the text data
def preprocess_text(text):
    # remove email addresses
    text = re.sub(r'\S*@\S*\s?', '', text)
    # remove any non-alphanumeric characters and convert to lowercase
    text = re.sub('[,\.!?]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r"\'", "", text)
    text = text.lower()

    # preprocess the text using gensim's preprocessing functions
    processed_text = preprocess_string(text)
    processed_text_str = ' '.join(processed_text)
    
    return processed_text_str