from .scanner import CodeType
from .result import Result


def decode_digi_key_barcode(code_type: CodeType, barcode):
    if code_type == CodeType.DataMatrix:
        return decode_datamatrix(barcode)


def decode_datamatrix(barcode):
    data = barcode.split(']')

    result = Result(distributor="DigiKey")
    for param in data:
        if param.startswith('P'):
            result.don = param.removeprefix('P')
        elif param.startswith('1P'):
            result.mon = param.removeprefix('1P')
        elif param.startswith('K'):
            result.order_number = {"number": param.removeprefix('K')}
        elif param.startswith('Q'):
            result.quantity = float(param.removeprefix('Q'))
        elif param.startswith('9D') and len(param) > 2:
            result.date_code = param.removeprefix('9D')
        elif param.startswith('1T') and len(param) > 2:
            result.LOT = param.removeprefix('1T')
        elif param.startswith('4L'):
            result.coo = param.removeprefix('4L')
        elif param.startswith('4K'):
            result.order_number["position"] = param.removeprefix('4K')
        elif param.startswith('10K'):
            pass
        elif param.startswith('11K'):
            pass
        elif param.startswith('12Z'):
            pass  # part id
        elif param.startswith('13Z'):
            pass  # load id

    return result if result.is_valid() else None
