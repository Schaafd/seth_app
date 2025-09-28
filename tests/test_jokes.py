from punnyland.jokes import JokeManager


def test_jokes_load_from_json():
    manager = JokeManager()
    jokes_per_level = manager.get_jokes_count()

    assert jokes_per_level  # at least one level
    assert all(level in range(1, 6) for level in jokes_per_level)
    assert all(count > 0 for count in jokes_per_level.values())


def test_random_joke_respects_level_bounds():
    manager = JokeManager()
    joke, level = manager.get_random_joke()

    assert manager.validate_corniness_level(level)
    assert isinstance(joke, str)
    assert joke
