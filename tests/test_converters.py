import json
import unittest
from pathlib import Path

from core.registry import (
    ConversionRequest,
    REGISTRY,
    available_targets,
    execute,
)

import converters 

SAMPLES = Path("data_sample")
OUT = Path("/tmp/kilo/converter_tests_out")


class TestAvailableTargets(unittest.TestCase):

    def test_csv_targets(self):
        self.assertEqual(available_targets(Path("x.csv")), [".json"])

    def test_json_targets(self):
        self.assertEqual(available_targets(Path("x.json")), [".csv"])

    def test_txt_targets(self):
        self.assertEqual(available_targets(Path("x.txt")), [".docx"])

    def test_docx_targets(self):
        self.assertEqual(sorted(available_targets(Path("x.docx"))), [".pdf", ".txt"])

    def test_odt_targets(self):
        self.assertEqual(sorted(available_targets(Path("x.odt"))), [".pdf", ".txt"])

    def test_unknown_extension(self):
        self.assertEqual(available_targets(Path("x.xyz")), [])


class TestConversionRequestValidate(unittest.TestCase):

    def setUp(self):
        OUT.mkdir(parents=True, exist_ok=True)

    def test_valid_request(self):
        req = ConversionRequest(SAMPLES / "test.csv", ".json", OUT)
        req.validate()  # nie powinien rzucic wyjatku

    def test_missing_source_file(self):
        req = ConversionRequest(SAMPLES / "nieistnieje.csv", ".json", OUT)
        with self.assertRaises(FileNotFoundError):
            req.validate()

    def test_missing_output_dir(self):
        req = ConversionRequest(SAMPLES / "test.csv", ".json", Path("/tmp/kilo/nieistnieje_dir"))
        with self.assertRaises(NotADirectoryError):
            req.validate()

    def test_unsupported_conversion(self):
        req = ConversionRequest(SAMPLES / "test.csv", ".pdf", OUT)
        with self.assertRaises(ValueError):
            req.validate()


class TestStructuralConverters(unittest.TestCase):

    def setUp(self):
        OUT.mkdir(parents=True, exist_ok=True)

    def test_csv_to_json(self):
        req = ConversionRequest(SAMPLES / "test.csv", ".json", OUT)
        result = execute(req)
        self.assertTrue(result.exists())
        self.assertEqual(result.suffix, ".json")
        with open(result, encoding="utf-8") as f:
            data = json.load(f)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertIn("id", data[0])

    def test_json_to_csv(self):
        json_path = OUT / "test.json"
        req1 = ConversionRequest(SAMPLES / "test.csv", ".json", OUT)
        execute(req1)
        req2 = ConversionRequest(json_path, ".csv", OUT)
        result = execute(req2)
        self.assertTrue(result.exists())
        self.assertEqual(result.suffix, ".csv")
        with open(result, encoding="utf-8") as f:
            content = f.read()
        self.assertIn("id,imie,nazwisko,miasto", content)

    def test_invalid_json_raises(self):
        req = ConversionRequest(SAMPLES / "invalid.json", ".csv", OUT)
        with self.assertRaises(ValueError):
            execute(req)


class TestDocumentConverters(unittest.TestCase):

    def setUp(self):
        OUT.mkdir(parents=True, exist_ok=True)

    def test_txt_to_docx(self):
        req = ConversionRequest(SAMPLES / "test.txt", ".docx", OUT)
        result = execute(req)
        self.assertTrue(result.exists())
        self.assertEqual(result.suffix, ".docx")

    def test_docx_to_txt(self):
        docx_path = OUT / "test.docx"
        req1 = ConversionRequest(SAMPLES / "test.txt", ".docx", OUT)
        execute(req1)
        req2 = ConversionRequest(docx_path, ".txt", OUT)
        result = execute(req2)
        self.assertTrue(result.exists())
        self.assertEqual(result.suffix, ".txt")
        with open(result, encoding="utf-8") as f:
            content = f.read()
        self.assertIn("przykładowy dokument tekstowy", content)


if __name__ == "__main__":
    unittest.main()
