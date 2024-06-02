from ctypes import *
from sys import argv
import subprocess
import re

InstanceHandle = c_void_p
FloatPointer = POINTER(c_float)

class EffectLib:
    #
    # For each namespace, try to find the specified function
    # until one actually elicits the function
    #
    def _find_func(self, func_name, args):
        for ns in self.nameSpaces:
            symb = '_ZN{}{}{}{}{}'.format(len(ns),ns,len(func_name),func_name,args)
            func = getattr(self.lib,symb, None)
            if func is not None:
                return func
        return None
    
    #
    # Basically we troll through the SO file and dig out all the
    # _ZTI.... symbols - these are, effectively, the symbol namespaces
    # we have to deal with. In FACT, because of the way we trim out two
    # "well known" namespaces, there should only be a max of one other
    # found.
    #
    def _find_namespaces(self, file):
        namespaces = []
        with open(file, "rb") as f:
            TAG = [b'_',b'Z',b'T',b'I']
            NC = 0
            while True: 
                c = f.read(1)
                if c == b'':
                    break
                if c == TAG[NC]:
                    NC+=1
                    if NC >= len(TAG):
                        # we found one
                        l = 0
                        n = f.read(1)
                        while n >= b'0' and n<= b'9':
                            l = (l * 10) + int(n)
                            n = f.read(1)
                        NS = (n + f.read(l-1)).decode("ascii")
                        if NS != "StratusExtensions" and NS != "dsp" and not NS in namespaces:
                            namespaces.append(NS)
                        NC = 0
                else:
                    NC = 0
        namespaces.append("dsp")
        return namespaces

    def __init__(self,so_file):

        lib = CDLL(so_file)

        self.lib = lib
        self.create = lib.create
        try:
            self.getExtensions = lib.getExtensions
        except:
            self.getExtensions = None

        self.nameSpaces = self._find_namespaces(so_file)

        #
        # Using StratusExtensions
        #
        if self.getExtensions is not None:
            self.stratusGetEffectId = getattr(lib,"_ZN17StratusExtensions11getEffectIdEv")
            self.stratusGetName = getattr(lib,"_ZN17StratusExtensions7getNameEv")
            self.stratusGetVersion = getattr(lib,"_ZN17StratusExtensions10getVersionEv")
            self.stratusGetKnobCount = getattr(lib,"_ZN17StratusExtensions12getKnobCountEv")
            self.stratusGetSwitchCount = getattr(lib,"_ZN17StratusExtensions14getSwitchCountEv")
        else:
            self.stratusGetEffectId = None
            self.stratusGetName = None
            self.stratusGetVersion = None
            self.stratusGetKnobCount = None
            self.stratusGetSwitchCount = None

        #
        # Using the effect
        #
        self.stratusSetKnob = self._find_func("setKnob","Eif")
        self.stratusGetKnob = self._find_func("getKnob","Ei")
        self.stratusSetSwitch = self._find_func("setSwitch","EiNS_12SWITCH_STATEE")
        self.stratusGetSwitch = self._find_func("getSwitch","Ei")
        self.stratusSetStompSwitch = self._find_func("setStompSwitch","ENS_12SWITCH_STATEE")
        self.stratusGetStompSwitch = self._find_func("getStompSwitch","Ev")
        self.stratusStompSwitchPressed = self._find_func("stompSwitchPressed","EiPfS0_")
        self.stratusCompute = self._find_func("compute","EiPfS0_")

        self.create.restype = InstanceHandle
        if self.getExtensions is not None:
            self.getExtensions.argtypes = [ InstanceHandle ]
            self.getExtensions.restype = InstanceHandle

            self.stratusGetEffectId.argtypes = [InstanceHandle]
            self.stratusGetEffectId.restype = c_char_p

            self.stratusGetName.argtypes = [InstanceHandle]
            self.stratusGetName.restype = c_char_p

            self.stratusGetVersion.argtypes = [InstanceHandle]
            self.stratusGetVersion.restype = c_char_p

            self.stratusGetKnobCount.argtypes = [InstanceHandle]
            self.stratusGetKnobCount.restype= c_uint

            self.stratusGetSwitchCount.argtypes = [InstanceHandle]
            self.stratusGetSwitchCount.restype= c_uint

        if self.stratusSetKnob is not None:
            self.stratusSetKnob.argtypes = [InstanceHandle, c_uint, c_float]

        if self.stratusGetKnob is not None:
            self.stratusGetKnob.argtypes = [InstanceHandle, c_uint]
            self.stratusGetKnob.restype = c_float

        if self.stratusSetSwitch is not None:
            self.stratusSetSwitch.argtypes = [InstanceHandle, c_uint, c_uint]

        if self.stratusGetSwitch is not None:
            self.stratusGetSwitch.argtypes = [InstanceHandle, c_uint]
            self.stratusGetSwitch.restype= c_uint

        if self.stratusSetStompSwitch is not None:
            self.stratusSetStompSwitch.argtypes = [InstanceHandle, c_uint]

        if self.stratusGetStompSwitch is not None:
            self.stratusGetStompSwitch.argtypes = [InstanceHandle]
            self.stratusGetStompSwitch.restype = c_uint

        if self.stratusCompute is not None:
            self.stratusCompute.argtypes = [InstanceHandle, c_uint, FloatPointer, FloatPointer]
            self.stratusCompute.argtypes = [InstanceHandle, c_uint, FloatPointer, FloatPointer]


