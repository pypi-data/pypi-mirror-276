"""
Class Name: KnowledgeManagementCompletionRequest
Description: Encapsulates the metadata required to complete a knowledge management orchestration request.
"""
from typing import Optional
from .knowledge_management_agent import KnowledgeManagementAgent
from foundationallm.models.orchestration import CompletionRequestBase

class KnowledgeManagementCompletionRequest(CompletionRequestBase):
    """
    Orchestration completion request.
    """    
    agent: Optional[KnowledgeManagementAgent] = None
