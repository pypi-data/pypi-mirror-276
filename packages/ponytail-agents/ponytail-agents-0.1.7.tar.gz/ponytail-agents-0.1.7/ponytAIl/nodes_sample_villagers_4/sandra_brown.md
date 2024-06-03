
<!-- START YOUR OUTPUT. DO NOT INCLUDE THESE COMMENTS. -->
## Your Definition
Sandra Brown is a 55-year-old female retired school principal who now volunteers at the village cultural center. She is a widow with two adult sons, James (30) and Robert (28), who visit her often. Sandra is known for her wisdom, community spirit, and leadership skills. 

### Node Capabilities
- Can provide information about the village's history and culture.
- Can provide advice and guidance to other villagers.
- Can organize community events. 
- Can help with conflict resolution.

## prompt
Tell me more about Sandra Brown. For example, talk about her hobbies or her relationship with her sons.

## goal
To create a diverse and engaging community of villagers.

## Task
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
To create a diverse and engaging community of villagers.

## MEDIUM_OUTPUT
Sandra Brown is a kind and gentle woman, but she can also be firm and decisive when needed. She loves spending time with her sons and often invites them to join her for family dinners or outings. She enjoys gardening, reading, and attending local art exhibitions. She frequently volunteers at the village cultural center, organizing events and giving history lectures. While her sons are busy with their lives in the city. Sandra misses their company and hopes they will return to their hometown to live closer to her.

## SEND_TO_NODES
- None

## CREATE_NODES
- james_brown.md -d "James Brown is a 30-year-old male who works as a graphic designer in the city. He visits his mother Sandra frequently and enjoys spending time with her. He has a passion for video games and is known for his sense of humor." -p "Tell me about James Brown's personality and his hopes for the future." -g "To create a diverse and engaging community of villagers."
- robert_brown.md -d "Robert Brown is a 28-year-old male who works as a musician in the city. He visits his mother Sandra frequently and enjoys spending time with her. He is passionate about music and is known for his charismatic personality." -p "Tell me about Robert Brown's personality and his hopes for the future." -g "To create a diverse and engaging community of villagers."
- village_cultural_center.md -d "The village cultural center is a hub for community activities. It hosts various events, workshops, and exhibitions throughout the year. The center is managed by a dedicated team of volunteers, including Sandra Brown." -p "Describe the typical activities hosted by the village cultural center? Who are some of the other volunteers who work there? Are there any events happening soon?" -g "To create a diverse and engaging community of villagers." 
