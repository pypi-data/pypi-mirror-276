from ezetl.data_models.base_db_table import BaseDBTableModel
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import LONGTEXT


def gen_longtext_column(i):
    if 'nullable' in i.keys():
        i['nullable'] = i['nullable'] == 1
    else:
        i['nullable'] = True
    obj = Column(LONGTEXT, nullable=i['nullable'])
    return obj


class MysqlTableModel(BaseDBTableModel):
    '''
    一个基于 SQLAlchemy 的mysql数据表模型类，并且提供了一些数据库操作的方法
    类中部分参数如下:
    reader.table_name: 表名
    reader.db_engine: SQLAlchemy数据库链接engine实例，可用此对象，执行数据库操作，如查询，执行sql
    reader.db_model: SQLAlchemy数据库对应此表的数据模型实例，可用此对象，执行对表中对象的操作，如增删改查等
    reader.table: SQLAlchemy数据库对应此表的数据表实例，可用此对象，执行对表的操作，如增删改查等
    '''

    def __init__(self, model_info):
        super().__init__(model_info)
        self.column_gen_map = {
            'LONGTEXT': gen_longtext_column
        }

