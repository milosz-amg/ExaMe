from openai import OpenAI
from questions_generating.functions_to_generate_pdf import *

def generate_questions_answers(pdf_text):
    client = OpenAI(
        api_key='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'
    )
    
    messages = [
        {"role": "system", "content": "You are a teacher assistant, responsible for preparing exam questions."},
        {"role": "user", "content": f"Teacher's answer: {pdf_text}"},
        {"role": "system", "content": "Based on given content, create 10 exam questions with perfect answers. Each answer should be about 25-30 words."}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1000
    )
    
    for choice in response.choices:
        qa_pair = choice.message.content
        
    return parse_questions_answers(qa_pair.replace('*', ''))

pdf_path = "questions_generating/presentations/anxiety.pdf"

# Prepare context for chat
extracted_text = extract_text_from_pdf(pdf_path)
questions, answers = generate_questions_answers(extracted_text)

# Generating pdf's
questions_answers_pdf = "questions_generating/exams/Exam_questions_with_answers.pdf"
create_questions_answers_pdf(questions, answers, questions_answers_pdf)

questions_only_pdf = "questions_generating/exams/Exam_questions_only.pdf"
create_questions_only_pdf(questions, questions_only_pdf)

