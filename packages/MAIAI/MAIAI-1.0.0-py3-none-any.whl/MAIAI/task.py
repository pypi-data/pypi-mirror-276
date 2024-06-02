from MAIAI import Agent
from openai import OpenAI

client = OpenAI()

class Task:
    def __init__(self, agent: Agent, goal: str, expected_output: str):
        self.agent = agent
        self.goal = goal
        self.expected_output = expected_output
    
    def execute(self):
        completion = client.chat.completions.create(
            model=self.agent.model,
            temperature=self.agent.temperature,
            messages=[
                {"role": "system", "content": f"{self.agent.role}"}, 
                {"role": "user", "content": f"""You MUST give your response as {self.expected_output}. 
                 {self.goal}"""}
            ]
        )

        try:
            output = completion.choices[0].message.content
        except Exception as e:
            output = None

        return output