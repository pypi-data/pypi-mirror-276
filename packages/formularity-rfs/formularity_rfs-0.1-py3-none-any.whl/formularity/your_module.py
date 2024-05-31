import re
import os
import spacy
import pymorphy2
import numpy as np
from collections import defaultdict
from sklearn.feature_extraction.text import CountVectorizer

nlp = spacy.load("ru_core_news_sm")
morph = pymorphy2.MorphAnalyzer()

class FormularityRFS:
    def __init__(self, collocations_file, stopwords_file):
        self.collocations = self.load_collocations(collocations_file)
        self.stopwords = self.load_stopwords(stopwords_file)
    
    def load_collocations(self, filepath):
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        return []
    
    def load_stopwords(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read().splitlines()
    
    def lemmatize_text(self, text):
        doc = nlp(text)
        lemmatized_words = [morph.parse(token.text)[0].normal_form for token in doc if not token.is_punct]
        return lemmatized_words
    
    def calculate_vocd(self, lemmatized_words):
        sample_size = 35
        iterations = 1000

        n_tokens = len(lemmatized_words)
        if n_tokens < sample_size:
            raise ValueError("Недостаточное количество токенов для анализа. Введите более длинный текст.")

        vocd_scores = []
        for _ in range(iterations):
            np.random.shuffle(lemmatized_words)
            samples = [lemmatized_words[i:i + sample_size] for i in range(0, n_tokens, sample_size) if len(lemmatized_words[i:i + sample_size]) == sample_size]

            ttrs = []
            for sample in samples:
                types = set(sample)
                token_count = len(sample)
                ttr = len(types) / token_count
                ttrs.append(ttr)

            if ttrs:
                vocd_scores.append(np.mean(ttrs))

        mean_vocd_score = np.mean(vocd_scores)
        return mean_vocd_score
    
    def extract_interjections(self, song_text):
        doc = nlp(song_text)
        interjections = [token.text for token in doc if token.pos_ == 'INTJ']
        return interjections
    
    def find_ngrams(self, text, min_len=2, max_len=14):
        vectorizer = CountVectorizer(ngram_range=(min_len, max_len), stop_words=self.stopwords).fit([text])
        ngrams_freq = vectorizer.transform([text]).toarray().flatten()
        ngrams = vectorizer.get_feature_names_out()
        ngrams_count = defaultdict(int)
        ngram_words = set()  
        for ngram, count in zip(ngrams, ngrams_freq):
            if count > 1:
                ngrams_count[ngram] += count
                ngram_words.update(ngram.split())
        return ngrams_count, ngram_words
    
    def filter_ngrams(self, ngrams):
        ngrams = sorted(ngrams, key=lambda x: len(x.split()), reverse=True)
        filtered_ngrams = []
        for ngram in ngrams:
            if not any(ngram in longer_ngram for longer_ngram in filtered_ngrams):
                filtered_ngrams.append(ngram)
        return filtered_ngrams
    
    def calculate_formulaicity(self, song_text):
        marked_text = song_text  
        interjections = self.extract_interjections(song_text)
        for interjection in interjections:
            marked_text = re.sub(f"(?i)\\b{re.escape(interjection)}\\b", f"<strong style='color: red;'>{interjection}</strong>", marked_text)

        dash_pattern = r"([А-Яа-я\w]+-[А-Яа-я\w]+(?!-?(Кое|кое|либо|то|нибудь|ка)))"
        dash = re.findall(dash_pattern, song_text)
        dash = [match[0] for match in dash]
        dash = list(set(dash) - set(interjections))
        for d in dash:
            marked_text = re.sub(f"(?i){re.escape(d)}", f"<strong style='color: purple;'>{d}</strong>", marked_text)

        found_collocations = []
        for col in self.collocations:
            if col in song_text:
                found_collocations.append(col)
                marked_text = re.sub(f"(?i){re.escape(col)}", f"<strong style='color: blue;'>{col}</strong>", marked_text)

        interjection_count = len(interjections)
        dash_count = len(dash)
        collocation_count = len(found_collocations)

        total_coefficient = 0.1 * interjection_count + 0.1 * dash_count + 0.1 * collocation_count

        lemmatized_words = self.lemmatize_text(song_text)

        try:
            vocd_score = self.calculate_vocd(lemmatized_words)
        except ValueError:
            vocd_score = None
            print("Невозможно посчитать VOCD")

        formulaicity_score = vocd_score if vocd_score is not None else 0
        formulaicity_score += total_coefficient

        ngrams_count, ngram_words = self.find_ngrams(song_text)
        unique_ngrams = [ngram for ngram in ngrams_count if ngrams_count[ngram] > 1]
        filtered_ngrams = self.filter_ngrams(unique_ngrams)
        score_increase = 0.1 * len(filtered_ngrams)

        formulaicity_score += score_increase

        for word in ngram_words:
            marked_text = re.sub(f"(?i)\\b{re.escape(word)}\\b", f"<strong style='color: green; text-decoration: underline;'>{word}</strong>", marked_text)

        print("Лемматизированные слова:", lemmatized_words)
        print("Междометия:", interjections)
        print("Биграммы:", dash)
        print("Найденные фразеологизмы:", found_collocations)
        print("Найденные уникальные n-граммы:", filtered_ngrams)
        print("Коэффициент для междометий:", 0.1 * interjection_count)
        print("Коэффициент для фразеологизмов:", 0.1 * collocation_count)
        print("Коэффициент для биграмм:", 0.1 * dash_count)
        print("Коэффициент для n-грамм:", score_increase)
        print("Коэффициент VOCD:", vocd_score)

        return formulaicity_score, marked_text, filtered_ngrams

def analyse(input_file="songs.txt", output_file="results.html", collocations_file="collocations.txt", stopwords_file="stopwords.txt"):
    if not os.path.exists(input_file):
        with open(input_file, "w", encoding="utf-8") as f:
            f.write("")
        print(f"Файл {input_file} появится в течение минуты. Пожалуйста, добавьте тексты песен в {input_file}, разделяя их знаком +, и запустите код заново.")
        return

    # Read collocations
    collocations = []
    if os.path.exists(collocations_file):
        with open(collocations_file, "r", encoding="utf-8") as f:
            collocations = [line.strip() for line in f.readlines() if line.strip()]

    # Read stopwords
    stopwords = []
    if os.path.exists(stopwords_file):
        with open(stopwords_file, "r", encoding="utf-8") as f:
            stopwords = f.read().splitlines()

    # Initialize analyzer object
    analyzer = FormularityRFS(collocations_file, stopwords_file)

    if os.path.exists(input_file) and os.path.getsize(input_file) > 0:
        with open(input_file, "r", encoding="utf-8") as f:
            songs = f.read().split("+")

        results = [
            "<html>",
            "<head><meta charset='utf-8'><title>Результаты анализа</title></head>",
            "<body>"
        ]
        for i, song in enumerate(songs):
            song = song.strip()
            if song:
                formulaicity_score, marked_text, filtered_ngrams = analyzer.calculate_formulaicity(song)
                ngram_list_html = "<ul>" + "".join([f"<li>{ngram}</li>" for ngram in filtered_ngrams]) + "</ul>"
                results.append(f"<h2>Песня {i+1}</h2><p>{marked_text}</p><p><strong>Найденные n-граммы:</strong> {ngram_list_html}</p><p><strong>Formulaicity coefficient:</strong> {formulaicity_score}</p>")

        results.append("</body></html>")

        # Write results to output file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n\n".join(results))

        print(f"Результаты записаны в файл {output_file}, он появится в течение минуты.")
    else:
        print(f"Файл {input_file} появится в течение минуты. Пожалуйста, добавьте тексты песен в {input_file}, разделяя их знаком +, и запустите код снова.")


