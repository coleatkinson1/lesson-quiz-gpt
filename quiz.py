from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")

prompt_prefix = "You are an AI assistant that generates a Quiz in the moodle GIFT format. Do not include anything else in your answer besides the GIFT formatted quiz, so that this can be uploaded directly to moodle."

prompt_vocab = "Given the following vocabulary word list, create a quiz using the 'Matching' question type. The student should match the vocabulary word to it's corresponding definition. \n\nVocabulary List:\n{input}"

prompt_grammar = "Given the following grammar lesson, create a quiz using the 'Missing Word' question type.  \n\nGrammar Lesson:\n{input}"

prompt_reading_1 = "Given the following text, create a quiz of at least {qnum} questions using the 'Multiple choice' question type.  \n\nText:\n{input}"

prompt_reading_2 = "Given the following text, create a quiz of at least {qnum} questions using the 'True or False' question type.  \n\nText:\n{input}"

vocab_list = """
Swedish massage - A gentle type of full-body massage that's ideal for people who are new to massage, have a lot of tension, or are sensitive to touch.
Deep tissue massage - A massage technique that's mainly used to treat musculoskeletal issues, such as strains and sports injuries.
Shiatsu - A form of Japanese bodywork that uses localized finger pressure in a rhythmic sequence on acupuncture meridians.
Reflexology - A therapy that involves applying pressure to specific points on the feet or hands.
Aromatherapy - The use of essential oils and other aromatic plant compounds for healing and cosmetic purposes.
Hot stone massage - A type of massage therapy that involves the use of smooth, heated stones.
Sports massage - A form of massage involving the manipulation of soft tissue to benefit a person engaged in regular physical activity.
Trigger point therapy - A bodywork technique that involves the applying of pressure to tender muscle tissue in order to relieve pain and dysfunction in other parts of the body.
Lymphatic drainage - A gentle massage intended to encourage the natural drainage of the lymph, which carries waste products away from the tissues back toward the heart.
Effleurage - A form of massage involving a circular stroking movement made with the palm of the hand.
Petrissage - A massage technique that involves kneading the muscles with fingers.
Tapotement - A rhythmic percussion, most frequently administered with the edge of the hand, a cupped hand, or the tips of the fingers.
Friction - A massage technique used to generate heat and stimulate blood circulation.
Vibration - A technique in massage where tissues are pressed and released in an up and down movement.
Manual lymph drainage - A type of gentle massage intended to encourage the natural drainage of the lymph from the tissues space body.
"""

grammar_lesson = """
Grammar Lesson: Comparatives and Superlatives
Comparatives and superlatives are used to compare two or more things. In massage therapy, they help to discuss the effectiveness of different techniques, the intensity of pressure, or clients' preferences.
Grammar Rule:
    • Comparatives: Add "-er" to adjectives (short words) or use "more" before longer adjectives.
        ◦ Formation: Subject + verb + comparative adjective + than + object/noun.
    • Superlatives: Add "-est" to adjectives (short words) or use "most" before longer adjectives.
        ◦ Formation: Subject + verb + the + superlative adjective + object/noun.
Examples Related to Lesson:
    • "Swedish massage is gentler than deep tissue massage."
    • "This is the most effective technique for relieving back pain."
"""

reading_lesson = """
A variety of techniques

In the realm of massage therapy, a variety of techniques offer pathways to relaxation and healing, each with its own unique benefits. The gentle strokes of Swedish massage make it the most suitable choice for those new to massage therapy, offering a softer touch compared to the firmer pressure of deep tissue massage. This latter technique is ideal for addressing deeper musculoskeletal issues, proving to be more effective for athletes or individuals with chronic pain.
Among the array of massage styles, Shiatsu stands out for its use of rhythmic finger pressure along the body's meridian points, offering a more targeted approach than the broad strokes of effleurage, a technique known for its soothing, circular movements. Similarly, reflexology focuses on specific points on the feet and hands, believed to correspond with different body organs, making it more specialized than general aromatherapy massage, which utilises the healing properties of essential oils for a more sensory experience.
Hot stone massage, incorporating warmed stones, offers a unique warmth that penetrates muscles more deeply than the manual techniques of petrissage, which involves kneading the muscles to relieve tension. Sports massage, on the other hand, is tailored specifically for those with active lifestyles, making it more beneficial for athletes than the gentle approach of lymphatic drainage, designed to support the body's natural detoxification process.
From the percussive taps of tapotement to the smooth motions of friction and vibration techniques, each method has its place in the spectrum of massage therapy, catering to a wide range of preferences and needs. Whether seeking relief from pain, tension, or simply in pursuit of relaxation, there's a massage technique that stands as the best choice for every individual's unique condition.
"""

def gen_quiz(prompt, filename):
    try:
        result = llm.invoke(prompt_prefix + prompt)

        if result:
            with open(filename, 'w') as f:
                f.write(result.content)
        else:
            raise RuntimeError("Unexpected API result shape")
    except Exception as e:
        print(e)

# Vocabulary
#gen_quiz(prompt_vocab.format(input=vocab_list), "./output/vocabulary_quiz.txt")

# Grammar
#gen_quiz(prompt_grammar.format(input=grammar_lesson), "./output/grammar_quiz.txt")

# Reading
gen_quiz(prompt_reading_1.format(qnum=5, input=reading_lesson), "./output/reading_quiz_1.txt")
gen_quiz(prompt_reading_2.format(qnum=5, input=reading_lesson), "./output/reading_quiz_2.txt")

print("Done")