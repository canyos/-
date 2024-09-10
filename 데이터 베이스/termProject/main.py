import psycopg2
from User import User
from Contributor import Contributor
from Regular import Regular
from Reviewer import Reviewer
import random

def connect():
    con = psycopg2.connect(
        database='sample2023',
        user='db2023',
        password='db!2023',
        host='::1',
        port='5432'
    )
    return con, con.cursor()


match_class = {"regular": Regular, "contributor": Contributor, "reviewer": Reviewer}
def login(cursor):
    while True:
        username = input("username:")
        password = input("password:")
        query = "select * from user_tb where username= %s and password= %s;"
        cursor.execute(query, (username, password))
        result = cursor.fetchall()
        if len(result) == 0:
            print("정보가 없습니다. 다시 입력해주세요.")
            continue
        else:
            print(result[0][1] + "(으)로 로그인")
            print("role: " + result[0][4])
            break
    return match_class[result[0][4]](result[0])


def mainScriptAndInput():
    print("1. 모든 글보기")
    print("2. 글 상세보기")
    print("3. 글쓰기")
    print("4. 카테고리 종류 보기")
    print("5. 검색하기")
    print("6. 랜덤 레시피 추천받기")
    print("7. 인기 레시피 보기")
    print("8. 돈 충전하기")
    print("9. 로그아웃")
    while True:
        inp = int(input("Enter:"))
        if 1 <= inp <= 9:
            break
    return inp


def showAllRecipe(cursor):
    query = "select * from recipe_tb order by recipe_id asc;"
    cursor.execute(query)
    result = cursor.fetchall()
    print()
    print("글 번호\t\t제목\t\t추천")
    for i in range(0, len(result)):
        print(f"{result[i][0]}\t\t\t{result[i][2]}\t\t{result[i][4]}")
    print()

def detailRecipe(cursor, rn):
    query = "select r.title, r.contents, r.recommend, u.username, r.rating from recipe_tb r, user_tb u where recipe_id = %s and r.user_id = u.user_id;"
    cursor.execute(query, rn)
    result = cursor.fetchall()
    print(f"제목: {result[0][0]}")
    print(f"작성자: {result[0][3]}")
    print(f"내용: {result[0][1]}")
    print(f"추천: {result[0][2]}")
    print(f"평점: {result[0][4]}")


def detailPrompt():
    print("1. 이 글을 추천")
    print("2. 후원 하기")
    print("3. 평가 하기")
    print("4. 글 삭제하기")
    print("5. 댓글 보기")
    print("6. 뒤로 가기")
    while True:
        inp = int(input("Enter: "))
        if 1 <= inp <= 6:
            return inp
        else:
            print("잘못입력하였습니다.")

def showCategory(cursor):
    query = "select * from category"
    cursor.execute(query)
    result = cursor.fetchall()
    for i in range(len(result)) :
        print(f"{i+1}: {result[i][1]}")

    sel = input("카테고리를 선택하세요:")

    query = "select distinct r.recipe_id, r.title, r.recommend from recipe_category rc, recipe_tb r where rc.category_id = %s and r.recipe_id = rc.recipe_id;"
    cursor.execute(query, sel)
    result = cursor.fetchall()
    if not result:
        print("해당 카테고리에 등록된 레시피가 없습니다.")
        return
    print("글 번호\t\t제목\t\t추천")
    for i in range(0, len(result)):
        print(f"{result[i][0]}\t\t\t{result[i][1]}\t\t{result[i][2]}")


def search(cursor):
    print("1: 제목으로 검색")
    print("2: 내용으로 검색")
    print("3: 카테고리로 검색")
    print("4: 작성자로 검색")
    print("5: 뒤로 가기")
    sel = int(input("입력: "))
    if not 1 <= sel <= 4 :
        return
    inp = input("검색어를 입력하세요:")
    if sel == 1:
        query = "SELECT r.recipe_id, r.title, r.recommend FROM recipe_tb r WHERE title LIKE %s;"
        query = cursor.mogrify(query, ('%' + inp + '%',))
    elif sel == 2:
        query = "select r.recipe_id, r.title, r.recommend from recipe_tb r where contents LIKE %s;"
        query = cursor.mogrify(query, ('%' + inp + '%',))
    elif sel == 3:
        query = "select r.recipe_id, r.title, r.recommend from recipe_tb r where category LIKE %s;"
        query = cursor.mogrify(query, ('%' + inp + '%',))
    elif sel == 4:
        query = "select r.recipe_id, r.title, r.recommend from recipe_tb r, user_tb u where r.user_id = u.user_id and u.username = %s;"
        query = cursor.mogrify(query, (inp,))

    cursor.execute(query)
    result = cursor.fetchall()
    print()
    print("글 번호\t\t제목\t\t추천")
    for i in range(0, len(result)):
        print(f"{result[i][0]}\t\t\t{result[i][1]}\t\t{result[i][2]}")

def randomRecipe(cursor):
    query = "select recipe_id from recipe_tb;"
    cursor.execute(query)
    result = cursor.fetchall()
    print()
    random_element = random.choice(result)
    detailRecipe(cursor, str(random_element[0]))




