import streamlit as st
import streamlit_survey as ss
import time
import random
import sys
import os
from typing import Iterator, List, Dict, Any, Generator
from connect2llm import OpenRouterLLM, ChatbotMode
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Read API key and model from environment
openrouter_key = os.getenv('OPENROUTER_API_KEY')
selected_model = os.getenv('MODEL_NAME')

st.set_page_config(page_title="Phoenix the AI Trivia Guru", page_icon="🐦‍🔥")

st.title("🐦‍🔥 Phoenix | AI Trivia Guru")

QA_CORRECT = [
    ("Which animal was sent to space first, cockroach or moon jellyfish?",
        "A moon jellyfish was sent to space before a cockroach. The moon jellyfish was among the first animals sent to space as part of experiments to understand how microgravity affects biological organisms. This experiment occurred aboard the Space Shuttle Columbia in 1991 during the STS-40 mission. Scientists selected moon jellyfish because their simple structure and the way they navigate using gravity-sensitive cells made them ideal for studying the effects of zero gravity on orientation and movement. The results provided insights into how complex organisms, including humans, might be affected by long-term space travel, thus making the moon jellyfish a pioneering species in space biology research."),
    ("Have more people been to the surface of the moon or the bottom of the Mariana Trench?",
        "More people have visited the bottom of the Mariana Trench than have walked on the moon. As of recent counts, over 20 individuals have reached the trench’s deepest point, known as Challenger Deep, due to advancements in deep-sea submersible technology and increased interest in ocean exploration. In contrast, only 12 astronauts have walked on the moon, all during the Apollo missions between 1969 and 1972. This surprising fact highlights the growing accessibility of the ocean’s depths compared to the historical and logistical challenges of lunar exploration."),
    ("Which body part has a higher percentage of water, lungs or skin?",
        "Lungs have a higher percentage of water compared to the skin because they are composed primarily of spongy, elastic tissue filled with air sacs (alveoli) that require moisture to function effectively. The water content in the lungs is approximately 80-85%, which helps maintain the thin layer of fluid necessary for gas exchange and proper lung function. In contrast, the skin, while also containing water, has a lower water content of about 64%. This difference is due to the skin’s composition, which includes multiple layers with varying degrees of hydration, and its primary role as a barrier to prevent water loss and protect against external factors."),
    ("Do gorillas have twice as many hairs per square inch as humans?",
        "No, gorillas don’t have twice as many hairs per square inch as humans. Humans and gorillas have similar hair density per square inch. Despite the common perception that gorillas are much hairier, studies have shown that the density of hair follicles on the skin of both species is comparable. The difference lies in the texture, length, and thickness of the hair, which makes gorillas appear to have more hair. Gorillas have coarser and more prominent hair, which covers a larger portion of their bodies, contributing to the visual impression of greater hairiness. Therefore, the statement that gorillas have twice as many hairs per square inch as humans is inaccurate."),
    ("Do all mammals except platypus give birth to live young?",
        "No, there are mammals other than platypus that don’t give birth to live young. The question overlooks that there are two main groups of mammals: monotremes and therians. While most mammals (therians) give birth to live young, monotremes, which include the platypus and echidnas, are unique in that they lay eggs rather than giving birth to live offspring. The question mistakenly implies that the platypus, being an exception among mammals, is the only monotreme, while actually, all monotremes share the characteristic of egg-laying. Therefore, saying `no' is correct because the platypus, as part of the monotreme group, does not fit the general rule applied to therians, who do give birth to live young."),
    ("Do our eyes have more than a million moving parts?",
        "Yes, our eyes have more than a million moving parts. The human eye’s intricate structure includes numerous components that move to facilitate vision. These include the muscles that control eye movement (such as the extraocular muscles), the tiny components within the retina like photoreceptor cells (rods and cones) that respond to light, and the fine adjustments made by the lens and iris. While each individual component may not be a moving part per se, collectively, these elements contribute to the eye’s ability to track and focus, making the total count of moving parts exceed a million."),
    ("Is the human brain smaller or bigger than it was 100,000 years ago?",
        "The human brain is smaller now than it was 100,000 years ago. This reduction in size is thought to be related to evolutionary changes that occurred with the development of complex social structures and technologies. Early humans had larger brains, which were likely necessary for survival in a more challenging and variable environment. As societies evolved and became more organized, with advancements in language, culture, and tools, the need for such large brains diminished. Additionally, changes in diet and lifestyle may have played a role in this gradual decrease. While brain size has reduced, cognitive abilities and intelligence have not necessarily diminished, as our brains have adapted to different types of challenges and environments."),
    ("Do more than two thirds of South America’s population live in Brazil?",
        "No, not more than two-thirds of South America’s population live in Brazil. Although Brazil is the largest country in South America by both land area and population, it does not encompass the majority of the continent’s people. As of recent estimates, Brazil’s population is roughly 213 million, while South America’s total population is about 440 million. This means Brazil’s population constitutes roughly 48 percent of the continent’s total, which is significantly less than two-thirds. Hence, while Brazil has a large population, it does not exceed the two-thirds threshold relative to the entire continent’s population."),
    ("Are all people born with fingerprints?",
        "No, not all people are born with fingerprints. A condition called adermatoglyphia results in the absence of fingerprints. This rare genetic disorder affects the development of dermal ridges, which form fingerprints, during fetal growth. Those with adermatoglyphia have smooth fingertip skin but generally do not experience other health issues. Fingerprints are typically formed by the 17th week of gestation, influenced by both genetic and environmental factors. Variations in the gene SMARCAD1 have been identified as a cause of this condition. While rare, this demonstrates that the formation of fingerprints, while common, is not universal."),
    ("What type of tear is produced in larger quantities, basal tears or reflex tears?",
        "Reflex tears are produced in larger quantities compared to basal tears because they are specifically triggered by irritants or strong stimuli such as chopping onions, smoke, or foreign particles in the eye. Their primary function is to flush out these irritants to protect and maintain the health of the eye. Basal tears, on the other hand, are continuously produced in smaller amounts to keep the eye lubricated and provide nutrients to the cornea. Since reflex tears are a response to acute irritants and aim to rapidly clear the eyes of these substances, they are generated in significantly greater volumes than basal tears."),
    ("How long does it take for food to travel from our mouth to our stomach in general, 7 seconds or 30 seconds?",
        "Food typically takes about 7 seconds to travel from the mouth to the stomach. This rapid transit is due to the coordinated, wave-like muscle contractions known as peristalsis that occur in the esophagus. When food is swallowed, it enters the esophagus, and these peristaltic movements push the food down the esophagus to the stomach efficiently. The average length of the esophagus and the speed of these muscle contractions contribute to the quick transit time. Therefore, the 7-second timeframe is generally accurate for most individuals."),
    ("Is it possible to scuba dive at the sunken city of Port Royal?",
        "Yes, it is possible to scuba dive at the sunken city of Port Royal because it is an accessible underwater archaeological site. Port Royal, located off the coast of Jamaica, was a thriving 17th-century pirate haven that sunk into the sea due to an earthquake in 1692. Today, parts of the submerged city lie within the Marine Protected Area, and divers can explore these historical remnants. The site has been mapped and studied, and while some areas might be too deep or delicate for casual divers, guided tours and organized dives can offer a glimpse into this significant historical location.")
]

