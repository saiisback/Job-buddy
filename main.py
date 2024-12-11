import google.generativeai as genai
import re
import pyttsx3
import speech_recognition as sr

#---------------------------------------------------
# AI Prompt Generation
#---------------------------------------------------
genai.configure(api_key="AIzaSyCrz_SVCJ3tMEq2IXs6wdGK--jzhwB9NzE")

role = input("Enter the job role you want interview questions for: ")

prompt = """
You are an AI specialized in generating interview questions and detailed model answers for specific job roles. 

Generate a set of 10 comprehensive interview questions for the job role of {job_role} in the following format:

[
    ["Question 1", "Answer 1", "Difficulty (Beginner/Intermediate/Advanced)"],
    ["Question 2", "Answer 2", "Difficulty (Beginner/Intermediate/Advanced)"],
    ...
]

These questions should assess the candidate’s:
1. Core technical skills.
2. Problem-solving abilities.
3. Communication and teamwork skills.
4. Industry-specific knowledge.
5. Analytical and creative thinking.

Provide a balanced mix of beginner, intermediate, and advanced-level questions. Ensure all questions and answers are relevant to the specified job role, concise, and reflect current industry standards. 

Ensure the format makes it easy to sort questions, answers, and difficulty levels programmatically.
"""

model = genai.GenerativeModel("gemini-1.5-flash")

print("Generating your questions.....")

response = model.generate_content(prompt.format(job_role=role))


# Save the response to a file
info = response.text

print("Sorting the questions.....")

#---------------------------------------------------
# Extracting Questions, Answers, and Levels
#---------------------------------------------------
# Now we parse the content correctly for sorting.
# Example format: [["Question 1", "Answer 1", "Beginner"], ...]

# Assuming the response is a valid string in the format provided in the prompt
questions = []
answers = []
difficulty = []
def parse_interview_data(response_text):
    # Removing unwanted characters and splitting into manageable sections
    raw_data = re.findall(r'\["(.*?)", "(.*?)", "(.*?)"\]', response_text)

    for question, answer, diff in raw_data:
        questions.append(question)
        answers.append(answer)
        difficulty.append(diff)

    # Combine into a sorted list of tuples for easy access
    sorted_data = []
    for i in range(len(questions)):
        sorted_data.append({
            "question": questions[i],
            "answer": answers[i],
            "difficulty": difficulty[i]
        })

    return sorted_data

# Parse the response
interview_data = parse_interview_data(response.text)

# Print the sorted data
#for item in interview_data:
#    print(f"Question: {item['question']}\nAnswer: {item['answer']}\nDifficulty: {item['difficulty']}\n")

#---------------------------------------------------
# Text-to-Speech Converter
#---------------------------------------------------
def speak(audio):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Choose the first voice (if available)
    engine.say(audio)
    engine.runAndWait()

#---------------------------------------------------
# Asking Questions and Taking Answers
#---------------------------------------------------
def listen_for_answer():
    """Takes microphone input from the user and returns a string output."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        try:
            audio = recognizer.listen(source)
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-in')
            print(f"You said: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, I did not understand that. Please try again.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition; {e}")
            return None

#---------------------------------------------------
# Conducting the Interview
#---------------------------------------------------

interview_answers = []

# Now iterate through sorted interview data
for i, item in enumerate(interview_data):
    print(f"Q{i+1}: {item['question']}")
    speak(f"Question {i+1}. {item['question']}")

    user_answer = None
    while user_answer is None:
        if user_answer != None:
            user_answer = listen_for_answer()
            interview_answers.append(user_answer)
        else:
            user_answer = listen_for_answer()

    print(f"Recorded answer for this question: {user_answer}\n")
    speak("Thank you for your response.")

# Display all interview answers
print(interview_answers)

#---------------------------------------------------
# checking Answers
#---------------------------------------------------

final_answers=[]
for i in range(len(questions)):
    user_answers=[]
    user_answers.append(questions[i])
    user_answers.append(answers[i])
    user_answers.append(interview_answers[i])
    user_answers.append(difficulty[i])
    final_answers.append(user_answers)

print(final_answers)
    
    
