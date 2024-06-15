from PyPDF2 import PdfReader
from fpdf import FPDF

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
        
    return text

def parse_questions_answers(qa_text):
    questions = []
    answers = []
    
    qa_text = (qa_text.replace("Question:", '')).strip().split("\n\n")
    
    for qa in qa_text:
        if "Answer:" in qa:
            question, answer = qa.split("Answer:", 1)
            questions.append(question.strip())
            answers.append(answer.strip())
    
    return questions, answers

def create_questions_answers_pdf(questions, answers, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    for i, (question, answer) in enumerate(zip(questions, answers)):
        pdf.set_font("Arial", style='B', size=12)
        pdf.multi_cell(0, 10, f"{question}")
        
        pdf.set_font("Arial", style='I', size=12)
        pdf.multi_cell(0, 10, answer)
        
        pdf.cell(0, 10, "", ln=True)
    
    pdf.output(filename)

def create_questions_only_pdf(questions, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    for i, question in enumerate(questions):
        pdf.set_font("Arial", style='B', size=12)
        pdf.multi_cell(0, 10, f"{question}")
        
        pdf.set_font("Arial", style='I', size=12)
        pdf.multi_cell(0, 10, "")
        
        pdf.cell(0, 10, "", ln=True)
    
    pdf.output(filename)

