import numpy as np
from typing import List
import torch
from torch import nn

class MLP(nn.Module):
    def __init__(self, in_features, out_features):
        super().__init__()
        self.Linear= nn.Sequential(
            nn.Linear(in_features=in_features, out_features=10),
            nn.ReLU(),
            nn.Linear(in_features=10, out_features=out_features)
        )

    def forward(self, data):
        return self.Linear(data)

class MLPTrainer:
    def __init__(self, model, num_epoch, verbose):
        self.model= model
        self.num_epoch= num_epoch
        self.verbose= verbose

    def train(self, X_train, y_train, X_test=None, y_test=None):
        self.optim= torch.optim.SGD(params=self.model.parameters(), lr=1e-3)
        self.loss_fn= nn.L1Loss()

        X_train= torch.tensor(X_train, dtype=torch.float32)
        y_train= torch.tensor(y_train, dtype=torch.float32)

        for epoch in range(self.num_epoch):
            train_loss= self.train_loop(X_train, y_train)

            test_loss="NaN"
            if(X_test is not None and y_test is not None):
                test_loss= self.test_loop(X_test, y_test)

            if(self.verbose):
                print(f"Epoch: {epoch}, Train_Loss: {train_loss}, Test Loss: {test_loss}")

    def train_loop(self, X_train, y_train):
        self.model.train()
        self.optim.zero_grad()
        y_pred= self.model(X_train)
        loss= self.loss_fn(y_pred, y_train)
        loss.backward()
        self.optim.step()
        return loss

    def test_loop(self, X_test, y_test):
        with torch.no_grad():
            self.model.eval()
            y_pred= self.model(X_test)
            loss= self.loss_fn(y_pred, y_test)
            return loss