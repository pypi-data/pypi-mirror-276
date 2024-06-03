# -*- coding: utf-8 -*-

r"""This module contains the model class. 

:Authors:   Kevin Michalewicz <k.michalewicz22@imperial.ac.uk>

"""

import torch
from torch.nn import Linear, ReLU, Conv2d, MaxPool2d, Module, Dropout

class NormalModeAnalysisCNN(Module):
    r"""Predicting the binding affinity of an antibody from its normal mode correlation map.

    Parameters
    ----------
    n_filters: int
        Number of filters in the convolutional layer.
    filter_size: int
        Size of filters in the convolutional layer.
    pooling_size: int
        Size of the max pooling operation.
    input_shape: int
        Shape of the normal mode correlation maps.

    """
    def __init__(
            self,
            n_filters=2,
            filter_size=5,
            pooling_size=1,
            input_shape=215,
    ):
        super(NormalModeAnalysisCNN, self).__init__()
        self.n_filters = n_filters
        self.filter_size = filter_size
        self.pooling_size = pooling_size
        self.input_shape = input_shape
        self.fully_connected_input = n_filters * ((input_shape-filter_size+1)//pooling_size) ** 2
        self.conv1 = Conv2d(1, n_filters, filter_size)
        self.pool = MaxPool2d(pooling_size, pooling_size)
        self.dropit = Dropout(p=0.05)
        self.relu = ReLU()
        self.fc1 = Linear(self.fully_connected_input, 1, bias=False)

    def forward(self, x):
        r"""Model's forward pass.

        Returns
        -------
        output: torch.Tensor
            Predicted binding affinity.
        inter_filter: torch.Tensor
            Filters before the fully-connected layer.
            
        """
        x = self.conv1(x) + torch.transpose(self.conv1(x), 2, 3)
        x = self.relu(x)
        x = self.pool(x)
        inter = x = self.relu(x)
        x = x.view(x.size(0), -1)
        x = self.dropit(x)
        x = self.fc1(x)

        return x.float(), inter
