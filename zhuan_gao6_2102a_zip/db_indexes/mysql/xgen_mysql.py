from util_mysql import enqueue, get_sorted_by_key
import pymysql

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

    """
    CREATE TABLE test_table001 LIKE dialog_out;
    """

    N_UNIT = 1000
    N_USERS = 20
    for i in range(315, 352):  # next 300
        print(i)
        for j in range(N_UNIT):
            xorder = i * N_UNIT + j
            xorder_user = xorder % N_USERS
            xvalue = f'第{xorder}条数据'
            xuser = f'u{xorder_user:03d}'
            enqueue(db, 'test_table001', xuser, xorder, xvalue)
    print('Data generation done.')
