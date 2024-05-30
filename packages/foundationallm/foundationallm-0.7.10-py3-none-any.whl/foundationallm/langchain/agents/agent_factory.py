from foundationallm.config import Configuration, Context
from foundationallm.models.orchestration import CompletionRequestBase
from foundationallm.langchain.agents import (
    LangChainAgentBase,
    LangChainKnowledgeManagementAgent
)

class AgentFactory:
    """
    Factory to determine which agent to use.
    """

    def __init__(
            self,
            completion_request: CompletionRequestBase,
            config: Configuration,
            context: Context
        ):
        """
        Initializes an Orchestration for selecting which agent to use for completion.

        Parameters
        ----------
        completion_request : CompletionRequest
            The completion request object containing the user prompt to execute, message history,
            and agent and data source metadata.
        config : Configuration
            Application configuration class for retrieving configuration settings.
        context : Context
            The user context under which to execution completion requests.    
        """
        self.completion_request = completion_request
        self.config = config
        self.context = context

    def get_agent(self) -> LangChainAgentBase:
        """
        Retrieves an agent of the the requested type.
        
        Returns
        -------
        AgentBase
            Returns an agent of the requested type.
        """
        agent = self.completion_request.agent
        if agent is None:
            raise ValueError("Agent not constructed. Cannot access an object of 'NoneType'.")
        
        match agent.type:
            case 'knowledge-management' | 'internal-context':
                return LangChainKnowledgeManagementAgent(config=self.config)
            case _:
                raise ValueError(f'The specified agent type {agent.type} is not supported.')
