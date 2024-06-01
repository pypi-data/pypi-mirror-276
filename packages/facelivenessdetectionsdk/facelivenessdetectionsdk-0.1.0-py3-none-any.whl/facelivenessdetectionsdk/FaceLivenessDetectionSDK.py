import ctypes
from os.path import dirname
import os

tensor_url = 'https://doubango.org/deep_learning/libtensorflow_r1.14_cpu+gpu_linux_x86-64.tar.gz'

from sys import version_info
if version_info >= (2,6,0):
    def swig_import_helper():
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_FaceLivenessDetectionSDK', [dirname(__file__)])
            ctypes.CDLL(dirname(__file__) + '/' + 'libFaceLivenessDetectionSDK.so')
        except ImportError:
            import _FaceLivenessDetectionSDK
            return _FaceLivenessDetectionSDK
        if fp is not None:
            try:
                _mod = imp.load_module('_FaceLivenessDetectionSDK', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _FaceLivenessDetectionSDK = swig_import_helper()
    del swig_import_helper
else:
    import _FaceLivenessDetectionSDK
del version_info
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError(name)

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0


try:
    import weakref
    weakref_proxy = weakref.proxy
except:
    weakref_proxy = lambda x: x


FLD_SDK_VERSION_MAJOR = _FaceLivenessDetectionSDK.FLD_SDK_VERSION_MAJOR
FLD_SDK_VERSION_MINOR = _FaceLivenessDetectionSDK.FLD_SDK_VERSION_MINOR
FLD_SDK_VERSION_MICRO = _FaceLivenessDetectionSDK.FLD_SDK_VERSION_MICRO
FLD_SDK_IMAGE_TYPE_RGB24 = _FaceLivenessDetectionSDK.FLD_SDK_IMAGE_TYPE_RGB24
FLD_SDK_IMAGE_TYPE_RGBA32 = _FaceLivenessDetectionSDK.FLD_SDK_IMAGE_TYPE_RGBA32
FLD_SDK_IMAGE_TYPE_BGRA32 = _FaceLivenessDetectionSDK.FLD_SDK_IMAGE_TYPE_BGRA32
FLD_SDK_IMAGE_TYPE_BGR24 = _FaceLivenessDetectionSDK.FLD_SDK_IMAGE_TYPE_BGR24
FLD_SDK_IMAGE_TYPE_NV12 = _FaceLivenessDetectionSDK.FLD_SDK_IMAGE_TYPE_NV12
FLD_SDK_IMAGE_TYPE_NV21 = _FaceLivenessDetectionSDK.FLD_SDK_IMAGE_TYPE_NV21
FLD_SDK_IMAGE_TYPE_YUV420P = _FaceLivenessDetectionSDK.FLD_SDK_IMAGE_TYPE_YUV420P
FLD_SDK_IMAGE_TYPE_YVU420P = _FaceLivenessDetectionSDK.FLD_SDK_IMAGE_TYPE_YVU420P
FLD_SDK_IMAGE_TYPE_YUV422P = _FaceLivenessDetectionSDK.FLD_SDK_IMAGE_TYPE_YUV422P
FLD_SDK_IMAGE_TYPE_YUV444P = _FaceLivenessDetectionSDK.FLD_SDK_IMAGE_TYPE_YUV444P
FLD_SDK_IMAGE_TYPE_Y = _FaceLivenessDetectionSDK.FLD_SDK_IMAGE_TYPE_Y
class FldSdkResult(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, FldSdkResult, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, FldSdkResult, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _FaceLivenessDetectionSDK.new_FldSdkResult(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _FaceLivenessDetectionSDK.delete_FldSdkResult
    __del__ = lambda self : None
    def code(self): return _FaceLivenessDetectionSDK.FldSdkResult_code(self)
    def phrase(self): return _FaceLivenessDetectionSDK.FldSdkResult_phrase(self)
    def json(self): return _FaceLivenessDetectionSDK.FldSdkResult_json(self)
    def numFaces(self): return _FaceLivenessDetectionSDK.FldSdkResult_numFaces(self)
    def isOK(self): return _FaceLivenessDetectionSDK.FldSdkResult_isOK(self)
FldSdkResult_swigregister = _FaceLivenessDetectionSDK.FldSdkResult_swigregister
FldSdkResult_swigregister(FldSdkResult)

class FldSdkParallelDeliveryCallback(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, FldSdkParallelDeliveryCallback, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, FldSdkParallelDeliveryCallback, name)
    def __init__(self, *args, **kwargs): raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _FaceLivenessDetectionSDK.delete_FldSdkParallelDeliveryCallback
    __del__ = lambda self : None
    def onNewResult(self, *args): return _FaceLivenessDetectionSDK.FldSdkParallelDeliveryCallback_onNewResult(self, *args)
FldSdkParallelDeliveryCallback_swigregister = _FaceLivenessDetectionSDK.FldSdkParallelDeliveryCallback_swigregister
FldSdkParallelDeliveryCallback_swigregister(FldSdkParallelDeliveryCallback)

class FldSdkEngine(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, FldSdkEngine, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, FldSdkEngine, name)
    def __init__(self, *args, **kwargs): raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __swig_getmethods__["init"] = lambda x: _FaceLivenessDetectionSDK.FldSdkEngine_init
    if _newclass:init = staticmethod(_FaceLivenessDetectionSDK.FldSdkEngine_init)
    __swig_getmethods__["deInit"] = lambda x: _FaceLivenessDetectionSDK.FldSdkEngine_deInit
    if _newclass:deInit = staticmethod(_FaceLivenessDetectionSDK.FldSdkEngine_deInit)
    __swig_getmethods__["process"] = lambda x: _FaceLivenessDetectionSDK.FldSdkEngine_process
    if _newclass:process = staticmethod(_FaceLivenessDetectionSDK.FldSdkEngine_process)
    __swig_getmethods__["exifOrientation"] = lambda x: _FaceLivenessDetectionSDK.FldSdkEngine_exifOrientation
    if _newclass:exifOrientation = staticmethod(_FaceLivenessDetectionSDK.FldSdkEngine_exifOrientation)
    __swig_getmethods__["requestRuntimeLicenseKey"] = lambda x: _FaceLivenessDetectionSDK.FldSdkEngine_requestRuntimeLicenseKey
    if _newclass:requestRuntimeLicenseKey = staticmethod(_FaceLivenessDetectionSDK.FldSdkEngine_requestRuntimeLicenseKey)
    __swig_getmethods__["warmUp"] = lambda x: _FaceLivenessDetectionSDK.FldSdkEngine_warmUp
    if _newclass:warmUp = staticmethod(_FaceLivenessDetectionSDK.FldSdkEngine_warmUp)
    __swig_destroy__ = _FaceLivenessDetectionSDK.delete_FldSdkEngine
    __del__ = lambda self : None
FldSdkEngine_swigregister = _FaceLivenessDetectionSDK.FldSdkEngine_swigregister
FldSdkEngine_swigregister(FldSdkEngine)

def FldSdkEngine_init(*args):
  current_dir = dirname(__file__)
  if os.path.exists(os.path.join(current_dir, ''))

  return _FaceLivenessDetectionSDK.FldSdkEngine_init(*args)
FldSdkEngine_init = _FaceLivenessDetectionSDK.FldSdkEngine_init

def FldSdkEngine_deInit():
  return _FaceLivenessDetectionSDK.FldSdkEngine_deInit()
FldSdkEngine_deInit = _FaceLivenessDetectionSDK.FldSdkEngine_deInit

def FldSdkEngine_process(*args):
  return _FaceLivenessDetectionSDK.FldSdkEngine_process(*args)
FldSdkEngine_process = _FaceLivenessDetectionSDK.FldSdkEngine_process

def FldSdkEngine_exifOrientation(*args):
  return _FaceLivenessDetectionSDK.FldSdkEngine_exifOrientation(*args)
FldSdkEngine_exifOrientation = _FaceLivenessDetectionSDK.FldSdkEngine_exifOrientation

def FldSdkEngine_requestRuntimeLicenseKey(rawInsteadOfJSON=False):
  return _FaceLivenessDetectionSDK.FldSdkEngine_requestRuntimeLicenseKey(rawInsteadOfJSON)
FldSdkEngine_requestRuntimeLicenseKey = _FaceLivenessDetectionSDK.FldSdkEngine_requestRuntimeLicenseKey

def FldSdkEngine_warmUp(*args):
  return _FaceLivenessDetectionSDK.FldSdkEngine_warmUp(*args)
FldSdkEngine_warmUp = _FaceLivenessDetectionSDK.FldSdkEngine_warmUp

# This file is compatible with both classic and new-style classes.


