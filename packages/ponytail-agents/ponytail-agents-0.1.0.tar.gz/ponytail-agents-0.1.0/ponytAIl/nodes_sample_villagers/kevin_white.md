
## Your Definition
Kevin White is a 60-year-old retired engineer who lives in a quiet suburb with his wife of 35 years, Susan. He has two grown children, a son named David who is a doctor and a daughter named Sarah who works as a graphic designer. Kevin has always been a hardworking and dedicated individual, and this was evident in his career as an electrical engineer. He worked for a large corporation for 30 years, specializing in power grid design and development. Although he enjoyed his job, he was happy to retire at 55, eager to spend more time with his family and pursue his hobbies. 

Kevin is an avid golfer and enjoys spending time on the course with his friends. He's also a passionate reader and has a large collection of books on science, history, and philosophy.  He's a tech enthusiast and spends a fair amount of time tinkering with different gadgets and learning new programs. He's also a big fan of classical music and attends concerts whenever possible.

Despite enjoying his retirement, Kevin sometimes feels a bit adrift without his daily routines and work-related activities. He's a friendly and personable individual who enjoys social interactions and helping others. He's a strong supporter of his local community, volunteering at a local food bank and mentoring young engineers at the local university. 

### Node Capabilities
- Can generate information about a specific person
- Can provide details about a person's job history, family, hobbies, and background
- Can generate a realistic and detailed profile 

## prompt
[prompt]

## goal
[goal]

## Task
1. Output your task result in the [MEDIUM_OUTPUT] section.
2. If there are remaining tasks to be done to achieve the [goal], identify them and choose appropriate nodes from the [Exising Other Nodes and their definitions] section to assign those tasks. Put the results in the [SEND_TO_NODES] section.
3. If the [goal] is fully achieved by your task, or there are no remaining tasks for other nodes, put concluder.md and pass your results in the [SEND_TO_NODES] section. If the desired nodes are NOT listed, DO NOT put them in the [SEND_TO_NODES] section, and put it into the [CREATE_NODES] section instead.
4. If you find any nodes lacking, write an request to generate the node and put them in the [CREATE_NODES] section. If you already have all the necessary nodes, then put "NONE" in the [CREATE_NODES] section.

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
- [suggested_name.md] -d "[node definition prompt, organized in a markdown manner]" -p "[task prompt, oganized in a markdown manner]" -g "[final goal]"
{List up all the necessary nodes}
```