def showComment(cursor, rid):
    query = "select u.username, c.contents from comment_tb c, user_tb u where c.recipe_id = %s and c.user_id = u.user_id;"
    cursor.execute(query, str(rid))
    result = cursor.fetchall()
    print("유저명\t\t내용")
    for i in range(0,len(result)):
        print(f"{result[i][0]}\t\t{result[i][1]}")


def showPopularRecipe(cursor):
    query = "select r.recipe_id, r.title, r.recommend from popular_recipe r;"
    cursor.execute(query)
    result = cursor.fetchall()
    print("글 번호\t\t제목\t\t추천")
    for i in range(0, len(result)):
        print(f"{result[i][0]}\t\t\t{result[i][1]}\t\t{result[i][2]}")


def signInRegular(con, cursor):
    uname = input("username:")
    query = "select * from user_tb where username = %s;"
    cursor.execute(query, (uname,))
    result = cursor.fetchall()
    if result:
        print("이미 존재하는 유저명입니다.")
        signInRegular(con,cursor)
        return
    password = input("password:")
    
    query = "with insertNum as(insert into user_tb(username,password,role) values(%s,%s,\'regular\') returning user_id)\
                insert into regular(user_id) select user_id from insertNum;"

    cursor.execute(query, (uname, password))
    con.commit()
    print("정상적으로 회원가입하였습니다.")


def signInContributor(con,cursor):
    query = "SELECT has_table_privilege(current_user, 'contributor', 'insert');"
    cursor.execute(query)
    result = cursor.fetchall()
    if result[0][0]==True:
        uname = input("username:")
        query = "select * from user_tb where username = %s;"
        cursor.execute(query, (uname,))
        result = cursor.fetchall()
        if result:
            print("이미 존재하는 유저명입니다.")
            signInRegular(con, cursor)
            return
        password = input("password:")

        query = "with insertNum as(insert into user_tb(username,password,role) values(%s,%s,\'contributor\') returning user_id)\
                        insert into contributor(user_id) select user_id from insertNum;"
        cursor.execute(query, (uname, password))
        con.commit()
        print("정상적으로 회원가입하였습니다.")
    else :
        print("권한이 없습니다. 관리자에게 문의하세요.")
        signIn(con,cursor)


def signInReviewer(con, cursor):
    query = "SELECT has_table_privilege(current_user, 'reviewer', 'insert');"
    cursor.execute(query)
    result = cursor.fetchall()
    if result[0][0] == True:
        uname = input("username:")
        query = "select * from user_tb where username = %s;"
        cursor.execute(query, (uname,))
        result = cursor.fetchall()
        if result:
            print("이미 존재하는 유저명입니다.")
            signInRegular(con, cursor)
            return
        password = input("password:")

        query = "with insertNum as(insert into user_tb(username,password,role) values(%s,%s,\'reviewer\') returning user_id)\
                                insert into reviewer(user_id) select user_id from insertNum;"
        cursor.execute(query, (uname, password))
        con.commit()
        print("정상적으로 회원가입하였습니다.")
    else:
        print("권한이 없습니다. 관리자에게 문의하세요.")
        signIn(con, cursor)


def signIn(con, cursor ):
    print("1. Regular로 가입하기")
    print("2. Contributor로 가입하기")
    print("3. Reviewer로 가입하기")
    sel = int(input("입력: "))
    if sel == 1:
        signInRegular(con,cursor)
    elif sel == 2:
        signInContributor(con,cursor)
    elif sel == 3:
        signInReviewer(con,cursor)
    else:
        return


if __name__ == '__main__':
    con, cursor = connect()
    while True:
        sel = int(input("1.회원가입\n2.로그인\n입력: "))
        if sel == 1:
            signIn(con, cursor)
        print("로그인 화면")
        user = login(cursor)
        while True:
            select = mainScriptAndInput()
            if select == 1:
                showAllRecipe(cursor)
            elif select == 2:
                rid = input("글 번호:")
                detailRecipe(cursor, rid)
                inp = detailPrompt()
                if inp == 1:  # 추천하기
                    user.recommend(con, cursor, rid)
                elif inp==6:  # 뒤로가기
                    continue
                elif inp == 2:# 후원
                    user.fund(con,cursor,rid)
                elif inp == 3:#평가
                    user.rate(con, cursor, rid)
                elif inp == 4:
                    user.deleteRecipe(con,cursor,rid)
                elif inp == 5:
                    showComment(cursor,rid)
                    print("1. 댓글 작성하기")
                    print("2. 뒤로가기")
                    sel = int(input("입력:"))
                    if sel == 1:
                        user.writeComment(con, cursor, rid)
            elif select == 3:
                user.writeRecipe(con, cursor)
            elif select == 4:
                showCategory(cursor)
            elif select == 5:
                search(cursor)
            elif select == 6:
                randomRecipe(cursor)
            elif select == 7:
                showPopularRecipe(cursor)
            elif select == 8:
                user.chargeMoney(con, cursor)
            elif select == 9:
                break;