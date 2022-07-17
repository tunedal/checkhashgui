from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main
from unittest.mock import Mock

import checkhashgui


class HashCheckTest(TestCase):
    def test_valid_hash_is_ok(self):
        hashes = [
            "f572d396fae9206628714fb2ce00f72e94f2258f",
            "5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03",
            ("e7c22b994c59d9cf2b48e549b1e24666636045930d3da7c1acb299" +
             "d1c3b7f931f94aae41edda2c2b207a36e10f8bcb8d45223e54878f" +
             "5b316e7ce3b6bc019629"),
            "b1946ac92492d2347c6235b4d2611184",
        ]
        for input_hash in hashes:
            with self.subTest(input_hash):
                message = check_hash(b"hello\n", input_hash)
                self.assert_ok(message)

    def test_invalid_hash_is_detected(self):
        hashes = [
            "f572d396fae9206627714fb2ce00f72e94f2258f",
            "5891b5b522d5df186d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03",
            ("e7c22b994c59d9cf2b48c549b1e24666636045930d3da7c1acb299" +
             "d1c3b7f931f94aae41eddb2c2b207a36e10f8bcb8d45223e54878f" +
             "5b316e7ce3b6bc019629"),
            "b1946ac92492d2347c6235b4d2611084",
        ]
        for input_hash in hashes:
            with self.subTest(input_hash):
                message = check_hash(b"hello\n", input_hash)
                self.assert_invalid(message)

    def test_invalid_hash_format_is_detected(self):
        message = check_hash(b"hello\n", "nonsense hash value")
        self.assertIn("ERROR: Unknown hash algorithm", message)
        self.assertNotIn("Kontrollsumman OK av filen", message)
        self.assertNotIn(":-)", message)

    def test_whitespace_in_hash_is_ignored(self):
        input_hash = "\r\nf572d396f ae92066 28714fb2ce00f72e94f2258f\n  \n"
        message = check_hash(b"hello\n", input_hash)
        self.assert_ok(message)

    def test_file_input_error_is_displayed(self):
        message = checkhashgui.check("/tmp/bad/filename/sn3t4ohtu", "a" * 40)
        self.assertIn("No such file or directory", message)
        self.assertNotIn("OK", message)

    def test_all_chunks_for_file_are_processed(self):
        lots_of_data = b"a" * 100_000 + b"\n"
        input_hash = "275eb5b380c47dc2e274f16249ff334f642d4265"
        self.assert_ok(check_hash(lots_of_data, input_hash))
        self.assert_invalid(check_hash(lots_of_data + b"a", input_hash))

    def assert_ok(self, message):
        self.assertIn("Kontrollsumman OK av filen", message)
        self.assertIn(":-)", message)
        self.assertNotIn("VARNING: Felaktig kontrollsumma", message)

    def assert_invalid(self, message):
        self.assertIn("VARNING: Felaktig kontrollsumma", message)
        self.assertNotIn("Kontrollsumman OK av filen", message)
        self.assertNotIn(":-)", message)


class ControllerTest(TestCase):
    def test_shows_about(self):
        view = Mock()
        checkhashgui.MainController(Mock(), view).about()
        message = view.set_text.call_args.args[0]
        self.assertTrue(message.startswith(
            "CHECKHASHGUI - Calculates the checksum"))
        self.assertIn("Copyright (c) 2012-2014 Per Tunedal", message)
        self.assertIn("Copyright (c) 2022 Henrik Tunedal", message)
        self.assertIn("This program is free software", message)


def check_hash(content, input_hash):
    with TemporaryDirectory() as tempdir:
        filename = Path(tempdir) / "test.txt"
        with filename.open("wb") as f:
            f.write(content)
        return checkhashgui.check(str(filename), input_hash + "\n")


if __name__ == "__main__":
    main()
