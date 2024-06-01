import json
import logging

from BedrockUtil import BedrockUtil

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
