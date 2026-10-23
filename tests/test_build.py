import unittest
from scripts.build import normalize, parse


class BuildTests(unittest.TestCase):
    def test_normalize_domain_variants(self):
        self.assertEqual(normalize("+.Video.Example.COM."), "video.example.com")
        self.assertEqual(normalize("DOMAIN-SUFFIX,cdn.example.com"), "cdn.example.com")

    def test_reject_non_domains(self):
        for value in ("", "# note", "1.2.3.4", "10.0.0.0/8", "bad_domain"):
            self.assertIsNone(normalize(value))

    def test_plain(self):
        self.assertEqual(parse("a.example\nA.EXAMPLE\n# x\n", "plain"), {"a.example"})

    def test_clash(self):
        text = "payload:\n  - DOMAIN,video.example\n  - DOMAIN-SUFFIX,cdn.example\n  - IP-CIDR,1.2.3.0/24\n"
        self.assertEqual(parse(text, "clash"), {"video.example", "cdn.example"})


if __name__ == "__main__":
    unittest.main()

