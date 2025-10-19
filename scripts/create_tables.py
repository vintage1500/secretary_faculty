"""Create database tables for the project.

This script uses the TableCreator in `database/database.py` which contains
DROP TABLE IF EXISTS ... and CREATE TABLE statements. Run this locally
with your virtual environment active.

WARNING: The TableCreator SQL statements DROP tables before creating them.
If you have production data, back it up first.
"""
from database.database import TableCreator


def main():
    creator = TableCreator()
    print("Creating tables (these operations will DROP existing tables if present)...")

    # Order matters because of foreign key dependencies
    creator.create_user_table()
    creator.create_question_categories()
    creator.create_question_subcategories()
    creator.create_static_question_table()
    creator.create_dynamic_question_table()

    print("All tables created.")


if __name__ == "__main__":
    main()
