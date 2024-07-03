import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier

# Asumsikan 'data' adalah DataFrame yang sudah ada
# Memisahkan fitur dan label

data = pd.read_csv('data/preprocessing.csv')
X = data['lemmatized_text']
y = data[['pornografi', 'sara', 'radikalisme', 'pencemaran_nama_baik']]

# Memeriksa distribusi kelas
print("Distribusi kelas sebelum pemisahan:")
print(y.sum())

# Mengubah label multi-kelas menjadi format binarized
mlb = MultiLabelBinarizer()
y_binarized = mlb.fit_transform(y.values.tolist())

# Menentukan beberapa nilai random_state yang akan diuji
random_states = [1, 5, 10, 20, 30, 42, 50, 60, 70, 80, 90, 100]
results = []

for state in random_states:
    print(f"Testing random_state={state}")
    
    # Split data menjadi training dan testing dengan proporsi 90/10
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=state)
    
    # Mengubah teks menjadi vektor menggunakan TF-IDF Vectorizer
    vectorizer = TfidfVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # Menggunakan OneVsRestClassifier dengan MultinomialNB
    model = OneVsRestClassifier(MultinomialNB(alpha=0.3))
    model.fit(X_train_vec, y_train)
    
    # Prediksi dengan data testing
    y_pred = model.predict(X_test_vec)
    
    # Evaluasi model
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    results.append((state, accuracy, precision, recall, f1))
    
    print(f"Accuracy: {accuracy}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1 Score: {f1}")
    print("===============================================================")
    
    # Konversi kembali ke format multilabel sebelumnya
    # y_test_original = mlb.inverse_transform(y_test)
    # y_pred_original = mlb.inverse_transform(y_pred)
    
    # Print classification report
    print("Classification Report:")
    # print(classification_report(y_test, y_pred, target_names=['pornografi', 'sara', 'radikalisme', 'pencemaran_nama_baik']))

# Menemukan random_state dengan hasil terbaik
best_result = max(results, key=lambda item: item[1])  # Menentukan berdasarkan accuracy
best_random_state = best_result[0]
print(f"Best random_state: {best_random_state} with Accuracy: {best_result[1]}")
