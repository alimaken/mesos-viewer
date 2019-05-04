# -*- coding: utf-8 -*-

class Helpers(object):

    @staticmethod
    def get_percent(value: str, precision: int = 2) -> float:
        """
        Converts a string representation of percentage of `0.00 - 1.00` to `0.00 - 100.00`
        :param precision: Precision to be used for return float value
        :param value: String percentage between `0.0` and `1.0`
        :return: Float percentage between `0` and `100`
        :rtype: float
        """
        if value:
            f = float(value)
            return round((f * 100) if (f < 1.0) else f, precision)
        else:
            return 0.0

    @staticmethod
    def get_percent_str(value: str, precision: int = 2) -> str:
        """
        Converts a string representation of percentage of `0.00 - 1.00` to `0.00 - 100.00`
        :param precision: Precision to be used for return float value
        :param value: String percentage between `0.0` and `1.0`
        :return: String representation of Float percentage between `0` and `100`
        :rtype: str
        """
        return str(Helpers.get_percent(value, precision))
