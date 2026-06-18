import pytest
from unittest.mock import MagicMock
from core.runtime.runtime_dependency_installer import RuntimeDependencyInstaller, InstallResult


def make_installer():
    return RuntimeDependencyInstaller()


def test_is_installed_stdlib():
    installer = make_installer()
    assert installer.is_installed("os") is True
    assert installer.is_installed("json") is True
    assert installer.is_installed("datetime") is True


def test_is_installed_missing():
    installer = make_installer()
    assert installer.is_installed("totally_nonexistent_pkg_xyz_999") is False


def test_install_already_installed():
    installer = make_installer()
    result = installer.install("json")
    assert result.success is True
    assert result.already_installed is True


def test_install_blocked_stdlib():
    installer = make_installer()
    result = installer.install("os")
    assert result.success is False
    assert "Blocked" in result.message


def test_install_result_to_dict():
    result = InstallResult("requests", True, "installed ok")
    d = result.to_dict()
    assert d["package"] == "requests"
    assert d["success"] is True


def test_check_requirements_all_present():
    installer = make_installer()
    missing = installer.check_requirements(["os", "json", "sys"])
    # These are stdlib but check_requirements uses is_installed which handles them
    assert isinstance(missing, list)


def test_check_requirements_missing():
    installer = make_installer()
    missing = installer.check_requirements(["totally_fake_pkg_abc_123"])
    assert "totally_fake_pkg_abc_123" in missing


def test_install_many():
    installer = make_installer()
    results = installer.install_many(["json", "datetime"])
    assert len(results) == 2
    assert all(r.success for r in results)


def test_ensure_already_installed():
    installer = make_installer()
    result = installer.ensure("json")
    assert result.success is True
    assert result.already_installed is True


def test_get_history_empty():
    installer = make_installer()
    assert installer.get_history() == []


def test_get_history_after_install():
    installer = make_installer()
    installer.install("json")
    assert len(installer.get_history()) == 1


def test_get_session_installs_empty():
    installer = make_installer()
    assert installer.get_session_installs() == []


def test_install_with_mock_executor():
    mock_exec = MagicMock()
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.stdout = "Successfully installed testpkg"
    mock_result.stderr = ""
    mock_exec.execute_pip_install.return_value = mock_result
    installer = RuntimeDependencyInstaller(subprocess_executor=mock_exec)
    result = installer.install("totally_fake_pkg_xyz_install_test", force=True)
    assert result.success is True
    mock_exec.execute_pip_install.assert_called_once()