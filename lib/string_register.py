"""Represents a string register (SXXX)"""
import register

class StringRegister(register.Register):
    """Represents a string register
    Between S000 - S999."""

    def __init__(self, is_16bit):
        register.Register.__init__(self, is_16bit, "S000")
