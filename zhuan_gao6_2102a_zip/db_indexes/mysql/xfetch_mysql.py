from util_mysql import enqueue, get_sorted_by_key
import pymysql
import datetime

if '__main__' == __name__:

    # 连接MySQL
    xdb_args = dict(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='rootA1-',
        database='db_bawei',
        charset='utf8'
    )
    db = pymysql.connect(**xdb_args)

    dt1 = datetime.datetime.now()
    print(dt1)

    xrows = get_sorted_by_key(db, 'test_table001', 'u001', limit=20)
    print(xrows)

    dt2 = datetime.datetime.now()
    print(dt2)
    xdelta = dt2 - dt1
    print(xdelta)

    # with-index: 0:00:00.001999
    # with-index: 0:00:00.008000
    # with-index: 0:00:00.007998
    # no-index:   0:00:00.352592
    # no-index:   0:00:00.399999
    # no-index:   0:00:00.396884
