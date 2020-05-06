from loguru import logger
import sqlite3
import io


class DataBase:

    def __init__(self, data_base):
        self.db = data_base

    def open_connection(self):

        try:
            conn = sqlite3.connect(self.db)
            return conn
        except Exception as e:
            logger.error('Open connection: {}'.format(e))

    def create_data_base(self):
        try:
            conn = sqlite3.connect(self.db)
            conn.close()
            logger.success('Data base created')
        except Exception as e:
            logger.error(e)

    def execute_sql(self, sql):

        try:
            conn = self.open_connection()

            cursor = conn.cursor()

            cursor.execute(sql)

            logger.success('run with success')

            conn.commit()

            conn.close()
        except Exception as e:
            logger.error('Create table: {}'.format(e))

    def consult(self, sql):

        try:
            conn = self.open_connection()

            cursor = conn.cursor()

            cursor.execute(sql)

            cache = cursor.fetchall()

            conn.close()

            if len(cache) > 0:
                return cache

            return None

        except Exception as e:
            logger.error('Consult: {}'.format(e))

    def backup(self, name):

        try:
            conn = self.open_connection()

            with io.open('{}.sql'.format(name), 'w') as f:
                for row in conn.iterdump():
                    f.write('%s\n' % row)

            logger.success('Backup created')
            conn.close()
        except Exception as e:
            logger.error('Bakcup: {}'.format(e))
