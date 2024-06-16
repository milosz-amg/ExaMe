from openai import OpenAI
from read_image import seperate, create_pdf


def create_raport(empty_exam, teacher_answers, student_answers):
    client = OpenAI(
        api_key='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'
    )

    questions, teacher_answers = seperate(empty_exam, teacher_answers)
    questions_2, student_answers = seperate(empty_exam,student_answers)
    
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
            output_string += f'Question{i}: {item}\nCorrect Answer{i}: {teacher_answers[i]}\nStudent Answer{i}: {student_answers[i]}\nGrade: {choice.message.content}'
        
    print(output_string)
    create_pdf(output_string, 'uploads/raport.pdf')

#create_raport('exam_pdfs/exam_questions_only.pdf', 'exam_pdfs/exam_teacher_answers.pdf', 'exam_pdfs/exam_teacher_answers.pdf')
        