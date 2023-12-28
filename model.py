import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import gymnasium as gym

class Model(nn.Module):
    def __init__(self, in_dim, out_dim):
        super(Model, self).__init__()

        self.in_dim = in_dim
        self.out_dim = out_dim

        self.layer1 = nn.Linear(in_dim, 128, dtype=torch.float32)
        self.layer2 = nn.Linear(128, out_dim, dtype=torch.float32)

        self.relu = nn.ReLU()
        self.softmax = nn.Softmax(dim = 1)

        self.optimizer = optim.Adam(self.parameters(), lr=0.001)

    def forward(self, x):
        x = self.relu(self.layer1(x))
        x = self.softmax(self.layer2(x))

        return x

        # x = F.relu(self.layer1(x))
        # x = self.layer2(x)
        # return F.softmax(x, dim=1)
    
    def act(self, state):
        # logits = self.forward(state.unsqueeze(0))
        # policy_distribution = torch.distributions.Categorical(logits=logits)
        # action = logits.argmax()
        # return action.item(), policy_distribution.log_prob(action)

        probs = self.forward(state.unsqueeze(0))
        m = torch.distributions.Categorical(probs)
        action = m.sample()
        return action.item(), m.log_prob(action)

def test_model():
    model = Model(4, 2)
    # test_tensor = torch.tensor([2, 2, 3, 4], dtype = torch.float32)
    # print(model.forward(test_tensor))
    env = gym.make("CartPole-v1", render_mode="rgb_array")
    obs, info = env.reset()
    test_tensor = obs
    print(model.act(torch.Tensor([obs])))
    print(torch.Tensor([obs]).shape)
    print(torch.Tensor(obs).unsqueeze(0).shape)

if __name__ == "__main__":

    test_model()