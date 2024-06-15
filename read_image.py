from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import time

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Frame, PageBreak

BLNK_QUIZ = "images/blank_quiz.jpg"
ANSWERED_QUIZ = "images/quiz.jpg"
OUTPUT_FILE="output.pdf"

def write_string_to_txt(file_path, text):
    with open(file_path, 'w') as file:
        file.write(text)

def read_txt_to_string(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    return lines

def remove_empty_strings(items):
    return [item for item in items if item]

def create_pdf(input_text, output_pdf_file):
    # Create a SimpleDocTemplate object
    doc = SimpleDocTemplate(output_pdf_file, pagesize=letter)
    width, height = letter
    
    # Get a sample stylesheet
    styles = getSampleStyleSheet()
    style = styles["BodyText"]
    
    # Split the input text into paragraphs
    lines = input_text.split('\n')
    
    # Create a list of Paragraph objects
    story = []
    for line in lines:
        if line.strip():  # Only add non-empty lines
            para = Paragraph(line.strip(), style)
            story.append(para)
        story.append(Paragraph("<br/>", style))  # Add a line break for spacing
    
    # Build the PDF
    doc.build(story)

def read_image(image_path):
    subscription_key = "7370e520ed3547a6b7d1d7a555c2ec12"
    endpoint = "https://exame.cognitiveservices.azure.com/"
    client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    # image
    local_image_path = image_path

    # Read the image file into a stream
    with open(local_image_path, "rb") as image_stream:
        read_response = client.read_in_stream(image_stream, raw=True)

    # Get the operation location (URL with an ID at the end)
    read_operation_location = read_response.headers["Operation-Location"]
    operation_id = read_operation_location.split("/")[-1]

    # Loop for active waiting for azure response
    while True:
        read_result = client.get_read_result(operation_id)
        if read_result.status.lower() not in ['notstarted', 'running']:
            break
        print('Waiting for result...')
        time.sleep(10)

    #text printer (will change later to interact with it)
    text = []
    if read_result.status == "succeeded":
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                text.append(line.text)

    # print(text)
    return(text)

# text_blank = read_txt_to_string("blank_to_text.txt")
# text_quiz_solved = read_txt_to_string("answer_to_text.txt")

text_blank= read_image("images/quiz_empty.png")
text_quiz_solved = read_image("images/quiz.jpg")
answers_handwritten=[]
questions_lines=[]

for line in text_quiz_solved:
    if line not in text_blank:
        answers_handwritten.append(line.strip())

for line in text_blank:
    if line not in answers_handwritten:
        questions_lines.append(line.strip())

single_question=""
single_answer=""
questions=[]
answers=[]

text_quiz_solved_cp = text_quiz_solved.copy()
while text_quiz_solved_cp:
    line = text_quiz_solved_cp.pop(0)
    line = line.strip()
    if line not in answers_handwritten:
        single_question+=line
    else:
        questions.append(single_question)
        single_question=""
questions.append(single_question)
questions = remove_empty_strings(questions)

text_quiz_solved_cp.clear()
text_quiz_solved_cp = text_quiz_solved.copy()

while text_quiz_solved_cp:
    line = text_quiz_solved_cp.pop(0)
    line = line.strip()
    if line not in questions_lines:
        single_answer+=line
    else:
        answers.append(single_answer)
        single_answer=""
answers.append(single_answer)
answers = remove_empty_strings(answers)


n = len(questions)
ouput_string=""
for i in range(n):
    ouput_string+="Q"+str(i+1)+":\n"+questions[i]+"\nA"+str(i+1)+":\n"+answers[i]+"\n"

# print(text_blank)
# print(text_quiz_solved)
# print(ouput_string)

create_pdf(ouput_string,OUTPUT_FILE)