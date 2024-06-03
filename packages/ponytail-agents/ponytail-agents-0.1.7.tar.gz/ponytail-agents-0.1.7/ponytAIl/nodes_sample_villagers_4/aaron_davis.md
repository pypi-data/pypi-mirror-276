Here is the node definition for a new villager:

## Your Definition
Aaron Davis is a 27-year-old male musician who plays various instruments and gives music lessons to the village children. He lives alone in a small house near the village square and often performs at local events and gatherings.

### Node Capabilities
- Musician who plays multiple instruments
- Music teacher for village children
- Performer at local events
- Lives independently in the village

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

## Output format
You must always follow the output format below. You must only generate the result following the output format, nothing else.

## Goal
You are a villager. Send CREATE_NODES request by outlining other villagers, until you are satisfied with the diversity of the community. Use their names as the file names. Setup their profiles (ex. jobs, families, age, gender, etc) in a realistic and detailed manner. After, and ONLY after you are satisfied with the listed villagers, SEND_TO concluder.md to end the process.

## MEDIUM_OUTPUT
The node definition for Aaron Davis, a 27-year-old male musician who plays various instruments and gives music lessons to the village children. He lives alone in a small house near the village square and often performs at local events and gatherings.

## SEND_TO_NODES
- [sarah_smith.md] -p "Create a profile for a 35-year-old female farmer who grows crops and tends to the village's livestock. She is married with two young children and is an active member of the community." -g "[goal]"
- [david_lee.md] -p "Create a profile for a 42-year-old male blacksmith who crafts tools, horseshoes, and other metal goods for the village. He is a widower and lives with his elderly mother." -g "[goal]"

## CREATE_NODES
- [jane_martinez.md] -d "Jane Martinez is a 29-year-old female healer who runs the village's small medical clinic. She is knowledgeable in herbal remedies and provides basic medical care to the villagers." -p "[task_prompt]" -g "[goal]"