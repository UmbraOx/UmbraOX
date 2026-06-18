from core.runtime.runtime_version import get_version, get_full_version, VERSION, CHANGELOG


def test_version_string():
    assert isinstance(get_version(), str)
    assert "." in get_version()


def test_full_version_contains_umbra():
    assert "UMBRA" in get_full_version()


def test_version_constant():
    assert VERSION == "2.0.0"


def test_changelog_has_current_version():
    assert VERSION in CHANGELOG


def test_changelog_has_entries():
    entries = CHANGELOG[VERSION]
    assert len(entries) > 5


def test_print_version_runs(capsys):
    from core.runtime.runtime_version import print_version
    print_version()
    captured = capsys.readouterr()
    assert "UMBRA" in captured.out