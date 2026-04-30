from backend.api.avatar_vocab import DEFAULT_VOCAB, fingerspell


def test_vocabulary_size_and_uniqueness():
    assert len(DEFAULT_VOCAB) >= 120
    assert len(set(DEFAULT_VOCAB)) == len(DEFAULT_VOCAB)


def test_fingerspell_basic():
    assert fingerspell("Saif") == ["FS-S", "FS-A", "FS-I", "FS-F"]


def test_fingerspell_strips_punctuation():
    assert fingerspell("Lahore!") == ["FS-L", "FS-A", "FS-H", "FS-O", "FS-R", "FS-E"]


def test_fingerspell_empty():
    assert fingerspell("!!!") == []
