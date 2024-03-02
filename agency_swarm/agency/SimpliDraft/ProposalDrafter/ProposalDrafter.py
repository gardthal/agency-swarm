from agency_swarm.agents import Agent
from agency_swarm.tools import CodeInterpreter

class ProposalDrafter(Agent):
    def __init__(self):
        super().__init__(
            name="ProposalDrafter",
            description="The Proposal Drafter is responsible for drafting proposals based on the guidelines and user input provided via the CEO. Their main tasks include structuring the proposal to ensure it meets specific criteria and preparing the proposal for review by the Reviewer agent.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[CodeInterpreter],
            tools_folder="./tools"
        )
