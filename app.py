from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Route for the home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for Exams Grader
@app.route('/exams-grader', methods=['GET', 'POST'])
def exams_grader():
    if request.method == 'POST':
        # Handle file uploads and the logic here
        return redirect(url_for('exams_grader'))
    return render_template('exams_grader.html')

# Route for Create Exam
@app.route('/create-exam', methods=['GET', 'POST'])
def create_exam():
    if request.method == 'POST':
        # Handle file uploads and the logic here
        return redirect(url_for('create_exam'))
    return render_template('create_exam.html')

if __name__ == '__main__':
    app.run(debug=True)
