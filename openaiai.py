from openai import OpenAI

client = OpenAI(
    api_key='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'
)

exam = [
    {
        "question": "What is obsessive-compulsive disorder (OCD)?",
        "teacher_answer": "OCD is a mental disorder characterized by recurring unwanted thoughts (obsessions) and repetitive behaviors or mental acts (compulsions) that a person feels compelled to perform.",
        "student_answer": "Obsessive-compulsive disorder (OCD) is a mental health condition where individuals experience recurring thoughts or obsessions that lead to repetitive behaviors or compulsions. These compulsions are often performed to alleviate anxiety or distress caused by the obsessions, but they can significantly interfere with daily life and relationships."
    },
    {
        "question": "Describe symptoms of major depressive disorder.",
        "teacher_answer": "Major depressive disorder includes persistent feelings of sadness, loss of interest in activities once enjoyed, changes in appetite or weight, sleep disturbances, fatigue, feelings of worthlessness, and thoughts of death or suicide.",
        "student_answer": "Major depressive disorder is a mental illness characterized by persistent feelings of sadness or emptiness, loss of interest in activities, changes in appetite or sleep patterns, fatigue, difficulty concentrating, and thoughts of suicide. It affects how a person feels, thinks, and behaves, often requiring treatment such as therapy or medication."
    },
    {
        "question": "What is schizophrenia?",
        "teacher_answer": "Schizophrenia is a chronic mental disorder characterized by distorted thinking, hallucinations, delusions, disorganized speech, and impaired emotional responses.",
        "student_answer": "Schizophrenia is a mental disorder that causes people to have hallucinations and delusions. It affects their ability to think clearly and manage emotions, impacting their daily life and relationships."
    },
    {
        "question": "Define bipolar disorder.",
        "teacher_answer": "Bipolar disorder is a mood disorder marked by extreme mood swings that include emotional highs (mania or hypomania) and lows (depression).",
        "student_answer": "Bipolar disorder is when someone has multiple personalities and changes from one to another rapidly."
    },
    {
        "question": "What are the symptoms of generalized anxiety disorder (GAD)?",
        "teacher_answer": "GAD involves excessive worry and anxiety about various aspects of life, often accompanied by physical symptoms like restlessness, fatigue, difficulty concentrating, muscle tension, and sleep disturbances.",
        "student_answer": "Generalized anxiety disorder is a condition where people are overly tidy and organized, feeling uncomfortable when things are out of place."
    }
]

for item in exam:
    messages = [
        {"role": "system", "content": "You are a teacher assistant, responsible for evaluating student responses."},
        {"role": "user", "content": f"Question: {item['question']}"},
        {"role": "user", "content": f"Teacher's answer: {item['teacher_answer']}"},
        {"role": "user", "content": f"Student's answer: {item['student_answer']}"},
        {"role": "system", "content": "Evaluate how much the student's response covers the question and how it connects to the expected answer provided by the teacher. Provide a percentage value and a brief summary in one, mostly two sentences."}
    ]
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1000
    )

    for choice in response.choices:
        print(choice.message.content)
