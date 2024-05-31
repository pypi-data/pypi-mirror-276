lambda_code_structure_list = [
    {
        "code": """from bedrock_util.TextCompletionUtil import generate_text_completion
from prompt_service import prompt_service


def lambda_handler(event, context):
    \"""
    This block of code demonstrates how to invoke methods for generating text completions
    and running a prompt service flow based on service ID which it verifies from prompt_store.yaml file.


    example:

    If we want to directly use the FM API
    print(generate_text_completion(event['model'], event['prompt']))

    If we want to use existing prompt flow
    if "prompt_input" in event:
        print(prompt_service.run_service("getMathDetails", event['model'], event["prompt_input"]))


    1. The first line generates a text completion using the model and prompt provided in the event,
       and prints the result.
    2. The if-statement checks if the 'prompt_input' key exists in the event.
       If it does, it runs the 'getMathDetails' service using the model and prompt input from the event,
       and prints the result.    

    \"""



    return {
        'statusCode': 200,
        'body': 'Hello from Lambda!'
    }""",
        "file_name": "lambda_function.py",
    },
    {
        "code": """import logging
from lib import boto3
from bedrock_util.MetaBedrockUtil import MetaBedrockUtil
from bedrock_util.MistralBedrockUtil import MistralBedrockUtil
from bedrock_util.AwsTitanBedrockUtil import AwsTitanBedrockUtil
from bedrock_util.AnthropicBedrockUtil import AnthropicBedrockUtil
from bedrock_util.CohereBedrockUtil import CohereBedrockUtil
from bedrock_util.model_map import model_map

bedrock = boto3.client(service_name='bedrock-runtime')
logger = logging.getLogger(__name__)

def generate_text_completion(model: str, prompt, **model_kwargs):
    if model is None or model_map.get(model) is None:
        logger.warning(f"Invalid model: {model}")
        return None

    fm_provider = model_map[model]
    fm_utils = {
        "Amazon": AwsTitanBedrockUtil,
        "Anthropic": AnthropicBedrockUtil,
        "Cohere": CohereBedrockUtil,
        "Meta": MetaBedrockUtil,
        "Mistral AI": MistralBedrockUtil
    }

    try:
        fm = fm_utils[fm_provider]()
        result = fm.text_completion(bedrock_client=bedrock, model=model, prompt=prompt, **model_kwargs)
        logger.info(f"Text completion generated for model: {model}")
        return result
    except KeyError:
        logger.error(f"Unsupported provider: {fm_provider}")
    except Exception as e:
        logger.exception(f"Error generating text completion for model: {model}")

    return None""",
        "file_name": "TextCompletionUtil.py",
    },
    {
        "code": """import json
import logging

from bedrock_util.BedrockUtil import BedrockUtil

logger = logging.getLogger(__name__)

class AwsTitanBedrockUtil(BedrockUtil):

    def text_completion(self, bedrock_client, model, prompt, **model_kwargs):
        prompt_request = {}
        prompt_response = {}
        model_id = model

        if prompt:
            prompt_request["inputText"] = prompt

            text_config = {
                'temperature': model_kwargs.get("temperature"),
                'topP': model_kwargs.get("top_p"),
                'maxTokenCount': model_kwargs.get("max_token")
            }
            stop_sequences = model_kwargs.get('stop_sequences')
            
            if stop_sequences:
                text_config['stopSequences'] = [seq.strip() for seq in stop_sequences.split(',') if seq.strip()]

            text_config = {k: v for k, v in text_config.items() if v}

            if text_config:
                prompt_request['textGenerationConfig'] = text_config

            body = json.dumps(prompt_request)
            accept = "application/json"
            content_type = "application/json"

            try:
                response = bedrock_client.invoke_model(
                    body=body, modelId=model_id, accept=accept, contentType=content_type
                )
                response_body = json.loads(response.get("body").read())
                prompt_response['output'] = response_body['results'][0]['outputText']
            except Exception as e:
                logger.error(f"Error in text_completion: {str(e)}")
                raise

        return prompt_response
""",
        "file_name": "AwsTitanBedrockUtil.py",
    },
    {
        "code": """import json
import logging

from bedrock_util.BedrockUtil import BedrockUtil

logger = logging.getLogger(__name__)

class AnthropicBedrockUtil(BedrockUtil):

    def text_completion(self, bedrock_client, model, prompt, **model_kwargs):
        prompt_request = {}
        prompt_response = {}
        model_id = model

        if prompt:
            try:
                prompt_request['anthropic_version'] = 'bedrock-2023-05-31'
                prompt_request["messages"] = [{"role": "user", "content": prompt}]
                prompt_request.update(model_kwargs)
                prompt_request.setdefault("max_tokens", 4000)

                body = json.dumps(prompt_request)
                accept = "application/json"
                content_type = "application/json"

                response = bedrock_client.invoke_model(
                    body=body, modelId=model_id, accept=accept, contentType=content_type
                )
                response_body = json.loads(response.get("body").read())

                prompt_response['output'] = response_body['content'][0]['text']

            except (KeyError, IndexError) as e:
                logger.error(f"Error occurred while processing response: {e}")
                prompt_response['output'] = None

            except Exception as e:
                logger.exception(f"An unexpected error occurred: {e}")
                raise

        return prompt_response
""",
        "file_name": "AnthropicBedrockUtil.py",
    },
    {
        "code": """import json
import logging
from bedrock_util.BedrockUtil import BedrockUtil

logger = logging.getLogger(__name__)

class CohereBedrockUtil(BedrockUtil):

    def text_completion(self, bedrock_client, model, prompt, **model_kwargs):
        prompt_request = {}
        prompt_response = {}
        model_id = model

        if prompt:
            if "command-r" in model_id:
                prompt_request['message'] = prompt
            else:
                prompt_request["prompt"] = prompt

            prompt_request.update(model_kwargs)

            body = json.dumps(prompt_request)
            accept = "application/json"
            content_type = "application/json"

            try:
                response = bedrock_client.invoke_model(
                    body=body, modelId=model_id, accept=accept, contentType=content_type
                )
                response_body = json.loads(response.get("body").read())

                if "command-r" in model_id:
                    prompt_response['output'] = response_body.get('text', '')
                else:
                    prompt_response['output'] = response_body.get('generations', [{}])[0].get('text', '')

            except Exception as e:
                logger.exception(f"Error in text_completion for model {model_id}: {str(e)}")
                raise

        return prompt_response
""",
        "file_name": "CohereBedrockUtil.py",
    },
    {
        "code": """import json
import logging

from bedrock_util.BedrockUtil import BedrockUtil

logger = logging.getLogger(__name__)

class MetaBedrockUtil(BedrockUtil):

    def text_completion(self, bedrock_client, model, prompt, **model_kwargs):
        prompt_request = {}
        prompt_response = {}
        model_id = model

        if prompt:
            prompt_request["prompt"] = prompt
            prompt_request.update(model_kwargs)

            try:
                body = json.dumps(prompt_request)
                accept = "application/json"
                content_type = "application/json"

                response = bedrock_client.invoke_model(
                    body=body, modelId=model_id, accept=accept, contentType=content_type
                )
                response_body = json.loads(response["body"].read())

                prompt_response['output'] = response_body['generation']

            except (KeyError, json.JSONDecodeError) as e:
                logger.error(f"Error processing response: {str(e)}")
                raise

            except Exception as e:
                logger.exception(f"Unexpected error occurred: {str(e)}")
                raise

        return prompt_response
""",
        "file_name": "MetaBedrockUtil.py",
    },
    {
        "code": """import json
import logging

from bedrock_util.BedrockUtil import BedrockUtil

logger = logging.getLogger(__name__)

class MistralBedrockUtil(BedrockUtil):

    def text_completion(self, bedrock_client, model, prompt, **model_kwargs):
        prompt_request = {}
        prompt_response = {}
        model_id = model

        if prompt:
            prompt_request["prompt"] = prompt
            prompt_request.update(model_kwargs)

            try:
                response = bedrock_client.invoke_model(
                    body=json.dumps(prompt_request),
                    modelId=model_id,
                    accept="application/json",
                    contentType="application/json"
                )
                response_body = json.loads(response["body"].read())
                prompt_response['output'] = response_body['outputs'][0]['text']
            except (KeyError, IndexError) as e:
                logger.error(f"Error extracting output from response: {e}")
                raise
            except Exception as e:
                logger.error(f"Error invoking model: {e}")
                raise

        return prompt_response
""",
        "file_name": "MistralBedrockUtil.py",
    },
    {
        "code": """from abc import ABC, abstractmethod


class BedrockUtil(ABC):

    @abstractmethod
    def text_completion(self, bedrock_client, model, prompt, **model_kwargs):
        pass
""",
        "file_name": "BedrockUtil.py",
    },
    {
        "code": """model_map = {

    "amazon.titan-text-express-v1": "Amazon",
    "amazon.titan-text-lite-v1": "Amazon",
    "amazon.titan-text-premier-v1:0": "Amazon",
    "anthropic.claude-v2": "Anthropic",
    "anthropic.claude-v2:1": "Anthropic",
    "anthropic.claude-3-sonnet-20240229-v1:0": "Anthropic",
    "anthropic.claude-3-haiku-20240307-v1:0": "Anthropic",
    "anthropic.claude-3-opus-20240229-v1:0": "Anthropic",
    "anthropic.claude-instant-v1": "Anthropic",
    "cohere.command-text-v14": "Cohere",
    "cohere.command-light-text-v14": "Cohere",
    "cohere.command-r-v1:0": "Cohere",
    "cohere.command-r-plus-v1:0": "Cohere",
    "meta.llama2-13b-chat-v1": "Meta",
    "meta.llama2-70b-chat-v1": "Meta",
    "meta.llama3-8b-instruct-v1:0": "Meta",
    "meta.llama3-70b-instruct-v1:0": "Meta",
    "mistral.mistral-7b-instruct-v0:2": "Mistral AI",
    "mistral.mixtral-8x7b-instruct-v0:1": "Mistral AI",
    "mistral.mistral-large-2402-v1:0": "Mistral AI",
    "mistral.mistral-small-2402-v1:0": "Mistral AI",

}""",
        "file_name": "model_map.py",
    },
    {
        "code": """import logging
from lib import yaml
from bedrock_util.TextCompletionUtil import generate_text_completion
from bedrock_util.model_map import model_map

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_prompt_config(file_path):
    try:
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        logger.error(f"The file {file_path} does not exist.")
    except Exception as e:
        logger.exception(f"Error decoding YAML in file {file_path}: {e}")
    return None

def validate_model(service_id, model):
    if service_map.get("PromptServices", {}).get(service_id):
        service = service_map["PromptServices"][service_id]
        allowed_providers = service.get("allowedFoundationModelProviders")
        if allowed_providers and model_map.get(model) in allowed_providers:
            return True
    logger.warning(f"Model ID {model} not allowed for service {service_id}")
    return False

def validate_prompt_inputs(service_id, prompt_inputs):
    if service_map.get("PromptServices", {}).get(service_id):
        service = service_map["PromptServices"][service_id]
        input_variables = service.get("inputVariables")
        if (not input_variables and not prompt_inputs) or (
            input_variables and prompt_inputs and sorted(input_variables) == sorted(prompt_inputs.keys())
        ):
            return True
    logger.warning(f"Invalid inputs provided for service ID {service_id}")
    return False

def run_service(service_id, model_id, prompt_input_variables=None, **model_kwargs):
    if validate_model(service_id, model_id) and validate_prompt_inputs(service_id, prompt_input_variables):
        prompt = service_map["PromptServices"][service_id]["prompt"]
        formatted_prompt = prompt.format(**(prompt_input_variables or {}))
        return generate_text_completion(model_id, formatted_prompt, **model_kwargs)

service_map = read_prompt_config("prompt_store.yaml")""",
        "file_name": "prompt_service.py",
    },
    {
        "code": """##############################################################################################
#   Create YAML file content for prompt service flow. Example:                               #
#                                                                                            #
#  PromptServices:                                                                           #
#                                                                                            #
#    getMathDetails:                                                                         #
#      prompt: |                                                                             #
#        You are an expert math teacher. Based on user input below provide assistance.       #
#                                                                                            #
#        input: {input}                                                                      #
#      inputVariables:                                                                       #
#        - input                                                                             #
#      allowedFoundationModelProviders:                                                      #
#        - Amazon                                                                            #
#        - Meta                                                                              #
#        - Anthropic                                                                         #
#        - Mistral AI                                                                        #
#        - Cohere                                                                            #
##############################################################################################""",
        "file_name": "prompt_store.yaml",
    },
]