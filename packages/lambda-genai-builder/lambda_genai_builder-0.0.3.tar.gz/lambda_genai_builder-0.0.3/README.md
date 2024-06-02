# lambda-genai-builder: A Python Package for Streamlined Development of Generative AI Applications on AWS Lambda

## Overview

The lambda-genai-builder is a Python package designed to facilitate the development and deployment of generative AI applications on AWS Lambda. This package creates a well-framed, lightweight structure that encapsulates generative AI operations, providing a structured and efficient approach to building and managing generative AI models. It offers a set of utilities, services, and a predefined project structure to streamline the development process and enhance productivity.

The main aim of the lambda-genai-builder package is to enhance generative AI development in AWS using Lambda functions. It simplifies the process of integrating generative AI capabilities into Lambda functions, making it easier for developers to build and deploy AI-powered applications.

## Installation and Implementation

### Project Structure Generation

The lambda-genai-builder package includes a powerful feature for generating an optimized project structure tailored for AWS Lambda. This generated structure adheres to best practices and provides a solid foundation for developing generative AI applications.

To generate the project structure, follow these steps:

1. Install the `lambda-genai-builder` package using the following command:
   ```
   pip install lambda-genai-builder
   ```

2. Navigate to your desired project folder (root folder) and execute the following command:
   ```
   lambda-genai-proj-build .
   ```

   This command will create the following files and folders under the root folder:
   - `lambda_util/`: A directory containing all the dependencies and utilities for prompt service and generative AI API operations.
   - `lambda_function.py`: The main entry point for your Lambda function.
   - `prompt_store.yaml`: A configuration file for storing prompt templates and service flows.
   - Additional folders related to boto3 and other Lambda dependencies to ensure smooth functioning of the Lambda function.

   The generated project structure provides a well-organized and modular architecture, enabling developers to focus on implementing the core functionality of their generative AI applications.

### Prompt Service Framework

The lambda-genai-builder package includes a robust prompt service framework that allows developers to define and execute predefined prompt flows for generating text completions. This framework provides a structured approach to configuring and managing prompt templates, input variables, and allowed foundation model providers.

The `prompt_store.yaml` file serves as a blueprint for defining prompt service flows. Here's the structure of the `prompt_store.yaml` file:

```yaml
PromptServices:
  <serviceID>:
    prompt: |
      <prompt>
    inputVariables:
      - <prompt input variables>
    guardrailIdentifier: <guardrail id - string data type> -- optional
    guardrailVersion: <guardrail version - string data type> -- optional but required if guardrailIdentifier is mentioned
    allowedFoundationModelProviders:
      - Amazon
      - Meta
      - Anthropic
      - Mistral AI
      - Cohere
```

Required fields are `serviceID`, `prompt`, and `inputVariables` if the prompt has input variables. The `allowedFoundationModelProviders` field can only have values from the specified list.

To utilize the prompt service framework, follow these steps:

1. Import the `run_service` function from the `lambda_util.lambda_genai_util.prompt_service` module:
   ```python
   from lambda_util.lambda_genai_util.prompt_service import run_service
   ```

2. Configure the prompt flows in the `prompt_store.yaml` file. Each prompt flow is defined under the `PromptServices` key and includes the following properties:
   - `prompt`: The prompt template for the service. Input variables can be specified using curly braces (e.g., `{input}`).
   - `inputVariables`: A list of input variable names required by the prompt.
   - `guardrailIdentifier` (optional): The guardrail identifier (string data type) created in AWS Bedrock to filter and secure prompt input and model responses.
   - `guardrailVersion` (optional but required if `guardrailIdentifier` is mentioned): The version of the guardrail (string data type).
   - `allowedFoundationModelProviders`: A list of allowed foundation model providers for the service. Allowed values are "Amazon", "Meta", "Anthropic", "Mistral AI", and "Cohere".

   Example configuration in `prompt_store.yaml`:
   ```yaml
   PromptServices:
     getMathDetails:
       prompt: |
         You are an expert math teacher. Based on user input below provide assistance.

         input: {input}
       inputVariables:
         - input
       guardrailIdentifier: "abcdefg"
       guardrailVersion: "1"
       allowedFoundationModelProviders:
         - Amazon
         - Meta
         - Anthropic
         - Mistral AI
         - Cohere
   ```

