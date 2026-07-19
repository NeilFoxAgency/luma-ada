import unittest

from startup_config import MissingEnvironmentVariables, require_environment_variables


class RequireEnvironmentVariablesTests(unittest.TestCase):
    def test_returns_trimmed_required_values(self):
        result = require_environment_variables(
            ["GOOGLE_API_KEY", "MAPS_API_KEY"],
            {"GOOGLE_API_KEY": " google-key ", "MAPS_API_KEY": "maps-key"},
        )

        self.assertEqual(
            result,
            {"GOOGLE_API_KEY": "google-key", "MAPS_API_KEY": "maps-key"},
        )

    def test_reports_all_missing_values_in_one_error(self):
        with self.assertRaises(MissingEnvironmentVariables) as context:
            require_environment_variables(
                ["GOOGLE_API_KEY", "ELEVENLABS_API_KEY", "MAPS_API_KEY"],
                {"GOOGLE_API_KEY": "", "ELEVENLABS_API_KEY": "   "},
            )

        message = str(context.exception)
        self.assertIn("GOOGLE_API_KEY", message)
        self.assertIn("ELEVENLABS_API_KEY", message)
        self.assertIn("MAPS_API_KEY", message)
        self.assertIn(".env", message)

    def test_does_not_require_unrequested_values(self):
        result = require_environment_variables(
            ["GOOGLE_API_KEY"],
            {"GOOGLE_API_KEY": "google-key"},
        )

        self.assertEqual(result, {"GOOGLE_API_KEY": "google-key"})


if __name__ == "__main__":
    unittest.main()
