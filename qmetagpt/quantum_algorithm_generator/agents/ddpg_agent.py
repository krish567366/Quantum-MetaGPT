from stable_baselines3 import DDPG
from .base_rl_agent import BaseRLAgent
from qmetagpt.utils.logger import get_logger

logger = get_logger(__name__)

class DDPGAgent(BaseRLAgent):
    def __init__(self, state_dim, action_dim, policy='MlpPolicy', **kwargs):
        super().__init__(state_dim, action_dim)
        self.policy = policy
        self.model_kwargs = kwargs
        self.model = None
        
    def build_model(self, policy_kwargs=None):
        logger.info(f"Building DDPG model with policy: {self.policy}")
        self.model = DDPG(
            self.policy,
            self._make_env(),
            policy_kwargs=policy_kwargs,
            **self.model_kwargs
        )
    
    def generate_circuit(self, state):
        action, _ = self.model.predict(state)
        return self._action_to_circuit(action)
    
    def train(self, env, total_timesteps=10000):
        logger.info(f"Training DDPG agent for {total_timesteps} timesteps")
        self.model.set_env(env)
        self.model.learn(total_timesteps=total_timesteps)
    
    def save(self, path):
        self.model.save(path)
        logger.info(f"Saved DDPG model to {path}")
    
    def load(self, path):
        self.model = DDPG.load(path)
        logger.info(f"Loaded DDPG model from {path}")
    
    def _make_env(self):
        from ..circuit_environment import QuantumCircuitEnv
        return QuantumCircuitEnv(None, 2)