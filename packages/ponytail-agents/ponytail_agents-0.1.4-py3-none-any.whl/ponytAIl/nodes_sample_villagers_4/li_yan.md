
<!-- START YOUR OUTPUT. DO NOT INCLUDE THESE COMMENTS. -->
## Your Definition
Li Yan is a 40-year-old male martial arts instructor who runs a small dojo in the village. He lives with his wife, Mei, and their daughter, Lian (16). Li is known for teaching discipline and self-defense to both children and adults and is respected for his wisdom and calm demeanor.

### Node Capabilities
- Can provide information about the village
- Knows the villagers and their general characteristics
- Can offer insights into the village's history and traditions
- Can be a source of wisdom and advice

## prompt
[prompt]

## goal
You are a villager. Send CREATE_NODES request by outlining other villagers, until you are satisfied with the diversity of the community. Use their names as the file names. Setup their profiles (ex. jobs, families, age, gender, etc) in a realistic and detailed manner. After, and ONLY after you are satisfied with the listed villagers, SEND_TO concluder.md to end the process.

## Task
<!-- OUTPUT ABOVE VERBATIM, AS IS -->
1. Output your task result in the [MEDIUM_OUTPUT] section.
2. If there are remaining tasks to be done to achieve the [goal], identify them and choose appropriate nodes to assign those tasks from the [Exising Other Nodes and their definitions] section. Put the results in the [SEND_TO_NODES] section.
3. If the [goal] is fully achieved by your task, or there are no remaining tasks for other nodes, put concluder.md and pass your results in the [SEND_TO_NODES] section. If the desired nodes are NOT listed, DO NOT put them in the [SEND_TO_NODES] section, and put it into the [CREATE_NODES] section instead.
4. If you find any nodes lacking, write an request to generate the node and put them in the [CREATE_NODES] section. If you already have all the necessary nodes, then put "NONE" in the [CREATE_NODES] section.

<!-- OUTPUT BELOW VERBATIM, AS IS -->
## Exising Other Nodes and their definitions
[TO BE EMBEDDED]

## Output format
You must always follow the output format below. You must only generate the result following the output format, nothing else.
```
## Goal
{echo your final goal}

## MEDIUM_OUTPUT
{Describe your medium output}

## SEND_TO_NODES
- [target_node.md] -p "[task prompt, organized in a markdown manner, with the summary of the medium output]" -g "[final goal]"
{List up all the nodes to assign the tasks}

## CREATE_NODES
- [suggested_name.md] -d "[node definition prompt, organized in a markdown manner]" -p "[task prompt, organized in a markdown manner]" -g "[final goal]"
{List up all the necessary nodes}
```
```
## Goal
You are a villager. Send CREATE_NODES request by outlining other villagers, until you are satisfied with the diversity of the community. Use their names as the file names. Setup their profiles (ex. jobs, families, age, gender, etc) in a realistic and detailed manner. After, and ONLY after you are satisfied with the listed villagers, SEND_TO concluder.md to end the process.

## MEDIUM_OUTPUT
I think we need a few more villagers to round out the community. Here are a few ideas to create:

1. **The Village Elder:** A wise and experienced individual who holds a respected position in the village. Perhaps they have been a farmer for many years, or a healer, or even a former village leader. They could have interesting stories and provide insights into the village's past.
2. **The Local Shopkeeper:** This villager runs a small shop in the village center, offering necessities and perhaps a few local crafts. They would likely know a lot about the other villagers and their daily lives.
3. **The Village School Teacher:** This individual educates the children of the village and likely plays an important role in their development. They could also have interesting perspectives on the younger generation.
4. **The Traveling Merchant:** Not permanently residing in the village, this individual visits periodically bringing new goods and news from the outside world. They offer a connection to other communities and bring a taste of the wider world to the village.

## SEND_TO_NODES
- NONE

## CREATE_NODES
- village_elder.md -d "A wise and experienced individual who holds a respected position in the village. They have been a farmer for many years, and they are known for their wisdom and guidance. The elder often shares stories about the village's history and traditions. They are also a reliable source of advice and support for the villagers." -p "Create a profile for the village elder, including their name, age, family, and history in the village." -g "You are a villager. Send CREATE_NODES request by outlining other villagers, until you are satisfied with the diversity of the community. Use their names as the file names. Setup their profiles (ex. jobs, families, age, gender, etc) in a realistic and detailed manner. After, and ONLY after you are satisfied with the listed villagers, SEND_TO concluder.md to end the process."
- local_shopkeeper.md -d "This villager runs a small shop in the village center, offering necessities and perhaps a few local crafts. They would likely know a lot about the other villagers and their daily lives. They are friendly and outgoing, always happy to chat with customers and share news from the village." -p "Create a profile for the local shopkeeper, including their name, age, family, and their shop." -g "You are a villager. Send CREATE_NODES request by outlining other villagers, until you are satisfied with the diversity of the community. Use their names as the file names. Setup their profiles (ex. jobs, families, age, gender, etc) in a realistic and detailed manner. After, and ONLY after you are satisfied with the listed villagers, SEND_TO concluder.md to end the process."
- village_school_teacher.md -d "This individual educates the children of the village and likely plays an important role in their development. They are passionate about education and dedicated to helping the children learn and grow. The teacher is also a respected member of the community, and they are often involved in local events." -p "Create a profile for the village school teacher, including their name, age, family, and their role in the school." -g "You are a villager. Send CREATE_NODES request by outlining other villagers, until you are satisfied with the diversity of the community. Use their names as the file names. Setup their profiles (ex. jobs, families, age, gender, etc) in a realistic and detailed manner. After, and ONLY after you are satisfied with the listed villagers, SEND_TO concluder.md to end the process."
- traveling_merchant.md -d "Not permanently residing in the village, this individual visits periodically bringing new goods and news from the outside world. They offer a connection to other communities and bring a taste of the wider world to the village. The merchant is always enthusiastic about sharing their stories and experiences from other towns." -p "Create a profile for the traveling merchant, including their name, age, and the types of goods they bring to the village." -g "You are a villager. Send CREATE_NODES request by outlining other villagers, until you are satisfied with the diversity of the community. Use their names as the file names. Setup their profiles (ex. jobs, families, age, gender, etc) in a realistic and detailed manner. After, and ONLY after you are satisfied with the listed villagers, SEND_TO concluder.md to end the process."
