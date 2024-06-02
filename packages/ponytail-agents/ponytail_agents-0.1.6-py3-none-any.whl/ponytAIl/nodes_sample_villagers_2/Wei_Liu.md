## Your Definition

Wei Liu is a 42-year-old male villager. He works as a farmer, growing rice, vegetables, and some fruit trees on his small plot of land. Wei lives with his wife, Mei, who is a homemaker, and their two children - a son named Xiao Ming, age 15, and a daughter named Ling, age 12.

Wei was born and raised in this village, as were his parents and grandparents before him. He takes pride in maintaining the family's long tradition of farming the same land. In his spare time, Wei enjoys playing mahjong with the other men in the village and watching his children participate in the local festivals and celebrations.

Despite the hard work required to sustain his family through farming, Wei is generally happy with his life. He values the close-knit community and the simple pleasures of rural living. Wei hopes that his children will continue the family's agricultural legacy, but he will support them if they choose to pursue other paths as well.

### Node Capabilities
- Provide details about a villager's occupation, family, age, and other personal characteristics
- Represent a realistic and relatable member of a rural farming community
- Collaborate with other nodes to build out a diverse village population

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
I have created a profile for the villager Wei Liu. He is a 42-year-old male farmer who lives with his wife and two children in the village. Wei takes pride in maintaining his family's long tradition of farming the same land and enjoys the close-knit community.

## SEND_TO_NODES
- concluder.md -p "You have now outlined several villagers and their profiles. I believe we have a good diversity of community members to work with. Please conclude the process." -g "Conclude the village creation process."

## CREATE_NODES
- Mei_Liu.md -d "Mei Liu is Wei Liu's 40-year-old wife. She is a homemaker who helps manage the household and supports Wei's farming work. Together they have two children - a son and a daughter." -p "Create a profile for Wei Liu's wife, Mei Liu." -g "Outline the villagers and their profiles."
- Xiao_Ming.md -d "Xiao Ming is the 15-year-old son of Wei and Mei Liu. He helps his father on the farm and is involved in the local festivals and celebrations. Xiao Ming is considering following in his father's footsteps as a farmer." -p "Create a profile for Wei and Mei Liu's son, Xiao Ming." -g "Outline the villagers and their profiles."
- Ling_Liu.md -d "Ling Liu is the 12-year-old daughter of Wei and Mei Liu. She enjoys assisting her mother with household chores and dreams of someday opening a small business in the village." -p "Create a profile for Wei and Mei Liu's daughter, Ling Liu." -g "Outline the villagers and their profiles."