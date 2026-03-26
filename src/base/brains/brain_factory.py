from src.common.config import Config
from src.base.components import LLMInterface, ToolProvider
from .base import BaseBrain
from .variants.llm_brain import LLMBrain

def create_brain(config: Config, llm_client: LLMInterface, tool_provider: ToolProvider) -> BaseBrain:
    return LLMBrain(config, llm_client)
