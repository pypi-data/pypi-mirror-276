import logging
from lambda_util import boto3
from MetaBedrockUtil import MetaBedrockUtil
from MistralBedrockUtil import MistralBedrockUtil
from AwsTitanBedrockUtil import AwsTitanBedrockUtil
from AnthropicBedrockUtil import AnthropicBedrockUtil
from CohereBedrockUtil import CohereBedrockUtil
from model_map import model_map

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

    return None