"""Tests for the onboarding analytics acceptance path.

Covers OXI-59: No E2E test exercises the 'accept analytics sharing' path
during onboarding. All existing tests only call skip_analytics_sharing().
"""

import pytest

from fixtures.onboarding_fixture import OnboardingConfig
from utils.multi_device_helpers import StepMixin


@pytest.mark.onboarding
@pytest.mark.raw_devices
class TestOnboardingAnalyticsAccept(StepMixin):
    """Verifies onboarding completes when the user accepts analytics sharing.

    Existing tests only exercise the 'Not now' (skip) path on the analytics
    consent screen.  This class covers the 'Share usage data' (accept) path
    using the OnboardingFlow fixture with skip_analytics=False.
    """

    async def test_onboarding_with_analytics_accepted(self, onboarding_flow_factory):
        """Complete onboarding flow with analytics sharing accepted.

        Steps:
            1. Launch app, navigate to Welcome screen
            2. Click 'Create Profile'
            3. Accept analytics sharing ('Share usage data')
            4. Complete profile creation, password, biometrics, loading
            5. Verify wallet landing screen is visible
        """
        driver = self.device.driver

        config = OnboardingConfig(
            skip_analytics=False,
            validate_each_step=True,
        )
        flow = onboarding_flow_factory(config, driver=driver)

        async with self.step(self.device, "Execute onboarding with analytics accepted"):
            result = flow.execute_complete_flow()

        async with self.step(self.device, "Verify onboarding success"):
            assert result["success"], "Onboarding flow should complete successfully"

        async with self.step(self.device, "Verify analytics acceptance was recorded"):
            analytics_result = result["step_results"]["analytics_screen"]
            assert analytics_result["action"] == "shared", (
                f"Expected analytics action 'shared', got '{analytics_result['action']}'"
            )