3. To execute a prompt service flow, utilize the `run_service` function:
   ```python
   service_id = "getMathDetails"
   model_id = "amazon.titan-text-premier-v1:0"
   prompt_input_variables = {
       "input": "What is the formula for calculating the area of a circle?"
   }

   result = run_service(service_id, model_id, prompt_input_variables)
   print(result)
   ```

   The `run_service` function has the following signature:
   ```python
   def run_service(service_id, model_id, prompt_input_variables=None, **model_kwargs):
       # ...
   ```

   - `service_id`: The ID of the prompt service flow to run.
   - `model_id`: The ID of the foundation model to use for text completion generation.
   - `prompt_input_variables`: A dictionary containing the input variables required by the prompt template.
   - `**model_kwargs`: Additional keyword arguments specific to the foundation model provider.

   The `run_service` function performs validation of the model and prompt inputs based on the configuration defined in the `prompt_store.yaml` file. It automatically selects the appropriate prompt template, formats it with the provided input variables, and generates the text completion using the specified model.

   The prompt service framework abstracts the complexities of managing prompt flows, allowing developers to concentrate on defining the prompts and input variables while the framework handles the underlying implementation details.

### Direct Model Invocation Utility

In addition to the prompt service framework, the lambda-genai-builder package provides a utility function for directly invoking foundation models and generating text completions based on a provided prompt.

To utilize the direct model invocation utility, follow these steps:

1. Import the `generate_text_completion` function from the `lambda_util.lambda_genai_util.TextCompletionUtil` module:
   ```python
   from lambda_util.lambda_genai_util.TextCompletionUtil import generate_text_completion
   ```

2. Invoke the `generate_text_completion` function with the desired model, prompt, and optional guardrail parameters:
   ```python
   model_id = "amazon.titan-text-premier-v1:0"
   prompt = "What is the capital of France?"
   guardrail_identifier = "mbmyptuqibd9"
   guardrail_version = "3"

   result = generate_text_completion(model_id, prompt, guardrail_identifier, guardrail_version)
   print(result)
   ```

   The `generate_text_completion` function has the following signature:
   ```python
   def generate_text_completion(model: str, prompt, guardrail_identifier=None, guardrail_version=None, **model_kwargs):
       # ...
   ```

   - `model`: The ID of the foundation model to use for text completion generation.
   - `prompt`: The input prompt for generating the text completion.
   - `guardrail_identifier` (optional): The guardrail identifier (string data type) created in AWS Bedrock to filter and secure prompt input and model responses.
   - `guardrail_version` (optional): The version of the guardrail (string data type).
   - `**model_kwargs`: Additional keyword arguments specific to the foundation model provider.

   The `generate_text_completion` function encapsulates the complexity of interacting with different foundation model providers and offers a unified interface for generating text completions. It automatically selects the appropriate utility class based on the specified model and invokes the corresponding `text_completion` method.

   This utility function enables developers to quickly generate text completions without the need for configuring prompt flows or managing additional dependencies, providing a streamlined approach for direct model invocation.

## Conclusion

The lambda-genai-builder Python package offers a comprehensive solution for developing and deploying generative AI applications on AWS Lambda. It creates a well-framed, lightweight structure that encapsulates generative AI operations, providing a set of tools and utilities to streamline the development process and enhance developer productivity.

The project structure generation feature simplifies the setup process by creating a well-organized and modular directory structure, ensuring best practices and facilitating maintainable code.

The prompt service framework enables developers to define and execute predefined prompt flows, providing a structured approach to generating text completions based on configurable prompts and input variables. The `run_service` function allows developers to easily execute prompt service flows with customizable input variables and model-specific parameters.

The direct model invocation utility, accessible through the `generate_text_completion` function, allows for quick and efficient generation of text completions without the need for additional configuration. It provides a straightforward way to invoke foundation models directly with a provided prompt, guardrail parameters, and model-specific parameters.

By leveraging the lambda-genai-builder package, developers can focus on defining prompts, input variables, and selecting the appropriate foundation models, while the package handles the underlying implementation details. This abstraction layer simplifies the development process and enables developers to build generative AI applications more effectively on AWS Lambda.

Whether you're building chatbots, content generation systems, or any other application that requires natural language processing, the lambda-genai-builder Python package provides a robust foundation and a set of tools to streamline the development process and accelerate the deployment of generative AI models on AWS Lambda, ultimately enhancing the integration of generative AI capabilities into Lambda functions.