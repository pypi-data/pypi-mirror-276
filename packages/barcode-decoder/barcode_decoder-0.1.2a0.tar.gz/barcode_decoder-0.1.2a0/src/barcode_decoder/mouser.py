import re
from .scanner import CodeType
from .result import Result


def decode_mouser_barcode(code_type: CodeType, barcode):
    if code_type == CodeType.DataMatrix:
        mouser_regexpr = r"(>\[\)>|\[\)>\^)06\][Kk](\d*)\]14K(\d*)]1P([\w\.\-\, ]*)\][Qq](\d*)\]11K(\d*)](4LCN|4LHU|4LPH|4LDE)]1V([\w\/ ]*)(\^d)?"
        mouser_regexpr_compiled = re.compile(mouser_regexpr)
        matched = mouser_regexpr_compiled.match(barcode)
        if matched:
            result = Result(distributor='Mouser',
                            order_number={'number': matched.group(2), 'position': None},
                            mon=matched.group(4),
                            don=None,
                            quantity=float(matched.group(5)),
                            invoice={'position': int(matched.group(3)), 'number': matched.group(6)},
                            LOT=matched.group(3).lstrip('1T').rstrip(']'),
                            date_code=None,
                            manufacturer=matched.group(8))
            return result if result.is_valid() else None
