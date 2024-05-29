from typing import Type

import torch
from pytorch_optimizer.base.optimizer import BaseOptimizer
from torch.optim import Optimizer


def AutoClippedOptimizer(
    optimizer_cls: Type[Optimizer],
    q: float = 0.1,
    window: int = 200,
    max_norm: float = None,
) -> Type[Optimizer]:
    """
    A factory function that returns an optimizer class with automatic gradient clipping.

    This function creates a new optimizer class that inherits from the given optimizer class and BaseOptimizer.
    The new class includes an automatic gradient clipping feature, which limits the magnitude of gradient updates.
    This can help to stabilize training in certain situations.

    This implementation is inspired by the paper "AutoClip: Adaptive Gradient Clipping for Source Separation Networks."
    (https://arxiv.org/abs/2007.14469) with two differences:
    1. Instead of keeping track of the whole grad norm history it limits its size to the window parameter.
    2. It enables to set max_norm to clamp max grad norm value.

    Parameters
    ----------
    optimizer_cls : Type[Optimizer]
        The base optimizer class to extend with automatic gradient clipping.
    q : float, optional
        The quantile at which to clip gradients. Gradients with norms larger than the q-th quantile of recent gradient norms are clipped.
        Default is 0.1.
    window : int, optional
        The number of recent gradient norms to consider when computing the q-th quantile for clipping.
        Default is 200.
    max_norm : float, optional
        An optional maximum gradient norm. If provided, gradients with norms larger than this value are always clipped to this value.
        Default is None, which means no absolute maximum gradient norm is enforced.

    Returns
    -------
    Type[Optimizer]
        A new optimizer class that includes automatic gradient clipping.
    """

    class AutoClippedOptimizerBase(Optimizer, BaseOptimizer):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.state["grad_history"] = torch.tensor([])
            self.q = q
            self.window = window
            self.max_norm = max_norm

        def _get_grad_norm(self) -> float:
            """
            Calculate the norm of the gradient for the current step.

            Returns
            -------
            float
                The norm of the gradient.
            """
            total_norm = 0
            for p in self._main_params():
                if p.grad is not None:
                    param_norm = p.grad.data.norm(2)
                    total_norm += param_norm.item() ** 2
            total_norm = total_norm ** (1.0 / 2)
            return total_norm

        def _autoclip_gradients(self):
            """
            Automatically clip the gradients based on the recent gradient norms.

            The gradients are clipped at the q-th quantile of the recent gradient norms.
            The recent gradient norms are stored in a window of a specified size.
            """
            obs_grad_norm = torch.tensor(self._get_grad_norm()).unsqueeze(0)
            self.state["grad_history"] = torch.cat(
                (
                    self.state["grad_history"].to(obs_grad_norm.device)[
                        -(self.window - 1) :
                    ],
                    obs_grad_norm,
                )
            )

            # Calculate the clip value
            clip_value = (
                self.state["grad_history"]
                .quantile(self.q)
                .clamp(min=1.0, max=self.max_norm)
            )
            torch.nn.utils.clip_grad_norm_(self._main_params(), clip_value.item())

        def _main_params(self):
            """
            Yields the main parameters of the optimizer.

            Yields
            ------
            torch.Tensor
                The parameters of the optimizer.
            """
            for group in self.param_groups:
                yield from group["params"]

        def step(self, closure=None, **kwargs):
            """
            Perform a single optimization step.

            This method first clips the gradients and then performs the optimization step.

            Parameters
            ----------
            closure : callable, optional
                A closure that reevaluates the model and returns the loss, by default None

            Returns
            -------
            Any
                The result of the optimization step.
            """
            self._autoclip_gradients()
            return super().step(closure=closure, **kwargs)

        @torch.no_grad()
        def reset(self):
            """
            Reset the state of the optimizer.

            This method clears the gradient history and resets the state of the base optimizer.
            """
            self.state["grad_history"] = torch.tensor([])
            super().reset()

    return type(
        f"AutoClipped{optimizer_cls.__name__}",
        (AutoClippedOptimizerBase, optimizer_cls),
        {},
    )
