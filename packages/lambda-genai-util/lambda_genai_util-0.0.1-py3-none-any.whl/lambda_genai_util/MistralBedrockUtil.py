import json
import logging

from BedrockUtil import BedrockUtil

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
