from abc import ABC, abstractmethod


class BedrockUtil(ABC):

    @abstractmethod
    def text_completion(self, bedrock_client, model, prompt, guardrail_identifier=None, guardrail_version=None, **model_kwargs):
        pass
