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


def delete_by_no_and_pw(no, pw):
    try:
        # DB연결
        db = conn()

        # cursor 생성
        cursor = db.cursor()

        # SQL 실행
        sql = 'delete from guestbook where no = %s and password = %s'
        count = cursor.execute(sql, (no, pw))

        # DB 반영
        db.commit()

        # 자원 정리
        cursor.close()
        db.close()

        # 결과 반환
        return count == 1

    except Exception as e:
        print(f'Error : {e}')


def findall():
    try:
        # DB연결
        db = conn()

        # cursor를 생성
        cursor = db.cursor(DictCursor)

        # SQL 실행
        sql = '''select no, name, message, date_format(reg_date, "%Y-%m-%d %p %h:%i:%s") as reg_date 
                from guestbook 
                order by reg_date desc'''
        cursor.execute(sql)

        # 결과 받아오기
        result = cursor.fetchall()

        # 자원 정리
        cursor.close()
        db.close()

        # 결과 반환
        return result

    except Exception as e:
        print(f'Error : {e}')


def insert(name, password, message):
    try:
        # DB연결
        db = conn()

        # cursor 생성
        cursor = db.cursor()

        # SQL 실행
        sql = 'insert into guestbook values(null, %s, %s, %s, now())'
        count = cursor.execute(sql, (name, password, message))

        # DB 반영
        db.commit()

        # 자원 정리
        cursor.close()
        db.close()

        # 결과 반환
        return count == 1

    except Exception as e:
        print(f'Error : {e}')




