from typing import TYPE_CHECKING

import numpy as np
from pydantic import NonNegativeInt

from .BaseDataClass import BaseDataClass
from ._helper_functions import (_ground_state_open, _ground_state_closed, check_algorithm_and_implementation)
from ..functions import convert_to_maxwell, optimal_Vg
from ..qarray_types import Cdd as CddType  # to avoid name clash with dataclass cdd
from ..qarray_types import CgdNonMaxwell, CddNonMaxwell, VectorList, Cgd_holes, Cgd_electrons, PositiveValuedMatrix, \
    NegativeValuedMatrix

if TYPE_CHECKING:
    from dataclasses import dataclass
else:
    from pydantic.dataclasses import dataclass

from ..latching_models import LatchingBaseModel

def both_none(a, b):
    return a is None and b is None


def all_positive(a):
    return np.all(a >= 0)


def all_negative(a):
    return np.all(a <= 0)


def all_positive_or_negative(a):
    return all_positive(a) or all_negative(a)


@dataclass(config=dict(arbitrary_types_allowed=True, auto_attribs_default=True))
class DotArray(BaseDataClass):

    """
    A class to represent a quantum dot array. The class is initialized with the following parameters:

    Cdd: CddNonMaxwell | None = None  # an (n_dot, n_dot) the capacitive coupling between dots
    Cgd: CgdNonMaxwell | None = None  # an (n_dot, n_gate) the capacitive coupling between gates and dots

    cdd: Cdd | None = None  # an (n_dot, n_dot) the capacitive coupling between dots
    cgd: PositiveValuedMatrix | NegativeValuedMatrix | None = None # an (n_dot, n_gate) the capacitive coupling between gates and dots

    algorithm: str | None = 'default'  # which algorithm to use
    implementation: str | None = 'rust'

    threshold: float | str = 1.  # if the threshold algorithm is used the user needs to pass the threshold
    max_charge_carriers: int | None = None  # if the brute force algorithm is used the user needs to pass the maximum number of charge carriers

    charge_carrier: str = 'hole'  # a string of either 'electron' or 'hole' to specify the charge carrie
    T: float | int = 0.  # the temperature of the system for if there is thermal broadening

    """

    Cdd: CddNonMaxwell | None = None  # an (n_dot, n_dot)the capacitive coupling between dots
    Cgd: CgdNonMaxwell | None = None  # an (n_dot, n_gate) the capacitive coupling between gates and dots
    cdd: CddType | None = None
    cgd: PositiveValuedMatrix | NegativeValuedMatrix | None = None

    algorithm: str | None = 'default'  # which algorithm to use
    implementation: str | None = 'rust'  # which implementation of the algorithm to use
    threshold: float | str = 1.  # if the threshold algorithm is used the user needs to pass the threshold
    max_charge_carriers: int | None = None  # if the brute force algorithm is used the user needs to pass the maximum number of charge carriers

    charge_carrier: str = 'hole'  # a string of either 'electron' or 'hole' to specify the charge carrie
    T: float | int = 0.  # the temperature of the system, only used for jax and jax_brute_force cores
    batch_size: int = 10000
    polish: bool = True  # a bool specifying whether to polish the result of the ground state computation

    latching_model: LatchingBaseModel | None = None  # a latching model to add latching to the dot occupation vector

    def __post_init__(self):
        """
        This function is called after the initialization of the dataclass. It checks that the capacitance matrices
        are valid and sets the cdd_inv attribute as the inverse of cdd.
        """

        # checking that either cdd and cgd or cdd and cgd are specified
        non_maxwell_pair_passed = not both_none(self.Cdd, self.Cgd)
        maxwell_pair_passed = not both_none(self.cdd, self.cgd)
        assertion_message = 'Either cdd and cgd or cdd and cgd must be specified'
        assert (non_maxwell_pair_passed or maxwell_pair_passed), assertion_message

        # if the non maxwell pair is passed, convert it to maxwell
        if non_maxwell_pair_passed:
            self.cdd, self.cdd_inv, self.cgd = convert_to_maxwell(self.Cdd, self.Cgd)

        # setting the cdd_inv attribute as the inverse of cdd
        self.cdd_inv = np.linalg.inv(self.cdd)

        # checking that the cgd matrix has all positive or all negative elements
        # so that the sign can be matched to the charge carrier
        assert all_positive_or_negative(self.cgd), 'The elements of cgd must all be positive or all be negative'

        # matching the sign of the cgd matrix to the charge carrier
        match self.charge_carrier.lower():
            case 'electrons' | 'electron' | 'e' | '-':
                self.charge_carrier = 'electrons'
                # the cgd matrix is positive for electrons
                self.cgd = Cgd_electrons(np.abs(self.cgd))
            case 'holes' | 'hole' | 'h' | '+':
                self.charge_carrier = 'holes'
                # the cgd matrix is negative for holes
                self.cgd = Cgd_holes(-np.abs(self.cgd))
            case _:
                raise ValueError(f'charge_carrier must be either "electrons" or "holes {self.charge_carrier}"')

        # by now in the code, the cdd and cgd matrices have been initialized as their specified types. These
        # types enforce most of the constraints on the matrices like positive-definitness for cdd for example,
        # but not all. The following asserts check the remainder.
        self.n_dot = self.cdd.shape[0]
        self.n_gate = self.cgd.shape[1]
        assert self.cgd.shape[0] == self.n_dot, 'The number of dots must be the same as the number of rows in cgd'

        # type casting the temperature to a float
        self.T = float(self.T)

        # checking the passed algorithm and implementation
        check_algorithm_and_implementation(self.algorithm, self.implementation)
        if self.algorithm == 'threshold':
            assert self.threshold is not None, 'The threshold must be specified when using the thresholded algorithm'

        if self.algorithm == 'brute_force':
            assert self.max_charge_carriers is not None, 'The maximum number of charge carriers must be specified'

        if self.latching_model is None:
            self.latching_model = LatchingBaseModel()

    def optimal_Vg(self, n_charges: VectorList, rcond: float = 1e-3) -> np.ndarray:
        """
        Computes the optimal dot voltages for a given charge configuration, of shape (n_charge,).
        :param n_charges: the charge configuration
        :param rcond: the rcond parameter for the least squares solver
        :return: the optimal dot voltages of shape (n_gate,)
        """
        return optimal_Vg(cdd_inv=self.cdd_inv, cgd=self.cgd, n_charges=n_charges, rcond=rcond)

    def ground_state_open(self, vg: VectorList | np.ndarray) -> np.ndarray:
        """
        Computes the ground state for an open dot array.
        :param vg: (..., n_gate) array of dot voltages to compute the ground state for
        :return: (..., n_dot) array of ground state charges
        """
        return _ground_state_open(self, vg)

    def ground_state_closed(self, vg: VectorList | np.ndarray, n_charges: NonNegativeInt) -> np.ndarray:
        """
        Computes the ground state for a closed dot array.
        :param vg: (..., n_gate) array of dot voltages to compute the ground state for
        :param n_charges: the number of charges to be confined in the dot array
        :return: (..., n_dot) array of the number of charges to compute the ground state for
        """
        return _ground_state_closed(self, vg, n_charges)
