
import json
import random
import pyttsx3
import speech_recognition as sr


engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()


def load_knowledge_base():
    try:
        with open('knowledge_base.json', 'r') as file:
            return json.load(file)
    except OSError:
        return {}

def get_user_answer():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your answer...")
        audio = recognizer.listen(source)

    try:
        answer = recognizer.recognize_google(audio)
        print(f"You said: {answer}")
        return answer
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Please repeat your answer.")
        return get_user_answer()  # Retry
    except sr.RequestError:
        speak("Sorry, there was an error with the speech service.")
        return None


def start_quiz(knowledge_base):
    if not knowledge_base:
        speak("Sorry, there are no quiz questions available.")
        return

    question = random.choice(list(knowledge_base.keys()))
    correct_answer = knowledge_base[question]

    speak(question)

    user_answer = get_user_answer()

    if user_answer and user_answer.lower() == correct_answer.lower():
        speak("Correct!")
    else:
        speak(f"Wrong! The correct answer is {correct_answer}.")


def main():
    speak("Hello! How can I assist you today?")
    
    knowledge_base = load_knowledge_base()
    
    while True:
        user_command = get_user_answer()
        
        if user_command is None:
            continue

        if "quiz" in user_command.lower():
            start_quiz(knowledge_base)
        elif "exit" in user_command.lower() or "stop" in user_command.lower():
            speak("Goodbye!")
            break
        else:
            speak("I'm not sure about that. You can say 'start quiz' to begin.")


if __name__ == "__main__":
    main()
