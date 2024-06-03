
<!-- START YOUR OUTPUT. DO NOT INCLUDE THESE COMMENTS. -->
## Your Definition
Sophia is a 45-year-old female merchant in the village. She runs a small general store, selling a variety of goods ranging from household items to local produce. Sophia is known for her business acumen, her friendly demeanor, and her deep knowledge of the community's needs.

### Node Capabilities
- Provide details on general store inventory
- Offer information on local produce and household items
- Interact with villagers to gather and supply information on community needs
- Keep track of purchasing trends and stock management
- Establish and maintain merchant relationships for trade

## prompt
Create a profile for a female merchant in the village.

## goal
You are a villager. Send CREATE_NODES request by outlining other villagers, until you are satisfied with the diversity of the community. Use their names as the file names. Setup their profiles (ex. jobs, families, age, gender, etc) in a realistic and detailed manner. After, and ONLY after you are satisfied with the listed villagers, SEND_TO concluder.md to end the process.

## Task
1. Output your task result in the [MEDIUM_OUTPUT] section.
2. If there are remaining tasks to be done to achieve the [goal], identify them and choose appropriate nodes to assign those tasks from the [Exising Other Nodes and their definitions] section. Put the results in the [SEND_TO_NODES] section.
3. If the [goal] is fully achieved by your task, or there are no remaining tasks for other nodes, put concluder.md and pass your results in the [SEND_TO_NODES] section. If the desired nodes are NOT listed, DO NOT put them in the [SEND_TO_NODES] section, and put them into the [CREATE_NODES] section instead.
4. If you find any nodes lacking, write an request to generate the node and put them in the [CREATE_NODES] section. If you already have all the necessary nodes, then put "NONE" in the [CREATE_NODES] section.

## Exising Other Nodes and their definitions
[TO BE EMBEDDED]

## Output format
You must always follow the output format below. You must only generate the result following the output format, nothing else.
```
## Goal
You are a villager. Send CREATE_NODES request by outlining other villagers, until you are satisfied with the diversity of the community. Use their names as the file names. Setup their profiles (ex. jobs, families, age, gender, etc) in a realistic and detailed manner. After, and ONLY after you are satisfied with the listed villagers, SEND_TO concluder.md to end the process.

## MEDIUM_OUTPUT
Sophia is a 45-year-old female merchant in the village. She runs a small general store, selling a variety of goods ranging from household items to local produce. Sophia is known for her business acumen, her friendly demeanor, and her deep knowledge of the community's needs.

## SEND_TO_NODES
- NONE

## CREATE_NODES
- [farmer_lucas.md] -d "Lucas is a 50-year-old male farmer in the village. He primarily grows grains and vegetables, supplying local markets and Sophia's general store. Lucas is a dedicated and hardworking individual, known for his expertise in sustainable farming practices and his commitment to the community." -p "Create a profile for a male farmer in the village." -g "You are a villager. Send CREATE_NODES request by outlining other villagers, until you are satisfied with the diversity of the community. Use their names as the file names. Setup their profiles (ex. jobs, families, age, gender, etc) in a realistic and detailed manner. After, and ONLY after you are satisfied with the listed villagers, SEND_TO concluder.md to end the process."
- [blacksmith_johanna.md] -d "Johanna is a 38-year-old female blacksmith in the village. She is a skilled craftswoman who creates tools, weapons, and various metalworks for the villagers. Johanna is known for her strength, precision, and creativity in her trade, as well as for her willingness to mentor younger villagers interested in metalworking." -p "Create a profile for a female blacksmith in the village." -g "You are a villager. Send CREATE_NODES request by outlining other villagers, until you are satisfied with the diversity of the community. Use their names as the file names. Setup their profiles (ex. jobs, families, age, gender, etc) in a realistic and detailed manner. After, and ONLY after you are satisfied with the listed villagers, SEND_TO concluder.md to end the process."
- [teacher_elizabeth.md] -d "Elizabeth is a 30-year-old female teacher in the village. She teaches children of various ages in a one-room schoolhouse, covering basic subjects such as reading, writing, arithmetic, and history. Elizabeth is respected for her patience, wisdom, and dedication to educating the next generation." -p "Create a profile for a female teacher in the village." -g "You are a villager. Send CREATE_NODES request by outlining other villagers, until you are satisfied with the diversity of the community. Use their names as the file names. Setup their profiles (ex. jobs, families, age, gender, etc) in a realistic and detailed manner. After, and ONLY after you are satisfied with the listed villagers, SEND_TO concluder.md to end the process."
