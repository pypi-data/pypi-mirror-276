import json
import logging
from lambda_util.lambda_genai_util.BedrockUtil import BedrockUtil

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
