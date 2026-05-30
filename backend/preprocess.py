import re
import string
from typing import List

# Simple English stopwords list (subset for no external deps)
STOPWORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'you', 'your', 'yours',
    'he', 'him', 'his', 'she', 'her', 'hers', 'it', 'its', 'they', 'them', 'their', 'theirs',
    'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as',
    'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before',
    'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further',
    'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other',
    'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just',
    'don', 'should', 'now'
}

def preprocess_text(text: str) -> List[str]:
    """
    Clean and tokenize text:
    - Lowercase
    - Remove punctuation and numbers
    - Remove stopwords
    - Split into tokens
    """
    # Lowercase
    text = text.lower()
    # Remove punctuation and numbers
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    # Tokenize
    tokens = text.split()
    # Remove stopwords and empty
    tokens = [token for token in tokens if token not in STOPWORDS and len(token) > 2]
    return tokens

def text_to_tfidf_vector(tokens: List[str], all_words: List[str]) -> dict:
    """
    Simple TF-IDF vector for cosine similarity.
    """
    tfidf = {word: 0 for word in all_words}
    term_freq = {}
    for token in tokens:
        term_freq[token] = term_freq.get(token, 0) + 1
    
    # Simple IDF: log(N / df), but mock df=1 for simplicity; use freq for now
    max_freq = max(term_freq.values()) if term_freq else 1
    for word, freq in term_freq.items():
        tfidf[word] = (freq / len(tokens)) * (1 / max_freq)  # Normalized TF * simple IDF
    
    return tfidf

