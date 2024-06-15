from sentence_transformers import SentenceTransformer, util
import spacy

# Load spaCy model for keyword extraction
nlp = spacy.load("en_core_web_sm")

# Function to extract keywords from text using Noun and Proper Nouns
def extract_keywords(text):
    doc = nlp(text)
    keywords = [token.text.lower() for token in doc if token.pos_ in ['NOUN', 'PROPN']]
    return set(keywords)

# Load the Sentence Transformer model
model = SentenceTransformer("sentence-transformers/distilbert-base-nli-mean-tokens")

expected_answers = [
    "Depression is a mental health disorder characterized by persistent sadness and a lack of interest or pleasure in activities.",
    "Depression is a condition where individuals feel overwhelmingly sad and hopeless for extended periods.",
    "Depression is a serious medical condition that negatively affects how you feel, the way you think, and how you act."
]

expected_keywords = [extract_keywords(answer) for answer in expected_answers]

# Example of student's response
student_response = "Depression is a serious mental health disorder characterized by persistent sadness, loss of interest in activities, and a range of physical and emotional symptoms that interfere with daily functioning."
# Compute embeddings for expected answers
expected_embeddings = model.encode(expected_answers)

# Compute embedding for the student's response
student_embedding = model.encode(student_response)

# Initialize similarity threshold
similarity_threshold = 0.6  # Adjust this based on your criteria

# Check similarities and keyword presence
is_correct = False
overall_similarity_scores = []
for idx, (expected_embedding, expected_keyword_set) in enumerate(zip(expected_embeddings, expected_keywords)):
    similarity = util.pytorch_cos_sim(student_embedding, expected_embedding)
    similarity_score = similarity.item()

    # Extract keywords from the student's response and calculate match percentage
    response_keywords = extract_keywords(student_response)
    keyword_match = response_keywords.intersection(expected_keyword_set)
    keyword_match_score = len(keyword_match) / len(expected_keyword_set) if expected_keyword_set else 0

    # Combine similarity score and keyword match score
    overall_score = (similarity_score + keyword_match_score) / 2
    overall_similarity_scores.append(overall_score)

    # Determine correctness based on combined score
    if overall_score > similarity_threshold:
        is_correct = True

# Print results
print(f"Student's Response: '{student_response}'")
print("Overall Evaluation with Expected Answers:")
for i, score in enumerate(overall_similarity_scores):
    print(f"  Answer {i+1}: Combined Score = {score:.4f}")

if is_correct:
    print("The student's answer is considered correct based on combined scoring.")
else:
    print("The student's answer does not match the expected criteria based on combined scoring.")
