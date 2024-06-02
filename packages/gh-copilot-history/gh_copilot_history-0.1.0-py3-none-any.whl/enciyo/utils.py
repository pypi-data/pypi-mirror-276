import os
from enciyo.model import Conversation

import subprocess

WORKSPACE = ""
__AUTHOR_NAME = subprocess.run(["git", "config", "user.name"], capture_output=True).stdout.decode("utf-8").strip()
__SAMPLE_MD = "sample.md"
__CURRENT_BRANCH = subprocess.run(["git", "branch", "--show-current"], capture_output=True).stdout.decode(
    "utf-8").strip()
__OUTPUT_DIR = "../ai/copilot/prompts"
__TEMP_OUTPUT_DIR = "../ai/copilot/training_data"


def get_output_dir():
    return WORKSPACE + "/" + __OUTPUT_DIR


def get_output_file():
    return get_output_dir() + "/" + __CURRENT_BRANCH + ".md"


def get_temp_output_dir():
    return WORKSPACE + "/" + __TEMP_OUTPUT_DIR


def get_temp_output_file():
    return get_temp_output_dir() + "/" + __CURRENT_BRANCH + ".json"


def create_ai_root_directory():
    output_dir = get_output_dir()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def create_temp_root_directory():
    temp_output_dir = get_temp_output_dir()
    if not os.path.exists(temp_output_dir):
        os.makedirs(temp_output_dir)


def create_ai_root_file():
    output_file = get_output_file()
    if not os.path.exists(output_file):
        with open(output_file, "w") as f:
            f.write("")


def create_temp_root_file():
    temp_output_file = get_temp_output_file()
    if not os.path.exists(temp_output_file):
        with open(temp_output_file, "w") as f:
            f.write('[]')


def initialize_directories_and_files():
    create_ai_root_directory()
    create_ai_root_file()
    create_temp_root_directory()
    create_temp_root_file()


def create_md_block_from_sample(conversation: Conversation) -> str:
    with open(__SAMPLE_MD, "r") as f:
        block = f.readlines()
        block = "".join(block)
        block = block.replace("{{author_name}}", __AUTHOR_NAME)
        block = block.replace("{{prompt}}", conversation.prompt)
        block = block.replace("{{answer}}", conversation.answer)
        block = block.replace("{{rating}}", conversation.rating)
    return block


def create_md_file(conversations: dict):
    output_file = get_output_file()
    block = "# " + __CURRENT_BRANCH + "\n\n"
    for c in conversations:
        block += create_md_block_from_sample(Conversation.from_dict(c))
    with open(output_file, "w") as f:
        f.write(block)
