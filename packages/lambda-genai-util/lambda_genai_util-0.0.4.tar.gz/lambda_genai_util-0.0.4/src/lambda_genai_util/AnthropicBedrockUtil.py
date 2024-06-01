import json
import logging
from lambda_util.lambda_genai_util.BedrockUtil import BedrockUtil

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
