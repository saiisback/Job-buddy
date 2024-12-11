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
You are an AI specialized in generating interview questions and model answers for specific job roles. I need a set of 10 comprehensive interview questions along with detailed answers for the job role of {job_role}. These questions should assess the candidate’s:
1. Core technical skills.
2. Problem-solving abilities.
3. Communication and teamwork skills.
4. Industry-specific knowledge.
5. Analytical and creative thinking.

Provide a mix of beginner, intermediate, and advanced-level questions. Format the output as follows:

1. Question: <Insert question>
   Answer: <Insert detailed answer>
   Level: <Beginner/Intermediate/Advanced>

Ensure the questions and answers are relevant to the given role, reflect current industry standards, and are concise yet informative.
"""

response = genai.generate_text(model="gemini-1.5-flash", prompt=prompt.format(job_role=role))

# Save the response to a file
file_name = "info.txt"
with open(file_name, "w") as file:
    file.write(response.result)

print("Questions and answers saved to info.txt")

#---------------------------------------------------
# Extracting Questions, Answers, and Levels
#---------------------------------------------------
# Read the content of the file
with open(file_name, "r") as file:
    text = file.read()

# Regex patterns to extract data
question_pattern = r'Question:\s*(.*?)\n\s*Answer:'
answer_pattern = r'Answer:\s*(.*?)\n\s*Level:'
level_pattern = r'Level:\s*(\w+)'

# Extracting data using regex
questions = re.findall(question_pattern, text, re.DOTALL)
answers = re.findall(answer_pattern, text, re.DOTALL)
levels = re.findall(level_pattern, text)

# Cleaning up white spaces
questions = [q.strip() for q in questions]
answers = [a.strip() for a in answers]
levels = [l.strip() for l in levels]

print("Questions, answers, and levels extracted.")

#---------------------------------------------------
# Text-to-Speech Converter
#---------------------------------------------------
def speak(audio):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Choose the second voice (if available)
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
def conduct_interview():
    for i, question in enumerate(questions):
        print(f"Q{i+1}: {question}")
        speak(f"Question {i+1}. {question}")

        user_answer = None
        while user_answer is None:
            user_answer = listen_for_answer()

        print(f"Your Answer: {user_answer}\n")
        speak("Thank you for your response.")

# Start the interview
conduct_interview()
