from foundationallm.config import Configuration, Context
from foundationallm.langchain.agents import AgentFactory, LangChainAgentBase
from foundationallm.models.orchestration import (
    CompletionRequestBase,
    CompletionResponse
)

class OrchestrationManager:
    """Client that acts as the entry point for interacting with the FoundationaLLM Python SDK."""

    def __init__(self,
                 completion_request: CompletionRequestBase,
                 configuration: Configuration,
                 context: Context):
        """
        Initializes an instance of the OrchestrationManager.
        
        Parameters
        ----------
        completion_request : CompletionRequest
            The CompletionRequest is the metadata object containing the details needed for
            the OrchestrationManager to assemble an agent with a language model and data source.
        context : Context
            The user context under which to execution completion requests.
        """
        self.agent = self.__create_agent(
            completion_request = completion_request,
            config = configuration,
            context = context
        )

    def __create_agent(
            self,
            config: Configuration,
            completion_request: CompletionRequestBase,
            context: Context) -> LangChainAgentBase:
        """Creates an agent for executing completion requests."""
        agent_factory = AgentFactory(
            completion_request=completion_request,
            config=config,
            context=context
        )
        return agent_factory.get_agent()

    def invoke(self, request: CompletionRequestBase) -> CompletionResponse:
        """
        Executes a completion request against the LanguageModel using 
        the LangChain agent assembled by the OrchestrationManager.
        
        Parameters
        ----------
        prompt : str
            The prompt for which a completion is being generated.
            
        Returns
        -------
        CompletionResponse
            Object containing the completion response and token usage details.
        """
        return self.agent.invoke(request)
