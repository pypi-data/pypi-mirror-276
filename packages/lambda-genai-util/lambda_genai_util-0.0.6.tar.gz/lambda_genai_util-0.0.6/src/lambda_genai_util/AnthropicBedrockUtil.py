import json
import logging
from lambda_util.lambda_genai_util.BedrockUtil import BedrockUtil

logger = logging.getLogger(__name__)

class AnthropicBedrockUtil(BedrockUtil):

    def text_completion(self, bedrock_client, model, prompt, guardrail_identifier=None, guardrail_version=None,  **model_kwargs):
        prompt_request = {}
        prompt_response = {}

        if prompt:
            try:
                prompt_request['anthropic_version'] = 'bedrock-2023-05-31'
                prompt_request["messages"] = [{"role": "user", "content": prompt}]
                prompt_request.update(model_kwargs)
                prompt_request.setdefault("max_tokens", 4000)

                body = json.dumps(prompt_request)
                accept = "application/json"
                content_type = "application/json"

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

                prompt_response['output'] = response_body['content'][0]['text']

            except (KeyError, IndexError) as e:
                logger.error(f"Error occurred while processing response: {e}")
                prompt_response['output'] = None

            except Exception as e:
                logger.exception(f"Error in text_completion for model {model}: {str(e)}")
                raise

        return prompt_response