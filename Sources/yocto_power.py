#*********************************************************************
#*
#* $Id: pic24config.php 8306 2012-10-17 05:23:41Z mvuilleu $
#*
#* Implements yFindPower(), the high-level API for Power functions
#*
#* - - - - - - - - - License information: - - - - - - - - - 
#*
#* Copyright (C) 2011 and beyond by Yoctopuce Sarl, Switzerland.
#*
#* 1) If you have obtained this file from www.yoctopuce.com,
#*    Yoctopuce Sarl licenses to you (hereafter Licensee) the
#*    right to use, modify, copy, and integrate this source file
#*    into your own solution for the sole purpose of interfacing
#*    a Yoctopuce product with Licensee's solution.
#*
#*    The use of this file and all relationship between Yoctopuce 
#*    and Licensee are governed by Yoctopuce General Terms and 
#*    Conditions.
#*
#*    THE SOFTWARE AND DOCUMENTATION ARE PROVIDED 'AS IS' WITHOUT
#*    WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING 
#*    WITHOUT LIMITATION, ANY WARRANTY OF MERCHANTABILITY, FITNESS 
#*    FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO
#*    EVENT SHALL LICENSOR BE LIABLE FOR ANY INCIDENTAL, SPECIAL,
#*    INDIRECT OR CONSEQUENTIAL DAMAGES, LOST PROFITS OR LOST DATA, 
#*    COST OF PROCUREMENT OF SUBSTITUTE GOODS, TECHNOLOGY OR 
#*    SERVICES, ANY CLAIMS BY THIRD PARTIES (INCLUDING BUT NOT 
#*    LIMITED TO ANY DEFENSE THEREOF), ANY CLAIMS FOR INDEMNITY OR
#*    CONTRIBUTION, OR OTHER SIMILAR COSTS, WHETHER ASSERTED ON THE
#*    BASIS OF CONTRACT, TORT (INCLUDING NEGLIGENCE), BREACH OF
#*    WARRANTY, OR OTHERWISE.
#*
#* 2) If your intent is not to interface with Yoctopuce products,
#*    you are not entitled to use, read or create any derived
#*    material from this source file.
#*
#*********************************************************************/


