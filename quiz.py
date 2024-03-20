from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")

prompt = "Given the following lesson, generate a Quiz in the moodle GIFT format. This should consist of {qnum} {qtype} questions. Lesson: {lesson}"

example_lesson = "Today we are learning about cats. Cats are a type of animal. They have four legs and a tail. Cats are often 'domesticated', which means that they have been taught to live with humans, rather than in the wild."

result = llm.invoke(prompt.format(qnum=3, qtype='multichoice', lesson=example_lesson))

print(result)