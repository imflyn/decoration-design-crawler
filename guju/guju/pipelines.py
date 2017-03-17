from guju.service.design_strategy_service import DesignStrategyService


class DesignStrategyPipeline(object):
    def __init__(self):
        self.design_strategy_service = DesignStrategyService()

    def process_item(self, item, spider):
        self.design_strategy_service.handle_item(item)
