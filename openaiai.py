from openai import OpenAI
from read_image import seperate
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

def create_pdf(file_path, questions, teacher_answers, student_answers, grades):
    # Set up the document
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    question_style = ParagraphStyle(
        name='QuestionStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold'
    )
    
    answer_style = ParagraphStyle(
        name='AnswerStyle',
        parent=styles['Normal'],
        fontName='Helvetica'
    )
    
    grade_style = ParagraphStyle(
        name='GradeStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique'
    )
    
    # Story to hold the elements
    story = []
    
    # Add questions, answers, and grades to the story
    for i in range(len(questions)):
        # Question
        question = Paragraph(f"<b>{questions[i]}</b>", question_style)
        story.append(question)
        story.append(Spacer(1, 12))
        
        # Teacher's Answer
        teacher_answer = Paragraph(f"Teacher's Answer: {teacher_answers[i]}", answer_style)
        story.append(teacher_answer)
        story.append(Spacer(1, 12))
        
        # Student's Answer
        student_answer = Paragraph(f"Student's Answer: {student_answers[i]}", answer_style)
        story.append(student_answer)
        story.append(Spacer(1, 12))
        
        # Grade
        grade = Paragraph(f"<i>Grade: {grades[i]}</i>", grade_style)
        story.append(grade)
        story.append(Spacer(1, 24))  # Extra space before the next question
    
    # Build the PDF
    doc.build(story)

def create_raport(empty_path, teacher_path, student_path):
    client = OpenAI(
        api_key='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'
    )

    questions, teacher_answers = seperate(empty_path, teacher_path)
    questions_2, student_answers = seperate(empty_path,student_path)
    grades = []
    output_string = ''
    for i, item in enumerate(questions):
        # print("Question:", item)
        # print("Teacher:", teacher_answers[i])
        # print("Student:", student_answers[i])
        messages = [
            {"role": "system", "content": "You are a teacher assistant, responsible for evaluating student responses."},
            {"role": "user", "content": f"Question: {item}"},
            {"role": "user", "content": f"Teacher's answer: {teacher_answers[i]}"},
            {"role": "user", "content": f"Student's answer: {student_answers[i]}"},
            {"role": "system", "content": "Evaluate how much the student's response covers the question and how it connects to the expected answer provided by the teacher. Provide a percentage value and a brief summary in one, mostly two sentences."}
        ]
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=1000
        )
        
        
        for choice in response.choices:
            # output_string += f'Question {i}: {item}\nCorrect Answer {i}: {teacher_answers[i]}\nStudent Answer{i}: {student_answers[i]}\nGrade: {choice.message.content}'
            grades.append(choice.message.content)
    # print(output_string)
    # create_pdf(output_string, './raport.pdf')
    create_pdf('uploads/raport.pdf', questions, teacher_answers, student_answers, grades)