__docformat__ = 'restructuredtext en'
from yocto_api import *
class YPower(YFunction):
    """
    The Yoctopuce application programming interface allows you to read an instant
    measure of the sensor, as well as the minimal and maximal values observed.
    
    """
    #--- (globals)


    #--- (end of globals)

    #--- (definitions)


    LOGICALNAME_INVALID             = YAPI.INVALID_STRING
    ADVERTISEDVALUE_INVALID         = YAPI.INVALID_STRING
    UNIT_INVALID                    = YAPI.INVALID_STRING
    CURRENTVALUE_INVALID            = YAPI.INVALID_DOUBLE
    LOWESTVALUE_INVALID             = YAPI.INVALID_DOUBLE
    HIGHESTVALUE_INVALID            = YAPI.INVALID_DOUBLE
    CURRENTRAWVALUE_INVALID         = YAPI.INVALID_DOUBLE
    RESOLUTION_INVALID              = YAPI.INVALID_DOUBLE
    CALIBRATIONPARAM_INVALID        = YAPI.INVALID_STRING
    CALIBRATIONOFFSET_INVALID       = YAPI.INVALID_LONG



    _PowerCache ={}

    #--- (end of definitions)

    def __init__(self,func):
        super(YPower,self).__init__("Power", func)
        #--- (YPower implementation)
        self._callback = None
        self._logicalName = YPower.LOGICALNAME_INVALID
        self._advertisedValue = YPower.ADVERTISEDVALUE_INVALID
        self._unit = YPower.UNIT_INVALID
        self._currentValue = YPower.CURRENTVALUE_INVALID
        self._lowestValue = YPower.LOWESTVALUE_INVALID
        self._highestValue = YPower.HIGHESTVALUE_INVALID
        self._currentRawValue = YPower.CURRENTRAWVALUE_INVALID
        self._resolution = YPower.RESOLUTION_INVALID
        self._calibrationParam = YPower.CALIBRATIONPARAM_INVALID
        self._calibrationOffset = -32767

    def _parse(self, j):
        if j.recordtype != YAPI.TJSONRECORDTYPE.JSON_STRUCT: return -1
        for member in j.members:
            if member.name == "logicalName":
                self._logicalName = member.svalue
            elif member.name == "advertisedValue":
                self._advertisedValue = member.svalue
            elif member.name == "unit":
                self._unit = member.svalue
            elif member.name == "currentValue":
                self._currentValue = round(member.ivalue/65.536) / 1000
            elif member.name == "lowestValue":
                self._lowestValue = round(member.ivalue/65.536) / 1000
            elif member.name == "highestValue":
                self._highestValue = round(member.ivalue/65.536) / 1000
            elif member.name == "currentRawValue":
                self._currentRawValue = member.ivalue/65536.0
            elif member.name == "resolution":
                self._resolution = 1.0 / round(65536.0/member.ivalue)
            elif member.name == "calibrationParam":
                self._calibrationParam = member.svalue
        return 0

    def get_logicalName(self):
        """
        Returns the logical name of the electrical power sensor.
        
        @return a string corresponding to the logical name of the electrical power sensor
        
        On failure, throws an exception or returns YPower.LOGICALNAME_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YPower.LOGICALNAME_INVALID
        return self._logicalName

    def set_logicalName(self, newval):
        """
        Changes the logical name of the electrical power sensor. You can use yCheckLogicalName()
        prior to this call to make sure that your parameter is valid.
        Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        @param newval : a string corresponding to the logical name of the electrical power sensor
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = newval
        return self._setAttr("logicalName", rest_val)


    def get_advertisedValue(self):
        """
        Returns the current value of the electrical power sensor (no more than 6 characters).
        
        @return a string corresponding to the current value of the electrical power sensor (no more than 6 characters)
        
        On failure, throws an exception or returns YPower.ADVERTISEDVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YPower.ADVERTISEDVALUE_INVALID
        return self._advertisedValue

    def get_unit(self):
        """
        Returns the measuring unit for the measured value.
        
        @return a string corresponding to the measuring unit for the measured value
        
        On failure, throws an exception or returns YPower.UNIT_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YPower.UNIT_INVALID
        return self._unit

    def get_currentValue(self):
        """
        Returns the current measured value.
        
        @return a floating point number corresponding to the current measured value
        
        On failure, throws an exception or returns YPower.CURRENTVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YPower.CURRENTVALUE_INVALID
        res = YAPI._applyCalibration(self._currentRawValue, self._calibrationParam, self._calibrationOffset, self._resolution)
        if res != YPower.CURRENTVALUE_INVALID:
            return res
        return self._currentValue

    def set_lowestValue(self, newval):
        """
        Changes the recorded minimal value observed.
        
        @param newval : a floating point number corresponding to the recorded minimal value observed
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(round(newval*65536.0,1))
        return self._setAttr("lowestValue", rest_val)


    def get_lowestValue(self):
        """
        Returns the minimal value observed.
        
        @return a floating point number corresponding to the minimal value observed
        
        On failure, throws an exception or returns YPower.LOWESTVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YPower.LOWESTVALUE_INVALID
        return self._lowestValue

    def set_highestValue(self, newval):
        """
        Changes the recorded maximal value observed.
        
        @param newval : a floating point number corresponding to the recorded maximal value observed
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = str(round(newval*65536.0,1))
        return self._setAttr("highestValue", rest_val)


    def get_highestValue(self):
        """
        Returns the maximal value observed.
        
        @return a floating point number corresponding to the maximal value observed
        
        On failure, throws an exception or returns YPower.HIGHESTVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YPower.HIGHESTVALUE_INVALID
        return self._highestValue

    def get_currentRawValue(self):
        """
        Returns the uncalibrated, unrounded raw value returned by the sensor.
        
        @return a floating point number corresponding to the uncalibrated, unrounded raw value returned by the sensor
        
        On failure, throws an exception or returns YPower.CURRENTRAWVALUE_INVALID.
        """
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YPower.CURRENTRAWVALUE_INVALID
        return self._currentRawValue

    def get_resolution(self):
        """
        Returns the resolution of the measured values. The resolution corresponds to the numerical precision
        of the values, which is not always the same as the actual precision of the sensor.
        
        @return a floating point number corresponding to the resolution of the measured values
        
        On failure, throws an exception or returns YPower.RESOLUTION_INVALID.
        """
        if self._resolution == YPower.RESOLUTION_INVALID:
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YPower.RESOLUTION_INVALID
        return self._resolution

    def get_calibrationParam(self):
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return YPower.CALIBRATIONPARAM_INVALID
        return self._calibrationParam

    def set_calibrationParam(self, newval):
        rest_val = newval
        return self._setAttr("calibrationParam", rest_val)


    def calibrateFromPoints(self , rawValues,refValues):
        """
        Configures error correction data points, in particular to compensate for
        a possible perturbation of the measure caused by an enclosure. It is possible
        to configure up to five correction points. Correction points must be provided
        in ascending order, and be in the range of the sensor. The device will automatically
        perform a lineat interpolatation of the error correction between specified
        points. Remember to call the saveToFlash() method of the module if the
        modification must be kept.
        
        For more information on advanced capabilities to refine the calibration of
        sensors, please contact support@yoctopuce.com.
        
        @param rawValues : array of floating point numbers, corresponding to the raw
                values returned by the sensor for the correction points.
        @param refValues : array of floating point numbers, corresponding to the corrected
                values for the correction points.
        
        @return YAPI.SUCCESS if the call succeeds.
        
        On failure, throws an exception or returns a negative error code.
        """
        rest_val = self._encodeCalibrationPoints(rawValues,refValues,self._resolution,self._calibrationOffset)
        return self._setAttr("calibrationParam", rest_val)

    def loadCalibrationPoints(self , rawValues,refValues):
        if self._cacheExpiration <= YAPI.GetTickCount():
            if YAPI.YISERR(self.load(YAPI.DefaultCacheValidity)):
                return self._lastErrorType
        return YAPI._decodeCalibrationPoints(self._calibrationParam,rawValues,refValues,self._resolution,self._calibrationOffset)

    def nextPower(self):
        """
        Continues the enumeration of electrical power sensors started using yFirstPower().
        
        @return a pointer to a YPower object, corresponding to
                a electrical power sensor currently online, or a None pointer
                if there are no more electrical power sensors to enumerate.
        """
        hwidRef = YRefParam()
        if YAPI.YISERR(self._nextFunction(hwidRef)):
            return None
        if hwidRef.value == "":
            return None
        return YPower.FindPower(hwidRef.value)

    def registerValueCallback(self, callback):
        """
        Registers the callback function that is invoked on every change of advertised value.
        The callback is invoked only during the execution of ySleep or yHandleEvents.
        This provides control over the time when the callback is triggered. For good responsiveness, remember to call
        one of these two functions periodically. To unregister a callback, pass a None pointer as argument.
        
        @param callback : the callback function to call, or a None pointer. The callback function should take two
                arguments: the function object of which the value has changed, and the character string describing
                the new advertised value.
        @noreturn
        """
        if callback is not None:
            self._registerFuncCallback(self)
        else:
            self._unregisterFuncCallback(self)
        self._callback = callback

    def set_callback(self, callback):
        self.registerValueCallback(callback)

    def setCallback(self, callback):
        self.registerValueCallback(callback)


    def advertiseValue(self,value):
        if self._callback is not None:
            self._callback(self, value)

# --- (end of YPower implementation)

# --- (Power functions)

    @staticmethod 
    def FindPower(func):
        """
        Retrieves a electrical power sensor for a given identifier.
        The identifier can be specified using several formats:
        <ul>
        <li>FunctionLogicalName</li>
        <li>ModuleSerialNumber.FunctionIdentifier</li>
        <li>ModuleSerialNumber.FunctionLogicalName</li>
        <li>ModuleLogicalName.FunctionIdentifier</li>
        <li>ModuleLogicalName.FunctionLogicalName</li>
        </ul>
        
        This function does not require that the electrical power sensor is online at the time
        it is invoked. The returned object is nevertheless valid.
        Use the method YPower.isOnline() to test if the electrical power sensor is
        indeed online at a given time. In case of ambiguity when looking for
        a electrical power sensor by logical name, no error is notified: the first instance
        found is returned. The search is performed first by hardware name,
        then by logical name.
        
        @param func : a string that uniquely characterizes the electrical power sensor
        
        @return a YPower object allowing you to drive the electrical power sensor.
        """
        if func in YPower._PowerCache:
            return YPower._PowerCache[func]
        res =YPower(func)
        YPower._PowerCache[func] =  res
        return res

    @staticmethod 
    def  FirstPower():
        """
        Starts the enumeration of electrical power sensors currently accessible.
        Use the method YPower.nextPower() to iterate on
        next electrical power sensors.
        
        @return a pointer to a YPower object, corresponding to
                the first electrical power sensor currently online, or a None pointer
                if there are none.
        """
        devRef = YRefParam()
        neededsizeRef = YRefParam()
        serialRef = YRefParam()
        funcIdRef = YRefParam()
        funcNameRef = YRefParam()
        funcValRef = YRefParam()
        errmsgRef = YRefParam()
        size = YAPI.C_INTSIZE
        #noinspection PyTypeChecker,PyCallingNonCallable
        p = (ctypes.c_int*1)()
        err = YAPI.apiGetFunctionsByClass("Power", 0, p, size,  neededsizeRef, errmsgRef)

        if YAPI.YISERR(err) or not neededsizeRef.value:
            return None

        if YAPI.YISERR(YAPI.yapiGetFunctionInfo(p[0],devRef, serialRef, funcIdRef, funcNameRef,funcValRef, errmsgRef)):
            return None

        return YPower.FindPower(serialRef.value + "." + funcIdRef.value)

    @staticmethod 
    def _PowerCleanup():
        pass

  # --- (end of Power functions)

