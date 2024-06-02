import unittest
from src.barcode_decoder.digi_key import decode_digi_key_barcode
from src.barcode_decoder.scanner import CodeType


class TestDigiKeyBarcodeDecoder(unittest.TestCase):
    def test_datamatrix_string_decode(self):
        str1 = (']d1[)>^06]pSAM14954CT-ND]1PLSHM-110-01-L-DH-A-S-K-TR]kPO22000140]1K74797379]10K88169536]11K1]4LCR]Q3]11ZPICK]12Z9597381]13Z213254]20Z0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
        decoded = decode_digi_key_barcode(CodeType.DataMatrix, str1.upper())
        self.assertEqual(decoded.distributor, "DigiKey")
        self.assertEqual(decoded.order_number['number'], 'PO22000140')
        self.assertEqual(decoded.invoice, None)
        self.assertEqual(decoded.don, 'SAM14954CT-ND')
        self.assertEqual(decoded.mon, 'LSHM-110-01-L-DH-A-S-K-TR')
        self.assertEqual(decoded.quantity, 3)
        self.assertEqual(decoded.LOT, None)
        self.assertEqual(decoded.date_code, None)
        self.assertEqual(decoded.manufacturer, None)


if __name__ == '__main__':
    unittest.main()
