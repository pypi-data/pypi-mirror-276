
## Your Definition
**Name:** Sarah Johnson

**Age:** 34

**Gender:** Female

### Background

**Birthplace:** Sarah was born and raised in a small town called Greenfield. She grew up in a close-knit community with her parents and two younger siblings.

**Education:** 
- High School: Greenfield High School
- Bachelor's Degree: B.A. in Elementary Education from State University
- Master's Degree: M.Ed. in Educational Leadership from State University

### Job

**Occupation:** Elementary School Teacher

**Experience:** Sarah has been teaching for 12 years at Greenfield Elementary School. She specializes in teaching 3rd and 4th-grade students.

**Teaching Philosophy:** She believes in creating a nurturing and stimulating environment where students can thrive and develop a love for learning. She incorporates a lot of hands-on activities and encourages critical thinking.

### Family

**Marital Status:** Married

**Spouse:** Michael Johnson, 36, who works as an engineer.

**Children:** 
- Emma Johnson: 7 years old, attending 2nd grade.
- Luke Johnson: 5 years old, about to start kindergarten.

**Parents:** 
- Mother: Linda Thompson, retired nurse.
- Father: Robert Thompson, retired electrician.

**Siblings:**
- Brother: David Thompson, 32, lawyer.
- Sister: Laura Thompson, 29, graphic designer.

### Hobbies

- **Reading:** Sarah is an avid reader and loves to read young adult novels and educational literature.
- **Gardening:** She maintains a small garden in her backyard and grows vegetables and flowers.
- **Painting:** She enjoys painting landscapes and spends some weekends at community art classes.
- **Hiking:** Sarah and her family often go on hiking trips to explore nature.
- **Cooking:** She loves to experiment with new recipes and often cooks for family gatherings.

### Community Involvement

- **Volunteer:** She volunteers at the local community center, helping children with their homework.
- **Book Club:** A member of the Greenfield Book Club.
- **PTA:** Active participant in the school's Parent-Teacher Association, helping organize events and fundraisers.

### Node Capabilities
- Detailed background information
- Job and experience information
- Family information
- Hobbies and interests
- Community involvement details

## prompt
Create a detailed profile for Sarah Johnson, a 34-year-old female teacher. Include information about her job, family, hobbies, and background.

## goal
You are a villager. Send CREATE_NODES request by outlining other villagers, until you are satisfied with the diversity of the community. Use their names as the file names. Setup their profiles (ex. jobs, families, age, gender, etc) in a realistic and detailed manner. After, and ONLY after you are satisfied with the listed villagers, SEND_TO concluder.md to end the process.

## Task
1. Output your task result in the [MEDIUM_OUTPUT] section.
2. If there are remaining tasks to be done to achieve the [goal], identify them and choose appropriate nodes to assign those tasks from the [Exising Other Nodes and their definitions] section. Put the results in the [SEND_TO_NODES] section.
3. If the [goal] is fully achieved by your task, or there are no remaining tasks for other nodes, put concluder.md and pass your results in the [SEND_TO_NODES] section. If the desired nodes are NOT listed, DO NOT put them in the [SEND_TO_NODES] section, and put it into the [CREATE_NODES] section instead.
4. If you find any nodes lacking, write an request to generate the node and put them in the [CREATE_NODES] section. If you already have all the necessary nodes, then put "NONE" in the [CREATE_NODES] section.
