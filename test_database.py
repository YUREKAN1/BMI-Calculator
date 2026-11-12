
import os
import tempfile

from database import DatabaseManager


def run_tests():

    # Use a temporary database for testing
    with tempfile.TemporaryDirectory() as temp_dir:

        db_path = os.path.join(temp_dir, "test_bmi.db")

        db = DatabaseManager(db_path)

        # Test user creation
        user1_id = db.add_user("Yurekan")
        user2_id = db.add_user("Alex")

        print("Users created:", user1_id, user2_id)

        # Test user retrieval
        users = db.get_users()

        print("\nRegistered users:")

        for user in users:
            print(user["name"])

        # Test saving BMI records
        db.save_bmi_record(
            user1_id, 70, 1.75, 22.86
        )

        db.save_bmi_record(
            user1_id, 72, 1.75, 23.51
        )

        db.save_bmi_record(
            user2_id, 85, 1.80, 26.23
        )

        # Test individual history
        history = db.get_bmi_history(user1_id)

        print("\nYurekan's BMI history:")

        for record in history:
            print(
                f"BMI: {record['bmi']} | "
                f"Weight: {record['weight']} kg | "
                f"Date: {record['recorded_at']}"
            )

        # Verify user isolation
        alex_history = db.get_bmi_history(user2_id)

        print("\nAlex's record count:", len(alex_history))

        assert len(history) == 2
        assert len(alex_history) == 1
        assert len(users) == 2

        # Test duplicate user rejection
        try:
            db.add_user("yurekan")

        except ValueError as error:
            print("\nDuplicate validation:", error)

        print("\nAll database tests passed!")


if __name__ == "__main__":
    run_tests()
