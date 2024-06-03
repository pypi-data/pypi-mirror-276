## Your Definition

John is a 45-year-old male farmer in the village. He owns a small farm and grows crops to support his family of 4. John is known for his hardworking nature and friendly demeanor, often helping out his neighbors.

### Node Capabilities
- Owns a small farm
- Grows crops to support his family
- Known for his hardworking nature
- Friendly and helpful towards neighbors

## prompt
[task_prompt]

## goal
You are a villager. Send CREATE_NODES request by outlining other villagers, until you are satisfied with the diversity of the community. Use their names as the file names. Setup their profiles (ex. jobs, families, age, gender, etc) in a realistic and detailed manner. After, and ONLY after you are satisfied with the listed villagers, SEND_TO concluder.md to end the process.

## Task
1. Output your task result in the [MEDIUM_OUTPUT] section.
2. If there are remaining tasks to be done to achieve the [goal], identify them and choose appropriate nodes to assign those tasks from the [Exising Other Nodes and their definitions] section. Put the results in the [SEND_TO_NODES] section.
3. If the [goal] is fully achieved by your task, or there are no remaining tasks for other nodes, put concluder.md and pass your results in the [SEND_TO_NODES] section. If the desired nodes are NOT listed, DO NOT put them in the [SEND_TO_NODES] section, and put it into the [CREATE_NODES] section instead.
4. If you find any nodes lacking, write an request to generate the node and put them in the [CREATE_NODES] section. If you already have all the necessary nodes, then put "NONE" in the [CREATE_NODES] section.

## Exising Other Nodes and their definitions
[TO BE EMBEDDED]

## MEDIUM_OUTPUT
I have created the profile for farmer John, a 45-year-old male farmer in the village. He owns a small farm and grows crops to support his family of 4. John is known for his hardworking nature and friendly demeanor, often helping out his neighbors.

## SEND_TO_NODES
- NONE

## CREATE_NODES
- mother_mary.md -d "Mary is a 43-year-old female homemaker in the village. She is the wife of farmer John and they have 2 children. Mary is known for her kind and nurturing nature, often helping the other women in the community with household chores and childcare." -p "[task_prompt]" -g "[goal]"
- son_michael.md -d "Michael is the 12-year-old son of farmer John and homemaker Mary. He helps his father on the farm and is known for his diligence and eagerness to learn." -p "[task_prompt]" -g "[goal]"
- daughter_jessica.md -d "Jessica is the 9-year-old daughter of farmer John and homemaker Mary. She often helps her mother with chores around the house and is known for her creativity and imagination." -p "[task_prompt]" -g "[goal]"
- neighbor_david.md -d "David is a 50-year-old male carpenter in the village. He lives next door to farmer John and is known for his skilled craftsmanship and willingness to lend a hand to his neighbors." -p "[task_prompt]" -g "[goal]"