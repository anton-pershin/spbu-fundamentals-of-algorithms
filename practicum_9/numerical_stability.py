from abc import ABC, abstractmethod
from typing import Literal, Sequence, Type, Any

import numpy as np
from numpy.typing import DTypeLike, ArrayLike


EvaluationMethod = Literal["standard", "optimal"]


class Evaluator(ABC):
    def __init__(
        self,
        dtype: DTypeLike,
        evaluation_method: EvaluationMethod,
    ):
        self.dtype = dtype
        self.eval_func = None
        self.reset_evaluation_method(evaluation_method)

    def __call__(self, *args):
        return self.eval_func(*args)

    def reset_evaluation_method(self, evaluation_method: EvaluationMethod):
        if evaluation_method == "standard":
            self.eval_func = self._eval_standard
        elif evaluation_method == "optimal":
            self.eval_func = self._eval_optimal
        else:
            raise ValueError(f"Unknown evaluation method: {evaluation_method}")

    @abstractmethod
    def _eval_standard(self, *args): ...

    @abstractmethod
    def _eval_optimal(self, *args): ...


class Polynomial(Evaluator):
    def __init__(
        self,
        dtype: DTypeLike,
        evaluation_method: EvaluationMethod,
        **kwargs,
    ):
        assert "coeffs" in kwargs, "coeffs must be specified"
        self.coeffs = np.array(kwargs["coeffs"], dtype=dtype)
        super().__init__(dtype, evaluation_method)

    def _eval_standard(self, x):

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        pass

    def _eval_optimal(self, x):

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        pass


class SeriesSum(Evaluator):
    def __init__(
        self,
        dtype: DTypeLike,
        evaluation_method: EvaluationMethod,
        **kwargs,
    ):
        assert "max_i" in kwargs, "max_i must be specified"
        self.max_i = kwargs["max_i"]
        super().__init__(dtype, evaluation_method)

    def _eval_standard(self):

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        pass

    def _eval_optimal(self):

        ##########################
        ### PUT YOUR CODE HERE ###
        ##########################

        pass


def _get_value(f, x=None):
    return f() if x is None else f(x)


def _print_relative_error(eval_by_precision: dict[int, Evaluator], val_exact, x=None):
    for n_bits in (16, 32):
        val_appr = _get_value(eval_by_precision[n_bits], x)
        if isinstance(val_appr, Sequence):
            for i in range(len(val_appr)):
                rel_err = np.abs((val_exact[i] - val_appr[i]) / val_exact[i])
                print(
                    f"Float{n_bits} value #{i+1}: {val_appr[i]:.5f}. "
                    f"Relative error: {rel_err:.2e}"
                )
        else:
            rel_err = np.abs((val_exact - val_appr) / val_exact)
            print(
                f"Float{n_bits} value: {val_appr:.5f}. "
                f"Relative error: {rel_err:.2e}"
            )


def run_different_precision_levels(
    evaluator: Type[Evaluator], evaluator_params: dict[str, Any], x=None
):
    dtypes = (np.float16, np.float32, np.float64)
    eval_by_precision = {
        n_bits: evaluator(dtype=dtype, evaluation_method="standard", **evaluator_params)
        for n_bits, dtype in zip(
            [16, 32, 64],
            dtypes,
        )
    }

    val_exact = _get_value(eval_by_precision[64], x)

    print("Relative errors for standard evaluation")
    _print_relative_error(eval_by_precision, val_exact, x)

    print("Relative errors for optimal evaluation")
    for eval in eval_by_precision.values():
        eval.reset_evaluation_method("optimal")

    _print_relative_error(eval_by_precision, val_exact, x)


if __name__ == "__main__":
    print("=== Sum evaluation ===".upper())
    run_different_precision_levels(
        SeriesSum,
        evaluator_params=dict(max_i=200),
    )
    print()

    print("=== Polynomial evaluation ===".upper())
    original_coeffs = [1.5, 10.2, -10.1, 1.0]
    x = 4.71
    run_different_precision_levels(
        Polynomial,
        evaluator_params=dict(coeffs=original_coeffs),
        x=x
    )

