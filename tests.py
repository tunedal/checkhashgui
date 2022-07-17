from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main
from unittest.mock import Mock

from checkhashgui import check


class HashCheckTest(TestCase):
    def test_valid_sha1_is_ok(self):
        input_hash = "f572d396fae9206628714fb2ce00f72e94f2258f"
        message = check_hash(b"hello\n", input_hash)
        self.assert_ok(message)

    def test_invalid_sha1_is_detected(self):
        input_hash = "f572d396fae9206628714fb2ce00f72e94f2358f"
        message = check_hash(b"hello\n", input_hash)
        self.assert_invalid(message)

    def assert_ok(self, message):
        self.assertIn("Kontrollsumman OK av filen", message)
        self.assertIn(":-)", message)
        self.assertNotIn("VARNING: Felaktig kontrollsumma", message)

    def assert_invalid(self, message):
        self.assertIn("VARNING: Felaktig kontrollsumma", message)
        self.assertNotIn("Kontrollsumman OK av filen", message)
        self.assertNotIn(":-)", message)


def check_hash(content, input_hash):
    view = Mock()
    with TemporaryDirectory() as tempdir:
        filename = Path(tempdir) / "test.txt"
        with filename.open("wb") as f:
            f.write(content)
        check(str(filename), input_hash + "\n", view)
    return view.set_text.call_args.args[0]


if __name__ == "__main__":
    main()
