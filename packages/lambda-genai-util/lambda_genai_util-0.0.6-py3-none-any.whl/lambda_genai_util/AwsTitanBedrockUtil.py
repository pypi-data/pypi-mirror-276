import json
import logging

from lambda_util.lambda_genai_util.BedrockUtil import BedrockUtil

logger = logging.getLogger(__name__)


class AwsTitanBedrockUtil(BedrockUtil):

    def text_completion(self, bedrock_client, model, prompt, guardrail_identifier=None, guardrail_version=None,**model_kwargs):
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

                if guardrail_identifier is None and guardrail_version is None:
                    response = bedrock_client.invoke_model(
                        body=body, modelId=model, accept=accept, contentType=content_type
                    )
                else:
                    response = bedrock_client.invoke_model(
                        body=body, modelId=model, accept=accept, contentType=content_type,
                        guardrailIdentifier=guardrail_identifier, guardrailVersion=guardrail_version
                    )
                response_body = json.loads(response.get("body").read())
                prompt_response['output'] = response_body['results'][0]['outputText']
            except Exception as e:
                logger.exception(f"Error in text_completion for model {model}: {str(e)}")
                raise

        return prompt_response