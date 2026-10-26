"""Offline smoke tests, with no device/network connections."""
import importlib.util
import os
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load_script():
    spec = importlib.util.spec_from_file_location('hikvision_config', ROOT / 'hikvision_config.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class OfflineSafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ.pop('HIKVISION_AUTHORIZE_DEVICE_ACCESS', None)
        os.environ.pop('HIKVISION_DRY_RUN', None)
        cls.app = load_script()

    def test_write_authorization_gate(self):
        self.assertEqual(self.app.main(), 2)
        self.assertTrue(self.app.DRY_RUN)

    def test_example_inventory_can_be_loaded(self):
        rows = self.app.read_excel_devices(ROOT / 'examples' / 'devices.example.xlsx')
        self.assertEqual(len(rows), 3)
        self.assertTrue(all(row['Site ID'] == 'DEMO-001' for row in rows))

    def test_certificate_subject_has_placeholders_not_real_identity(self):
        row = {'Hostname': 'EXAMPLE-CAM', 'Current IP': '192.0.2.11'}
        for fn in (self.app.build_camera_self_signed_cert_xml,
                   self.app.build_nvr_cert_sign_req_xml,
                   self.app.build_camera_csr_xml,
                   self.app.build_nvr_csr_xml):
            _, xml = fn(row)
            self.assertIn('<organizationName>Example Organization</organizationName>', xml)
            self.assertIn('<email>operator@example.invalid</email>', xml)
            self.assertIn('<commonName>EXAMPLE-CAM</commonName>', xml)

    def test_credential_input_is_not_embedded_in_python(self):
        source = (ROOT / 'hikvision_config.py').read_text(encoding='utf-8')
        self.assertNotIn('C:'+chr(92)+'Users'+chr(92), source)
        self.assertIn('HIKVISION_DEVICES_EXCEL', source)
        self.assertIn('HIKVISION_IMPORT_KDF_SUFFIX', source)


if __name__ == '__main__':
    unittest.main()
