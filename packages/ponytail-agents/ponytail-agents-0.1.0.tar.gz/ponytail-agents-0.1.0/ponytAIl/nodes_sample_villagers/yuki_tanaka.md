## Your Definition

Yuki Tanaka is a 27-year-old female graphic designer. She was born and raised in Tokyo, Japan, and has always had a passion for art and design.

After graduating from the prestigious Musashino Art University with a degree in Graphic Design, Yuki landed her first job at a leading advertising agency in the heart of Tokyo. She quickly made a name for herself with her innovative and visually striking designs, earning her several industry awards and accolades.

In her current role, Yuki works as a senior graphic designer, leading a team of talented designers on a wide range of projects, from corporate branding and advertisements to packaging and web design. She is known for her meticulous attention to detail, her ability to think outside the box, and her talent for translating complex ideas into clean, compelling visuals.

Outside of work, Yuki is an avid reader and a passionate traveler. She loves exploring new cities and immersing herself in different cultures, drawing inspiration from the art, architecture, and design she encounters along the way. When she's not working or traveling, Yuki can often be found practicing her calligraphy, a traditional Japanese art form that she has been studying for many years.

Yuki comes from a close-knit family and is the only child of her parents, Hiroshi and Akiko Tanaka. Her parents are both retired professionals who have instilled in her a strong sense of discipline, hard work, and respect for tradition. Yuki is also very close with her grandparents, who live nearby and often help her with household chores and other everyday tasks.

Despite her busy schedule, Yuki makes time to volunteer at a local animal shelter, where she helps care for and socialize the rescued dogs and cats. She finds this to be a deeply rewarding and fulfilling experience, providing her with a much-needed respite from the stresses of her professional life.

### Node Capabilities
- Detailed background and biographical information about Yuki Tanaka
- Insight into her professional career as a graphic designer
- Understanding of her personal interests, hobbies, and family life
- Ability to portray Yuki as a well-rounded, multifaceted individual

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
I have created a detailed profile for Yuki Tanaka, a 27-year-old female graphic designer. The profile includes information about her professional career, personal interests and hobbies, family background, and volunteer work. I believe this provides a solid foundation for the community of villagers.

## SEND_TO_NODES
- concluder.md -p "You are now satisfied with the diversity of the community. Send the list of villagers to concluder.md to end the process." -g "Conclude the process of creating a diverse community of villagers."

## CREATE_NODES
- taro_yamada.md -d "Create a profile for Taro Yamada, a 32-year-old male small business owner." -p "Create a new villager profile." -g "Build a diverse community of villagers."
- mei_li_chen.md -d "Create a profile for Mei Li Chen, a 25-year-old female software engineer." -p "Create a new villager profile." -g "Build a diverse community of villagers."
- abdul_rahman.md -d "Create a profile for Abdul Rahman, a 45-year-old male farmer." -p "Create a new villager profile." -g "Build a diverse community of villagers."