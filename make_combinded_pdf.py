from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_pdf(input_text_file, output_pdf_file):
    # Read the content of the input text file
    with open(input_text_file, 'r') as file:
        text = file.read()
    
    # Create a canvas object
    c = canvas.Canvas(output_pdf_file, pagesize=letter)
    width, height = letter
    
    # Set the starting position of the text
    x = 72  # 1 inch from the left
    y = height - 72  # 1 inch from the top
    
    # Set the font and size
    c.setFont("Helvetica", 12)
    
    # Draw the text line by line
    for line in text.split('\n'):
        c.drawString(x, y, line)
        y -= 14  # Move to the next line (12 points font size + 2 points spacing)
    
    # Save the PDF
    c.save()

# Define input and output files
input_text_file = 'input.txt'
output_pdf_file = 'output.pdf'

# Create the PDF
create_pdf(input_text_file, output_pdf_file)
