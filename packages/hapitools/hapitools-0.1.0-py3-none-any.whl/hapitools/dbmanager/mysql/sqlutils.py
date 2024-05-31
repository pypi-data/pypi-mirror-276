class SqlUtils:
    def __init__(self):
        self._sql = ''
        self._has_set_value = False

    def select(self, columns='*'):
        self._sql += f"SELECT {columns}"
        return self

    def update(self, table):
        self._sql += f'UPDATE {table}'
        return self

    def insert(self, table, values_dict):
        columns = []
        values = []
        for key in values_dict:
            columns.append(key)
            values.append(str(self._formate_value(values_dict.get(key))))
        c = ','.join(columns)
        v = ','.join(values)
        self._sql += f'INSERT INTO {table}({c}) VALUES({v})'
        return self

    def insert_ignore(self, table, values_dict):
        columns = []
        values = []
        for key in values_dict:
            columns.append(key)
            values.append(str(self._formate_value(values_dict.get(key))))
        c = ','.join(columns)
        v = ','.join(values)
        self._sql += f'INSERT IGNORE INTO {table}({c}) VALUES({v})'
        return self

    def table(self, table):
        self._sql += f" FROM {table}"
        return self

    def where(self):
        self._sql += f" WHERE"
        return self

    def c_and(self):
        self._sql += f" AND"
        return self

    def c_or(self):
        self._sql += f" OR"
        return self

    def equals(self, column, value):
        self._sql += f" `{column}`={self._formate_value(value)}"
        return self

    def not_equals(self, column, value):
        self._sql += f" `{column}` != {self._formate_value(value)}"
        return self

    def c_in(self, column, lst):
        self._sql += f" `{column}` IN {lst}"
        return self

    def is_null(self, column):
        self._sql += f" `{column}` IS NULL"
        return self

    def is_not_null(self, column):
        self._sql += f" `{column}` IS NOT NULL"
        return self

    def le(self, column, value):
        self._sql += f" `{column}` <= {self._formate_value(value)}"
        return self

    def lt(self, column, value):
        self._sql += f" `{column}` < {self._formate_value(value)}"
        return self

    def ge(self, column, value):
        self._sql += f" `{column}` >= {self._formate_value(value)}"
        return self

    def gt(self, column, value):
        self._sql += f" `{column}` > {self._formate_value(value)}"
        return self

    def set_value(self, column, value):
        if self._has_set_value:
            self._sql += f', `{column}`={self._formate_value(value)}'
        else:
            self._sql += f' set `{column}`={self._formate_value(value)}'
            self._has_set_value = True
        return self

    def build(self):
        return self._sql

    def _formate_value(self, value):
        if type(value) is str:
            return f"\'{value}\'"
        else:
            return value


if __name__ == '__main__':
    sql = SqlUtils().select().table("user").where().equals("name", "a").c_and().equals("id", 1).build()
    print(sql)
