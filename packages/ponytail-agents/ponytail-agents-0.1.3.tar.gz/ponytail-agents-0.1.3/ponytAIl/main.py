import sys
import os
from pathlib import Path
import argparse
import random
import flute
from flute.Modules.PromptProcessorFactory import PromptProcessorFactory
import re
from datetime import datetime

def select_model(model):
    if model == "random-fast":
        fast_models = ["gpt-4o", "claude-3-haiku-20240307", "models/gemini-1.5-flash-latest"]
        return random.choice(fast_models)
    elif model == "random-accurate":
        accurate_models = ["gpt-4-turbo", "claude-3-opus-20240229", "models/gemini-1.5-pro-latest"]
        return random.choice(accurate_models)
    else:
        return model

def create_node(folder, file_name, task, goal, node_definition, model, processor, output_file):
    with open(os.path.join(folder, "node_creator.md"), "r", encoding="utf-8") as file:
        system = file.read()
        system = system.replace("[node_definition]", node_definition, 1)
        system = system.replace("[file_name]", file_name, 1)
        system = system.replace("[goal]", goal, 1)

    selected_model = select_model(model)
    factory = PromptProcessorFactory()
    processor = factory.create_prompt_processor(selected_model)
    response = processor.generate_response(task, temperature=1.0, top_p=1.0, max_tokens=4096, system=system).strip()
    
    if response.startswith('```'):
        response = response[3:]
    if response.endswith('```'):
        response = response[:-3]

    print(f"model: {selected_model}")
    print(response)

    with open(os.path.join(folder, file_name), "w", encoding="utf-8") as file:
        file.write(response)
    with open(output_file, "a", encoding="utf-8") as file:
        file.write(f"File : {file_name} has been created.\n---\n")  # 改行と区切り線を追加して、実行ごとに区切る

def process_nodes(folder, nodes, task, goal, model, processor, output_file):
    for node in nodes:
        file_path = os.path.join(folder, node["file_name"])
        with open(file_path, "r", encoding="utf-8") as file:
            system = file.read()
            system = system.replace("[goal]", goal, 1)

        selected_model = select_model(model)
        factory = PromptProcessorFactory()
        processor = factory.create_prompt_processor(selected_model)
        response = processor.generate_response(task, temperature=1.0, top_p=1.0, max_tokens=4096, system=system).strip()

        if response.startswith('```'):
            response = response[3:]
        if response.endswith('```'):
            response = response[:-3]

        print(f"model: {selected_model}")
        print(f"file: {node}")
        print(response)

        node["response"] = response
        file_name = node["file_name"] # バグ対策
        # 結果をファイルに追記する
        full_results = f"model: {selected_model}\nfile: {file_name}\n## RESPONSE\n{response}\n" # 結果を格納
        with open(output_file, "a", encoding="utf-8") as file:
            file.write(full_results + "\n---\n")  # 改行と区切り線を追加して、実行ごとに区切る

def process_response(response, folder, goal, model, processor, iteration, nodes, concluder_inputs, output_file):
    if response.split("## SEND_TO_NODES")[1].split("## CREATE_NODES")[0].find("NONE") >= 0 and response.split("## CREATE_NODES")[1].find("NONE") >= 0:
        return nodes, concluder_inputs

    send_to_nodes = re.findall(r"- *\[?(.*?)\]? *-p *\"(.*?)\" *-g *\"(.*?)\"", response.split("## SEND_TO_NODES")[1].split("## CREATE_NODES")[0], re.DOTALL)
    create_nodes = re.findall(r"- *\[?(.*?)\]? *-d *\"(.*?)\" *-p *\"(.*?)\" *-g *\"(.*?)\"", response.split("## CREATE_NODES")[1], re.DOTALL)

    for node_info in create_nodes:
        node_name = node_info[0]
        node_definition = node_info[1]
        task = node_info[2]
        if not os.path.exists(os.path.join(folder, node_name)):
            create_node(folder, node_name, task, goal, node_definition, model, processor, output_file)
        nodes.append({"file_name": node_name, "response": ""})

    if not send_to_nodes and not create_nodes:
        return nodes, concluder_inputs

    iteration += 1
    print(f"iteration: {iteration}")
    with open(output_file, "a", encoding="utf-8") as file:
        file.write(f"iteration: {iteration}\n")

    for node_info in send_to_nodes:
        node_name = node_info[0]
        task = node_info[1]
        if node_name == "concluder.md":
            concluder_inputs.append(task)
        else:
            if not os.path.exists(os.path.join(folder, node_name)):
                node_definition = processor.generate_response(f"## Task\nDefine the role of the node given the node name \"{node_name}\" and the \"{goal}\". Only output the result.", temperature=1.0, top_p=1.0, max_tokens=4096).strip()
                print(node_definition)
                create_node(folder, node_name, task, goal, node_definition, model, processor)

            nodes.append({"file_name": node_name, "response": ""})

    process_nodes(folder, nodes, task, goal, model, processor, output_file)

    for node in nodes:
        nodes, concluder_inputs = process_response(node["response"], folder, goal, model, processor, iteration, nodes, concluder_inputs, output_file)

    return nodes, concluder_inputs

