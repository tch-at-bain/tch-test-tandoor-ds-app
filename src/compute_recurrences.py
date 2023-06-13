"""
compute_recurrences.py
=============================
main module/script of python-example
"""

import os
import math
import logging
from recurrence_calculators import FibonacciCalculator, RecurrenceCalculator

# This is one way to explicitly set the log level in code
log_level = os.environ.get("LOGLEVEL", "INFO").upper()
logging.basicConfig(format="%(asctime)s %(levelname)s:   %(message)s", level=log_level)
logger = logging.getLogger()


def ratio(calc: RecurrenceCalculator, index: int) -> float:
    """
    Compute the ratio of adjacent recurrence values

    Parameters
    ----------
    index
        index of the recurrence value in denominator

    Returns
    -------
    float
        (index+1) recurrence value divided by the index recurrence value
    """
    return round(calc.compute(index + 1) / calc.compute(index), 5)


if __name__ == "__main__":
    N = 50

    # r[n] = r[n-1] + r[n-2], r[0] = 1, r[1] = 1
    fib_calc = FibonacciCalculator()
    logger.info("The %dth Fibonacci number is %f", N, fib_calc.compute(N))

    # print the first 20 Fibonacci numbers
    logger.info([fib_calc.compute(i) for i in range(20)])
    # print the relative ratios which approach the golden ratio
    logger.info([ratio(fib_calc, i) for i in range(20)])
    logger.info(
        "Phi equals %f and by %d the ratio is %f\n",
        (1 + math.sqrt(5)) / 2,
        N,
        ratio(fib_calc, N),
    )

    # r[n] = r[n-1] - 2*r[n-3]
    rec_calc = RecurrenceCalculator([-1, -3], [1, -2], [1, 1, 1])
    logger.info([rec_calc.compute(i) for i in range(20)])
    logger.info(
        [round(rec_calc.compute(i + 1) / rec_calc.compute(i), 5) for i in range(20)]
    )

    # This line will throw a warning level log message because the parameters do not match in length
    # rec_calc_warn = RecurrenceCalculator([-1, -3, -4], [1, -2], [1, 1, 1])
