from flask import Flask, request, send_from_directory, redirect, render_template, url_for
import os
from questions_generating.generate_question import generate_questions_answers, create_questions_answers_pdf, create_questions_only_pdf, extract_text_from_pdf
from openaiai import create_raport


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Route for the home page
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/create-exam', methods=['GET', 'POST'])
def create_exam():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'exam_pdf' not in request.files:
            return redirect(request.url)
        file = request.files['exam_pdf']

        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return redirect(request.url)
        else:
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(pdf_path)

            # Prepare context for chat
            extracted_text = extract_text_from_pdf(pdf_path)
            questions, answers = generate_questions_answers(extracted_text)

            # Generating PDFs
            questions_answers_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'Exam_questions_with_answers.pdf')
            questions_only_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'Exam_questions_only.pdf')
            create_questions_answers_pdf(questions, answers, questions_answers_pdf_path)
            create_questions_only_pdf(questions, questions_only_pdf_path)

            return send_from_directory(directory=app.config['UPLOAD_FOLDER'], path='Exam_questions_only.pdf', as_attachment=True)

    return render_template('create_exam.html')

# Route for Exams Grader
@app.route('/exams-grader', methods=['GET', 'POST'])
def exams_grader():
    if request.method == 'POST':
        # Handle file uploads and the logic here
        if 'empty_exam' not in request.files or 'teacher_images' not in request.files or 'student_images' not in request.files:
            return redirect(request.url)
        empty_file = request.files['empty_exam']
        teacher_file = request.files['teacher_images']
        student_file = request.files['student_images']

        # If the user does not select a file, the browser submits an empty file without a filename
        if empty_file.filename == '' or teacher_file.filename == '' or student_file.filename == '':
            return redirect(request.url)
        else:
            empty_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], empty_file.filename)
            empty_file.save(empty_pdf_path)
            teacher_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], teacher_file.filename)
            teacher_file.save(teacher_pdf_path)
            student_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], student_file.filename)
            student_file.save(student_pdf_path)

            create_raport(empty_pdf_path, teacher_pdf_path, student_pdf_path)

            return send_from_directory(directory=app.config['UPLOAD_FOLDER'], path='raport.pdf', as_attachment=True)

    return render_template('exams_grader.html')
    

if __name__ == '__main__':
    app.run(debug=True)
