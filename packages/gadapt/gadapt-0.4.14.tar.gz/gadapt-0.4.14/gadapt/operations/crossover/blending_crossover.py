import random

from gadapt.operations.crossover.base_crossover import BaseCrossover


class BlendingCrossover(BaseCrossover):
    """
    Blending Crossover combines
    gene values from the two parents into new variable values in offsprings.
    One value of the offspring variable comes from a combination of the two
    corresponding values of the parental genes
    """

    def __init__(
        self,
    ):
        super(BlendingCrossover, self).__init__()
        self._current_gene_number = -1

    def _combine(self):
        decision_variable = self._father_gene.decision_variable
        val_father = self._father_gene.variable_value
        val_mother = self._mother_gene.variable_value
        x = 1
        if val_mother > val_father:
            x = -1
        beta_steps = random.randint(
            0, round(abs((val_father - val_mother) / decision_variable.step))
        )
        val1 = round(
            val_father - (beta_steps * x) * decision_variable.step,
            decision_variable.decimal_places,
        )
        val2 = round(
            val_mother + (beta_steps * x) * decision_variable.step,
            decision_variable.decimal_places,
        )
        return val1, val2
