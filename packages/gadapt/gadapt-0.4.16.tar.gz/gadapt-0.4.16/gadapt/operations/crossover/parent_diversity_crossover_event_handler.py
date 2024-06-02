from gadapt.ga_model.chromosome import Chromosome
from gadapt.ga_model.allele import Allele
from gadapt.utils import ga_utils
from gadapt.operations.crossover.base_crossover_event_handler import (
    BaseCrossoverEventHandler,
)


class ParentDiversityCrossoverEventHandler(BaseCrossoverEventHandler):
    """
    Handles crossover events using parent diversity mutation.
    """

    def __init__(self):
        self._genetic_diversity = None

    def _get_genetic_diversity(self, mother_gene, father_gene) -> float:
        return abs(mother_gene.variable_value - father_gene.variable_value) / (
            father_gene.gene.max_value - father_gene.gene.min_value
        )

    def _get_parent_diversity(self):
        return round(ga_utils.average(self._genetic_diversity), 2)

    def on_gene_crossed(self, mother_gene: Allele, father_gene: Allele):
        if mother_gene is None or father_gene is None:
            return
        self._genetic_diversity.append(
            self._get_genetic_diversity(mother_gene, father_gene)
        )

    def on_all_genes_crossed(self, offspring1: Chromosome, offspring2: Chromosome):
        parent_diversity = self._get_parent_diversity()
        offspring1.parent_diversity = parent_diversity
        offspring2.parent_diversity = parent_diversity

    def pre_cross_genetic_material(self, *args, **kwargs):
        self._genetic_diversity = []
