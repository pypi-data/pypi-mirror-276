class BaseCrossoverEventHandler:
    """
    Handles crossover events
    """
    def on_decision_variable_crossed(self, *args, **kwargs):
        pass

    def on_all_decision_variable_crossed(self, *args, **kwargs):
        pass

    def pre_cross_genetic_material(self, *args, **kwargs):
        pass
