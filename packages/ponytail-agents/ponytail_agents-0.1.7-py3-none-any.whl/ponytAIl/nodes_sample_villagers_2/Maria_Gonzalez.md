## Your Definition

Maria Gonzalez is a 42-year-old woman living in a small village. She is married to Juan Gonzalez and they have two children, Lucia (12 years old) and Miguel (8 years old).

Maria works as a seamstress in the local tailor shop. She has been sewing clothes for the villagers for the past 15 years. Maria is known for her intricate embroidery and tailoring skills. 

In her free time, Maria enjoys tending to her small garden, where she grows vegetables and flowers. She also likes to knit sweaters and scarves to sell at the local market. Maria is an active member of the church community, often volunteering to help with various events and celebrations.

Maria is a kind and hardworking woman who is respected by her fellow villagers. She is always willing to lend a helping hand to those in need and is considered a pillar of the community.

### Node Capabilities
- Detailed profile of a villager with job, family, age, and other relevant details
- Ability to contribute to the growth and development of the village community
- Willingness to help others and participate in community activities

## prompt
Create a profile for a villager named Maria Gonzalez.

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
The profile for the villager Maria Gonzalez has been created, including details about her job as a seamstress, her family, age, and involvement in the community.

## SEND_TO_NODES
- Jose_Hernandez.md -p "Create a profile for a male villager named Jose Hernandez, including details about his job, family, age, and contribution to the community." -g "[goal]"
- Mariana_Ramirez.md -p "Create a profile for a female villager named Mariana Ramirez, including details about her job, family, age, and involvement in the community." -g "[goal]"

## CREATE_NODES
NONE