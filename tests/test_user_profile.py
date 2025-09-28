from punnyland.user import UserProfile


def test_user_profile_defaults(temp_home):
    profile = UserProfile()

    assert profile.config_dir.exists()
    assert profile.config_file.parent == profile.config_dir
    assert profile.get_corniness_level() == 3
    assert profile.is_setup_completed() is False


def test_add_to_favorites_is_idempotent(temp_home):
    profile = UserProfile()
    joke = "Why did the scarecrow win an award? Because he was outstanding in his field!"

    first_add = profile.add_to_favorites(joke, 3)
    second_add = profile.add_to_favorites(joke, 3)

    assert first_add is True
    assert second_add is False
    assert profile.get_favorites()[0]["joke"] == joke
