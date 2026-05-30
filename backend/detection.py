import numpy as np
from typing import Tuple, List, Dict
from backend.preprocess import preprocess_text, text_to_tfidf_vector
import difflib

def kmp_search(text: str, pattern: str) -> List[Tuple[int, int]]:
    """Knuth-Morris-Pratt for exact substring matches. Returns list of (start, end) positions."""
    if not pattern or not text:
        return []
    # Preprocess: lower and clean for case-insensitive
    text = text.lower()
    pattern = pattern.lower()
    
    # Compute LPS (longest prefix suffix) array for pattern
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    
    # KMP search
    matches = []
    i = 0
    j = 0
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == len(pattern):
            matches.append((i - j, i))
            j = lps[j - 1]
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return matches

def rabin_karp_search(text: str, pattern: str, base=31, mod=10**9 + 9) -> List[Tuple[int, int]]:
    """Rabin-Karp rolling hash for substring detection."""
    if not pattern or not text:
        return []
    text = text.lower()
    pattern = pattern.lower()
    n, m = len(text), len(pattern)
    
    # Hash functions
    def rolling_hash(s: str) -> int:
        h = 0
        for char in s:
            h = (h * base + (ord(char) - ord('a') + 1)) % mod
        return h
    
    pat_hash = rolling_hash(pattern)
    txt_hash = rolling_hash(text[:m])
    matches = []
    
    h_multiplier = pow(base, m - 1, mod)
    
    for i in range(n - m + 1):
        if pat_hash == txt_hash:
            if text[i:i+m] == pattern:  # Verify to avoid hash collision
                matches.append((i, i + m))
        if i < n - m:
            txt_hash = (txt_hash - ord(text[i]) * h_multiplier % mod + mod) % mod
            txt_hash = (txt_hash * base + (ord(text[i + m]) - ord('a') + 1)) % mod
    return matches

def lcs_length(text1: str, text2: str) -> int:
    """Longest Common Subsequence length using DP."""
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]

def lcs_similarity(text1: str, text2: str) -> float:
    """LCS similarity percentage."""
    return (2 * lcs_length(text1, text2) / (len(text1) + len(text2))) * 100

def cosine_similarity(tfidf1: Dict[str, float], tfidf2: Dict[str, float]) -> float:
    """Cosine similarity between TF-IDF vectors."""
    all_words = list(set(tfidf1.keys()) | set(tfidf2.keys()))
    vec1 = np.array([tfidf1.get(w, 0) for w in all_words])
    vec2 = np.array([tfidf2.get(w, 0) for w in all_words])
    dot = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return (dot / (norm1 * norm2)) * 100

def detect_plagiarism(query_text: str, doc_text: str, doc_id: str = None) -> Dict:
    """
    Full detection: preprocess, run algos, return scores and highlights.
    """
    # Preprocess
    query_tokens = preprocess_text(query_text)
    doc_tokens = preprocess_text(doc_text)
    all_words = list(set(query_tokens + doc_tokens))
    query_tfidf = text_to_tfidf_vector(query_tokens, all_words)
    doc_tfidf = text_to_tfidf_vector(doc_tokens, all_words)
    
    # Scores
    # KMP/RK are for exact substring matching.
    # Tokenization removes punctuation/stopwords, so we need to run KMP/RK on the same cleaned form.
    cleaned_query = " ".join(query_tokens)
    cleaned_doc = " ".join(doc_tokens)

    # Use a portion of query to find exact overlap in cleaned text.
    pattern = " ".join(query_tokens[:min(50, len(query_tokens))])

    kmp_matches = kmp_search(cleaned_doc, pattern) if pattern.strip() else []
    rk_matches = rabin_karp_search(cleaned_doc, pattern) if pattern.strip() else []

    lcs_score = lcs_similarity(query_text, doc_text)
    cos_score = cosine_similarity(query_tfidf, doc_tfidf)


    
    # Highlighting with difflib
    matcher = difflib.SequenceMatcher(None, query_text, doc_text)
    highlights = []
    for m in matcher.get_matching_blocks():
        if m.size > 10:
            matching_snippet = query_text[m.a:m.a + m.size]
            highlights.append({
                'type': 'match', 
                'query_start': m.a, 
                'query_end': m.a + m.size, 
                'doc_start': m.b, 
                'doc_end': m.b + m.size,
                'matching_text': matching_snippet,
                'size': m.size
            })
    
    return {
        'kmp_matches': len(kmp_matches),
        'rabin_karp_matches': len(rk_matches),
        'lcs_similarity': lcs_score,
        'cosine_similarity': cos_score,
        'overall_similarity': max(lcs_score, cos_score),
        'highlights': highlights[:10]  # Top 10
    }

