from click.testing import CliRunner


def test_cli_help_succeeds(cli_module):
    runner = CliRunner()
    result = runner.invoke(cli_module.main, ["--help"])

    assert result.exit_code == 0
    assert "punnyland" in result.output.lower()


def test_cli_joke_command_runs(monkeypatch, cli_module):
    runner = CliRunner()
    monkeypatch.setattr(cli_module.click, "confirm", lambda *_, **__: False)
    monkeypatch.setattr(cli_module.time, "sleep", lambda *_: None)
    result = runner.invoke(cli_module.main, ["joke", "--level", "3"])

    assert result.exit_code == 0
    assert "=" in result.output


def test_daily_command_marks_seen(monkeypatch, cli_module):
    runner = CliRunner()
    monkeypatch.setattr(cli_module.time, "sleep", lambda *_: None)

    first = runner.invoke(cli_module.main, ["daily"])
    assert first.exit_code == 0

    second = runner.invoke(cli_module.main, ["daily"])
    assert "already heard today's joke" in second.output


def test_random_command_updates_history(monkeypatch, cli_module):
    runner = CliRunner()
    monkeypatch.setattr(cli_module.time, "sleep", lambda *_: None)

    result = runner.invoke(cli_module.main, ["random"])

    assert result.exit_code == 0
    assert cli_module.user_profile.get_total_jokes_heard() == 1


def test_favorites_command_removes_entry(monkeypatch, cli_module):
    profile = cli_module.user_profile
    profile.add_to_favorites("Mock joke", 3)

    monkeypatch.setattr(cli_module.click, "confirm", lambda *_, **__: True)
    monkeypatch.setattr(cli_module.click, "prompt", lambda *_, **__: 1)

    runner = CliRunner()
    result = runner.invoke(cli_module.main, ["favorites"])

    assert result.exit_code == 0
    assert not profile.get_favorites()
    assert "removed" in result.output.lower()


def test_stats_command_reports_counts(cli_module):
    profile = cli_module.user_profile
    profile.add_joke_to_history("A counted joke", 2)
    profile.add_to_favorites("Favorite joke", 4)

    runner = CliRunner()
    result = runner.invoke(cli_module.main, ["stats"])

    assert result.exit_code == 0
    assert "total jokes heard" in result.output.lower()
    assert "favorite jokes" in result.output.lower()


def test_search_command_finds_results(cli_module):
    runner = CliRunner()
    result = runner.invoke(cli_module.main, ["search", "scarecrow"])

    assert result.exit_code == 0
    assert "found" in result.output.lower()


def test_settings_command_updates_level(monkeypatch, cli_module):
    responses = iter([1, 5, 4])

    def fake_prompt(*_, **__):
        try:
            return next(responses)
        except StopIteration:
            return 4

    monkeypatch.setattr(cli_module.click, "prompt", fake_prompt)
    monkeypatch.setattr("builtins.input", lambda *_, **__: "")
    monkeypatch.setattr(cli_module.time, "sleep", lambda *_: None)
    monkeypatch.setattr(cli_module, "show_corniness_scale", lambda: None)
    monkeypatch.setattr(cli_module, "show_settings_panel", lambda *_, **__: None)

    runner = CliRunner()
    result = runner.invoke(cli_module.main, ["settings"])

    assert result.exit_code == 0
    assert cli_module.user_profile.get_corniness_level() == 5