def main():
    parser = argparse.ArgumentParser(description="Ponytail command-line interface")
    parser.add_argument("-f", "--file_path", required=True, help="Path to the input folder")
    parser.add_argument("-g", "--goal", required=True, help="Goal or objective of the task")
    parser.add_argument("-m", "--model", default="random-fast", help="Name of the model to use")
    parser.add_argument("-r", "--result", default="", help="Additional result or output (optional)")

    args = parser.parse_args()

    file_path = args.file_path
    goal = args.goal
    model = args.model
    result = args.result

    required_files = ["starter.md", "concluder.md", "node_creator.md"]
    missing_files = []
    folder = os.path.dirname(file_path)
    for file in required_files:
        if not os.path.exists(os.path.join(folder, file)):
            missing_files.append(file)

    if missing_files:
        print(f"Error: The following files are missing in the specified folder:")
        for file in missing_files:
            print(f"- {file}")
        sys.exit(1)

    iteration = 1

    # 現在の日時からタイムスタンプを生成
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # 結果を保存するファイルのパス
    output_folder = os.path.dirname(folder)
    output_file = os.path.join(output_folder, f"full_results_{timestamp}.md")

    selected_model = select_model(model)
    factory = PromptProcessorFactory()
    processor = factory.create_prompt_processor(selected_model)

    with open(file_path, "r", encoding="utf-8") as file:
        system = file.read()

    file_list = [file for file in Path(folder).glob("*.md") if file.name != os.path.basename(file_path)]
    embedded_content = ""
    for file_path in file_list:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            sections = content.split("##")
            for i, section in enumerate(sections):
                if "Your Definition" in section:
                    definition_section = section.split("##")[0].strip()
                    next_section_index = i + 1
                    if next_section_index < len(sections):
                        definition_section = definition_section.replace("Your Definition", "").split(sections[next_section_index])[0].strip()
                    embedded_content += f"### {file_path.name}\n{definition_section}\n"
                    break

    system = system.replace("[TO BE EMBEDDED]", embedded_content)
    # デバッグ用
    # print(system)

    response = processor.generate_response(goal, temperature=1.0, top_p=1.0, max_tokens=4096, system=system).strip()

    if response.startswith('```'):
        response = response[3:]
    if response.endswith('```'):
        response = response[:-3]

    print(f"iteration: {iteration}")
    print(f"model: {selected_model}")
    print(response)

    # 結果をファイルに追記する
    full_results = f"iteration: {iteration}\nmodel: {selected_model}\nfile: {os.path.basename(file_path)}\n## RESPONSE\n{response}"
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(full_results + "\n---\n")  # 改行と区切り線を追加して、実行ごとに区切る

    nodes = []
    concluder_inputs = []

    nodes, concluder_inputs = process_response(response, folder, goal, model, processor, iteration, nodes, concluder_inputs, output_file)

    with open(os.path.join(folder, "concluder.md"), "r", encoding="utf-8") as file:
        system = file.read()
        system = system.replace("[goal]", goal, 1)

    final_prompt = "\n".join(concluder_inputs + [node["response"] for node in nodes])
    final_model = select_model(model)
    final_response = processor.generate_response(temperature=1.0, top_p=1.0, max_tokens=4096, system=system, prompt=final_prompt).strip()

    
    if final_response.startswith('```'):
        final_response = final_response[3:]
    if final_response.endswith('```'):
        final_response = final_response[:-3]

    print(f"Final model: {final_model}")
    print(f"Final response:\n{final_response}")
    full_results = f"iteration: {iteration}\nmodel: {final_model}\nfile: concluder.md\n## RESPONSE\n{final_response}"
    with open(output_file, "a", encoding="utf-8") as file:
        file.write(full_results)

if __name__ == "__main__":
    main()