import re
from functools import wraps

import base58


def validate_message(validator_class):
    def decorator(handler_func):
        @wraps(handler_func)
        def wrapper(update, context):
            # Validate the Solana address
            if validator_class.validate(update.message.text):
                return handler_func(update, context)
            else:
                raise ValidationException(validator_class.error_msg())

        return wrapper

    return decorator


class MessageValidator:
    @staticmethod
    def validate(message):
        pass

    @staticmethod
    def error_msg():
        return "Message data invalid"


class SolanaAddressValidator(MessageValidator):
    @staticmethod
    def validate(message):
        try:
            decoded = base58.b58decode(message)
            return len(decoded) == 32
        except ValueError:
            return False

    @staticmethod
    def error_msg():
        return "Solana address is invalid"


class SellPercentValidator(MessageValidator):
    @staticmethod
    def validate(percent):
        # Validate the input as an integer from 1 to 100
        if isinstance(percent, str) and re.match(r"^\d+(\.\d+)?$", percent):
            try:
                value = float(percent)  # Convert the string to a float
                return 1 <= value <= 100
            except ValueError:
                return False
        return False

    @staticmethod
    def error_msg():
        return "Percentage is invalid. It should be a number between 1 and 100, like 1, 2.5, or 50."


class SolAmountValidator(MessageValidator):
    @staticmethod
    def validate(amount):
        # SHOULD BE FLOAT OR INT  which comes as string from 0.005 to 50
        # Convert the string to a float and validate the range
        try:
            amount = float(amount.replace(',', '.'))
            return 0.001 <= amount <= 50
        except ValueError:
            return False  # Return False if the conversion fails

    @staticmethod
    def error_msg():
        return "Solana amount is invalid. It should be number e.g: 0.5, 5, 12. More than 0.001 and less than 50."


class SlippageValidator(MessageValidator):
    @staticmethod
    def validate(slippage):
        # Validate the input as a number between 0.01 and 25 (int or float as string)
        if isinstance(slippage, str) and re.match(r"^\d+([.,]\d+)?$", slippage):
            try:
                value = float(slippage.replace(',', '.'))
                return 0.01 <= value <= 25
            except ValueError:
                return False
        return False

    @staticmethod
    def error_msg():
        return "Slippage is invalid. It should be a number between 1 and 25, like 1, 1.5, or 25."


class TriggerPriceValidator(MessageValidator):
    @staticmethod
    def validate(trigger):
        trigger = trigger.replace(',', '.')
        # Should be either:
        # 1. Price in USD (positive float or int which comes as string)
        # 2. Percent  int number which comes as string like +5% or -5%
        # 3. Capitalization: string like 1K, 5K, 1M, 5M, 1B, 5B
        # 4. Multiplier positive int or float which comes as string with x in the end e.g. 0.5x 2x 1.5x
        # Check for USD price (positive float or int)
        if isinstance(trigger, str):
            try:
                value = float(trigger)
                if value > 0:
                    return True
            except ValueError:
                pass
        # Check for percent format like +5% or -5%
        if isinstance(trigger, str) and re.match(r"^[+-]?\d+%$", trigger):
            return True

        # Check for capitalization format like 1K, 5K, 1M, etc.
        if isinstance(trigger, str) and re.match(r"^\d+(\.\d+)?[KMBkmb]$", trigger):
            return True

        # Check for multiplier format like 0.5x, 2x, etc.
        if isinstance(trigger, str) and re.match(r"^\d+(\.\d+)?x$", trigger):
            return True

        return False

    @staticmethod
    def error_msg():
        return ("Invalid trigger price. Should be:\n"
                "- MCap in thousands (K), millions (M) or billions (B)\n"
                "- Price in USD (e.g. “0.05”)\n"
                "- Multiple (e.g. “0.8x”)\n"
                "- Percentage change (e.g. 5%, -5%)\n"
                )


class ValidationException(Exception):
    pass
