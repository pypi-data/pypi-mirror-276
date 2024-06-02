from gadapt.ga_model.chromosome import Chromosome
from gadapt.ga_model.allele import Allele


class BaseCrossoverEventHandler:
    """
    Handles crossover events
    """

    def on_gene_crossed(self, mother_gene: Allele, father_gene: Allele):
        pass

    def on_all_genes_crossed(self, offspring1: Chromosome, offspring2: Chromosome):
        pass

    def pre_cross_genetic_material(self, *args, **kwargs):
        pass
