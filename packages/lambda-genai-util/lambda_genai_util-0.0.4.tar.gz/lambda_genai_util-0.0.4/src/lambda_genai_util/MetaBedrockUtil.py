import json
import logging

from lambda_util.lambda_genai_util.BedrockUtil import BedrockUtil

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
