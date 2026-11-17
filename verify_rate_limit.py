import os
import datetime
import json
import unittest
from main import check_and_increment_query_limit, QUERY_COUNTS_FILE, MAX_DAILY_QUERIES

class TestRateLimit(unittest.TestCase):
    def setUp(self):
        # Save existing file if exists
        self.backup = None
        if os.path.exists(QUERY_COUNTS_FILE):
            with open(QUERY_COUNTS_FILE, "r", encoding="utf-8") as f:
                self.backup = f.read()

    def tearDown(self):
        # Restore backup or remove file
        if self.backup is not None:
            with open(QUERY_COUNTS_FILE, "w", encoding="utf-8") as f:
                f.write(self.backup)
        elif os.path.exists(QUERY_COUNTS_FILE):
            os.remove(QUERY_COUNTS_FILE)

    def test_five_queries_limit(self):
        test_user = "test_user_rate_limit_123"
        today_str = datetime.datetime.now().strftime("%Y-%m-%d")

        # Clear test_user if present
        if os.path.exists(QUERY_COUNTS_FILE):
            with open(QUERY_COUNTS_FILE, "r", encoding="utf-8") as f:
                counts = json.load(f)
            if today_str in counts and test_user in counts[today_str]:
                del counts[today_str][test_user]
                with open(QUERY_COUNTS_FILE, "w", encoding="utf-8") as f:
                    json.dump(counts, f)

        # 1st to 5th queries should succeed
        for i in range(1, 6):
            is_allowed, remaining = check_and_increment_query_limit(test_user)
            self.assertTrue(is_allowed, f"Query {i} should be allowed")
            self.assertEqual(remaining, 5 - i, f"Remaining should be {5 - i} after query {i}")

        # 6th query should be blocked
        is_allowed, remaining = check_and_increment_query_limit(test_user)
        self.assertFalse(is_allowed, "6th query should be blocked")
        self.assertEqual(remaining, 0, "Remaining should be 0 when blocked")

        print("SUCCESS: 5 queries per user per day limit verified successfully!")

if __name__ == "__main__":
    unittest.main()
