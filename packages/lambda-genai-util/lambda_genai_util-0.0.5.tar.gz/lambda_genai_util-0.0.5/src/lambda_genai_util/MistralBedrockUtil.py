import json
import logging

from lambda_util.lambda_genai_util.BedrockUtil import BedrockUtil

logger = logging.getLogger(__name__)

class MistralBedrockUtil(BedrockUtil):

    def text_completion(self, bedrock_client, model, prompt,guardrail_identifier=None, guardrail_version=None, **model_kwargs):
        prompt_request = {}
        prompt_response = {}

        if prompt:
            prompt_request["prompt"] = prompt
            prompt_request.update(model_kwargs)

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

                response_body = json.loads(response["body"].read())
                prompt_response['output'] = response_body['outputs'][0]['text']
            except (KeyError, IndexError) as e:
                logger.error(f"Error extracting output from response: {e}")
                raise
            except Exception as e:
                logger.exception(f"Error in text_completion for model {model}: {str(e)}")
                raise

        return prompt_response
