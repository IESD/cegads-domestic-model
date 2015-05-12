from .model import ModelFactory

class Appliance(object):
    """A specific appliance instance
    each appliance of a similar type will share the same underlying model object
    this is just a thin wrapper around ApplianceModel to modify its output
    """
    def __init__(self, model):
        self.model = model

    def __getattr__(self, name):
        return getattr(self.model, name)


class ApplianceFactory(object):
    """A thing to make appliance instances using a given model factory
    """
    def __init__(self, path, freq="1Min", method="cubic"):
        self.model_factory = ModelFactory(path, freq, method)

    def __call__(self, appliance):
        model = self.model_factory(appliance)
        return Appliance(model)
