import re
import traceback

# from .answer_relevant_grammar import answer_relevant_grammar
from .constants import LOGICAL_MODEL
from aphrodite import SamplingParams


# Answer vetting
# For now, this checks answer relevancy too. The danger with abstracting answer relevancy into a separate step is that anything which relies on knowledge that is obviously mentioned in the text already up until this point, will get screwed
async def check_answer_relevancy_with_text(qatuple, engine_wrapper):
    retries = 0
    while retries <= 4:
        decision_prompt = f"""You are an expert educational AI. Given a paragraph or two from a larger text, a question based on the paragraphs, and an answer to the question, you will make a determination as to whether the answer only uses the information in the paragraphs for its main points. Essentially: you will check if the answer is constrained to the information in the paragraphs provided. Your task includes first analyzing the answer, thinking through whether or not the answer reflects aspects of the paragraphs provided. 

Following this, at the very end of your response, you will write "Relevant" or "Irrelevant" depending on your analysis of the answer with regards to the text. 

### Instruction:
Text: 
\"\"\"
Polar bears are primarily found in the Arctic Circle, where they have adapted to the harsh cold environment. Their diet is primarily based on marine mammals, with seals being the most crucial part of their diet. Polar bears are skilled hunters, often waiting by seals' breathing holes to catch their prey. Occasionally, they also eat birds, bird eggs, and small mammals. They also consume significant amounts of berries and fish. These bears are known for their ability to survive in extreme conditions, thanks to their thick fur and fat layers which provide insulation, as well as their efficient digestion system, which makes good use of the few nutrients available.
\"\"\"

Question (based on text): \"\"\"What are the primary food sources of polar bears?\"\"\"

Supposed answer to the question (this is what you are fact-checking): \"\"\"Polar bears primarily eat seals, but they also consume significant amounts of berries and fish. Their efficient digestion system, which has been studied through MRIs, allows them to process a wide variety of foods.\"\"\"

### Response:
## Reasoning and thought process:
### Deep Analysis of the Text:
#### Content Scope and Detail: The text describes the diet of polar bears, focusing on their primary and secondary food sources.
#### Type of Information: The information is descriptive, outlining what polar bears eat, including seals, birds, eggs, small mammals, berries, and fish.

### Comprehensive Understanding of the Answer:
#### Key Components Identification: The answer mentions seals, berries, fish, and the efficiency of the polar bears' digestive system, referencing MRIs.
#### Depth of Explanation: The answer includes factual claims about the diet and a scientific statement about digestion studies.

### Targeted Comparison of Answer with Text:
#### Content Alignment: The claims about seals, berries, and fish align with the text.The reference to the digestive system's efficiency is supported but not the specific mention of MRIs.
#### Depth Alignment: The depth of the answer regarding diet aligns with the text, but the detail about MRIs introduces unnecessary depth.

### Identification of Extraneous Information:
#### Spotting Additional Details: The MRI claim.
#### Assessing Impact of Additional Information: The MRI detail, while interesting, is not supported by the text and deviates from the text's scope.

### Final Judgment on Answer Relevance:
#### Relevance Assessment: The answer is partially relevant but introduces unsupported details.
#### Explanation of Judgment: Since the answer mostly aligns with the text but includes extraneous information (MRIs), the final judgment is: Irrelevant.


### Instruction:
Text: 
\"\"\"
The Pythagorean theorem is a fundamental principle in geometry, stating that in a right-angled triangle, the square of the length of the hypotenuse (the side opposite the right angle) is equal to the sum of the squares of the lengths of the other two sides. This theorem is often expressed as the equation a² + b² = c², where a and b are the lengths of the two sides that form the right angle, and c is the length of the hypotenuse. Historically, this theorem has been attributed to the ancient Greek mathematician Pythagoras, although evidence suggests it was known to mathematicians in several cultures before him.
\"\"\"

Question (based on text): \"\"\"What does the Pythagorean theorem state in the context of geometry?\"\"\"

Supposed answer to the question (this is what you are fact-checking): \"\"\"The Pythagorean theorem, crucial in geometry, states that in a right-angled triangle, a² + b² = c², where a and b are the perpendicular sides and c is the hypotenuse. Additionally, it is noteworthy that this theorem was utilized in ancient Egypt for land surveying purposes.\"\"\"

### Response:
## Reasoning and thought process:
### Deep Analysis of the Text:
#### Content Scope and Detail: The text explains the Pythagorean theorem, its formula, and historical background.
#### Type of Information: The information is descriptive and explanatory, detailing the theorem and its mathematical representation.

### Comprehensive Understanding of the Answer:
#### Key Components Identification: The answer describes the theorem, its geometric context, and its historical application in ancient Egypt.
#### Depth of Explanation: The answer provides a mathematical explanation and historical context.

### Targeted Comparison of Answer with Text:
#### Content Alignment: The theorem's description and formula align with the text.The historical usage in ancient Egypt is not mentioned in the text.
#### Depth Alignment: The depth of explanation on the theorem aligns, but the historical context does not.

### Identification of Extraneous Information:
#### Spotting Additional Details: The claim about ancient Egypt.
#### Assessing Impact of Additional Information: This detail, while historically interesting, is not mentioned in the text and is irrelevant to the text's content.

### Final Judgment on Answer Relevance:
#### Relevance Assessment: The answer is partially relevant but includes significant extraneous historical information.
#### Explanation of Judgment: Due to the inclusion of unsupported historical context, the final judgment is: Irrelevant.


### Instruction:
Text: 
\"\"\"
Sigmund Freud, an Austrian neurologist and the father of psychoanalysis, introduced the concept of the unconscious mind. He suggested that the unconscious mind stores feelings, thoughts, and desires that are too threatening or painful for conscious awareness. Freud believed that these repressed elements could influence behavior and personality. One of his key methods for exploring the unconscious mind was through dream analysis, where he interpreted the meaning of dreams as a pathway to understanding the hidden desires and thoughts of the individual. Freud also developed the theory of the Oedipus complex, which proposes that during the phallic stage of psychosexual development, a male child experiences unconscious sexual desires for his mother and hostility toward his father.
\"\"\"

Question (based on text): \"\"\"What methods did Freud use to explore the unconscious mind, and what are some key concepts he introduced in this area?\"\"\"

Supposed answer to the question (this is what you are fact-checking): \"\"\"Freud used dream analysis as a method to explore the unconscious mind. He also introduced the concept of the Oedipus complex, suggesting that during a specific stage of development, a child experiences unconscious desires.\"\"\"

### Response:
## Reasoning and thought process:
### Deep Analysis of the Text:
#### Content Scope and Detail: The text discusses Freud's methods for exploring the unconscious mind and key concepts he introduced.
#### Type of Information: The information is descriptive, detailing Freud's methods and theories.

### Comprehensive Understanding of the Answer:
#### Key Components Identification: The answer mentions dream analysis and the Oedipus complex.
#### Depth of Explanation: The answer provides a factual description of Freud's methods and concepts.

### Targeted Comparison of Answer with Text:
#### Content Alignment: The text directly supports the claims about dream analysis and the Oedipus complex.
#### Depth Alignment: The depth of explanation in the answer aligns with the text's information.

### Identification of Extraneous Information:
#### Spotting Additional Details: The MRI claim.
#### Assessing Impact of Additional Information: The MRI detail, while interesting, is not supported by the text and deviates from the text's scope.


### Final Judgment on Answer Relevance:
#### Relevance Assessment: The answer accurately reflects the text's content.
#### Explanation of Judgment: Each part of the answer is directly supported by the text, so the final judgment is: Relevant.


### Instruction:
Text: 
\"\"\"
The Library of Alexandria, one of the largest and most significant libraries of the ancient world, was dedicated to the Muses—the nine goddesses of the arts. It flourished under the patronage of the Ptolemaic dynasty and functioned as a major center of scholarship. The library was estimated to house anywhere between 40,000 to 400,000 scrolls at its peak. The destruction of the library, which occurred over several incidents, marked a significant loss of cultural and scientific knowledge.
\"\"\"

Question (based on text): \"\"\"What was the importance of the Library of Alexandria in the ancient world?\"\"\"

Supposed answer to the question (this is what you are fact-checking): \"\"\"The Library of Alexandria was crucial in the ancient world as a center of scholarship and cultural development. It housed a vast collection of works, providing scholars with access to knowledge from various fields. The library's destruction is often attributed to Julius Caesar's fire during the Siege of Alexandria, a claim supported by several historical documents and archaeological findings.\"\"\"

### Response:
## Reasoning and thought process:
### Deep Analysis of the Text:
#### Content Scope and Detail: The text describes the Library of Alexandria's role, its size, patronage, and the impact of its destruction.
#### Type of Information: The information is descriptive, focusing on the library's significance and general history.

### Comprehensive Understanding of the Answer:
#### Key Components Identification: The answer highlights the library's role in scholarship and cultural development and references its destruction by Julius Caesar's fire.
#### Depth of Explanation: The answer provides both a general overview of the library's significance and specific historical claims regarding its destruction.

### Targeted Comparison of Answer with Text:
#### Content Alignment: The library's role as a center of scholarship and cultural development aligns with the text. The text does not mention Julius Caesar's fire or support this with historical documents and archaeological findings.
#### Depth Alignment: While the answer aligns in depth regarding the library's role, the specific claim about Julius Caesar and the supporting evidence is a detailed addition not present in the text.

### Identification of Extraneous Information:
#### Spotting Additional Details: The specifics about Julius Caesar's fire and the mention of historical documents and archaeological findings.
#### Assessing Impact of Additional Information: This additional information introduces a specific historical narrative and evidence not covered in the text, deviating from the text's content.

### Final Judgment on Answer Relevance:
#### Relevance Assessment: The answer starts correctly but introduces unsupported details about the library's destruction.
#### Explanation of Judgment: Due to the inclusion of specific and unsupported historical details, the final judgment is: Irrelevant.


### Instruction:
Text: 
\"\"\"
The planet Venus has a very dense atmosphere composed mainly of carbon dioxide, with clouds of sulfuric acid. This composition creates a runaway greenhouse effect, leading to surface temperatures hot enough to melt lead. Venus rotates very slowly on its axis, taking about 243 Earth days to complete one rotation, which is longer than its orbital period around the Sun. Interestingly, Venus rotates in the opposite direction to most planets in the solar system. This retrograde rotation is thought to be the result of a collision with a large celestial body early in its history.
\"\"\"

Question (based on text): \"\"\"What are the main characteristics of Venus's atmosphere and rotation?\"\"\"

Supposed answer to the question (this is what you are fact-checking): \"\"\"Venus's atmosphere is dense, primarily composed of carbon dioxide, and contains clouds of sulfuric acid, leading to extremely high temperatures. The planet has a unique rotation, taking 243 Earth days to rotate once and rotating in a retrograde direction due to gravitational interactions with Earth and other planets.\"\"\"

### Response:
## Reasoning and thought process:
### Deep Analysis of the Text:
#### Content Scope and Detail: The text provides specific information on Venus's atmosphere and rotation.
#### Type of Information: The text is descriptive, outlining the characteristics of Venus's atmosphere and rotation.

### Comprehensive Understanding of the Answer:
#### Key Components Identification: The answer discusses Venus's atmosphere, temperature, rotation period, direction, and the cause of its retrograde rotation.
#### Depth of Explanation: The answer includes descriptive details and a causal explanation for the retrograde rotation.

### Targeted Comparison of Answer with Text:
#### Content Alignment: The claims about the atmosphere, temperature, rotation period, and direction align with the text.The text does not support the claim about gravitational interactions with Earth and other planets.
#### Depth Alignment: The depth of the answer aligns with the text except for the unsupported causal explanation.

### Identification of Extraneous Information:
#### Spotting Additional Details: The cause of the retrograde rotation as gravitational interactions.
#### Assessing Impact of Additional Information: This detail introduces an unsupported causal explanation and deviates from the text.

### Final Judgment on Answer Relevance:
#### Relevance Assessment: The answer is mostly relevant but introduces an unsupported causal claim.
#### Explanation of Judgment: Due to the inclusion of an unsupported reason for Venus's retrograde rotation, the final judgment is: Irrelevant.


### Instruction:
Text: \"\"\"{qatuple[2]}\"\"\"

Question (based on text): \"\"\"{qatuple[0]}\"\"\"

Supposed answer to the question (this is what you are fact-checking): \"\"\"{qatuple[1]}\"\"\"

### Response:
## Reasoning and thought process (be careful about extra details, even vague ones):
"""
        try:
            sampling_params = SamplingParams(
                max_tokens=5500,
                stop=["</s>", "# Input:", "[INST]", "### Instruction", "[INST"],
                temperature=0.2,
            )
            completion = await engine_wrapper.submit(decision_prompt, sampling_params)
            completion_pattern = re.compile(
                r"Reasoning and thought process \(be careful about extra details, even vague ones\):\n(.+)",
                re.DOTALL | re.IGNORECASE,
            )
            judgement_pattern = re.compile(
                r"Explanation of Judgment:(.+)", re.DOTALL | re.IGNORECASE
            )
            response = completion_pattern.search(completion).group(1).strip()
            # # print(response)
            determination = judgement_pattern.search(response).group(1).strip()
            # print("\n\nDETERMINATION:\n------")
            # print(determination)
            # print("\n---------\n")
            if (
                "irrelevant" in determination.lower()
                or "mostly" in determination.lower()
                or "partial" in determination.lower()
                or "introduces information not present in the text"
                in determination.lower()
            ):  # Hack to get around faulty 13b outputs
                return (False, response), completion
            elif "relevant" in determination or "Relevant" in determination:
                return (True, response), completion
            else:
                retries += 1
        except:
            retries += 1
            # print(
            #     f"Something went catastrophically wrong with this one. Investigate! Here's the completion:\n{completion}"
            # )
            traceback.print_exc()
    return None, None


