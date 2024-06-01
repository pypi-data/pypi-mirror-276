# -*- coding: utf-8 -*-
import os
import sqlite3
from abc import abstractmethod, ABC

from sqlink.dao import DB_TYPE_SQLITE, DB_TYPE_MYSQL


# ====================================================================================================================
class MetaDatabase(ABC):
    """元数据库类，提供库级的操作。

    由于元编程无法使用代码提示，因此采取继承写法。

    Example:
        @Entity
        @dataclass
        class Student:  # 定义一个数据类
            name: str
            student_id: int = Constraint.auto_primary_key

        @Dao(Student)
        class DaoStudent:  # 定义一个数据访问类

            @Sql("select * from student where student_id=?;")
            def get_student(self, student_id):
                pass

        class Database(MetaDatabase):  # 定义一个数据库类，继承元数据库类
            dao1 = DaoStudent()  # 将各个数据访问类实例化为类中静态变量，集中管理，统一对外。
            dao2 = ...
            dao3 = ...

            def __init__(self):
                super().__init__()
                self.update_db_type("sqlite")  # 声明数据库类型

            def connect(self):
                connection = ...
                self.update_connection(connection)


        db = Database()  # 实例化数据库类，并传入数据库路径
        db.connect()  # 连接数据库
        db.create_tables()  # 创建数据表

    """

    def update_connection(self, connection):
        """设置数据库连接"""
        if not connection:
            raise ValueError(
                "数据库连接异常。"
            )
        self.connection = connection
        self.cursor = self.connection.cursor()
        self._update_cursor()

    def update_db_type(self, db_type: str):
        """设置数据库类型"""
        if db_type not in [DB_TYPE_SQLITE, DB_TYPE_MYSQL]:
            raise ValueError(
                "数据库类型设置错误。"
            )
        self.db_type = db_type
        for dao in self.dao_list:
            dao.update_db_type(self.db_type)

    @abstractmethod
    def connect(self, *args, **kwargs):
        """创建数据库连接connection后，必须再调用update_connection方法"""

    def disconnect(self):
        """断开数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def create_tables(self):
        """当表不存在时，才会创建数据表。因此可以反复调用该方法，而不会产生错误。"""
        for dao in self.dao_list:
            dao.create_table()  # noqa
        self.commit()

    def get_create_table_sql(self) -> list[str]:
        """返回各个entity的建表sql语句"""
        return [dao.get_create_table_sql() for dao in self.dao_list]

    def commit(self):
        """提交事务"""
        self.connection.commit()

    def rollback(self):
        """回滚事务"""
        self.connection.rollback()

    def execute(self, sql: str, args=None):
        """给外部提供的直接执行sql的接口，避免了再调用内部的connection"""
        if args:
            self.cursor.execute(sql, args)
        else:
            self.cursor.execute(sql)

    def _update_cursor(self):
        for dao in self.dao_list:
            dao.update_cursor(cursor=self.cursor)

    def __new__(cls, *args, **kwargs):
        # 获取子类的所有属性
        subclass_attrs = dir(cls)
        # 初步筛选静态变量（不包括方法和特殊属性）
        static_attrs = [attr for attr in subclass_attrs
                        if not callable(getattr(cls, attr)) and not attr.startswith("__")]
        # 根据是否具有entity属性筛选出最终dao属性，以便在类内部可见
        cls.dao_list = [getattr(cls, attr) for attr in static_attrs
                        if hasattr(getattr(cls, attr), "entity")
                        and hasattr(getattr(cls, attr), "update_cursor")]
        return super().__new__(cls)

    def __init__(self):
        self.db_type = None
        self.connection = None
        self.cursor = None


class SqliteDatabase(MetaDatabase):

    def __init__(self):
        super().__init__()
        self.update_db_type("sqlite")

    def connect(self, db_path: str, *args, **kwargs):
        self.__check_path(db_path)
        connection = sqlite3.connect(db_path, *args, **kwargs)
        self.update_connection(connection)

    @staticmethod
    def __check_path(path):
        """检查并确保目录存在"""
        db_folder = os.path.dirname(path)
        if db_folder != '' and not os.path.exists(db_folder):
            os.makedirs(db_folder, exist_ok=True)
