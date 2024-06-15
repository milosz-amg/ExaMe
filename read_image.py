from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import time

subscription_key = "7370e520ed3547a6b7d1d7a555c2ec12"
endpoint = "https://exame.cognitiveservices.azure.com/"
client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# image
local_image_path = 'img.png'

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
text = ''
if read_result.status == "succeeded":
    for text_result in read_result.analyze_result.read_results:
        for line in text_result.lines:
            text += line.text + '\n'

print(text)
