"""a place for all cegads exceptions to be defined

Exceptions:
CEGADSException - general purpose, parent exception class
InvalidDataFileError - indicates a problem with a data file
InvalidYearError - trying to access a year that is not available in the data
InvalidDeviceError - trying to access a device that is not available in the data
UnsupportedAppliance - trying to access a device that is not available in the data

"""
class CEGADSException(Exception): pass
class InvalidDataFileError(CEGADSException): pass
class InvalidYearError(CEGADSException): pass
class InvalidDeviceError(CEGADSException): pass
class UnsupportedAppliance(CEGADSException): pass



__all__ = ['InvalidDataFileError', 'UnsupportedAppliance', 'InvalidYearError', 'CEGADSException', 'InvalidDeviceError']
