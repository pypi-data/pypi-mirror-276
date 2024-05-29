import math

from gadapt.utils.ga_utils import (
    normally_distributed_random,
)
from gadapt.operations.mutation.gene_mutation.base_gene_mutator import BaseGeneMutator


class NormalDistributionGeneMutator(BaseGeneMutator):
    """
    Generates random or normally distributed values.
    """

    def _make_mutated_value(self):
        return self._make_normally_distributed_random_value_until_changed()

    def _make_normally_distributed_random_value_until_changed(self):
        return self._execute_function_until_value_changed(
            self._make_normally_distributed_random_value
        )

    def _calculate_normal_distribution_standard_deviation(self):
        return 0.05

    def _make_normally_distributed_random_value(self):
        curr_value = self.gene.variable_value
        if math.isnan(curr_value):
            curr_value = self.gene.decision_variable.make_random_value()
        decision_variable_range = (
            self.gene.decision_variable.max_value
            - self.gene.decision_variable.min_value
        )
        mean = (
            curr_value - self.gene.decision_variable.min_value
        ) / decision_variable_range
        normal_distribution_random_value = normally_distributed_random(
            mean, self._calculate_normal_distribution_standard_deviation(), 0, 1
        )
        number_of_steps = round(
            (normal_distribution_random_value * decision_variable_range)
            / self.gene.decision_variable.step
        )
        return (
            self.gene.decision_variable.min_value
            + number_of_steps * self.gene.decision_variable.step
        )
