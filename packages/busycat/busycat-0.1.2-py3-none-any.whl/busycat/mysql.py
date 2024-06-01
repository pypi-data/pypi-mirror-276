import pymysql
import json
import time
from typing import List, Dict, Any, Tuple, Union


class MySQLConnect:
    def __init__(self, host: str, user: str, pwd: str, db_name: str, port: int = 3306, max_retries: int = 5,
                 retry_delay: int = 5):
        self.host = host
        self.user = user
        self.password = pwd
        self.db_name = db_name
        self.port = port
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.db = None
        self.cursor = None
        self.connect()

    def connect(self):
        retries = 0
        while retries < self.max_retries:
            try:
                self.db = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.db_name,
                    port=self.port
                )
                self.cursor = self.db.cursor()
                print("Connected to the database successfully")
                break
            except pymysql.MySQLError as e:
                retries += 1
                print(f"Connection failed ({retries}/{self.max_retries}), retrying in {self.retry_delay} seconds...")
                time.sleep(self.retry_delay)
        if retries == self.max_retries:
            raise Exception("Maximum retry limit reached, failed to connect to the database")

    def ensure_connection(self):
        if not self.db.open:
            self.connect()

    def trans_to_json(self, description: Tuple, results: List[Tuple]) -> str:
        fields = [field[0] for field in description]
        data = [dict(zip(fields, row)) for row in results]
        json_data = json.dumps(data, default=str)
        return json_data

    def execute(self, sql: str, params: Union[Tuple, List[Tuple]] = None) -> Union[
        List[Dict[str, Any]], Dict[str, Any], bool]:
        self.ensure_connection()
        retries = 0
        while retries < self.max_retries:
            try:
                with self.db.cursor() as cursor:
                    if params:
                        if isinstance(params, list):
                            cursor.executemany(sql, params)
                        else:
                            cursor.execute(sql, params)
                    else:
                        cursor.execute(sql)

                    if sql.strip().lower().startswith("select"):
                        results = cursor.fetchall()
                        description = cursor.description
                        return json.loads(self.trans_to_json(description, results))
                    else:
                        self.db.commit()
                        return True
            except pymysql.MySQLError as e:
                print(f"SQL execution error: {e}")
                if e.args[0] in (2006, 2013, 2014, 2018, 2027):  # Lost connection or server gone away
                    print("Attempting to reconnect...")
                    self.connect()
                    retries += 1
                else:
                    self.db.rollback()
                    return False
        raise Exception("Maximum retry limit reached, failed to execute the query")

    def quit(self) -> None:
        try:
            self.cursor.close()
            self.db.close()
        except pymysql.MySQLError as e:
            print(f"Error closing connection: {e}")

