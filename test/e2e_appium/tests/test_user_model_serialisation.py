"""
Tests for User → TestUser serialisation path.

Validates that user data survives the `User.to_test_data()` →
`TestUser.from_onboarding_result()` conversion that occurs during onboarding.

Covers the data-loss bug described in OXI-48 where `recovery_phrase` /
`seed_phrase` is silently dropped during this conversion.

These tests run without any device or cloud infrastructure.
"""

import pytest

from core.models import TestUser
from models.user_model import User, UserProfile


SEED_PHRASE_12 = "abandon ability able about above absent absorb abstract absurd abuse access accident"


class TestUserToTestUserSerialisation:
    """Round-trip and field-completeness tests for the User → TestUser conversion."""

    @pytest.mark.xfail(
        reason="OXI-48: User.to_test_data() omits recovery_phrase/seed_phrase",
        strict=True,
    )
    def test_user_to_test_user_preserves_seed_phrase(self):
        """Verify seed_phrase/recovery_phrase survives User → dict → TestUser conversion."""
        user = User(
            profile=UserProfile("SeedPhraseUser"),
            recovery_phrase=SEED_PHRASE_12,
        )

        payload = user.to_test_data()
        test_user = TestUser.from_onboarding_result(payload, config=None)

        assert test_user.seed_phrase is not None, (
            "seed_phrase should not be None after round-trip"
        )
        assert len(test_user.seed_phrase) > 0, (
            "seed_phrase should not be empty after round-trip"
        )
        expected_words = SEED_PHRASE_12.split()
        assert test_user.seed_phrase == expected_words, (
            f"Expected {expected_words}, got {test_user.seed_phrase}"
        )

    @pytest.mark.xfail(
        reason="OXI-48: User.to_test_data() omits seed_phrase key",
        strict=True,
    )
    def test_user_to_test_data_includes_all_required_fields(self):
        """Verify to_test_data() includes every field needed by TestUser.from_onboarding_result()."""
        user = User(
            profile=UserProfile("FieldCheckUser"),
            recovery_phrase=SEED_PHRASE_12,
        )
        data = user.to_test_data()

        required_keys = ["display_name", "password", "seed_phrase", "wallet_address"]
        missing = [k for k in required_keys if k not in data]
        assert not missing, f"Missing required key(s): {missing}"

    def test_to_test_data_preserves_display_name(self):
        """Verify display_name round-trips through both models."""
        user = User(profile=UserProfile("DisplayNameUser"))
        payload = user.to_test_data()
        test_user = TestUser.from_onboarding_result(payload, config=None)

        assert test_user.display_name == "DisplayNameUser"

    def test_to_test_data_preserves_password(self):
        """Verify password round-trips through both models."""
        user = User(
            profile=UserProfile("PasswordUser"),
            password="MyStrongPass1!",
        )
        payload = user.to_test_data()
        test_user = TestUser.from_onboarding_result(payload, config=None)

        assert test_user.password == "MyStrongPass1!"

    def test_to_test_data_preserves_wallet_address(self):
        """Verify wallet_address round-trips through both models."""
        user = User(profile=UserProfile("WalletUser"))
        payload = user.to_test_data()
        test_user = TestUser.from_onboarding_result(payload, config=None)

        assert test_user.wallet_address == payload["wallet_address"]
        assert test_user.wallet_address is not None

    def test_from_onboarding_result_source_is_onboarded(self):
        """Verify TestUser created via from_onboarding_result has source='onboarded'."""
        user = User(profile=UserProfile("SourceUser"))
        payload = user.to_test_data()
        test_user = TestUser.from_onboarding_result(payload, config=None)

        assert test_user.source == "onboarded"

    def test_from_onboarding_result_with_string_seed_phrase(self):
        """Verify from_onboarding_result splits a string seed_phrase into a word list."""
        payload = {
            "display_name": "SplitTest",
            "password": "Pass123!word",
            "seed_phrase": SEED_PHRASE_12,
            "wallet_address": "0x" + "ab" * 20,
        }
        test_user = TestUser.from_onboarding_result(payload, config=None)

        assert isinstance(test_user.seed_phrase, list)
        assert len(test_user.seed_phrase) == 12

    def test_from_onboarding_result_with_list_seed_phrase(self):
        """Verify from_onboarding_result accepts a list seed_phrase directly."""
        words = SEED_PHRASE_12.split()
        payload = {
            "display_name": "ListTest",
            "password": "Pass123!word",
            "seed_phrase": words,
            "wallet_address": "0x" + "cd" * 20,
        }
        test_user = TestUser.from_onboarding_result(payload, config=None)

        assert test_user.seed_phrase == words


class TestTestUserDynamicAttributes:
    """Tests for dynamic attribute behaviour on TestUser."""

    def test_profile_link_dynamic_attribute(self):
        """Verify profile_link can be set and read on TestUser."""
        user = TestUser(display_name="DynAttrUser")
        user.profile_link = "https://example.com/profile"

        assert user.profile_link == "https://example.com/profile"

    def test_arbitrary_dynamic_attribute(self):
        """Verify arbitrary attributes can be attached to TestUser instances."""
        user = TestUser(display_name="ArbitraryAttr")
        user.custom_field = 42

        assert user.custom_field == 42

    def test_to_dict_does_not_include_dynamic_attributes(self):
        """Verify to_dict() only contains the declared dataclass fields."""
        user = TestUser(display_name="DictTest")
        user.profile_link = "https://example.com"

        data = user.to_dict()
        assert "profile_link" not in data
        assert "display_name" in data
