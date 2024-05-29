# AutoClipper

AutoClippedOptimizer is a Python factory function that returns an optimizer class with automatic gradient clipping. This feature can help to stabilize training in certain situations by limiting the magnitude of gradient updates.

The implementation is inspired by the paper "AutoClip: Adaptive Gradient Clipping for Source Separation Networks" (<https://arxiv.org/abs/2007.14469>) with two key differences:

1. Instead of keeping track of the whole grad norm history, it limits its size to a specified window.
2. It enables setting a max_norm to clamp the max grad norm value.

## Usage

```python
from autoclipper import AutoClippedOptimizer

# Create a new optimizer class with automatic gradient clipping
optimizer_cls = AutoClippedOptimizer(optimizer_cls, q=0.1, window=200, max_norm=None)

# Use the new optimizer class in your training loop
optimizer = optimizer_cls(model.parameters(), lr=0.01)
```

## Parameters

- `optimizer_cls` (Type[Optimizer]): The base optimizer class to extend with automatic gradient clipping.
- `q` (float, optional): The quantile at which to clip gradients. Gradients with norms larger than the q-th quantile of recent gradient norms are clipped. Default is 0.1.
- `window` (int, optional): The number of recent gradient norms to consider when computing the q-th quantile for clipping. Default is 200.
- `max_norm` (float, optional): An optional maximum gradient norm. If provided, gradients with norms larger than this value are always clipped to this value. Default is None, which means no absolute maximum gradient norm is enforced.

## Methods

- `__init__(self, *args, **kwargs)`: Initializes the optimizer.
- `_get_grad_norm(self)`: Calculates the norm of the gradient for the current step.
- `_autoclip_gradients(self)`: Automatically clips the gradients based on the recent gradient norms.
- `_main_params(self)`: Yields the main parameters of the optimizer.
- `step(self, closure=None, **kwargs)`: Performs a single optimization step.
- `reset(self)`: Resets the state of the optimizer.
