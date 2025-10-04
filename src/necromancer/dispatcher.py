# dispatcher.py

from necromancer.prompt import Prompt

import os
from openai import OpenAI

import openai

print("openai lib version:", openai.__version__)


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


class Dispatcher:
    def __init__(self, role: str, job: str, annotation: str, preamble: str):
        self.role = role
        self.job = job
        self.annotation = annotation
        self.preamble = preamble

        self.prompt = Prompt(role, job, annotation, preamble)
        self.prompt.build()

        self.schema = {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The complete, raw code solution.",
                }
            },
            "required": ["code"],
            "additionalProperties": False,
        }

        self.response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "CodeBlock",
                "schema": self.schema,
            },
            # "strict": true enforces token-by-token validation against the schema
            "strict": True,
        }

    def dispatch(self) -> None:
        response = client.responses.create(
            model="gpt-5",
            instructions=self.prompt.system_prompt,
            input=self.prompt.user_prompt,
            response_format=self.response_format,
        )
        parsed = getattr(response, "output_parsed", None)
        if parsed is None:
            # fallback: try to parse the raw text output
            as_text = response.output_text
            parsed = json.loads(as_text)

        code = parsed["code"]
        print(code)
