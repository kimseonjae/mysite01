from django.db import models
from MySQLdb import connect
from MySQLdb.cursors import DictCursor


def conn():
    return connect(
        user='webdb',
        password='webdb',
        host='localhost',
        port=3306,
        db='webdb',
        charset='utf8')


def findall_contents(no):
    try:
        # DB연결
        db = conn()

        # cursor를 생성
        cursor = db.cursor(DictCursor)

        # SQL 실행

        sql = 'select * from board b where b.no = %s'
        cursor.execute(sql, (no,))

        # 결과 받아오기
        result = cursor.fetchall()

        # 자원 정리
        cursor.close()  # 커서
        db.close()      # DB연결 끊기

        # 결과 반환
        return result

    except Exception as e:
        print(f'Error : {e}')

def findall_list():
    try:
        # DB연결
        db = conn()

        # cursor를 생성
        cursor = db.cursor(DictCursor)

        # SQL 실행
        sql = '''select b.no, b.title, u.name, b.hit, b.reg_date, b.depth 
                from board b, user u 
                where b.user_no = u.no 
                order by b.g_no desc, b.o_no'''
        cursor.execute(sql)

        # 결과 받아오기
        result = cursor.fetchall()

        # 자원 정리
        cursor.close()  # 커서
        db.close()      # DB연결 끊기

        # 결과 반환
        return result

    except Exception as e:
        print(f'Error : {e}')


def find_max_g_no():
    try:
        # DB연결
        db = conn()

        # cursor를 생성
        cursor = db.cursor(DictCursor)

        # SQL 실행
        sql = 'select max(g_no)+1 as max_g_no from board'
        cursor.execute(sql)

        # 결과 받아오기
        result = cursor.fetchall()

        # 자원 정리
        cursor.close()  # 커서
        db.close()      # DB연결 끊기

        # 결과 반환
        return result[0]['max_g_no']

    except Exception as e:
        print(f'Error : {e}')


def insert(title, contents, g_no, user_no):
    try:
        # 연결
        db = conn()

        # cursor 생성
        cursor = db.cursor()

        # SQL 실행
        sql = 'insert into board values(null, %s, %s, 0, now(), %s, 1, 0, %s)'
        count = cursor.execute(sql, (title, contents, g_no, user_no))

        # commit
        db.commit()

        # 자원 정리
        cursor.close()
        db.close()

        # 결과 반환
        return count == 1

    except Exception as e:
        print(f'error: {e}')


def update(title, contents, no):
    try:
        # DB연결
        db = conn()

        # cursor 생성
        cursor = db.cursor()

        # SQL 실행
        sql = 'update board set title = %s, contents = %s where no=%s'
        count = cursor.execute(sql, (title, contents, no))

        # DB 반영
        db.commit()

        # 자원 정리
        cursor.close()  # 커서
        db.close()      # DB연결 끊기

        # 결과 반환
        return count == 1

    except Exception as e:
        print(f'Error : {e}')


def delete(no, user_no):
    try:
        # DB연결
        db = conn()

        # cursor 생성
        cursor = db.cursor()

        # SQL 실행
        sql = 'delete from board where no = %s and user_no = %s'
        count = cursor.execute(sql, (no, user_no))

        # DB 반영
        db.commit()

        # 자원 정리
        cursor.close()  # 커서
        db.close()      # DB연결 끊기

        # 결과 반환
        return count == 1

    except Exception as e:
        print(f'Error : {e}')


def search(kwd):
    try:
        # DB연결
        db = conn()

        # cursor를 생성
        cursor = db.cursor(DictCursor)

        # SQL 실행
        sql = '''
              select a.no, a.title, a.name, a.hit, a.reg_date
              from (select b.no, b.title, b.contents, u.name, b.hit, b.reg_date 
                    from board b, user u 
                    where b.user_no = u.no) as a
              where a.name like %s
              or a.title like %s
              or a.contents like %s
              order by a.no desc'''
        cursor.execute(sql, (kwd, kwd, kwd))

        # 결과 받아오기
        result = cursor.fetchall()

        # 자원 정리
        cursor.close()  # 커서
        db.close()      # DB연결 끊기

        # 결과 반환
        return result

    except Exception as e:
        print(f'Error : {e}')


def reply(title, contents, g_no, o_no, depth, user_no):
    try:
        # 연결
        db = conn()

        # cursor 생성
        cursor = db.cursor()

        # SQL 실행
        sql = "insert into board values(null, %s, %s, 0, now(), %s, %s, %s, %s)"
        count = cursor.execute(sql, (title, contents, g_no, o_no, depth, user_no))

        # commit
        db.commit()

        # 자원 정리
        cursor.close()
        db.close()

        # 결과 반환
        return count == 1

    except Exception as e:
        print(f'error: {e}')