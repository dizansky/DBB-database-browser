import sqlite3
import mysql.connector
import psycopg2
import json
import os
from typing import List, Dict, Any, Tuple
class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.db_type = None
        self.connection_params = {}
        self.connections_file = 'db_connections.json'
        self.load_connections()
    def load_connections(self):
        if os.path.exists(self.connections_file):
            try:
                with open(self.connections_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    def save_connections(self, connections):
        try:
            with open(self.connections_file, 'w') as f:
                json.dump(connections, f, indent=2)
        except Exception as e:
            print(f"Error saving connections: {e}")
    def connect_sqlite(self, db_path):
        try:
            self.connection = sqlite3.connect(db_path, check_same_thread=False)
            self.db_type = 'sqlite'
            self.connection_params = {'path': db_path}
            return True, "Connected to SQLite"
        except Exception as e:
            return False, str(e)
    def connect_mysql(self, host, user, password, database, port=3306):
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port
            )
            self.db_type = 'mysql'
            self.connection_params = {
                'host': host,
                'user': user,
                'password': password,
                'database': database,
                'port': port
            }
            return True, "Connected to MySQL"
        except Exception as e:
            return False, str(e)
    def connect_postgresql(self, host, user, password, database, port=5432):
        try:
            self.connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port
            )
            self.db_type = 'postgresql'
            self.connection_params = {
                'host': host,
                'user': user,
                'password': password,
                'database': database,
                'port': port
            }
            return True, "Connected to PostgreSQL"
        except Exception as e:
            return False, str(e)
    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self.db_type = None
    def is_connected(self):
        return self.connection is not None
    def get_tables(self) -> List[str]:
        if not self.is_connected():
            return []
        try:
            cursor = self.connection.cursor()
            if self.db_type == 'sqlite':
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            elif self.db_type == 'mysql':
                cursor.execute("SHOW TABLES")
            elif self.db_type == 'postgresql':
                cursor.execute()
            tables = [row[0] for row in cursor.fetchall()]
            cursor.close()
            return tables
        except Exception as e:
            print(f"Error getting tables: {e}")
            return []
    def get_table_structure(self, table_name) -> List[Dict[str, Any]]:
        if not self.is_connected():
            return []
        try:
            cursor = self.connection.cursor()
            if self.db_type == 'sqlite':
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                result = [
                    {
                        'name': col[1],
                        'type': col[2],
                        'null': col[3],
                        'pk': col[5]
                    }
                    for col in columns
                ]
            elif self.db_type == 'mysql':
                cursor.execute(f"DESCRIBE {table_name}")
                columns = cursor.fetchall()
                result = [
                    {
                        'name': col[0],
                        'type': col[1],
                        'null': col[2],
                        'pk': col[3]
                    }
                    for col in columns
                ]
            elif self.db_type == 'postgresql':
                cursor.execute(f"""
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_name='{table_name}'
                """)
                columns = cursor.fetchall()
                result = [
                    {
                        'name': col[0],
                        'type': col[1],
                        'null': '?',
                        'pk': '?'
                    }
                    for col in columns
                ]
            cursor.close()
            return result
        except Exception as e:
            print(f"Error getting table structure: {e}")
            return []
    def get_table_data(self, table_name, limit=100) -> Tuple[List[str], List[Tuple]]:
        if not self.is_connected():
            return [], []
        try:
            cursor = self.connection.cursor()
            query = f"SELECT * FROM {table_name} LIMIT {limit}"
            cursor.execute(query)
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            cursor.close()
            return columns, rows
        except Exception as e:
            print(f"Error getting table data: {e}")
            return [], []
    def execute_query(self, query: str, params: list = None) -> Tuple[bool, Any]:
        if not self.is_connected():
            return False, "Not connected to database"
        try:
            cursor = self.connection.cursor()
            if query.strip().upper().startswith('SELECT'):
                if params:
                    if self.db_type == 'sqlite':
                        cursor.execute(query, params)
                    else:
                        cursor.execute(query, params)
                else:
                    cursor.execute(query)
                columns = [description[0] for description in cursor.description]
                rows = cursor.fetchall()
                cursor.close()
                return True, (columns, rows)
            else:
                if params:
                    if self.db_type == 'sqlite':
                        cursor.execute(query, params)
                    else:
                        cursor.execute(query, params)
                else:
                    cursor.execute(query)
                self.connection.commit()
                affected = cursor.rowcount
                cursor.close()
                return True, f"Query executed. Affected rows: {affected}"
        except Exception as e:
            self.connection.rollback()
            return False, str(e)
    def insert_row(self, table_name: str, data: Dict[str, Any]) -> Tuple[bool, str]:
        if not self.is_connected():
            return False, "Not connected"
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            values = list(data.values())
            if self.db_type == 'sqlite':
                placeholders = ', '.join(['?'] * len(data))
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            print(f"[INSERT] {query}")
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            cursor.close()
            print(f"✅ Row inserted successfully")
            return True, "Row inserted successfully"
        except Exception as e:
            print(f"❌ Insert error: {str(e)}")
            return False, str(e)
    def update_row(self, table_name: str, set_data: Dict[str, Any], where_clause: str) -> Tuple[bool, str]:
        if not self.is_connected():
            return False, "Not connected"
        try:
            if self.db_type == 'sqlite':
                set_clause = ', '.join([f"{k}=?" for k in set_data.keys()])
                values = list(set_data.values())
            else:
                set_clause = ', '.join([f"{k}=%s" for k in set_data.keys()])
                values = list(set_data.values())
            query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
            print(f"[UPDATE] {query}")
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            cursor.close()
            print(f"✅ Row updated successfully")
            return True, "Row updated successfully"
        except Exception as e:
            print(f"❌ Update error: {str(e)}")
            return False, str(e)
    def delete_row(self, table_name: str, where_clause: str) -> Tuple[bool, str]:
        if not self.is_connected():
            return False, "Not connected"
        try:
            query = f"DELETE FROM {table_name} WHERE {where_clause}"
            print(f"[DELETE] {query}")
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            cursor.close()
            print(f"✅ Row deleted successfully")
            return True, "Row deleted successfully"
        except Exception as e:
            print(f"❌ Delete error: {str(e)}")
            return False, str(e)
    def export_to_csv(self, table_name: str, filename: str) -> Tuple[bool, str]:
        try:
            import pandas as pd
            cursor = self.connection.cursor()
            query = f"SELECT * FROM {table_name}"
            cursor.execute(query)
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            cursor.close()
            rows_list = [list(row) if isinstance(row, (list, tuple)) else [row] for row in rows]
            df = pd.DataFrame(rows_list, columns=columns)
            df.to_csv(filename, index=False, encoding='utf-8')
            return True, f"Exported to {filename}"
        except ImportError:
            return False, "pandas library not installed"
        except Exception as e:
            return False, str(e)
    def export_to_excel(self, table_name: str, filename: str) -> Tuple[bool, str]:
        try:
            import pandas as pd
            cursor = self.connection.cursor()
            query = f"SELECT * FROM {table_name}"
            cursor.execute(query)
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            cursor.close()
            rows_list = [list(row) if isinstance(row, (list, tuple)) else [row] for row in rows]
            df = pd.DataFrame(rows_list, columns=columns)
            df.to_excel(filename, index=False, sheet_name='Data')
            return True, f"Exported to {filename}"
        except ImportError as e:
            if 'openpyxl' in str(e):
                return False, "openpyxl library not installed"
            return False, "pandas library not installed"
        except Exception as e:
            return False, str(e)
    def get_row_count(self, table_name: str) -> int:
        if not self.is_connected():
            return 0
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            cursor.close()
            return count
        except:
            return 0
    def escape_value(self, value):
        if value is None:
            return "NULL"
        if isinstance(value, (int, float)):
            return str(value)
        return f"'{str(value).replace(chr(39), chr(39) + chr(39))}'"