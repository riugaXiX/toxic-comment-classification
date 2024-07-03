import csv
from collections import defaultdict
import re

def preprocess_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip().lower().split()

word_freq = defaultdict(lambda: defaultdict(int))
doc_count = 0

with open('selected_samples.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        doc_id = doc_count
        doc_count += 1
        lemmatized_text = preprocess_text(row['lemmatized_text'])
        if lemmatized_text:
            for word in lemmatized_text:
                word_freq[doc_id][word] += 1

print(f"Total dokumen yang diproses: {doc_count}")
print(f"Total dokumen setelah preprocessing: {len(word_freq)}")

word_list = sorted(set(word for doc_freq in word_freq.values() for word in doc_freq))
word_index = {word: idx for idx, word in enumerate(word_list)}

bow_matrix = []
for doc_id, doc_freq in word_freq.items():
    vector = [doc_freq[word] for word in word_list]
    bow_matrix.append([f'Dokumen {doc_id+1}'] + vector)

vector_list = [(doc_id, word_index[word], freq) for doc_id, doc_freq in word_freq.items() for word, freq in doc_freq.items() if freq > 0]

csv_filename = 'bow_representation_with_vectors.csv'
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    writer.writerow(['Dokumen'] + word_list)
    for row in bow_matrix:
        writer.writerow(row)

    writer.writerow([])
    writer.writerow(['Dokumen_Index', 'Kata_Index', 'Frekuensi'])
    for vec in vector_list:
        writer.writerow(vec)

print(f"File CSV '{csv_filename}' telah berhasil dibuat.")
print(f"Total dokumen dalam BoW: {len(bow_matrix)}")
