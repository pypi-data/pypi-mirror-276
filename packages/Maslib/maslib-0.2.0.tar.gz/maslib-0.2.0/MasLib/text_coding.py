import pandas as pd
import matplotlib.pyplot as plt
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation, NMF, TruncatedSVD
from wordcloud import WordCloud
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    """
    Eng:Text preprocessing: punctuation marks removal, tokenization, stop word removal and lemmatization.
    Fra:Prétraitement du texte: suppression des signes de ponctuation, tokenisation, suppression des mots vides et lemmatisation.
    Rus:Предобработка текста: удаление знаков препинания, токенизация, удаление стоп-слов и лемматизация.
    Ger:Textvorverarbeitung: Interpunktionszeichen entfernen, Tokenisieren, Stoppwörter entfernen und Lemmatisieren.
    """
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens if token.isalpha() and token.lower() not in stop_words]
    return ' '.join(tokens)

def vectorize_text(documents_df, text_column, stop_words='english', max_df=0.95, min_df=2):
    """
    Eng: Text transformation into vector representation using CountVectorizer.
    Fra: Transformation des textes en représentation vectorielle en utilisant CountVectorizer.
    Rus: Преобразование текстов в векторное представление с использованием CountVectorizer.
    Ger: Umwandlung von Texten in Vektorrepräsentationen mit CountVectorizer.
    """
    documents_df[text_column] = documents_df[text_column].apply(preprocess_text)
    vectorizer = CountVectorizer(stop_words=stop_words, max_df=max_df, min_df=min_df)
    X = vectorizer.fit_transform(documents_df[text_column])
    return X, vectorizer

def tfidf_vectorize_texts(df, text_column, stop_words='english'):
    """
    Eng: Text vectorization using TfidfVectorizer.
    Fra: Vectorisation des textes à l'aide de TfidfVectorizer.
    Rus: Векторизация текстов с помощью TfidfVectorizer.
    Ger: Textvektorisierung mit TfidfVectorizer.
    """
    df[text_column] = df[text_column].apply(preprocess_text)
    vectorizer = TfidfVectorizer(stop_words=stop_words)
    tfidf_vectors = vectorizer.fit_transform(df[text_column])
    feature_names = vectorizer.get_feature_names_out()
    tfidf_df = pd.DataFrame(tfidf_vectors.toarray(), columns=feature_names)
    return tfidf_df

def lda_model(documents_df, text_column, stop_words='english', n_components=5, random_state=42):
    """
    Eng: Topic modeling using Latent Dirichlet Allocation (LDA).
    Fra: Modélisation thématique à l'aide de Latent Dirichlet Allocation (LDA).
    Rus: Тематическое моделирование с использованием Latent Dirichlet Allocation (LDA).
    Ger: Themenmodellierung mit Latent Dirichlet Allocation (LDA).
    """
    X, vectorizer = vectorize_text(documents_df, text_column, stop_words)
    lda = LatentDirichletAllocation(n_components=n_components, random_state=random_state)
    lda.fit(X)

    for topic_idx, topic in enumerate(lda.components_):
        print(f"Topic {topic_idx + 1}:")
        print(" ".join([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-10 - 1:-1]]))
        print()

    for topic_idx, topic in enumerate(lda.components_):
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(
            ' '.join([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-10 - 1:-1]]))
        plt.figure(figsize=(8, 4))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title(f'Topic {topic_idx + 1} Word Cloud')
        plt.axis('off')
        plt.show()

def nmf_model(documents_df, text_column, stop_words='english', n_components=5, random_state=42):
    """
    Eng: Topic modeling using Non-Negative Matrix Factorization (NMF).
    Fra: Modélisation thématique à l'aide de la factorisation en matrices non négatives (NMF).
    Rus: Тематическое моделирование с использованием Non-Negative Matrix Factorization (NMF).
    Ger: Themenmodellierung mit Non-Negative Matrix Factorization (NMF).
    """
    X, vectorizer = vectorize_text(documents_df, text_column, stop_words)
    nmf = NMF(n_components=n_components, random_state=random_state)
    nmf.fit(X)

    for topic_idx, topic in enumerate(nmf.components_):
        print(f"Topic {topic_idx + 1}:")
        print(" ".join([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-10 - 1:-1]]))
        print()

    for topic_idx, topic in enumerate(nmf.components_):
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(
            ' '.join([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-10 - 1:-1]]))
        plt.figure(figsize=(8, 4))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title(f'Topic {topic_idx + 1} Word Cloud')
        plt.axis('off')
        plt.show()

