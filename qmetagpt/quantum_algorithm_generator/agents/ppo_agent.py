import torch
from stable_baselines3 import PPO
from .base_rl_agent import BaseRLAgent
from ..circuit_environment import QuantumCircuitEnv
from ...utils.logger import get_logger

logger = get_logger(__name__)

class PPOAgent(BaseRLAgent):
    def __init__(self, state_dim, action_dim, policy='MlpPolicy', **kwargs):
        super().__init__(state_dim, action_dim)
        self.policy = policy
        self.model_kwargs = kwargs
        self.model = None
        
    def build_model(self, policy_kwargs=None):
        logger.info(f"Building PPO model with policy: {self.policy}")
        self.model = PPO(
            self.policy,
            self._make_env(),
            policy_kwargs=policy_kwargs,
            **self.model_kwargs
        )
    
    def generate_circuit(self, state):
        action, _ = self.model.predict(state)
        return self._action_to_circuit(action)
    
    def train(self, env, total_timesteps=10000):
        logger.info(f"Training PPO agent for {total_timesteps} timesteps")
        self.model.set_env(env)
        self.model.learn(total_timesteps=total_timesteps)
    
    def save(self, path):
        self.model.save(path)
        logger.info(f"Saved PPO model to {path}")
    
    def load(self, path):
        self.model = PPO.load(path)
        logger.info(f"Loaded PPO model from {path}")
    
    def _make_env(self):
        return QuantumCircuitEnv(None, 2)