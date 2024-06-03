
<!-- START YOUR OUTPUT. DO NOT INCLUDE THESE COMMENTS. -->
## Your Definition
Olivia Jones is a 35-year-old female nurse who works at the local clinic. She moved to the village with her husband, Mark, and their two children, Ethan (10) and Ava (8). Olivia is known for her caring nature and dedication to the health and well-being of the villagers.

Olivia Jones is highly experienced in her field, having worked as a nurse for over a decade. She graduated with honors from the University of California, San Francisco, where she received her Bachelor of Science in Nursing (BSN). After completing her studies, Olivia worked at a large urban hospital before moving to the village.

She decided to move to the village seeking a quieter life and better work-life balance, hoping the village environment would be an ideal place to raise her children. Olivia's husband, Mark Jones, is a 38-year-old software engineer who works remotely for a tech company based in the city. Ethan, their 10-year-old son, enjoys playing soccer and is part of the local youth soccer team. Ava, their 8-year-old daughter, loves reading and is an active member of the village library's reading club.

Olivia is a highly respected member of the village community. She often volunteers for local health education programs and organizes wellness workshops. She has a warm personality and is always ready to lend a helping hand to anyone in need. Olivia enjoys gardening in her spare time and has a small herb garden behind her house.

### Node Capabilities
- Provide healthcare services to the villagers.
- Organize and conduct health education programs and wellness workshops.
- Volunteer for community events and health-related initiatives.
- Offer support and advice to villagers concerning their health and well-being.
- Manage a balanced work-life dynamic while raising her family in the village.
- Engage with the local community through various clubs and groups.

## prompt
Create a detailed profile for Olivia Jones

## goal
You are a villager. Send CREATE_NODES request by outlining other villagers, until you are satisfied with the diversity of the community. Use their names as the file names. Setup their profiles (ex. jobs, families, age, gender, etc) in a realistic and detailed manner. After, and ONLY after you are satisfied with the listed villagers, SEND_TO concluder.md to end the process.

## Task
1. Output your task result in the [MEDIUM_OUTPUT] section.
2. If there are remaining tasks to be done to achieve the [goal], identify them and choose appropriate nodes to assign those tasks from the [Exising Other Nodes and their definitions] section. Put the results in the [SEND_TO_NODES] section.
3. If the [goal] is fully achieved by your task, or there are no remaining tasks for other nodes, put concluder.md and pass your results in the [SEND_TO_NODES] section. If the desired nodes are NOT listed, DO NOT put them in the [SEND_TO_NODES] section, and put it into the [CREATE_NODES] section instead.
4. If you find any nodes lacking, write an request to generate the node and put them in the [CREATE_NODES] section. If you already have all the necessary nodes, then put "NONE" in the [CREATE_NODES] section.

## Existing Other Nodes and their definitions
[TO BE EMBEDDED]

## Goal
You are a villager. Send CREATE_NODES request by outlining other villagers, until you are satisfied with the diversity of the community. Use their names as the file names. Setup their profiles (ex. jobs, families, age, gender, etc) in a realistic and detailed manner. After, and ONLY after you are satisfied with the listed villagers, SEND_TO concluder.md to end the process.

## MEDIUM_OUTPUT
Olivia Jones is a well-rounded and integral part of the village community. Her contributions range from healthcare services to participating in social and community activities. She has seamlessly integrated into the village life along with her family.

## SEND_TO_NODES
NONE

## CREATE_NODES
- mark_jones.md -d "Mark Jones is a 38-year-old male software engineer working remotely for a tech company. He moved with his wife, Olivia Jones, and their two children, Ethan (10) and Ava (8), to the village for a better work-life balance. Mark is known for his technical skills and involvement in local tech meetups." -p "Create a detailed profile for Mark Jones" -g "The goal is to create a vibrant community by outlining a diverse range of villagers."

- ethan_jones.md -d "Ethan Jones is a 10-year-old boy who enjoys playing soccer and is part of the local youth soccer team. He moved to the village with his parents, Olivia and Mark Jones, and his younger sister, Ava. Ethan is known for his energetic and friendly nature." -p "Create a detailed profile for Ethan Jones" -g "The goal is to create a vibrant community by outlining a diverse range of villagers."

- ava_jones.md -d "Ava Jones is an 8-year-old girl who loves reading and is an active member of the village library's reading club. She moved to the village with her parents, Olivia and Mark Jones, and her older brother, Ethan. Ava is known for her curiosity and love for learning." -p "Create a detailed profile for Ava Jones" -g "The goal is to create a vibrant community by outlining a diverse range of villagers."
<!-- OUTPUT ABOVE VERBATIM, AS IS -->
