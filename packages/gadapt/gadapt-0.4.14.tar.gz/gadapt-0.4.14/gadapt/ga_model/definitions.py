"""
Genetic algorithm definitions
"""

RANDOM = "random"
COST_DIVERSITY = "cost_diversity"
PARENT_DIVERSITY = "parent_diversity"
CROSS_DIVERSITY = "cross_diversity"
TOURNAMENT = "tournament"
FROM_TOP_TO_BOTTOM = "from_top_to_bottom"
ROULETTE_WHEEL = "roulette_wheel"
UNIFORM = "uniform"
BLENDING = "blending"
AVG_COST = "avg_cost"
MIN_COST = "min_cost"
REQUESTED = "requested"
GENERATIONS = "generations"
AVG = "avg"
MIN = "min"
PARAM_SEPARATOR = ","
FLOAT_NAN = float("NaN")
NOT_IMPLEMENTED = "not implemented"
EXTREME_POINTED = "extreme_pointed"
NORMAL_DISTRIBUTION = "normal_distribution"
POPULATION_MUTATION_STRINGS = [
    COST_DIVERSITY,
    PARENT_DIVERSITY,
    RANDOM,
    CROSS_DIVERSITY,
]
POPULATION_MUTATION_SELECTION_STRINGS = [RANDOM, PARENT_DIVERSITY]
CHROMOSOME_MUTATION_STRINGS = [RANDOM, CROSS_DIVERSITY]
GENE_MUTATION_STRINGS = [RANDOM, NORMAL_DISTRIBUTION, CROSS_DIVERSITY, EXTREME_POINTED]
SELECTION_STRINGS = [RANDOM, FROM_TOP_TO_BOTTOM, ROULETTE_WHEEL, TOURNAMENT]
EXIT_CRITERIA_STRINGS = [AVG_COST, MIN_COST, REQUESTED, GENERATIONS]