class Effect:
    """A class that allows a Python script to interact with a Chaos Stratus effect library

    Chaos Audio Stratus pedal effects libraries are standard binary shared libraries that 
    implement a specific interface. Given an effect library file, this module does all that
    it can to find the function symbols in the library that represent the implementations of 
    that interface and thus provide a Python wrapper to the library to allow you to test the
    library outside of the constraints of the Stratus pedal itself.

    All effects that are built using the Faust integration for the Chaos Stratus are compatible
    with this module. In addition, effects not built using Faust (including those built before
    the Faust integration was available) should be "compatible enough" with the wrapper to be
    usable - they may not implement the StratusExtensions interface that provides useful information
    such as number of knobs and switches or what have you, but they do implement the basic
    functional interface, and this module does its level best to find that implementation in the 
    shared library.

    Note that the effect has to be built for the system upon which your python script isd
    to run - that means you must either install this package onto your pedal, or you must
    build your effect library for the intended python system.

    Again, the Faust tools can help you with this.

    Attributes (only available through the StratusExtensions interface)
    -------------------------------------------------------------------
    effectId : string 
        the UUID of the effect library
    extensionsPresent : boolean 
        whether or not the StratusExtensions interface is present
    knobCount : int 
        the number of control knobs the effect uses
    name : string 
        the friendly name of the effect library
    switchCount : int 
        the number of control switches the effect uses
    version : string
        the version of the effect library

    Constructor
    -----------
    Effect(effect_library_path)
        Load an effect library and construct the Python interface to that library

    Methods
    -------
    setKnob(index, value):
        Set the value the 0-based-indexed knob to the provided float value
    getKnob(index):
        Get the value the 0-based-indexed knob as a float
    setSwitch(index,value):
        Set the value the 0-based-indexed switch to the provided int value (0, 1, or 2)
    getSwitch(index):
        Get the value the 0-based-indexed switch as an int (0, 1, or 2)
    setStompSwitch(value):
        Set the value the Stratus stomp switch to the provided int value (0, 1, or 2)
    getStompSwitch(self):
        Get the value the Stratus stomp switch as an int (0, 1, or 2)
    compute(inputs):
        Apply the effect algorithm to the passed array of float values
    computeBuf(inputs):
        Apply the effect algorithm to the passed buffer of float values
    """
    def __init__(self,so_file):
        """
        Parameters
        ---------
        so_file : str
            The file path to the effect shared library object
        """
        self.effect_lib = EffectLib(so_file)

        self.effect = self.effect_lib.create()
        
        if self.effect_lib.getExtensions is not None:
            effectExtensions = self.effect_lib.getExtensions(self.effect)
            self.knobCount = self.effect_lib.stratusGetKnobCount(effectExtensions)
            self.switchCount = self.effect_lib.stratusGetSwitchCount(effectExtensions)
            self.version = self.effect_lib.stratusGetVersion(effectExtensions).decode()
            self.name = self.effect_lib.stratusGetName(effectExtensions).decode()
            self.effectId = self.effect_lib.stratusGetEffectId(effectExtensions).decode()
            self.extensionsPresent = True
        else:
            self.extensionsPresent = False
            self.knobCount = -1
            self.switchCount = -1
            self.version = 0
            self.name = "Unknown"
            self.effectId = "Unknown"

    def setKnob(self,index, value):
        """Set the value the indicated knob to the provided value
        
        Parameters
        ----------
        index : int
            The 0-based index of the knob to affect
        value : float
            The value to which the knob should be set
        """
        self.effect_lib.stratusSetKnob(self.effect, index, value)
    def getKnob(self,index):
        """Get the value the indicated knob

        Parameters
        ----------
        index : int
            The 0-based index of the knob to address        
        
        Returns
        -------
        float
            The value of the indicated knob (0, 1, or 2)
        """
        return self.effect_lib.stratusGetKnob(self.effect, index)
    def setSwitch(self,index,value):
        """Set the value the indicated switch to the provided value (0, 1, or 2)
        
        Parameters
        ----------
        index : int
            The 0-based index of the switch to affect
        value : int
            The value to which the switch should be set (0, 1, or 2)
        """
        self.effect_lib.stratusSetSwitch(self.effect, index, value)
    def getSwitch(self,index):
        """Get the value the indicated switch

        Parameters
        ----------
        index : int
            The 0-based index of the switch to address        
        
        Returns
        -------
        int
            The value of the indicated switch (0, 1, or 2)
        """
        return self.effect_lib.stratusGetSwitch(self.effect, index)
    def setStompSwitch(self,value):
        """Set the value the Stratus stomp switch to the provided value

        Parameters
        ----------
        value : int
            The value to which the switch should be set (0, 1, or 2)
        """
        self.effect_lib.stratusSetStompSwitch(self.effect, value)
    def getStompSwitch(self):
        """Get the value the Stratus stomp switch
        
        Returns
        -------
        int
            The value of the Stratus stomp switch (0, 1, or 2)
        """
        return self.effect_lib.stratusGetStompSwitch(self.effect)
    def stompSwitchPressed(self,inputs):
        count = len(inputs)
        input_floats = (c_float * count)(*inputs)
        output_floats = (c_float * count)(0.0)
        self.effect_lib.stratusStompSwitchPressed(self.effect, count, input_floats, output_floats)
        return [output_float for output_float in output_floats]
    def compute(self,inputs):
        """Run the effect on the passed array of float values

        The return value of the function is an array of float values representing the output
        of the algorithm... or, in simple terms, your cool effect applied to your input sound!

        Parameters
        ----------
        inputs : [float]
            An array of individual DSP sample values upon which the effect algorithm
            acts. The Stratus uses a sample rate of 44100hz, and 4-byte float values.

        Returns
        -------
        [float]
            The result of the computation.
        """
        count = len(inputs)
        input_floats = (c_float * count)(*inputs)
        output_floats = (c_float * count)(*inputs)
        self.effect_lib.stratusCompute(self.effect, count, input_floats, output_floats)
        return [output_float for output_float in output_floats]
    def stompSwitchPressedBuf(self,inputs):
        if len(inputs) % 4 != 0:
            raise ValueError("inputs must be a buffer of 4-byte floating point values")
        outputs = bytearray(len(inputs))
        count = len(inputs)//4
        input_floats = (c_float * count)(*inputs)
        output_floats = (c_float * count)(*inputs)

        self.effect_lib.stratusStompSwitchPressed(self.effect, c_uint(count), input_floats, output_floats)
        return outputs
    def computeBuf(self,inputs):
        """Run the effect on the passed array of float values

        The return value of the function is an array of float values representing the output
        of the algorithm... or, in simple terms, your cool effect applied to your input sound!

        Parameters
        ----------
        inputs : buffer
            A buffer of individual DSP sample values upon which the effect algorithm
            acts. The Stratus uses a sample rate of 44100hz, and 4-byte float values.

            The buffer length must, of course, be divisible by 4.

        Returns
        -------
        buffer
            The result of the computation.

        Raises
        ------
        ValueError
            If the input buffer length is not divisible by 4
        """

        if len(inputs) % 4 != 0:
            raise ValueError("inputs must be a buffer of 4-byte floating point values")
        outputs = bytearray(len(inputs))
        count = len(inputs)//4
        Buffer = c_float * count
        input_floats = Buffer.from_buffer(inputs)
        output_floats = Buffer.from_buffer(outputs)
        self.effect_lib.stratusCompute(self.effect, c_uint(count), input_floats, output_floats)
        return outputs
