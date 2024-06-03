"""
    A collection of models related to embeddings.
"""

import numpy as np
from typing import List
from ..utils.log import logger

class SkipGram:
    """
        Default skipgram model as it was in word2vec.
    """

    def __init__(self, vocab_size: int, dim: int):
        self.vocab_size = vocab_size
        self.dim = dim
        self.core = np.random.normal(0, 1, (2*vocab_size, dim,))
        # The bottom half of the matrix is "context" vectors

    def __getitem__(self, item: int):
        return self.core[item]

    def step_positive(self, input: int, context: int, lr: np.float32):
        new_input = self.core[input] + lr * self.core[self.vocab_size + context]
        new_context = self.core[self.vocab_size + context] + lr * self.core[input]
        self.core[input] = new_input
        self.core[self.vocab_size + context] = new_context

    def step_negative(self, input: int, negative: int, lr: np.float32):
        new_input = self.core[input] - lr * self.core[self.vocab_size + negative]
        new_negative = self.core[self.vocab_size - negative] + lr * self.core[input]
        self.core[input] = new_input
        self.core[self.vocab_size + negative] = new_negative

    def loss(self, inputs, contexts, negatives):
        e: np.float32 = 0
        for i, input in enumerate(inputs):
            for context in contexts[i]:
                e -= np.dot(self.core[input], self.core[self.vocab_size + context])
            for negative in negatives[i]:
                e += np.dot(self.core[input], self.core[self.vocab_size + negative])
        return e / (np.size(contexts) + np.size(negatives))

    def fit(self, inputs: List[int], contexts: List[List[int]], negatives: List[List[int]],
            epochs: int = 1, lr: np.float32 = 0.001, lr_decay: np.float32 = 1):
        for epoch in range(epochs):
            for i, input in enumerate(inputs):
                for context in contexts[i]:
                    self.step_positive(input, context, lr)
                for negative in negatives[i]:
                    self.step_negative(input, negative, lr)
            logger.info(f"Loss at epoch {epoch + 1}: {self.loss(inputs, contexts, negatives)}")
            lr *= lr_decay

    def save(self, path: str):
        np.save(path, self.core)

    @staticmethod
    def load(path: str):
        core = np.load(path)
        vocab_size = core.shape[0] // 2
        dim = core.shape[1]
        model = SkipGram(vocab_size, dim)
        model.core = core
        return model





