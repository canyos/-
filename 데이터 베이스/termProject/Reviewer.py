from User import *
class Reviewer(User):
    def __init__(self,tup):
        super().__init__(tup)

    def writeRecipe(self, con, cursor):
        print("Contributor만 글을 작성할 수 있습니다.")
        print("관리자에게 문의하세요.")
        print()

    def rate(self,con, cursor, rid):
        query = "select user_id from ratings where recipe_id = %s and user_id = %s;"
        cursor.execute(query,(str(rid),str(self.user_id)))
        result = cursor.fetchall()
        r = int(input("평점 입력(0~5):"))
        if result:
            query = "begin;update ratings set score = %s where user_id = %s and recipe_id = %s;\
                update recipe_tb set rating =(select avg(score)from ratings where recipe_id = %s) where recipe_id = %s;"
            cursor.execute(query, (str(r), str(self.user_id), str(rid),str(rid),str(rid)))
            con.commit()
            print("평가를 수정함")
        else :
            query = "begin;insert into ratings values (%s,%s,%s);\
                     update recipe_tb set rating =(select avg(score)from ratings where recipe_id = %s) where recipe_id = %s;"
            cursor.execute(query,(str(self.user_id),str(rid),str(r), str(rid), str(rid)))
            con.commit()
            print("평가를 작성함")

