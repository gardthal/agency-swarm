import os
from typing import List

from pydantic import Field, model_validator, field_validator

from agency_swarm import BaseTool, get_openai_client
from agency_swarm.util import create_agent_template


class FinalizeAgency(BaseTool):
    """
    This tool finalizes the agency structure and it's imports. Please make sure to use at only at the very end, after all agents have been created.
    """

    def run(self):
        os.chdir(self.shared_state.get("agency_path"))

        client = get_openai_client()

        # read agency.py
        with open("./agency.py", "r") as f:
            agency_py = f.read()
            f.close()

        res = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=examples + [
                {'role': "user", 'content': agency_py},
            ],
            temperature=0.0,
        )

        message = res.choices[0].message.content

        # write agency.py
        with open("./agency.py", "w") as f:
            f.write(message)
            f.close()

        return "Successfully finalized agency structure. You can now instruct the user to run the agency.py file."

    @model_validator(mode="after")
    def validate_agency_path(self):
        if not self.shared_state.get("agency_path"):
            raise ValueError("Agency path not found. Please use CreateAgencyFolder tool to create the agency folder first.")


SYSTEM_PROMPT = """"Please read the file provided by the user and fix all the imports and indentation accordingly. 

Only output the full valid python code and nothing else."""

example_input = """
from agency_swarm import Agency

from BasicInformationCurator import BasicInformationCurator
from BasicTaskExecutor import BasicTaskExecutor
from BasicCEO import BasicCEO

class BasicAgency(Agency):
    def __init__(self, **kwargs):
    
        if 'agency_chart' not in kwargs:
            kwargs['agency_chart'] = [
                ceo,
                [ceo, taskExecutor],
                [ceo, infoCurator],
            ]
        if 'shared_instructions' not in kwargs:
            kwargs['shared_instructions'] = "./manifesto.md"

        super().__init__(**kwargs)

if __name__ == '__main__':
    agency = BasicAgency()
    agency.demo_gradio()
"""

example_output = """
from agency_swarm import Agency
from BasicInformationCurator import BasicInformationCurator
from BasicTaskExecutor import BasicTaskExecutor
from BasicCEO import BasicCEO

class BasicAgency(Agency):
    def __init__(self, **kwargs):

        if 'agency_chart' not in kwargs:
            ceo = BasicCEO()
            taskExecutor = BasicTaskExecutor()
            infoCurator = BasicInformationCurator()
            
            kwargs['agency_chart'] = [
                ceo,
                [ceo, taskExecutor],
                [ceo, infoCurator],
            ]
        if 'shared_instructions' not in kwargs:
            kwargs['shared_instructions'] = "./manifesto.md"

        super().__init__(**kwargs)

if __name__ == '__main__':
    agency = BasicAgency()
    agency.demo_gradio()"""

examples = [
    {'role': "system", 'content': SYSTEM_PROMPT},
    {'role': "user", 'content': example_input},
    {'role': "assistant", 'content': example_output}
]
