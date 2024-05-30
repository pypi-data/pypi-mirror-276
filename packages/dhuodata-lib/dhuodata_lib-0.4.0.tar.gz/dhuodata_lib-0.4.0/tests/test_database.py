# import unittest
# from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
# from sqlalchemy.orm import sessionmaker
# from dhuolib.repository import DatabaseConnection, GenericRepository  # Adjust this import according to your project structure
# from sqlalchemy import text


# class TestDatabaseConnection(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls):
#         cls.connection_string = 'sqlite:///:memory:'
#         cls.db_connection = DatabaseConnection(cls.connection_string)

#     def test_database_connection_init(self):
#         db_connection = DatabaseConnection(self.connection_string)
#         self.assertIsNotNone(db_connection.engine)
#         self.assertIsNotNone(db_connection.session)

#     def test_session_scope(self):
#         with self.db_connection.session_scope() as session:
#             self.assertIsNotNone(session)


# class TestGenericRepository(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls):
#         cls.connection_string = 'sqlite:///:memory:'
#         cls.db_connection = DatabaseConnection(cls.connection_string)
#         cls.table_name = 'test_table'
#         cls.repo = GenericRepository(cls.db_connection, cls.table_name)
#         cls.repo.create_table(['name VARCHAR(255)', 'age INTEGER'])

#     @classmethod
#     def tearDownClass(cls):
#         with cls.db_connection.session_scope() as session:
#             session.execute(text(f"DROP TABLE IF EXISTS {cls.table_name}"))

#     def setUp(self):
#         self.db_connection = self.__class__.db_connection
#         self.repo = self.__class__.repo
#         self.table_name = self.__class__.table_name

#     def tearDown(self):
#         with self.db_connection.session_scope() as session:
#             session.execute(text(f"DELETE FROM {self.table_name}"))

#     def test_create_table(self):
#         new_repo = GenericRepository(self.db_connection, 'new_table')
#         new_repo.create_table(['description TEXT'])
#         with self.db_connection.session_scope() as session:
#             result = session.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='new_table';")).fetchone()
#             self.assertIsNotNone(result)
#             self.assertEqual(result[0], 'new_table')

#     def test_insert(self):
#         data = {'id': 1, 'name': 'John Doe', 'age': 30}
#         inserted = self.repo.insert(data)
#         with self.repo.db.session_scope() as session:
#             result = session.execute(text(f"SELECT * FROM {self.repo.table_name} WHERE id=1")).fetchone()
#             self.assertIsNotNone(result)
#             self.assertEqual(result.name, 'John Doe')
#             self.assertEqual(result.age, 30)
#             self.assertEqual(inserted.name, 'John Doe')
#             self.assertEqual(inserted.age, 30)

#     def test_get_items_with_pagination(self):
#         for i in range(10):
#             data = {'id': i+1, 'name': f'User {i+1}', 'age': 20 + i}
#             self.repo.insert(data)
        
#         items = self.repo.get_items_with_pagination(1, 5)
#         self.assertEqual(len(items), 5)
#         self.assertEqual(items[0].name, 'User 1')
#         self.assertEqual(items[4].name, 'User 5')

#         items = self.repo.get_items_with_pagination(2, 5)
#         self.assertEqual(len(items), 5)
#         self.assertEqual(items[0].name, 'User 6')
#         self.assertEqual(items[4].name, 'User 10')

#     def test_update(self):
#         data = {'id': 1, 'name': 'John Doe', 'age': 40, 'predict_result': 'Negative'}
#         self.repo.insert(data)
#         updated_data = {'id': 1, 'name': 'John Doe', 'age': 40, 'predict_result': 'Positive'}
#         updated = self.repo.update(updated_data)
#         with self.repo.db.session_scope() as session:
#             result = session.execute(text(f"SELECT * FROM {self.repo.table_name} WHERE id=1")).fetchone()
#             self.assertIsNotNone(result)
#             self.assertEqual(data["predict_result"], 'Negative')
#             self.assertEqual(updated.predict_result, 'Positive')

#     def test_insert_invalid_data(self):
#         invalid_data = {'id': 1, 'invalid_column': 'Invalid Data'}
#         with self.assertRaises(Exception):
#             self.repo.insert(invalid_data)
