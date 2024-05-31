import os
import re
import pickle
import ssdeep
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier


class LicenseIdentifier:
    def __init__(self):
        self.cache_dir = os.path.join(os.path.dirname(__file__), 'cache')
        self.cache_file = os.path.join(
            self.cache_dir, 'license_identifier.pkl'
        )
        self.hash_file = os.path.join(self.cache_dir, 'license_hashes.dat')
        self.vectorizer = None
        self.classifier = None
        self.hash_cache = {}
        self.load_hashes()
        if not os.path.exists(self.cache_dir):
            os.mkdir(self.cache_dir)
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'rb') as f:
                self.vectorizer, self.classifier = pickle.load(f)
        else:
            self.license_texts = []
            self.license_spdx_codes = []
            self.spdx_dir = os.path.join(os.path.dirname(__file__), 'spdx')
            for file_name in os.listdir(self.spdx_dir):
                if file_name.endswith('.txt'):
                    license_spdx_code = os.path.splitext(file_name)[0]
                    self.license_spdx_codes.append(license_spdx_code)
                    with open(
                        os.path.join(self.spdx_dir, file_name), 'r'
                    ) as f:
                        license_text = f.read()
                        license_text = self.normalize_text(license_text)
                        self.license_texts.append(license_text)
                        hashfile = self.hash_file
                        idxstr = license_spdx_code
                        hashstr = ssdeep.hash(license_text)
                        self.store_hashes(hashfile, idxstr, hashstr)

            self.vectorizer = TfidfVectorizer(
                ngram_range=(1, 3), stop_words='english'
            )
            X = self.vectorizer.fit_transform(self.license_texts)

            self.classifier = RandomForestClassifier()
            y = self.license_spdx_codes
            self.classifier.fit(X, y)

            with open(self.cache_file, 'wb') as f:
                pickle.dump((self.vectorizer, self.classifier), f)

    def normalize_text(self, text):
        text = text.lower().strip()
        text = re.sub(
            r'\b(copyright|©|copr|all rights reserved)\b', '', text,
            flags=re.IGNORECASE
        )
        text = re.sub('[^0-9a-zA-Z]+', ' ', text)
        text = re.sub(' +', ' ', text)
        return text

    def store_hashes(self, hashfile, idxstr, hashstr):
        str_hash = idxstr + "|" + hashstr
        with open(hashfile, 'a+') as file:
            file.seek(0)
            if str_hash + '\n' not in file.readlines():
                file.write(str_hash + '\n')

    def load_hashes(self):
        if os.path.exists(self.hash_file):
            with open(self.hash_file, 'r') as file:
                for line in file:
                    idxstr, hashstr = line.strip().split('|')
                    self.hash_cache[hashstr] = idxstr

    def identify_license(self, text):
        text = self.normalize_text(text)
        input_hash = ssdeep.hash(text)
        for cached_hash, spdx_code in self.hash_cache.items():
            similarity = ssdeep.compare(input_hash, cached_hash)
            if similarity >= 95:
                return spdx_code, similarity / 100.1
        X = self.vectorizer.transform([text])
        predicted_class = self.classifier.predict(X)[0]
        predicted_proba = self.classifier.predict_proba(X)[0]
        class_index = self.classifier.classes_.tolist().index(predicted_class)
        if predicted_proba[class_index] < 0.5:
            return '', 0.0
        else:
            return predicted_class, predicted_proba[class_index]


