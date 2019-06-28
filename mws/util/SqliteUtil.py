import sqlite3
import os


class EasySqlite:
    """
    sqlite数据库操作工具类
    database: 数据库文件地址，例如：db/mydb.db
    """
    _connection = None

    def __init__(self, database=None):
        # 连接数据库
        if database is None:
            print(os.path.dirname(os.path.abspath(__file__)))
            database = os.path.abspath('./data/data.db')
        self._connection = sqlite3.connect(database)

    def _dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def execute(self, sql, args=[], result_dict=True, commit=True) -> list:
        """
        执行数据库操作的通用方法
        Args:
        sql: sql语句
        args: sql参数
        result_dict: 操作结果是否用dict格式返回
        commit: 是否提交事务
        Returns:
        list 列表，例如：
        [{'id': 1, 'name': '张三'}, {'id': 2, 'name': '李四'}]
        """
        if result_dict:
            self._connection.row_factory = self._dict_factory
        else:
            self._connection.row_factory = None
        # 获取游标
        _cursor = self._connection.cursor()
        # 执行SQL获取结果
        _cursor.execute(sql, args)
        if commit:
            self._connection.commit()
        data = _cursor.fetchall()
        _cursor.close()
        return data


if __name__ == '__main__':
    db = EasySqlite('../data/data.db')
    # print(db.execute("select name from sqlite_master where type=?", ['table']))
    # print(db.execute("pragma table_info([user])"))
    # print(execute("insert into user(id, name, password) values (?, ?, ?)", [2, "李四", "123456"]))
    print(db.execute("insert into user values('admin','admin','admin',datetime('now'),datetime('now'))"))
    print(db.execute("select id, nickname userName, pwd pwd from user"))
    print(db.execute("select * from user", result_dict=False))
    print(db.execute("select * from user"))
