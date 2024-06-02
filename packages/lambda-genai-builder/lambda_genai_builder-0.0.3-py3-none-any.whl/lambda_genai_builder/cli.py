# cli.py
import click
import os
import subprocess
from pathlib import Path
from lambda_genai_builder.code_content import lambda_code_structure_list


def create_lambda_handler(code_path):
    for code_data in lambda_code_structure_list:
        if code_data["file_name"] in ["lambda_function.py", "prompt_store.yaml"]:
            file_path = os.path.join(code_path, code_data["file_name"])

        with open(file_path, "w") as file:
            file.write(code_data["code"])


@click.command()
@click.argument("root_dir")
def create_gen_ai_project_structure(root_dir):
    base_path = Path(root_dir).resolve()
    lib_dir = os.path.join(base_path, "lambda_util")

    # Create build directory
    os.makedirs(lib_dir)

    #install boto3
    subprocess.check_call(["pip", "install", "boto3", "-t", base_path])

    subprocess.check_call(["pip", "install", "lambda-genai-util", "pyyaml", "-t", lib_dir])

    create_lambda_handler(base_path)


if __name__ == "__main__":
    create_gen_ai_project_structure()
