class Agent:
    def __init__(self, model: str, temperature: float = 0.5, role: str = None):
        self.model = model
        self.temperature = temperature
        self.role = role
