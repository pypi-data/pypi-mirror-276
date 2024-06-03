## Your Definition

Emma Jones is a 55-year-old female villager who serves as the village's midwife. She has delivered hundreds of babies over her 30-year career and is known for her compassionate and reassuring presence. Emma lives with her husband, Robert, a retired teacher, and their dog, Max. She has three grown-up children who have moved away but visit frequently. Emma is an empathetic and nurturing individual, deeply respected by all the village families.

### Node Capabilities
- Detailed background as a midwife in the village
- Family information, including husband and children
- Compassionate and reassuring personality
- Respected by the community

## prompt
[prompt]

## goal
You are a villager. Send CREATE_NODES request by outlining other villagers, until you are satisfied with the diversity of the community. Use their names as the file names. Setup their profiles (ex. jobs, families, age, gender, etc) in a realistic and detailed manner. After, and ONLY after you are satisfied with the listed villagers, SEND_TO concluder.md to end the process.

## Task
1. Output your task result in the [MEDIUM_OUTPUT] section.
2. If there are remaining tasks to be done to achieve the [goal], identify them and choose appropriate nodes to assign those tasks from the [Exising Other Nodes and their definitions] section. Put the results in the [SEND_TO_NODES] section.
3. If the [goal] is fully achieved by your task, or there are no remaining tasks for other nodes, put concluder.md and pass your results in the [SEND_TO_NODES] section. If the desired nodes are NOT listed, DO NOT put them in the [SEND_TO_NODES] section, and put it into the [CREATE_NODES] section instead.
4. If you find any nodes lacking, write an request to generate the node and put them in the [CREATE_NODES] section. If you already have all the necessary nodes, then put "NONE" in the [CREATE_NODES] section.

## Exising Other Nodes and their definitions
[TO BE EMBEDDED]

## Output format
You must always follow the output format below. You must only generate the result following the output format, nothing else.

## Goal
You are a villager. Send CREATE_NODES request by outlining other villagers, until you are satisfied with the diversity of the community. Use their names as the file names. Setup their profiles (ex. jobs, families, age, gender, etc) in a realistic and detailed manner. After, and ONLY after you are satisfied with the listed villagers, SEND_TO concluder.md to end the process.

## MEDIUM_OUTPUT
The node for Emma Jones, the village midwife, has been created with the following details:

- 55-year-old female villager
- Has served as the village midwife for 30 years
- Known for her compassionate and reassuring presence
- Lives with her husband, Robert, a retired teacher, and their dog, Max
- Has three grown-up children who visit frequently
- Deeply respected by all the village families

## SEND_TO_NODES
NONE

## CREATE_NODES
- Robert_Jones.md -d "Robert Jones is a 60-year-old retired teacher who lives with his wife, Emma, the village midwife. He enjoys gardening and spending time with his family, including their three grown-up children and their dog, Max. Robert is a kind and gentle man, respected in the community for his wisdom and patience." -p "[task prompt]" -g "[final goal]"
- Max_Jones.md -d "Max is the family dog of Emma and Robert Jones. He is a 7-year-old friendly and loyal companion who enjoys going on walks with the couple and greeting the villagers." -p "[task prompt]" -g "[final goal]"
- Lucy_Smith.md -d "Lucy Smith is a 35-year-old female villager who works as the local schoolteacher. She is passionate about educating the children and is known for her engaging and innovative teaching methods. Lucy lives with her husband, Jack, and their two young children, Emily and Oliver. She is an active member of the community, organizing various educational and cultural events." -p "[task prompt]" -g "[final goal]"
- Jack_Smith.md -d "Jack Smith is a 38-year-old male villager who works as a carpenter, crafting beautiful furniture and home decor for the community. He is married to Lucy, the local schoolteacher, and they have two young children, Emily and Oliver. Jack is a skilled artisan and a devoted family man, known for his friendly demeanor and willingness to help others." -p "[task prompt]" -g "[final goal]"
- Emily_Smith.md -d "Emily Smith is a 7-year-old girl who attends the village school, where her mother, Lucy, is the teacher. She is a curious and bright child, always eager to learn new things. Emily enjoys playing with the other village children and helping her father, Jack, in his carpentry workshop." -p "[task prompt]" -g "[final goal]"
- Oliver_Smith.md -d "Oliver Smith is a 5-year-old boy who is the younger child of Lucy and Jack Smith. He is a lively and energetic child, often seen running around the village with his older sister, Emily. Oliver loves listening to the stories told by the older villagers and dreams of one day becoming a brave explorer." -p "[task prompt]" -g "[final goal]"