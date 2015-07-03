import logging

log = logging.getLogger()

class Appliance(object):
    """A specific appliance instance
    each appliance of a similar type will share the same underlying model object
    this is just a thin wrapper around ApplianceModel to modify its output
    """
    def __init__(self, model, cycle_length):
        self.model = model
        self.cycle_length = cycle_length

    def __getattr__(self, name):
        return getattr(self.model, name)

    def simulation(self, days, freq, **kwargs):
        log.debug("simulating {}".format(self))
        return self.model.simulation(days, self.cycle_length, freq, **kwargs)

    def __repr__(self):
        return "{}({}, {})".format(self.__class__.__name__, self.model.name, self.cycle_length)
