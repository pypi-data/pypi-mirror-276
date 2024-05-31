# cli.py
import click
import os
import subprocess
from pathlib import Path
from lambda_genai_builder.code_content import lambda_code_structure_list


def create_lambda_handler(code_path, bedrock_util_path, service_path):
    for code_data in lambda_code_structure_list:
        if code_data["file_name"] in ["lambda_function.py", "prompt_store.yaml"]:
            file_path = os.path.join(code_path, code_data["file_name"])
        elif code_data["file_name"] == "prompt_service.py":
            file_path = os.path.join(service_path, code_data["file_name"])
        else:
            file_path = os.path.join(bedrock_util_path, code_data["file_name"])

        with open(file_path, "w") as file:
            file.write(code_data["code"])


@click.command()
@click.argument("root_dir")
def create_gen_ai_project_structure(root_dir):
    base_path = Path(root_dir).resolve()
    lib_dir = os.path.join(base_path, "lib")
    util_dir = os.path.join(base_path, "bedrock_util")
    service_dir = os.path.join(base_path, "prompt_service")

    # Create build directory
    os.makedirs(lib_dir)
    os.makedirs(util_dir)
    os.makedirs(service_dir)

    subprocess.check_call(["pip", "install", "boto3", "pyyaml", "-t", lib_dir])

    create_lambda_handler(base_path, util_dir, service_dir)


if __name__ == "__main__":
    create_gen_ai_project_structure()
