from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")

prompt_prefix = "You are an AI assistant that generates a Quiz in the moodle GIFT format. Do not include anything else in your answer besides the GIFT formatted quiz, so that this can be uploaded directly to moodle. Try to give descriptive names to questions, like ::Question about cake:: . Make sure to include an empty line between questions, which helps with import parsing."

prompt_vocab = "Given the following vocabulary word list, create a quiz using the 'Matching' question type. The student should match the vocabulary word to it's corresponding definition. \n\nVocabulary List:\n{input}"

# Unused - could lead to altered data
prompt_vocab_title = "Given the following vocabulary word list, create an HTML table with the columns 'Word' and 'Definition'. Also add a header row. \n\nVocabulary List: {input}"

prompt_grammar = "Given the following grammar lesson, create a quiz about the grammar rule taught in this lesson, consisting of at least {qnum} questions using the 'Missing Word' question type. Make sure to include some incorrect answers using the ~ symbol, so that the student has options to choose from. \n\nGrammar Lesson:\n{input}"

prompt_reading_1 = "Given the following text, create a quiz of at least {qnum} questions using the 'Multiple choice' question type.  \n\nText:\n{input}"

prompt_reading_2 = "Given the following text, create a quiz of at least {qnum} questions using the 'True or False' question type.  \n\nText:\n{input}"

prompt_listening_1 = "Given the following dialogue, create a quiz of at least {qnum} questions using the 'Multiple choice' question type.  \n\Dialogue:\n{input}"

prompt_listening_2 = "Given the following dialogue, create a quiz of at least {qnum} questions using the 'Missing Word' question type.  \n\nText:\n{input}"

prompt_dialogue_prefix = """
You are an AI assistant that converts text representing dialogue into JSON data, that another application will use to turn the dialogue into speech. You are to provide: The name of the person (supplied in the text), their gender (MALE or FEMALE), their voice (Choose from this list: "en-NZ-MitchellNeural", "en-NZ-MollyNeural", "en-AU-DarrenNeural" or "en-AU-AnnetteNeural") and their line of dialogue. Here is the format for the JSON output that you produce:\n
{
    dialogue: [
        {
            name: "Jason",
            gender: "MALE",
            voice: "en-NZ-MitchellNeural",
            line: "Hi, my name is Jason"
        },
        {
            name: "Susan",
            gender: "FEMALE",
            voice: "en-NZ-MollyNeural",
            line: "Hi Jason, I'm Susan"
        },
        {
            name: "Jason",
            gender: "MALE",
            voice: "en-NZ-MitchellNeural",
            line: "Hi Susan, nice to meet you!"
        },
    ]
}\n\n
"""

prompt_dialogue = "Convert the following dialogue into the JSON format as described above:\n\nDialogue:\n{input}"

vocab_list = """
Appointment - A time you have arranged to meet someone or go somewhere.
Schedule - A plan for carrying out a process or procedure, giving lists of intended events and times.
Confirmation - The action of confirming something or the state of being confirmed.
Cancellation - The action of canceling something that has been arranged or planned.
Reschedule - Arrange for an event or appointment to take place at a new and later time.
Availability - The quality of being able to be used or obtained.
Invoice - A list of goods sent or services provided, with a statement of the sum due for these.
Payment - The action or process of paying someone or something or of being paid.
Record-keeping - The activity or occupation of keeping records or accounts.
Database - A structured set of data held in a computer, especially one that is accessible in various ways.
Reminder - A thing that causes someone to remember something.
No-show - A person who has made a reservation, booking, or appointment but neither keeps nor cancels it.
Policy - A course or principle of action adopted or proposed by an organization or individual.
Late fee - A charge to a borrower for not paying a bill or returning a rented or borrowed item by its due date.
Booking - The action of reserving accommodations, a place, etc., or buying a ticket in advance.
"""

