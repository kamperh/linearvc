"""
Reduced rank regression.

From: <https://github.com/krey/rrpy/blob/main/rrpy/reduced_rank_ridge.py>
"""

import numpy as np
import sklearn.linear_model


def _fit_rrr_no_intercept_all_ranks(
    X: np.ndarray, Y: np.ndarray, alpha: float, solver: str
):
    ridge = sklearn.linear_model.Ridge(
        alpha=alpha, fit_intercept=False, solver=solver
    )
    beta_ridge = ridge.fit(X, Y).coef_
    Lambda = np.eye(X.shape[1]) * np.sqrt(alpha)
    X_star = np.concatenate((X, Lambda))
    Y_star = X_star @ beta_ridge.T
    _, _, Vt = np.linalg.svd(Y_star, full_matrices=False)
    return beta_ridge, Vt


def _fit_rrr_no_intercept(
    X: np.ndarray,
    Y: np.ndarray,
    alpha: float,
    rank: int,
    solver: str,
    memory=None,
):
    memory = sklearn.utils.validation.check_memory(memory)
    fit = memory.cache(_fit_rrr_no_intercept_all_ranks)
    beta_ridge, Vt = fit(X, Y, alpha, solver)
    return (
        Vt[:rank, :].T,
        beta_ridge,
        Vt[:rank, :].T @ (Vt[:rank, :] @ beta_ridge),
    )


class ReducedRankRidge(
    sklearn.base.MultiOutputMixin,
    sklearn.base.RegressorMixin,
    sklearn.linear_model._base.LinearModel,
):
    def __init__(
        self,
        alpha=1.0,
        fit_intercept=True,
        rank=None,
        ridge_solver="auto",
        memory=None,
    ):
        self.alpha = alpha
        self.fit_intercept = fit_intercept
        self.rank = rank
        self.ridge_solver = ridge_solver
        self.memory = memory

    def fit(self, X, y):
        if self.fit_intercept:
            X_offset = np.average(X, axis=0)
            y_offset = np.average(y, axis=0)
            # doesn't modify inplace, unlike -=
            X = X - X_offset
            y = y - y_offset
        self.Vr, beta_ridge, self.coef_ = _fit_rrr_no_intercept(
            X, y, self.alpha, self.rank, self.ridge_solver, self.memory
        )
        self.Vrt_times_beta = self.Vr.T @ beta_ridge
        self.rank_ = np.linalg.matrix_rank(self.coef_)
        if self.fit_intercept:
            self.intercept_ = y_offset - X_offset @ self.coef_.T
        else:
            self.intercept_ = np.zeros(y.shape[1])
        return self
