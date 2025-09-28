"""Shared pytest fixtures for Punnyland tests."""

import sys
import importlib
import pytest


@pytest.fixture()
def temp_home(monkeypatch, tmp_path):
    """Point HOME/USERPROFILE at an isolated directory for user data files."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    return tmp_path


@pytest.fixture()
def cli_module(temp_home):
    """Reload the CLI module with the temporary home directory in place."""
    for name in list(sys.modules):
        if name.startswith("punnyland"):
            sys.modules.pop(name)
    cli = importlib.import_module("punnyland.cli")
    cli.user_profile.complete_setup("Test Runner", 3)
    return cli
