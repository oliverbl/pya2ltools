import unittest

from pya2ltools.a2l.reader.token import Lexer

from pya2ltools.a2l.reader.reader import compu_method, measurement


class TestReadCalibrationData(unittest.TestCase):
    def test_read_calibration_data(self):
        measurement_text = """
            MEASUREMENT ASAM.M.SCALAR.UBYTE.IDENTICAL
      "Scalar measurement"
      UBYTE CM.IDENTICAL 0 0 0 255
      ECU_ADDRESS 0x13A00
      FORMAT "%5.0"    /* Note: Overwrites the format stated in the computation method */
    /end MEASUREMENT
"""
        m = measurement(Lexer.from_string(measurement_text))[0]["measurements"][0]

        compu_method_text = """ COMPU_METHOD CM.IDENTICAL
      "conversion that delivers always phys = int"
      IDENTICAL "%3.0" "hours"
    /end COMPU_METHOD
        """
        c = compu_method(Lexer.from_string(compu_method_text))[0]["compu_methods"][0]

        m.compu_method = c