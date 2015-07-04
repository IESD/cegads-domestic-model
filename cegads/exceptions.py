class CEGADSException(Exception): pass
class InvalidDataFileError(CEGADSException): pass
class ScenarioNotFound(CEGADSException): pass
class InvalidYearError(CEGADSException): pass
class InvalidDeviceError(CEGADSException): pass
class UnsupportedAppliance(CEGADSException): pass



__all__ = ['InvalidDataFileError', 'ScenarioNotFound', 'UnsupportedAppliance', 'InvalidYearError', 'CEGADSException', 'InvalidDeviceError']
