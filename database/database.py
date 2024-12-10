import psycopg2
from config import DB_USER, DB_HOST, DB_NAME, DB_PASSWORD
from datetime import datetime
# зачем нам chat_id в частозадаваемых

class DataBase:
    def __init__(self):
        self.database = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )

    def manager(self, sql, *args,
                fetchone: bool = False,
                fetchall: bool = False,
                fetchmany: bool = False,
                commit: bool = False):
        with self.database as db:
            with db.cursor() as cursor:
                cursor.execute(sql, args)
                if commit:
                    result = db.commit()
                elif fetchone:
                    result = cursor.fetchone()
                elif fetchall:
                    result = cursor.fetchall()
                elif fetchmany:
                    result = cursor.fetchmany()
            return result


class TableCreator(DataBase):
    def create_user_table(self):
        sql = """
            DROP TABLE IF EXISTS users;
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                first_name TEXT NOT NULL,
                second_name TEXT NOT NULL,
                third_name TEXT NOT NULL,
                us_group TEXT NOT NULL,
                username TEXT NOT NULL,
                administrator BOOLEAN DEFAULT false,
                chat_id BIGINT NOT NULL UNIQUE
            );
        """
        self.manager(sql, commit=True)

    def create_static_question_table(self):
        sql = """
            DROP TABLE IF EXISTS static_questions;
            CREATE TABLE IF NOT EXISTS static_questions (
                static_question_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                answer TEXT NOT NULL
            ); 
        """
        self.manager(sql, commit=True)

    def create_dynamic_question_table(self):
        sql = """
            DROP TABLE IF EXISTS dynamic_questions;
            CREATE TABLE IF NOT EXISTS dynamic_questions (
                dynamic_question_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                student_name TEXT NOT NULL,
                student_group TEXT NOT NULL,
                description TEXT NOT NULL,
                student_username TEXT NOT NULL,
                student_chat_id TEXT NOT NULL,
                answer BOOLEAN DEFAULT false
            );
        """
        self.manager(sql, commit=True)


class UserManager(DataBase):
    def get_is_user_administrator(self, chat_id):
        sql = """
            SELECT administrator FROM users 
            WHERE chat_id = %s;
        """
        return self.manager(sql, chat_id, fetchone=True)

    def user_exists(self, chat_id):
        sql = """
        SELECT 1 FROM users WHERE chat_id = %s;
        """
        return self.manager(sql, chat_id, fetchone=True)

    def add_user(self, first_name, second_name, third_name, us_group, username, chat_id):
        sql = """
               INSERT INTO users(first_name, second_name, third_name, us_group, username, chat_id)
               VALUES (%s, %s, %s, %s, %s, %s);
           """
        self.manager(sql, first_name, second_name, third_name, us_group, username, chat_id, commit=True)


class StaticQuestionManager(DataBase):
    def get_static_question_category(self):
        sql = """
            SELECT category FROM static_questions;
        """
        return self.manager(sql, fetchall=True)

    def get_all_static_question_by_category(self, category):
        sql = """
            SELECT * FROM static_questions
            WHERE category = 'first_category';
        """
        return self.manager(sql, fetchall=True)


class DynamicQuestionManager(DataBase):
    def add_dynamic_question(self, student_name, student_group, description, student_username, student_chat_id):
        sql = """
            INSERT INTO dynamic_questions(student_name, student_group, description, student_username, student_chat_id)
            VALUES (%s, %s, %s, %s, %s);
        """
        self.manager(sql, student_name, student_group, description, student_username, student_chat_id, commit=True)

    def get_has_dynamic_question(self):
        sql = """
            SELECT student_name, student_group, description, student_username, student_chat_id FROM dynamic_questions
            WHERE answer = false;
        """
        return self.manager(sql, fetchall=True)


class MainManager:
    def __init__(self):
        self.user: UserManager = UserManager()
        self.static_question: StaticQuestionManager = StaticQuestionManager()
        self.dynamic_question: DynamicQuestionManager = DynamicQuestionManager()


creator = TableCreator()
# creator.create_user_table()
# creator.create_static_question_table()
# creator.create_dynamic_question_table()
