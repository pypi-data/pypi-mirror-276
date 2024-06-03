from __future__ import annotations

import pytest

from pydepinject import requires  # noqa: E402


@pytest.fixture
def venv_root(tmp_path):
    """Return the root directory for virtual environments."""
    path = tmp_path / "venvs"
    path.mkdir()
    return path


@pytest.mark.parametrize("ephemeral", [True, False], ids=["ephemeral", "non-ephemeral"])
def test_decorator(venv_root, ephemeral):
    assert not list(venv_root.iterdir())

    with pytest.raises(ImportError):
        import six

    @requires("six", venv_root=venv_root, ephemeral=ephemeral)
    def examplefn():
        print("examplefn")
        import six

        assert six.__version__

    examplefn()
    with pytest.raises(ImportError):
        import six

    if ephemeral:
        assert not list(venv_root.iterdir())
    else:
        assert len(list(venv_root.iterdir())) == 1


@pytest.mark.parametrize("ephemeral", [True, False], ids=["ephemeral", "non-ephemeral"])
def test_context_manager(venv_root, ephemeral):
    assert not list(venv_root.iterdir())

    with pytest.raises(ImportError):
        import six

    with requires("six", venv_root=venv_root, ephemeral=ephemeral):
        import six

        assert six.__version__

    with pytest.raises(ImportError):
        import six

    if ephemeral:
        assert not list(venv_root.iterdir())
    else:
        assert len(list(venv_root.iterdir())) == 1


def test_function_call(venv_root):
    assert not list(venv_root.iterdir())

    with pytest.raises(ImportError):
        import six

    requires_instance = requires("six", venv_root=venv_root)
    requires_instance()
    import six

    assert six.__version__
    assert len(list(venv_root.iterdir())) == 1

    requires_instance._deactivate_venv()
    with pytest.raises(ImportError):
        import six


def test_no_installs(venv_root):
    assert not list(venv_root.iterdir())

    @requires("pytest", venv_root=venv_root, ephemeral=False)
    def examplefn():
        print("examplefn")

    examplefn()
    assert not list(venv_root.iterdir())


def test_reuse_venv(venv_root):
    assert not list(venv_root.iterdir())

    @requires("six", venv_root=venv_root, ephemeral=False)
    def examplea():
        import six

        assert six.__version__
        examplea.called = True

    @requires("six", venv_root=venv_root, ephemeral=False)
    def exampleb():
        import six

        assert six.__version__
        global exampleb_called
        exampleb.called = True

    examplea()
    with pytest.raises(ImportError):
        import six

    exampleb()
    with pytest.raises(ImportError):
        import six

    assert examplea.called is exampleb.called is True
    assert len(list(venv_root.iterdir())) == 1


def test_one_venv_multiple_packages(venv_root):
    assert not list(venv_root.iterdir())

    venv_name = "test_one_venv_multiple_packages"

    @requires("six", venv_root=venv_root, venv_name=venv_name, ephemeral=False)
    def examplefn():
        import six

        assert six.__version__

    @requires("pyparsing", venv_root=venv_root, venv_name=venv_name, ephemeral=False)
    def examplefn2():
        import pyparsing

        assert pyparsing.__version__

        import six

        assert six.__version__

    examplefn()
    examplefn2()

    with pytest.raises(ImportError):
        import six
    with pytest.raises(ImportError):
        import pyparsing

    assert len(list(venv_root.iterdir())) == 1
