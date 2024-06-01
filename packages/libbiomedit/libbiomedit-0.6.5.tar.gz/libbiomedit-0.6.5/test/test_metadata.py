import unittest
from datetime import datetime, timezone, timedelta
from typing import Callable, Sequence, Dict, Any

from libbiomedit.metadata import MetaData, ValidatedStr, HexStr1024, HexStr256, Purpose


class TestMetadata(unittest.TestCase):
    def test_validata_type_meta(self) -> None:
        def check(x: str, y: str) -> Callable[[str], str]:
            def _c(s: str) -> str:
                if not x < s < y:
                    raise ValueError("wrong")
                return s

            return _c

        class T(ValidatedStr):
            validator = check("1", "3")

        self.assertEqual(T("2"), "2")
        with self.assertRaises(ValueError):
            T("3")

    def setUp(self) -> None:
        self.dct = {
            "transfer_id": 42,
            "sender": "A" * 32,
            "recipients": ["B" * 256],
            "timestamp": "2019-10-11T14:50:12+0100",
            "checksum": "A" * 64,
            "checksum_algorithm": "SHA256",
            "compression_algorithm": "gzip",
            "version": MetaData.version,
            "purpose": "PRODUCTION",
        }
        self.metadata = MetaData(
            transfer_id=42,
            sender=HexStr1024("A" * 32),
            recipients=[HexStr1024("B" * 256)],
            timestamp=datetime(
                2019, 10, 11, 14, 50, 12, 0, timezone(timedelta(0, 3600), "CET")
            ),
            checksum=HexStr256("A" * 64),
            purpose=Purpose.PRODUCTION,
        )

    def test_from_dict(self) -> None:
        self.assertEqual(MetaData.from_dict(self.dct), self.metadata)
        # Check medatadata generated with sett v5
        sett_v5_dict = {
            "sender": "14948C167662768AD33C8D2C7DE1E0794C1C000B",
            "recipients": [
                "14948C167662768AD33C8D2C7DE1E0794C1C000B",
                "14948C167662768AD33C8D2C7DE1E0794C1C000A",
            ],
            "checksum": "d7c3094d6ba7d8f31a8950c83f61078ca2"
            "c1b3b7cad6c188e9257a52a1e27411",
            "timestamp": "2024-04-22T12:34:31.208872700Z",
            "version": "0.7.1",
            "checksum_algorithm": "SHA256",
            "compression_algorithm": "zstandard",
            "transfer_id": None,
            "purpose": None,
        }
        sett_v5_metadata = MetaData(
            sender=HexStr1024("14948C167662768AD33C8D2C7DE1E0794C1C000B"),
            recipients=[
                HexStr1024("14948C167662768AD33C8D2C7DE1E0794C1C000B"),
                HexStr1024("14948C167662768AD33C8D2C7DE1E0794C1C000A"),
            ],
            checksum=HexStr256(
                "d7c3094d6ba7d8f31a8950c83f61078ca2c1b3b7cad6c188e9257a52a1e27411"
            ),
            timestamp=datetime(2024, 4, 22, 12, 34, 31, 208872, timezone.utc),
            version="0.7.1",
            checksum_algorithm="SHA256",
            compression_algorithm="zstandard",
            transfer_id=None,
            purpose=None,
        )
        self.assertEqual(MetaData.from_dict(sett_v5_dict), sett_v5_metadata)

        invalid_dicts: Sequence[Dict[str, Any]] = [
            {
                "sender": "A" * 31,
                "recipients": ["B" * 256],
                "timestamp": "2019-10-11T14:50:12+0100",
                "checksum": "A" * 64,
                "version": MetaData.version,
            },
            {
                "transfer_id": 42,
                "sender": "A" * 32,
                "recipients": ["B" * 257],
                "timestamp": "2019-10-11T14:50:12+0100",
                "checksum": "A" * 64,
                "version": MetaData.version,
            },
            {
                "transfer_id": 42,
                "sender": "A" * 32,
                "recipients": ["B" * 256],
                "timestamp": "invalid timestamp",
                "checksum": "A" * 64,
                "version": MetaData.version,
            },
            {
                "transfer_id": 42,
                "sender": "A" * 32,
                "recipients": ["B" * 256],
                "timestamp": "2019-10-11T14:50:12+0100",
                "checksum": "A" * 65,
                "version": MetaData.version,
            },
            {
                "transfer_id": 42,
                "sender": "A" * 32,
                "recipients": ["B" * 256],
                "timestamp": "2019-10-11T14:50:12+0100",
                "checksum": "A" * 65,
                "version": MetaData.version,
                "purpose": "UNKNOWN",
            },
        ]
        for n, dct in enumerate(invalid_dicts):
            with self.subTest(index=n):
                with self.assertRaises(ValueError):
                    MetaData.from_dict(dct)
        dct = {
            "invalid_key": "Demo",
            "transfer_id": 42,
            "sender": "A" * 32,
            "recipients": ["B" * 256],
            "timestamp": "2019-10-11T14:50:12+0100",
            "checksum": "A" * 64,
            "version": MetaData.version,
            "purpose": "TEST",
        }
        with self.assertWarns(UserWarning):
            MetaData.from_dict(dct)

    def test_asdict(self) -> None:
        dct: Dict[str, Any] = {**self.dct, "checksum": "a" * 64}
        self.assertEqual(MetaData.asdict(self.metadata), dct)