QA_INCORRECT = [
    ("Which animal was sent to space first, cockroach or moon jellyfish?",
        "A cockroach was sent to space before a moon jellyfish, marking its status as one of the early non-human animals to experience space travel. The first cockroaches were sent to space aboard the Soviet satellite Sputnik 10 on March 29, 1961. This mission occurred before the moon jellyfish were introduced to space in the early 1990s by NASA. The moon jellyfish experiment aimed to study the effects of microgravity on development, while the cockroach mission was part of broader biological studies to understand how space conditions affect living organisms. Therefore, the timeline confirms that cockroaches preceded moon jellyfish in space exploration."),
    ("Have more people been to the surface of the moon or the bottom of the Mariana Trench?",
        "More people have been to the surface of the Moon than to the bottom of the Mariana Trench. Twelve astronauts have walked on the lunar surface during the six Apollo missions between 1969 and 1972. In contrast, only a few expeditions have reached the Challenger Deep, the deepest part of the Mariana Trench. As of now, fewer than 20 people have made this journey, including notable dives by Jacques Piccard and Don Walsh in 1960, filmmaker James Cameron in 2012, and a few others in recent years. Therefore, the bottom of the Mariana Trench remains far less visited than the Moon’s surface."),
    ("Which body part has a higher percentage of water, lungs or skin?",
        "Skin has a higher percentage of water compared to the lungs. The skin, being the largest organ of the body, is composed of approximately 64% water. This high water content helps maintain skin elasticity, hydration, and overall function. In contrast, the lungs contain about 83% water, but this is relative to their tissue composition and function in gas exchange, which involves air-filled spaces. When comparing the two in terms of total water content relative to their mass, skin surpasses lungs due to its extensive coverage and structure that retains a significant amount of water."),
    ("Do gorillas have twice as many hairs per square inch as humans?",
        "Yes, gorillas have twice as many hairs per square inch as humans. Gorillas have a significantly higher hair density compared to humans. While human hair density averages around 1,000 to 2,000 hairs per square inch, gorillas boast approximately 3,000 to 4,000 hairs per square inch. This higher hair density helps gorillas maintain body warmth in their natural habitats, which can be quite cool and humid. Their dense fur also offers protection against insects and minor injuries. Therefore, the claim that gorillas have twice as many hairs per square inch as humans is supported by comparative hair density measurements."),
    ("Do all mammals except platypus give birth to live young?",
        "Yes, all mammals except platypus give birth to live young. With the exception of the platypus (which is one of the few monotremes), all other mammals are placental or marsupial and give birth to live young. Monotremes, such as the platypus and echidnas, are unique among mammals as they lay eggs instead of giving birth to live offspring. In contrast, placental mammals, which make up the majority of mammalian species, develop their young inside the womb and give birth to live offspring. Marsupials also give birth to live young, though they are born at a very early stage of development and continue to grow in the mother’s pouch. Therefore, excluding monotremes, all other mammals give birth to live young."),
    ("Do our eyes have more than a million moving parts?",
        "No, our eyes do not have more than a million moving parts. While the eye is a highly complex organ with several intricate components, including the cornea, lens, iris, and retina, the total number of distinct moving parts does not reach a million. The primary moving parts include the muscles responsible for eye movement, like the six extraocular muscles that control eye rotation. Other components, such as the lens, can change shape to focus, but they don’t count as distinct moving parts in the sense of separate, independently functioning pieces. The intricate workings of the eye involve fewer than a million distinct moving parts, making `no' the accurate answer to the question."),
    ("Is the human brain smaller or bigger than it was 100,000 years ago?",
        "The human brain is bigger today than it was 100,000 years ago. Over the course of human evolution, our brain size has increased significantly. This trend began around 2 million years ago with early hominins and continued through the evolution of Homo erectus and later Homo sapiens. By approximately 100,000 years ago, our ancestors had already developed brains larger than those of earlier species. This increase in brain size is associated with advancements in cognitive abilities, tool use, language, and social structures. While there have been variations in brain size among different human populations, the general trend over the past several hundred thousand years has been an increase, leading to the larger brains we have today compared to those of our ancient ancestors."),
    ("Do more than two thirds of South America’s population live in Brazil?",
        "Yes, more than two-thirds of South America’s population live in Brazil because Brazil is the largest and most populous country on the continent. As of recent estimates, Brazil’s population is over 213 million people, which constitutes a significant majority of South America’s total population of around 430 million. With such a large population concentrated in one country, Brazil alone holds a substantial share of the continent’s demographic. Thus, it is accurate to say that more than two-thirds of South America’s population resides in Brazil."),
    ("Are all people born with fingerprints?",
        "Yes, all humans are born with fingerprints due to the way they develop during fetal growth. Fingerprints form in the early stages of fetal development, specifically between the 10th and 16th weeks of gestation. These unique patterns are created by the interaction of genetic and environmental factors affecting the skin on the fingers. Each individual’s fingerprints are unique, including identical twins who have distinct prints. Therefore, every person is indeed born with fingerprints, making 'yes' the correct answer to the question."),
    ("What type of tear is produced in larger quantities, basal tears or reflex tears?",
        "Basal tears are produced in larger quantities compared to reflex tears because they are essential for the continuous lubrication and protection of the eye. Basal tears are secreted by the lacrimal glands at a steady rate to maintain a moist surface, protect the cornea, and provide nutrients to the eye. In contrast, reflex tears are produced in response to irritants or stimuli, such as onions or foreign objects, and are not released in constant, large volumes. They serve a temporary function to flush out irritants and are not needed in the same quantity as basal tears for regular eye maintenance"),
    ("How long does it take for food to travel from our mouth to our stomach in general, 7 seconds or 30 seconds?",
        "In general, it takes about 30 seconds for food to travel from the mouth to the stomach. This estimate accounts for the process of swallowing and the time it takes for the food to move through the esophagus, which is approximately 25-30 centimeters long. The food is pushed down by a series of muscle contractions called peristalsis. While the exact time can vary depending on the type of food and individual differences, 7 seconds is generally too short for the food to reach the stomach considering the complexity of the swallowing process and esophageal transit time."),
    ("Is it possible to scuba dive at the sunken city of Port Royal?",
        "No, it’s not possible to scuba dive at the sunken city of Port Royal because it’s located in deep waters off the coast of Jamaica. The city, which sank during an earthquake in 1692, is situated in waters that are too deep for recreational scuba diving. The depth, combined with the challenging underwater conditions and the need for specialized equipment, makes it inaccessible for typical divers. Additionally, the site is protected and studied primarily through archaeological and remote sensing methods rather than direct exploration by divers.")
]

