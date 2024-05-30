from gadapt.utils import ga_utils
from gadapt.operations.crossover.base_crossover_event_handler import BaseCrossoverEventHandler


class ParentDiversityCrossoverEventHandler(BaseCrossoverEventHandler):
    """
    Handles crossover events using parent diversity mutation.
    """

    def __init__(self):
        self._genetic_diversity = None

    def _get_genetic_diversity(self, mother_gene, father_gene) -> float:
        return abs(
            mother_gene.variable_value - father_gene.variable_value
        ) / (
            father_gene.decision_variable.max_value
            - father_gene.decision_variable.min_value
        )

    def _get_parent_diversity(self):
        return round(ga_utils.average(self._genetic_diversity), 2)

    def on_decision_variable_crossed(self, *args, **kwargs):
        mother_gene = kwargs.get('mother_gene')
        father_gene = kwargs.get('father_gene')
        if mother_gene is None or father_gene is None:
            return
        self._genetic_diversity.append(self._get_genetic_diversity(mother_gene, father_gene))

    def on_all_decision_variable_crossed(self, *args, **kwargs):
        parent_diversity = self._get_parent_diversity()
        offspring1 = kwargs.get('offspring1')
        offspring2 = kwargs.get('offspring2')
        if offspring1 is None or offspring2 is None:
            return
        offspring1.parent_diversity = parent_diversity
        offspring2.parent_diversity = parent_diversity

    def pre_cross_genetic_material(self, *args, **kwargs):
        self._genetic_diversity = []
