from User import *
class Contributor(User):
    def __init__(self,tup):
        super().__init__(tup)

    def writeRecipe(self, con, cursor):
        title = input("제목을 입력하세요:")
        content = input("내용을 입력하세요:")
        category = input("카테고리를 입력하세요:")
        category = category.strip()
        query = "insert into recipe_tb(user_id,title,contents,category) values (%s,%s, %s, %s);"
        cursor.execute(query, (str(self.user_id), title, content, category))
        con.commit()
        query = "select * from category where category_name = %s"
        query = cursor.mogrify(query, (category,))
        cursor.execute(query)
        result = cursor.fetchall()
        if not result:
            query = "insert into category(category_name) values (%s);"
            query = cursor.mogrify(query, (category,))
            cursor.execute(query)
            con.commit()
        query = "insert into recipe_category(category_id,recipe_id) values(\
            (select category_id from category where category_name = %s),\
            (select recipe_id from recipe_tb where title = %s)\
        );"
        query = cursor.mogrify(query, (category,title,))
        cursor.execute(query)
        con.commit()

    def rate(self,con,cursor,rid):
        print("Reviewer만 평가를 작성할 수 있습니다.")
        print("관리자에게 문의하세요.")
        print()