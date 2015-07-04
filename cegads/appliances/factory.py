from .model import ModelFactory
from .appliance import Appliance

class ApplianceFactory(object):
    """A thing to make appliance instances using a given model factory
    """
    def __init__(self, path=None, freq="1Min", method="cubic"):
        self.model_factory = ModelFactory(path, freq, method)

    def __call__(self, appliance, cycle_length, daily_consumption):
        model = self.model_factory(appliance, daily_consumption)
        return Appliance(model, cycle_length)
