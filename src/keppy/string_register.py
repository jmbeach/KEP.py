"""Represents a string register (SXXX)"""
from keppy.register import Register

class StringRegister(Register):
    """Represents a string register
    Between S000 - S999."""

    def __init__(self, is_16bit, initial_address="S0000"):
        Register.__init__(self, is_16bit, initial_address)
