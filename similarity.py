from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')

# Example sentences (answers)
answer1 = "Depression is a mental health disorder characterized by persistent sadness and a lack of interest or pleasure in activities."
answer2 = "Depression is a condition where individuals experience prolonged periods of sadness and hopelessness."

# Tokenize sentences into words
tokens1 = word_tokenize(answer1.lower())
tokens2 = word_tokenize(answer2.lower())

# Train Word2Vec model
model = Word2Vec([tokens1, tokens2], vector_size=100, window=5, min_count=1, sg=1)

# Calculate cosine similarity between average word vectors
vector1 = sum(model.wv[word] for word in tokens1) / len(tokens1)
vector2 = sum(model.wv[word] for word in tokens2) / len(tokens2)

similarity = model.wv.cosine_similarities(vector1, [vector2])[0]
print(f"Word2Vec cosine similarity: {similarity}")