class CopyrightIdentifier:
    def __init__(self):
        self.year_range_pattern = re.compile(
            r'(\d{4}\s*(?:-|\s+to\s+)\s*\d{4}|\d{4})'
        )
        self.cache_dir = os.path.join(os.path.dirname(__file__), 'cache')
        self.tfidf_cache = os.path.join(self.cache_dir, 'tfidf_data.pkl')
        self.model_cache = os.path.join(self.cache_dir, 'model.pkl')
        self.datasets_dir = os.path.join(os.path.dirname(__file__), 'datasets')
        if not os.path.exists(self.cache_dir):
            os.mkdir(self.cache_dir)
        if os.path.exists(self.tfidf_cache):
            with open(self.tfidf_cache, 'rb') as f:
                X_train_tfidf, X_test_tfidf, y_train, y_test, vectorizer = (
                    pickle.load(f)
                )
        else:
            cr_pos_path = os.path.join(self.datasets_dir, 'cr_pos')
            cr_neg_path = os.path.join(self.datasets_dir, 'cr_neg')
            with open(cr_pos_path, 'r') as file:
                cr_pos_content = file.readlines()
            with open(cr_neg_path, 'r') as file:
                cr_neg_content = file.readlines()
            labeled_data = (
                [{'text': line.strip(), 'label': 'copyright'}
                 for line in cr_pos_content] +
                [{'text': line.strip(), 'label': 'non-copyright'}
                 for line in cr_neg_content]
            )
            texts = [example['text'] for example in labeled_data]
            labels = [example['label'] for example in labeled_data]
            X_train, X_test, y_train, y_test = train_test_split(
                texts, labels, test_size=0.3, random_state=42
            )
            vectorizer = TfidfVectorizer()
            X_train_tfidf = vectorizer.fit_transform(X_train)
            X_test_tfidf = vectorizer.transform(X_test)
            with open(self.tfidf_cache, 'wb') as f:
                pickle.dump((X_train_tfidf, X_test_tfidf, y_train, y_test,
                             vectorizer), f)

        if os.path.exists(self.model_cache):
            with open(self.model_cache, 'rb') as f:
                classifier = pickle.load(f)
        else:
            classifier = RandomForestClassifier()
            classifier.fit(X_train_tfidf, y_train)
            with open(self.model_cache, 'wb') as f:
                pickle.dump(classifier, f)

    def identify_year_range(self, text):
        match = re.search(self.year_range_pattern, text)
        if match:
            return match.group(1)
        return None

    def identify_statement(self, text, year_range):
        statement = text.replace('Copyright', '').replace(
            year_range, ''
        ).strip()
        return statement

    def identify_copyright(self, text):
        lines = text.splitlines()
        for line in lines:
            if 'copyright' in line.lower():
                year_range = self.identify_year_range(line)
                if year_range:
                    statement = self.identify_statement(line, year_range)
                    return year_range, statement
        return None, None

    def copyright_extraction(self, text):
        with open(self.tfidf_cache, 'rb') as f:
            _, _, _, _, vectorizer = pickle.load(f)
        with open(self.model_cache, 'rb') as f:
            classifier = pickle.load(f)
        pattern = r"[^0-9<>,.()@a-zA-Z-\s]+"
        text_inputs = [re.sub(pattern, "", line.strip().lower())
                       for line in text.splitlines()]
        input_tfidf = vectorizer.transform(text_inputs)
        predictions = classifier.predict(input_tfidf)
        results = []
        for text, prediction in zip(text_inputs, predictions):
            if (text.startswith('copyright') or " copyright" in text):
                if ("copyright " in text and len(text) <= 50 and
                        "yyyy" not in text and prediction == 'copyright'):
                    results.append({
                        "text": text,
                        "prediction": prediction
                    })
        return results


class LicenseAndCopyrightIdentifier:
    def __init__(self):
        self.license_identifier = LicenseIdentifier()
        self.copyright_identifier = CopyrightIdentifier()

    def identify_license(self, text):
        return self.license_identifier.identify_license(text)

    def identify_year_range(self, text):
        return self.copyright_identifier.identify_year_range(text)

    def identify_statement(self, text):
        return self.copyright_identifier.identify_copyright(text)

    def copyright_extraction(self, text):
        return self.copyright_identifier.copyright_extraction(text)

    def identify_copyright(self, text):
        year_range = self.identify_year_range(text)
        if year_range is None:
            return '', ''
        else:
            statement = self.identify_statement(text)
            return year_range, statement
