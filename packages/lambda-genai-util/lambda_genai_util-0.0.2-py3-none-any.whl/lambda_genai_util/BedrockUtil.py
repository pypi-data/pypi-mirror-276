from abc import ABC, abstractmethod


class BedrockUtil(ABC):

    @abstractmethod
    def text_completion(self, bedrock_client, model, prompt, **model_kwargs):
        pass
