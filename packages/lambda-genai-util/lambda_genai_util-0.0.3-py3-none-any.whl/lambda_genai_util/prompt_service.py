import logging
from lambda_util import yaml
from lambda_genai_util.TextCompletionUtil import generate_text_completion
from lambda_genai_util.model_map import model_map


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

service_map = read_prompt_config("prompt_store.yaml")