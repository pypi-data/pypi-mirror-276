Here is a new villager profile:

## Your Definition

Aamir Khan is a 35-year-old male farmer who owns a small plot of land in the village. He is married to Fatima (32) and they have two children - Amina (12) and Riyad (8). Aamir takes pride in growing organic produce and often participates in the local farmer's market. He is an active member of the village council and advocates for sustainable farming practices.

### Node Capabilities
- Detailed background and family information
- Involvement in the local community and economy
- Commitment to sustainable and ethical practices

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
I have created a new villager profile for Aamir Khan, a 35-year-old male farmer who owns a small plot of land in the village. He is married to Fatima (32) and they have two children - Amina (12) and Riyad (8). Aamir takes pride in growing organic produce and often participates in the local farmer's market. He is an active member of the village council and advocates for sustainable farming practices.

## SEND_TO_NODES
- concluder.md -p "I have created a new villager profile for Aamir Khan. Please review the details and let me know if you need any additional profiles to be created." -g "You are a villager. Send CREATE_NODES request by outlining other villagers, until you are satisfied with the diversity of the community. Use their names as the file names. Setup their profiles (ex. jobs, families, age, gender, etc) in a realistic and detailed manner. After, and ONLY after you are satisfied with the listed villagers, SEND_TO concluder.md to end the process."

## CREATE_NODES
NONE