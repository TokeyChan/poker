import gymnasium
from gymnasium import spaces
import game as poker

class PokerEnv(gymnasium.Env):
    metadata = {
        "render_modes": ["human"]
    }
    def __init__(self):
        self.game = poker.Game()
        
        self.observation_space = spaces.Dict({
            
        })
    
        self.action_space = spaces.Discrete(6)

    def step(self, action):
        pass