if __name__ == "__main__":  # test
    logic_llm = Llama(
        model_path=LOGICAL_MODEL,
        n_gqa=8,
        offload_kqv=True,
        n_ctx=8000,
        n_gpu_layers=1000,
        rope_scaling_type=1,
    )  # load the logical LLM and offload everything
    q_test = [
        (
            ") Explain how our understanding of planetary motion has changed over time.",
            "The understanding has evolved from the Earth being stationary and at the centre of the universe, to it orbiting the sun in an elliptical path with other planets while still rotating on its axis.",
            "The story of our world is a story that is still very imperfectly known. A couple of hundred years ago men possessed the history of little more than the last three thousand years. What happened before that time was a matter of legend and speculation.  Over a large part of the civilized world it was believed and taught that the world had been created suddenly in 4004 B.C., though authorities differed as to whether this had occurred in the spring or autumn of that year. This fantastically precise misconception was based upon a too literal interpretation of the Hebrew Bible, and upon rather arbitrary theological assumptions connected therewith.  Such ideas have long since been abandoned by religious teachers, and it is universally recognized that the universe in which we live has to all appearances existed for an enormous period of time and possibly for endless time.  Of course there may be deception in these appearances, as a room may be made to seem endless by putting mirrors facing each other at either end. But that the universe in which we live has existed only for six or seven thousand years may be regarded as an altogether exploded idea.\n\nThe earth, as everybody knows nowadays, is a spheroid, a sphere slightly compressed, orange fashion, with a diameter of nearly 8,000 miles.  Its spherical shape has been known at least to a limited number of intelligent people for nearly 2,500 years, but before that time it was supposed to be flat, and various ideas which now seem fantastic were entertained about its relations to the sky and the stars and planets.  We know now that it rotates upon its axis (which is about 24 miles shorter than its equatorial diameter) every twenty-four hours, and that this is the cause of the alternations of day and night, that it circles about the sun in a slightly distorted and slowly variable oval path in a year. Its distance from the sun varies between ninety-one and a half millions at its nearest and ninety-four and a half million miles.",
        ),
        (
            ") Identify and explain changes in human understanding throughout history regarding the age of the Earth.",
            "Initially, religious texts suggested a young earth dating back no more than several thousand years. However, evidence from geology and astronomy has shown us that the earth is over four billion years old.",
            "The story of our world is a story that is still very imperfectly known. A couple of hundred years ago men possessed the history of little more than the last three thousand years. What happened before that time was a matter of legend and speculation.  Over a large part of the civilized world it was believed and taught that the world had been created suddenly in 4004 B.C., though authorities differed as to whether this had occurred in the spring or autumn of that year. This fantastically precise misconception was based upon a too literal interpretation of the Hebrew Bible, and upon rather arbitrary theological assumptions connected therewith.  Such ideas have long since been abandoned by religious teachers, and it is universally recognized that the universe in which we live has to all appearances existed for an enormous period of time and possibly for endless time.  Of course there may be deception in these appearances, as a room may be made to seem endless by putting mirrors facing each other at either end. But that the universe in which we live has existed only for six or seven thousand years may be regarded as an altogether exploded idea.\n\nThe earth, as everybody knows nowadays, is a spheroid, a sphere slightly compressed, orange fashion, with a diameter of nearly 8,000 miles.  Its spherical shape has been known at least to a limited number of intelligent people for nearly 2,500 years, but before that time it was supposed to be flat, and various ideas which now seem fantastic were entertained about its relations to the sky and the stars and planets.  We know now that it rotates upon its axis (which is about 24 miles shorter than its equatorial diameter) every twenty-four hours, and that this is the cause of the alternations of day and night, that it circles about the sun in a slightly distorted and slowly variable oval path in a year. Its distance from the sun varies between ninety-one and a half millions at its nearest and ninety-four and a half million miles.",
        ),
        (
            ") Using specific scientific principles, explain why we know Earth is approximately 8000 miles in diameter and how its distance from the sun varies.",
            "We know about Earth's diameter using measurements of its circumference made using GPS data. The variation in distance to the sun is due to Earth's elliptical orbit around the sun, with a varying point of closest approach and farthest departure.",
            "The story of our world is a story that is still very imperfectly known. A couple of hundred years ago men possessed the history of little more than the last three thousand years. What happened before that time was a matter of legend and speculation.  Over a large part of the civilized world it was believed and taught that the world had been created suddenly in 4004 B.C., though authorities differed as to whether this had occurred in the spring or autumn of that year. This fantastically precise misconception was based upon a too literal interpretation of the Hebrew Bible, and upon rather arbitrary theological assumptions connected therewith.  Such ideas have long since been abandoned by religious teachers, and it is universally recognized that the universe in which we live has to all appearances existed for an enormous period of time and possibly for endless time.  Of course there may be deception in these appearances, as a room may be made to seem endless by putting mirrors facing each other at either end. But that the universe in which we live has existed only for six or seven thousand years may be regarded as an altogether exploded idea.\n\nThe earth, as everybody knows nowadays, is a spheroid, a sphere slightly compressed, orange fashion, with a diameter of nearly 8,000 miles.  Its spherical shape has been known at least to a limited number of intelligent people for nearly 2,500 years, but before that time it was supposed to be flat, and various ideas which now seem fantastic were entertained about its relations to the sky and the stars and planets.  We know now that it rotates upon its axis (which is about 24 miles shorter than its equatorial diameter) every twenty-four hours, and that this is the cause of the alternations of day and night, that it circles about the sun in a slightly distorted and slowly variable oval path in a year. Its distance from the sun varies between ninety-one and a half millions at its nearest and ninety-four and a half million miles.",
        ),
        (
            ") Demonstrate an understanding of Earth's rotational and orbital movement using scientific concepts.",
            "Earth rotates on its axis once every 24 hours, causing day and night cycles. It also orbits around the sun in a slightly elliptical path, which affects how close it is to the sun at different times of the year - leading to seasons.",
            "The story of our world is a story that is still very imperfectly known. A couple of hundred years ago men possessed the history of little more than the last three thousand years. What happened before that time was a matter of legend and speculation.  Over a large part of the civilized world it was believed and taught that the world had been created suddenly in 4004 B.C., though authorities differed as to whether this had occurred in the spring or autumn of that year. This fantastically precise misconception was based upon a too literal interpretation of the Hebrew Bible, and upon rather arbitrary theological assumptions connected therewith.  Such ideas have long since been abandoned by religious teachers, and it is universally recognized that the universe in which we live has to all appearances existed for an enormous period of time and possibly for endless time.  Of course there may be deception in these appearances, as a room may be made to seem endless by putting mirrors facing each other at either end. But that the universe in which we live has existed only for six or seven thousand years may be regarded as an altogether exploded idea.\n\nThe earth, as everybody knows nowadays, is a spheroid, a sphere slightly compressed, orange fashion, with a diameter of nearly 8,000 miles.  Its spherical shape has been known at least to a limited number of intelligent people for nearly 2,500 years, but before that time it was supposed to be flat, and various ideas which now seem fantastic were entertained about its relations to the sky and the stars and planets.  We know now that it rotates upon its axis (which is about 24 miles shorter than its equatorial diameter) every twenty-four hours, and that this is the cause of the alternations of day and night, that it circles about the sun in a slightly distorted and slowly variable oval path in a year. Its distance from the sun varies between ninety-one and a half millions at its nearest and ninety-four and a half million miles.",
        ),
    ]

    print("Begin HGWELLS test")
    result = check_answer_relevancy_with_text(q_test[2], logic_llm)
    if not result[0]:  # if not relevant
        print("Made right choice for bad answer")
    else:
        print("Made wrong choice for bad answer")

    d2 = check_answer_relevancy_with_text(q_test[1], logic_llm)
    if d2[0]:
        print("Made wrong choice for bad answer")
    else:
        print("Made right choice for bad answer")  # It caught something I missed!!!!
