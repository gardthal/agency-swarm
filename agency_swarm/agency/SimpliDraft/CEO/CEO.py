from agency_swarm.agents import Agent
from agency_swarm.tools import CodeInterpreter

class CEO(Agent):
    def __init__(self):
        super().__init__(
            name="CEO",
            description="The CEO (Chief Execution Officer) serves as the primary communicator with the user, collects input for drafting proposals, and conveys final approval after review. This agent should be able to initiate communication with the Proposal Drafter and receive final reviews from the Reviewer.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[CodeInterpreter],
            tools_folder="./tools"
        )