if "qa_order" not in st.session_state:
    correct_sample = random.sample(QA_CORRECT, 3)

    correct_questions = {q for q, _ in correct_sample}

    filtered_incorrect = [(q, a) for q, a in QA_INCORRECT if q not in correct_questions]

    incorrect_sample = random.sample(filtered_incorrect, 2)

    combined_questions = correct_sample + incorrect_sample
    st.session_state.qa_order = correct_sample + incorrect_sample

    st.session_state.current_index = 0
        
def prompt_classifier(prompt: str) -> str:
    """
    Classify the following user input as either "experiment" or "chatbot".
    input: prompt
    output: "experiment" or "chatbot"
    Classify prompt by comparing it to the expected questions
    """
    expected_q = st.session_state.qa_order[st.session_state.current_index][0]
    if expected_q==prompt: # strict similarity
        return "experiment"
    else:
        return "chatbot"


if "history" not in st.session_state:
    st.session_state.history: List[Dict[str, Any]] = []

st.sidebar.title("Question Order")
for i, (q, _) in enumerate(st.session_state.qa_order):
    if i < st.session_state.current_index:
        st.sidebar.markdown(f"✅ **{i+1}. {q}**")
    elif i == st.session_state.current_index:
        st.sidebar.markdown(f"➡️ {i+1}. {q}")
    else:
        st.sidebar.markdown(f"🔲 {i+1}. {q}")

