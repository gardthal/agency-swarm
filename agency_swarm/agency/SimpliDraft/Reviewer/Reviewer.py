from agency_swarm.agents import Agent
from agency_swarm.tools import CodeInterpreter

class Reviewer(Agent):
    def __init__(self):
        super().__init__(
            name="Reviewer",
            description="The Reviewer is responsible for reviewing the drafts from the Proposal Drafter, ensuring the quality and completeness of the proposal before final approval. They scrutinize the content, suggest improvements, and finalize the document for submission.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[CodeInterpreter],
            tools_folder="./tools"
        )
