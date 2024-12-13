print("System is booting up.")

import google.generativeai as genai
import re
import pyttsx3
import speech_recognition as sr

#---------------------------------------------------
# AI Prompt Generation
#---------------------------------------------------
genai.configure(api_key="AIzaSyCrz_SVCJ3tMEq2IXs6wdGK--jzhwB9NzE")

print("starting the Ai")

role = input("Enter the job role you want interview questions for: ")
name = input("Enter the name of the candidate:")

prompt = """
You are an AI specialized in generating interview questions and detailed model answers for specific job roles. 
 
Generate a set of 5 comprehensive interview questions for the job role of {job_role} in the following format:

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

print(info)

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
print("Hope you are ready for the interview")
speak(f"hello {name}, how are you?, we are starting the question")
for i, item in enumerate(interview_data):
    print(f"Q{i+1}: {item['question']}")
    speak(f"Question {i+1}. {item['question']}")

    user_answer = None
    while user_answer is None:
        user_answer = listen_for_answer()
        interview_answers.append(user_answer)

    print(f"Recorded answer for this question: {user_answer}\n")
    speak("Thank you for your response.")

# Display all interview answers
print(interview_answers)

#---------------------------------------------------
# checking Answers
#---------------------------------------------------

for i in interview_answers:
    if i ==None:
        list.remove(i)
    else:
        pass

print(interview_answers)

final_answers=[]
for i in range(len(questions)):
    user_answers=[]
    user_answers.append(questions[i])
    user_answers.append(answers[i])
    user_answers.append(interview_answers[i])
    user_answers.append(difficulty[i])
    final_answers.append(user_answers)

print(f"Good work {name}.for completing the interview")

candidate_final_answers=f"here are the answers {name} gave for the job {role} \n"
for i in final_answers:
    each_answer="question:"+i[0]+"\n"+"expected answer:"+i[1]+"\n"+"User answers:"+i[2]+"\n"+"diffculty:"+i[3]+"\n"
    candidate_final_answers += each_answer

print(candidate_final_answers)

print("Analysing your interview....")
print("Generating the feedback....")

feedbackprompt ='''
Review the following interview responses provided by the candidate, for a series of technical and behavioral questions. Evaluate each response against the expected answers provided, offering constructive and detailed feedback that the candidate can use to understand exactly where they fell short.  

For each question, provide the following:  
1. Feedback on the Response: 
   - Identify key areas of weakness, such as lack of knowledge, poor articulation, or missing details.  
   - Compare the candidate's answer to the expected answer, highlighting gaps and inaccuracies.  

2. Suggestions for Improvement: 
   - Explain how the candidate could have answered better.  
   - Offer specific advice or frameworks they can use to approach similar questions in the future.  

3. Skill Assessment: 
   - Rate the candidate's proficiency level (e.g., Beginner, Intermediate, Advanced) for the specific topic of the question.  

4. Role Compatibility: 
   - Based on their answers, assess their overall suitability for the role they are aiming for.  

5. Mentorship Advice:
   - Provide actionable tips for improvement, including resources (books, courses, websites, or tools) and strategies for gaining the required skills and confidence.  

Ensure that the feedback is detailed, supportive, and written in a way that the candidate can clearly understand their shortcomings and how to address them.  

Input:  
Here are the answers user gave:  
{answers}  

Output Format: 
- Question: [Insert Question]  
- Expected Answer Summary: [Insert Expected Answer Summary]  
- Candidate’s Answer: [Insert Candidate’s Answer]  
- Feedback:  [Detailed feedback here]  
- Suggestions for Improvement:  [Suggestions here]  
- Skill Assessment: [Beginner/Intermediate/Advanced]  
- Role Compatibility: [Insert Evaluation]  
- Mentorship Advice:  [Actionable steps here]  

Use a clear and encouraging tone to provide feedback, ensuring the candidate feels motivated to improve.
'''

feedbackresponse = model.generate_content(feedbackprompt.format(answers=candidate_final_answers))

print(feedbackresponse.text)
speak(feedbackresponse.text)