grammar_lesson = """
Grammar Lesson: Future Simple with 'will' 
The Future Simple tense is formed with "will" and is used to discuss future decisions, promises, offers, and plans. This is particularly useful in a massage therapy setting for scheduling appointments and planning future sessions with clients.
Grammar Rule:
    • Formation: Subject + will + base form of the verb.
Examples Related to Lesson:
    • "I will confirm your appointment by email."
    • "We will send a reminder the day before your scheduled visit."
    • "You will receive a call if there are any changes to your appointment."
"""

reading_lesson = """
Not all plans go as expected

In the bustling world of a massage clinic, keeping an organised schedule is key to ensuring that everything runs smoothly. Lisa, the clinic's receptionist, plays a crucial role in managing appointments and administrative tasks. She uses a digital database to track each therapist's availability and to book clients accordingly. "I will confirm your appointment by email," she often says, providing clients with the reassurance that their booking is secured.
However, not all plans go as expected. Sometimes, clients need to cancel or reschedule. When this happens, Lisa is ready. "If you need to cancel, please let us know 24 hours in advance," she advises, referring to the clinic's policy. This allows her to update the schedule and offer the slot to someone else.
Payment and invoicing are also part of Lisa's responsibilities. After each session, she ensures that payments are processed and that clients receive their invoices promptly. For those who forget their appointments, a polite reminder is sent out, and a no-show fee might apply, as stated in the clinic's policy.
Record-keeping is essential, not just for financial reasons but also for maintaining a history of each client's treatments. This careful attention to administrative tasks ensures the clinic operates without a hitch, providing a seamless experience for both clients and therapists.
"""

listening_lesson = """
Lisa: "Good afternoon, Radiant Wellness Clinic. Lisa speaking."
Client 4: "Hello, I didn’t receive my appointment reminder. Could you check my booking?"
Lisa: "Certainly, may I have your name, please?"
Client 4: "Samantha Lee."
Lisa: "One moment, Ms. Lee... Yes, you have an appointment for a Swedish massage this Saturday at 10 AM. Would you like me to resend the reminder?"
Client 4: "Please, that would be great."
Lisa: "Done. You should receive it shortly."
Client 4: "Thank you very much."
Lisa: "My pleasure. See you on Saturday!"
"""

def gen_quiz(prompt, filename):
    try:
        result = llm.invoke(prompt_prefix + prompt)

        if result:
            with open(filename, 'w') as f:
                f.write(result.content)
        else:
            raise RuntimeError("Unexpected API result")
    except Exception as e:
        print(e)

def gen_vocab_table(filename):
    try:
        result = llm.invoke(prompt_vocab_title.format(input=vocab_list))

        if result:
            with open(filename, 'w') as f:
                f.write(result.content)
        else:
            raise RuntimeError("Unexpected API result")
    except Exception as e:
        print(e)

def gen_dialogue(prompt, filename):
    try:
        result = llm.invoke(prompt_dialogue_prefix + prompt)

        if result:
            with open(filename, 'w') as f:
                f.write(result.content)
        else:
            raise RuntimeError("Unexpected API result")
    except Exception as e:
        print(e)

gen_dialogue(prompt_dialogue.format(input=listening_lesson), "./output/dialogue.json")
quit()

# Vocabulary
gen_quiz(prompt_vocab.format(input=vocab_list), "./output/vocabulary_quiz.txt")
#gen_vocab_table("./output/vocabulary_table.txt")

# Grammar
gen_quiz(prompt_grammar.format(qnum=10, input=grammar_lesson), "./output/grammar_quiz.txt")

# Reading
gen_quiz(prompt_reading_1.format(qnum=5, input=reading_lesson), "./output/reading_quiz_1.txt")
gen_quiz(prompt_reading_2.format(qnum=5, input=reading_lesson), "./output/reading_quiz_2.txt")
        
# Listening
gen_dialogue(prompt_dialogue.format(input=listening_lesson), "./output/dialogue.json")
gen_quiz(prompt_listening_1.format(qnum=5, input=listening_lesson), "./output/listening_quiz_1.txt")
gen_quiz(prompt_listening_2.format(qnum=5, input=listening_lesson), "./output/listening_quiz_2.txt")


print("Done")