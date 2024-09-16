"""
Miscellaneous utility functions.

Author: Matthew Baas, Benjamin van Niekerk, Herman Kamper
Date: 2024
"""

from torch import Tensor
import torch


def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def fast_cosine_dist(
    source_feats: Tensor, matching_pool: Tensor, device: str = "cpu"
) -> Tensor:
    """
    Like torch.cdist, but fixed dim=-1 and for cosine distance.

    Based on:
    <https://github.com/bshall/knn-vc/blob/master/matcher.py>
    """
    source_norms = torch.norm(source_feats, p=2, dim=-1).to(device)
    matching_norms = torch.norm(matching_pool, p=2, dim=-1)
    dotprod = (
        -torch.cdist(source_feats[None].to(device), matching_pool[None], p=2)[0]
        ** 2
        + source_norms[:, None] ** 2
        + matching_norms[None] ** 2
    )
    dotprod /= 2

    dists = 1 - (dotprod / (source_norms[:, None] * matching_norms[None]))
    return dists


def pca_transform(
    X: Tensor, mean: Tensor, components: Tensor, explained_variance: Tensor
) -> Tensor:
    X = X - mean
    X_transformed = X @ components.T
    X_transformed /= torch.sqrt(explained_variance)
    return X_transformed


def pca_inverse_transform(
    X: Tensor, mean: Tensor, components: Tensor, explained_variance: Tensor
) -> Tensor:
    Xi = X @ (explained_variance[:, None].sqrt() * components)
    return Xi + mean
