"""
    电子词典数据库处理
        根据服务端的需求进行数据的处理交互
"""
import pymysql


# 创建数据库操作类
class Database:
    def __init__(self):
        self.db = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='123456',
            database='elect_dict',
            charset='utf8'
        )
        self.cur = self.create_cur()

    # 创建游标
    def create_cur(self):
        return self.db.cursor()

    # 关闭数据库
    def close_database(self):
        self.db.close()

    def register(self, name, passwd):
        try:
            sql = "insert into user (name, passwd) values (%s, %s)"
            self.cur.execute(sql, [name, passwd])
            self.db.commit()
            return True
        except:
            self.cur.close()
            self.db.close()
        return False

    def login(self, name, passwd):
        try:
            sql = "select name, passwd from user where name = %s and passwd = %s;"
            self.cur.execute(sql, [name, passwd])
            result = self.cur.fetchone()
            if result:
                return True
        except:
            self.cur.close()
            self.db.close()
        return False

    def query_word(self, word):
        try:
            sql = "select meaning from words where word = %s;"
            self.cur.execute(sql, [word])
            meaning = self.cur.fetchone()[0]
            if meaning:
                return meaning
        except:
            self.cur.close()
            self.db.close()
            return 'Not Found'


    def save_hist(self, word, name):
        # 得到用户的id
        sql1 = "select id from user where name = %s;"
        self.cur.execute(sql1, [name])
        user_id = self.cur.fetchone()[0]
        # 插入历史表中
        sql2 = "insert into hist (word, user_id) values (%s, %s)"
        try:
            self.cur.execute(sql2, [word, user_id])
            self.db.commit()
        except:
            self.db.rollback()



    def get_hist(self, name):
        try:
            # 筛选出符合条件的用户信息便于记录查询历史
            sql = """
                    select name, word, time from user left join hist on user.id = hist.user_id  
                    where name = %s order by time desc limit 10;          
            """
            result = self.cur.execute(sql, [name])
            return self.cur.fetchall()

        except:
            return
