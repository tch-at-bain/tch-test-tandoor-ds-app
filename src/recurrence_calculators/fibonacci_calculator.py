import logging
from typing import List


class RecurrenceCalculator:
    """General recurrence calculator using efficient memoization"""

    # define recurrence relation of type r[n] = c[0]*r[n+o[0]] + c[1]*r[n+o[1]] + ...
    # so offsets = [-1, -2] and coefficients = [1, 1] would be r[n] = r[n-1] + r[n-2]
    def __init__(
        self, offsets: List[int], coefficients: List[float], sequence: List[float]
    ) -> None:
        """
        Define the recurrence definition and initial terms

        Parameters
        ----------
        offsets
            list of the index offsets
        coefficients
            list of the coefficients corresponding to the offsets
        sequence
            starting few values of the recurrence from index 0

        Returns
        ------
        None
        """
        self.logger = logging.getLogger()
        self.offsets = offsets
        self.coefficients = coefficients
        self.computed_values = {}
        for i, val in enumerate(sequence):
            self.computed_values[i] = val
        if len(self.offsets) != len(self.coefficients):
            self.logger.error("mismatching input lengths in definition!")

    def compute(self, index: int) -> float:
        """
        Generates the value storing partial values along the way

        Parameters
        ----------
        index
            input index to either lookup or compute

        Returns
        -------
        float
            value of the recurrence at n
        """
        if index < 0:
            raise Exception("requested negative index %d!" % index)
        if index not in self.computed_values:
            self.logger.debug("computing value at n=%d", index)
            self.computed_values[index] = sum(
                [
                    self.coefficients[i] * self.compute(index + offset)
                    for i, offset in enumerate(self.offsets)
                ]
            )
        return self.computed_values[index]

    def count(self) -> int:
        """
        Looks up how many values are currently cached

        Returns
        -------
        int
            how many stored values this calculator has computed
        """
        return len(self.computed_values.keys())


class FibonacciCalculator(RecurrenceCalculator):
    """Extended class with specific starting inputs for fibonacci calculation"""

    def __init__(self) -> None:
        """
        Inherited constructor with hard coded update rule
        """
        super(FibonacciCalculator, self).__init__([-1, -2], [1, 1], [1, 1])

    def reset_start(self, sequence: List[float]) -> None:
        """
        Function to follow the same rule but start with different seed sequence

        Parameters
        ----------
        sequence
            list of starting terms from index 0

        Returns
        -------
        None
        """
        self.computed_values = {}
        for i, val in enumerate(sequence):
            self.computed_values[i] = val
