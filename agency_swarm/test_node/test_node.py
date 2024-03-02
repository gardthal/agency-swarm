from agency_swarm.agency.SimpliDraft import SimpliDraft
from agency_swarm.nodes import AgencyNode

class TestNode(AgencyNode):
    def __init__(self, **kwargs):
        
        if 'agency' not in kwargs:
            kwargs['agency'] = SimpliDraft()

        super().__init__(**kwargs)