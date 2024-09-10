from User import *
class Regular(User):
    def __init__(self, tup):
        super().__init__(tup)

    def writeRecipe(self, con, cursor):
        print("Contributor만 글을 작성할 수 있습니다.")
        print("관리자에게 문의하세요.")
        print()

    def rate(self,con,cursor,rid):
        print("Reviewer만 평가를 작성할 수 있습니다.")
        print("관리자에게 문의하세요.")
        print()