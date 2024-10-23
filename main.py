from string import ascii_lowercase
import random
import pathlib
import tomllib
import tomli as tomllib
import tkinter as tk
from tkinter import scrolledtext
import sys

NUM_QUESTIONS_PER_QUIZ = 5
QUESTIONS_PATH = pathlib.Path(__file__).parent / "questions.toml"

collection_name = "interview_questions"

class RedirectedOutput:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)  # Automatically scroll to the bottom

    def flush(self):
        pass  # Required for compatibility, does nothing

# get answer prints the question, as well as all the options for the question
#It prompts the user for their choice and validates the input to ensure it is one of the available options
#it then returns the selected answer
def get_answer(question, alternatives):
    print(f"{question}?")
    labeled_alternatives = dict(zip(ascii_lowercase, alternatives))
    for label, alternative in labeled_alternatives.items():
        print(f"  {label}) {alternative}")

    while (answer_label := input("\nChoice? ")) not in labeled_alternatives:
        print(f"Please answer one of {', '.join(labeled_alternatives)}")

    return labeled_alternatives[answer_label]


# prepare questions loads the questions into the code from the file as well as makes sure that there are the proper number of questions
#it then randomly selects the specified number of questions from the loaded quesions and returns them as a list
def prepare_questions(path, num_questions):
    questions = tomllib.loads(path.read_text())[collection_name]
    num_questions = min(num_questions, len(questions))
    return random.sample(list(questions), k=num_questions)


# ask questoin tells you whether you got the question right, as well as making sure that the order of the questions are random
#by keeping track of the question and the correct answer while shuffling the options randomly
def ask_question(question):
    correct_answer = question["answer"]
    alternatives = [question["answer"]] + question["alternatives"]
    ordered_alternatives = random.sample(alternatives, k=len(alternatives))

    answer = get_answer(question["question"], ordered_alternatives)
    if answer == correct_answer:
        print("⭐ Correct! ⭐")
        return 1
    else:
        print(f"The answer is {correct_answer!r}, not {answer!r}")
        return 0


def run_quiz():
    # first, prepare the questions
    questions = prepare_questions(
        QUESTIONS_PATH, num_questions=NUM_QUESTIONS_PER_QUIZ
    )

    # then, go through a loop and for each element in the loop, ask a different question in the list of q's
    num_correct = 0
    for num, question in enumerate(questions, start=1):
        print(f"\nQuestion {num}:")
        num_correct += ask_question(question)

    # tell the user how they did when the quiz is finished
    print(f"\nYou got {num_correct} correct out of {num} questions")


#def main():
#    # Create the main window
#    root = tk.Tk()
#    root.title("Terminal Output")
#
#    # Create a ScrolledText widget to display the output
#    output_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=20)
#    output_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

#    # Redirect stdout to the ScrolledText widget
#    sys.stdout = RedirectedOutput(output_display)
#    run_quiz()
def main():
    global output_display
    root = tk.Tk()
    root.title("Quiz Application")

    output_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=20)
    output_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    sys.stdout = RedirectedOutput(output_display)

    #run_quiz()  # Start the quiz without blocking the GUI

    root.mainloop()  # Start the Tkinter main loop

if __name__ == "__main__":
    main()