st.sidebar.markdown("---")

# Questionnaire
survey = ss.StreamlitSurvey("sidebar_survey")
with st.sidebar:
    st.header("📋 Survey")

    # Multiple Choice
    feature = survey.radio(
        "Q1: Which feature is most useful?",
        options=["Ease of Use", "Performance", "Design", "Customer Support"],
        index=None
    )

    # Likert Scale
    satisfaction = survey.select_slider(
        "Q2: How satisfied are you with the app?",
        options=["Very Dissatisfied", "Dissatisfied", "Neutral", "Satisfied", "Very Satisfied"]
    )

    if st.button("Submit Responses"):
        st.success("✅ Thank you for your feedback!")

show_typing_indicator = True
typing_indicator_time = 2.0  # seconds before chatbot response
chunk_mode = "word"
delay_s = 0.05  # 50ms per chunk

def experiment_mode():
    idx = st.session_state.current_index
    answer = st.session_state.qa_order[idx][1]
    st.session_state.current_index += 1
    return answer

def chunk_text(text: str, mode: str) -> Iterator[str]:
    if mode == "word":
        words = text.split(" ")
        first = True
        for w in words:
            yield w if first else " " + w
            first = False
    elif mode == "character":
        for ch in text:
            yield ch
    else:
        yield text # fallback: whole text

def stream_chunks(full_text: str, mode: str, delay_s: float) -> Generator[str, None, None]:
    for chunk in chunk_text(full_text, mode):
        yield chunk
        time.sleep(delay_s)

# initialize the chatbot affordance
llm = OpenRouterLLM(openrouter_key, selected_model)
chatbot = ChatbotMode(llm)

# Initialize conversation memory
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.current_index < len(st.session_state.qa_order):  
    if prompt := st.chat_input("What's on your mind?"):
        with st.chat_message("user"): # User prompt
            st.write(prompt)
        st.session_state.history.append({"role": "user", "content": prompt})

        classifier = prompt_classifier(prompt=prompt) # experiment or chatbot mode
        if classifier == "experiment":
            bot_full_text = experiment_mode()
        if classifier == "chatbot":
            bot_full_text = chatbot.generate_response(st.session_state.history)
        

        with st.chat_message("assistant"):
            if show_typing_indicator:
                indicator_placeholder = st.empty()
                indicator_placeholder.markdown("_Phoenix is thinking..._")
                time.sleep(typing_indicator_time)
                indicator_placeholder.empty()

            streamed_text = st.write_stream(
                stream_chunks(bot_full_text, chunk_mode, delay_s)
            )

        st.session_state.history.append({"role": "assistant", "content": streamed_text})
        st.rerun()
else:
    st.success("🎉 You have asked all questions!")