def lsa_model(documents_df, text_column, stop_words='english', n_components=5, random_state=42):
    """
    Eng: Topic modeling using Latent Semantic Analysis (LSA).
    Fra: Modélisation thématique à l'aide de l'analyse sémantique latente (LSA).
    Rus: Тематическое моделирование с использованием Latent Semantic Analysis (LSA).
    Ger: Themenmodellierung mit Latent Semantic Analysis (LSA).
    """
    X, vectorizer = vectorize_text(documents_df, text_column, stop_words)
    lsa = TruncatedSVD(n_components=n_components, random_state=random_state)
    lsa.fit(X)

    for topic_idx, topic in enumerate(lsa.components_):
        print(f"Topic {topic_idx + 1}:")
        print(" ".join([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-10 - 1:-1]]))
        print()

    for topic_idx, topic in enumerate(lsa.components_):
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(
            ' '.join([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-10 - 1:-1]]))
        plt.figure(figsize=(8, 4))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title(f'Topic {topic_idx + 1} Word Cloud')
        plt.axis('off')
        plt.show()

def elbow_method_tfidf(df, text_column, stop_words='english', k_range=range(2, 11)):
    """
    Eng: The elbow method for selecting the optimal number of clusters using TF-IDF.
    Fra: La méthode du coude pour choisir le nombre optimal de clusters en utilisant TF-IDF.
    Rus: Метод локтя для выбора оптимального количества кластеров с использованием TF-IDF.
    Ger: Die Ellbogenmethode zur Auswahl der optimalen Anzahl von Clustern unter Verwendung von TF-IDF.
    """
    tfidf_df = tfidf_vectorize_texts(df, text_column, stop_words)
    scaler = StandardScaler()
    scaled_tfidf = scaler.fit_transform(tfidf_df)
    
    silhouette_scores = []
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans_labels = kmeans.fit_predict(scaled_tfidf)
        silhouette_score_avg = silhouette_score(scaled_tfidf, kmeans_labels)
        silhouette_scores.append(silhouette_score_avg)
    
    plt.plot(k_range, silhouette_scores, marker='o', linestyle='--', color='b')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Silhouette Score')
    plt.title('Elbow Method for Optimal Number of Clusters')
    plt.xticks(k_range)
    plt.grid(True)
    plt.show()


def sentiment_analysis(df, text_column,language='english'):
    """
    Eng: Example of sentiment analysis using a simple SVM classifier.
    Fra: Exemple d'analyse des sentiments à l'aide d'un simple classificateur SVM.
    Rus: Пример анализа настроений с использованием простого классификатора SVM.
    Ger: Beispiel für die Stimmungsanalyse mit einem einfachen SVM-Klassifikator.
    """
    df[text_column] = df[text_column].apply(preprocess_text)
    vectorizer = TfidfVectorizer(stop_words=language)
    X = vectorizer.fit_transform(df[text_column])
    y = df['sentiment']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = Pipeline([('classifier', SVC(kernel='linear', random_state=42))])
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    print(classification_report(y_test, y_pred))

def lda_topic_modeling(df, column_name, stop_words='english'):
    """
    Eng: Topic modeling using Latent Dirichlet Allocation (LDA).
    Fra: Modélisation thématique à l'aide de Latent Dirichlet Allocation (LDA).
    Rus: Тематическое моделирование с использованием Latent Dirichlet Allocation (LDA).
    Ger: Themenmodellierung mit Latent Dirichlet Allocation (LDA).
    """
    df[column_name] = df[column_name].apply(preprocess_text)
    vectorizer = TfidfVectorizer(stop_words=stop_words, max_df=0.9, min_df=0.2)
    data_text_modeling = vectorizer.fit_transform(df[column_name])
    
    lda = LatentDirichletAllocation(n_components=10, random_state=42)
    lda.fit(data_text_modeling)
    
    tsne_model = TSNE(n_components=2, init='random')
    tsne_results = tsne_model.fit_transform(data_text_modeling)
    
    plt.scatter(tsne_results[:, 0], tsne_results[:, 1])
    plt.show()
    
    for topic_idx, topic in enumerate(lda.components_):
        print(f"Topic {topic_idx + 1}:")
        print(" ".join([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-10 - 1:-1]]))
        print()
    
    for topic_idx, topic in enumerate(lda.components_):
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join([vectorizer.get_feature_names_out()[i] for i in topic.argsort()[:-10 - 1:-1]]))
        plt.figure(figsize=(8, 4))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title(f'WorldCloud Topic {topic_idx + 1}')
        plt.axis('off')
        plt.show()


