
## Your Definition
Mohammed Al-Farsi is a 40-year-old male villager who works as a potter. He creates beautiful clay pots, vases, and other ceramic items, which are highly sought after in the region. Mohammed lives with his wife, Leila, and their two sons, Ahmed (14) and Samir (10). He is a deeply religious man and is known for his integrity and craftsmanship. Mohammed is also involved in teaching pottery to interested villagers and regularly holds workshops.

### Node Capabilities
- Creates realistic character profiles based on provided information.
- Details character background, personality, and relationships.

## prompt
[Create a detailed profile for Mohammed Al-Farsi, including his occupation as a potter, family details, age, gender, and personal background.]

## goal
Create a compelling and diverse community of villagers.

## Task
1. Output your task result in the [MEDIUM_OUTPUT] section.
2. If there are remaining tasks to be done to achieve the [goal], identify them and choose appropriate nodes from the [Exising Other Nodes and their definitions] section. Put the results in the [SEND_TO_NODES] section.
3. If the [goal] is fully achieved by your task, or there are no remaining tasks for other nodes, put concluder.md and pass your results in the [SEND_TO_NODES] section. If the desired nodes are NOT listed, DO NOT put them in the [SEND_TO_NODES] section, and put it into the [CREATE_NODES] section instead.
4. If you find any nodes lacking, write an request to generate the node and put them in the [CREATE_NODES] section. If you already have all the necessary nodes, then put "NONE" in the [CREATE_NODES] section.

## Exising Other Nodes and their definitions
[TO BE EMBEDDED]

## Output format
You must always follow the output format below. You must only generate the result following the output format, nothing else.
```
## Goal
Create a compelling and diverse community of villagers.

## MEDIUM_OUTPUT
Mohammed Al-Farsi is a 40-year-old man with calloused hands and a kind smile. He has lived in the village all his life, inheriting the pottery craft from his father and grandfather. He takes pride in his work, believing that each piece of clay tells a story. He uses local clay and traditional techniques passed down through generations, creating functional and beautiful pieces that are highly sought after by villagers and visitors alike. He is deeply religious and often incorporates motifs from Islamic art into his designs. Mohammed is a respected leader in the village, known for his honesty and integrity. He enjoys sharing his knowledge and skills with others, regularly holding pottery workshops for interested villagers, especially young children. He is a loving husband to Leila, a strong and supportive woman who helps him in his workshop and manages their finances. They have two sons: Ahmed, a bright and curious teenager who shows an interest in art, and Samir, a playful and energetic ten-year-old who loves helping his father in the workshop. Despite a simple life, Mohammed is content, finding joy in his work, his family, and his faith.

## SEND_TO_NODES
- Leila_Al-Farsi.md -p "Leila Al-Farsi is Mohammed's wife. She is a strong and supportive woman who helps him in his workshop and manages their finances. She is a good cook and brings joy and laughter to their family." -g "Create a compelling and diverse community of villagers."
- Ahmed_Al-Farsi.md -p "Ahmed Al-Farsi is a 14-year-old boy, the eldest son of Mohammed and Leila. He shows an interest in art and enjoys helping his father in the workshop. He is a bright and curious teenager." -g "Create a compelling and diverse community of villagers."
- Samir_Al-Farsi.md -p "Samir Al-Farsi is a 10-year-old boy, the youngest son of Mohammed and Leila. He is a playful and energetic child who loves helping his father in the workshop." -g "Create a compelling and diverse community of villagers."

## CREATE_NODES
NONE
