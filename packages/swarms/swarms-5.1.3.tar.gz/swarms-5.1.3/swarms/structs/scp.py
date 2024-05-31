"""
Swarm Communication Protocol
- RAG as a communication protocol
- Each Agent is connected to a database so they can see each others 
memories, actions, and experiences

"""

from swarms.structs.omni_agent_types import AgentType
from swarms.structs.base_structure import BaseStructure
from typing import List
from swarms.memory.base_vectordb import BaseVectorDatabase


class SCP(BaseStructure):
    def __init__(
        self,
        agents: List[AgentType],
        memory_system: BaseVectorDatabase = None,
        *args,
        **kwargs,
    ):
        super().__init__()
        self.agents = agents
        self.memory_system = memory_system
