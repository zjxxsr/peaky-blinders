from common import USER, KEY, VALUE
import time
import pymysql
import copy


def enqueue(db, tbl_name, user, key, value):
    """
    入队
    :param db: mysql实例
    :param tbl_name: 表名
    :param user: 用户名
    :param key: 键（除了配置表conf，一般都是纳秒时间戳）
    :param value: 值 （如果是dict则按key-value插入值，如果不是dict则用键名'value'插入。）
    :return: None
    """
    mysql_upsert(db, tbl_name, user, key, value)
    
    
def mysql_upsert(db, tbl_name, user, key, value):
    """
    upsert = update or insert
    有数据则更新，无则插入。
    :param db: mysql实例
    :param tbl_name: 表名
    :param user: 用户名
    :param key: 键（一般都是纳秒时间戳）
    :param value: 值 （如果是dict则按key-value插入值，如果不是dict则用键名'value'插入。）
    :return: int 影响的行数
    """
    xrow = mysql_get_one(db, tbl_name, user, key)
    if xrow is None:
        cnt = mysql_insert_one(db, tbl_name, user, key, value)
        return cnt
    cnt = mysql_update_one(db, tbl_name, user, key, value)
    return cnt


def escape(db, xstr):
    """
    https://stackoverflow.com/questions/3617052/escape-string-python-for-mysql
    https://mysql-python.sourceforge.net/MySQLdb.html
    :param db: mysql实例
    :param xstr: string或可以转为string的对象
    :return: escaped string in mysql
    """
    xstr = str(xstr)
    xstr = db.escape_string(xstr)
    return xstr


def mysql_get_one(db, tbl_name, user, key):
    tbl_name = escape(db, tbl_name)
    user = escape(db, user)
    key = escape(db, key)
    # https://stackoverflow.com/questions/7268178/python-mysql-and-select-output-to-dictionary-with-column-names-for-keys
    # https://stackoverflow.com/questions/53368579/typeerror-cursor-got-an-unexpected-keyword-argument-dictionary-using-flaske
    with pymysql.cursors.DictCursor(db) as xcursor:
        xsql = f"SELECT * FROM `{tbl_name}` WHERE `user` = '{user}' AND `key` = '{key}' LIMIT 1"
        # print(xsql)
        xcursor.execute(xsql)
        xrows = xcursor.fetchall()
        xrows_len = len(xrows)
        if 0 == xrows_len:
            return None
        else:
            for xrow in xrows:
                xrow['key'] = int(xrow['key'])
                return xrow


def mysql_insert_one(db, tbl_name, user, key, value):
    tbl_name = escape(db, tbl_name)
    user = escape(db, user)
    key = escape(db, key)
    if isinstance(value, dict):
        xkeys = ''
        xvalues = ''
        xfirst = True
        for k, v in value.items():
            k = escape(db, k)
            v = escape(db, v)
            if xfirst:
                xfirst = False
            else:
                xkeys += ', '
                xvalues += ', '
            xkeys += f'`{k}`'
            xvalues += f"'{v}'"
    else:
        xkeys = '`value`'
        xvalues = escape(db, value)
        xvalues = f"'{xvalues}'"
    with db.cursor() as xcursor:
        xgkey = key + ',' + user
        xsql = f"INSERT INTO `{tbl_name}` (`user`, `key`, `gkey`, {xkeys}) VALUES ('{user}', '{key}', '{xgkey}', {xvalues})"
        # print(xsql)
        cnt = xcursor.execute(xsql)
        db.commit()
        return cnt


def mysql_update_one(db, tbl_name, user, key, value):
    tbl_name = escape(db, tbl_name)
    user = escape(db, user)
    key = escape(db, key)
    if isinstance(value, dict):
        xvalues = ''
        xfirst = True
        for k, v in value.items():
            k = escape(db, k)
            v = escape(db, v)
            if xfirst:
                xfirst = False
            else:
                xvalues += ', '
            xvalues += f"`{k}` = '{v}'"
    else:
        value = escape(db, value)
        xvalues = f"`value` = '{value}'"
    with db.cursor() as xcursor:
        xsql = f"UPDATE `{tbl_name}` set {xvalues} WHERE `user` = '{user}' AND `key` = '{key}' LIMIT 1"
        print(xsql)
        cnt = xcursor.execute(xsql)
        db.commit()
        return cnt


def get_sorted_by_key(db, tbl_name, user, limit=None, is_keep_others=True):
    tbl_name = escape(db, tbl_name)
    user = escape(db, user)
    if limit is None:
        xlimit = ""
    else:
        limit = int(limit)
        xlimit = f" LIMIT {limit} "
    # https://stackoverflow.com/questions/7268178/python-mysql-and-select-output-to-dictionary-with-column-names-for-keys
    # https://stackoverflow.com/questions/53368579/typeerror-cursor-got-an-unexpected-keyword-argument-dictionary-using-flaske
    with pymysql.cursors.DictCursor(db) as xcursor:
        xsql = f"SELECT * FROM `{tbl_name}` WHERE `user` = '{user}' ORDER BY `key` DESC {xlimit}"
        print(xsql)
        xcursor.execute(xsql)
        xrows_list = xcursor.fetchall()
        xrows = []
        for xdict in xrows_list:
            xdict['key'] = int(xdict['key'])
            xrows.append(xdict)
        xrows_len = len(xrows)
        if 0 == xrows_len:
            return []
        else:
            if is_keep_others:
                return xrows
            last_key = xrows[-1]['key']
            xsql = f"DELETE FROM `{tbl_name}` WHERE `user` = '{user}' AND `key` < '{last_key}'"
            print(xsql)
            cnt = xcursor.execute(xsql)
            db.commit()
            return xrows


if '__main__' == __name__:

    def _main():
        xdb_args = dict(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='rootA1-',
            database='db_bawei',
            charset='utf8'
        )

        db = pymysql.connect(**xdb_args)

        for i in range(5):
            ts = time.time_ns()
            enqueue(db, 'dialog_out', 'u1234xxxx', ts, {
                VALUE: f'聊天记录00{i}',
                'io': 'o',
            })

        xres = get_sorted_by_key(db, 'dialog_out', 'u1234xxxx', limit=3, is_keep_others=False)
        print(xres)

    _main()
