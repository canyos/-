class User:
    def __init__(self, tup):
        self.user_id = tup[0]
        self.username = tup[1]
        self.password = tup[2]
        self.money = tup[3]

    def recommend(self, con, cursor, rid):
        query = "select * from recommend WHERE user_id = %s AND recipe_id = %s;"
        cursor.execute(query, (self.user_id, rid))
        result = cursor.fetchall()
        query = "select user_id from recipe_tb where recipe_id = %s;"
        cursor.execute(query, rid)
        result2 = cursor.fetchall()
        if result2[0][0] == self.user_id:
            print("자신의 게시 글은 추천할 수 없습니다.")
        elif not result:
            query = "INSERT INTO recommend (user_id, recipe_id) VALUES (%s, %s);"
            cursor.execute(query, (self.user_id, rid))

            query = "UPDATE recipe_tb SET recommend = recommend + 1 WHERE recipe_id = %s;"
            cursor.execute(query, rid)
            con.commit()
            print("정상적으로 추천하였습니다.")
        else:
            print("이미 추천한 게시글 입니다.")


    def writeRecipe(self, con, cursor):
        pass

    def fund(self, con, cursor, rid):
        f = int(input("후원할 금액을 입력하세요: "))
        if(f>self.money):
            print("금액이 부족합니다")
            return
        query = \
        "begin; update user_tb set money = money - %s where user_id = %s; update user_tb set money = money+%s where user_id = (select user_id from recipe_tb where recipe_id = %s); end"
        cursor.execute(query, (str(f), str(self.user_id), str(f),rid))
        con.commit()
        self.money += f
        print("후원이 정상적으로 처리되었습니다.")

    def deleteRecipe(self,con,cursor,rid):
        if not rid == self.user_id:
            print("자신의 글만 삭제할 수 있습니다.")
            return

        query = "delete from recipe_tb where recipe_id = %s;"
        cursor.execute(query, str(rid))
        con.commit()
        print("글이 삭제되었습니다.")

    def writeComment(self,con,cursor,rid):
        content = input("내용을 입력하세요:")
        query = "insert into comment_tb(recipe_id, user_id, contents) values(%s,%s,%s);"
        cursor.execute(query,(str(rid),str(self.user_id),content))
        con.commit()

    def rate(self,con,cursor,rid):
        pass

    def chargeMoney(self,con, cursor):
        mon = int(input("충전할 금액을 입력하세요:"))
        query = "update user_tb set money = money + %s where user_id = %s;"
        self.money += mon
        cursor.execute(query,(str(mon),str(self.user_id)))
        print(f"현재 잔액 :  {self.money}")
        con.commit()