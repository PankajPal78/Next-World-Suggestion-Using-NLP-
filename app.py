from flask import Flask, render_template, request
import pandas as pd
import textdistance
import re
from collections import Counter

app = Flask(__name__)

words = []

# Correct variable name to populate the words list
with open('autocorrect book.txt', 'r', encoding='utf-8') as f:
    data = f.read().lower()
    words = re.findall(r'\w+', data)  # Use 'words' to store the result of re.findall

V = set(words)
words_freq_dict = Counter(words)
Total = sum(words_freq_dict.values())
probs = {}

for k in words_freq_dict.keys():
    probs[k] = words_freq_dict[k] / Total

@app.route('/')  # Corrected to route
def index():
    return render_template('index.html', suggestions=None)

@app.route('/suggest', methods=['POST'])  # Corrected to route and 'POST'
def suggest():
    keyword = request.form['keyword'].lower()
    if keyword:
        similarities = [1 - textdistance.Jaccard(qval=2).distance(v, keyword) for v in words_freq_dict.keys()]
        df = pd.DataFrame.from_dict(probs, orient='index').reset_index()
        df.columns = ['word', 'Probs']
        df['Similarity'] = similarities
        suggestions = df.sort_values(['Similarity', 'Probs'], ascending=False)[['word', 'Similarity']]  # Corrected column name
        suggestions_list = suggestions.to_dict('records')
        return render_template('index.html', suggestions=suggestions_list)

if __name__ == '__main__':  # Corrected typo in the main block
    app.run(debug=True)
