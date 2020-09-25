"""
    建立查询字典, 将字典内容保存在数据库
"""
import pymysql


def create():
    # 1. 建立数据库链接
    db = pymysql.connect(
        user='root',
        password='123456',
        database='elect_dict',
        charset='utf8',
    )
    # 创建数据库游标
    cur = db.cursor()

    # 2. 将文件读取出来整理成列表格式（单词, 含义）
    list_dict = []
    with open("dict.txt") as file:
        for line in file:
            line_data = line.split(' ', maxsplit=1)
            word = line_data[0]
            meaning = line_data[1].lstrip()
            list_dict.append((word, meaning))

    # 3. 写入数据库操作
    print(list_dict[-1])
    sql = 'insert into words values (%s, %s)'
    cur.executemany(sql, list_dict)
    cur.close()
    db.commit()
    db.rollback()
    db.close()


def main():
    create()


if __name__ == '__main__':
    main()
