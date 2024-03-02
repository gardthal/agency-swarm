from agency_swarm import Agency
from .Reviewer import Reviewer
from .ProposalDrafter import ProposalDrafter
from .CEO import CEO

class SimpliDraft(Agency):
    def __init__(self, **kwargs):

        if 'agency_chart' not in kwargs:
            ceo = CEO()
            proposal_drafter = ProposalDrafter()
            reviewer = Reviewer()
            
            kwargs['agency_chart'] = [
                ceo,
                [ceo, proposal_drafter],
                [proposal_drafter, reviewer],
                [reviewer, ceo]
            ]
        if 'shared_instructions' not in kwargs:
            kwargs['shared_instructions'] = './agency_manifesto.md'

        super().__init__(**kwargs)

if __name__ == '__main__':
    agency = SimpliDraft()
    agency.demo_gradio()