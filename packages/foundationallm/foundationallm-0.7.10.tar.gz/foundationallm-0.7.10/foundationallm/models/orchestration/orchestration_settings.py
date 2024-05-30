from typing import Optional
from pydantic import BaseModel

class OrchestrationSettings(BaseModel):
    """
        Represents settings for the orchestration.
        
        Parameters
        ----------
        agent_parameters : dict
            Parameters to set or override the behavior of the agent.
        endpoint_configuration : dict
            Parameters to set or override the endpoint configuration used by the orchestrator
            to access a language model.
        model_parameters : dict
            Parameters to set or override the behavior of the language model as defined on the agent.
        orchestrator : str
            The orchestrator to use for the orchestration. Defaults to 'LangChain'.
    """
    agent_parameters: Optional[dict] = None
    endpoint_configuration: Optional[dict] = None
    model_parameters: Optional[dict] = None
    orchestrator: Optional[str] = 'LangChain'
