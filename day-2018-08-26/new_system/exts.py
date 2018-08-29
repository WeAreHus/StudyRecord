# coding:utf8
from models import Student, Subject


def exts(cla):
    # 所有课程的学分
    allcredit = 0
    # 未获得的学分
    gotcredit = 0
    # 平均绩点
    GPA = 0
    for c in cla:
        GPA = GPA + c.score[0].GPA * c.credit
        allcredit = allcredit + c.credit
        if c.score[0].resit_score is not None:
            if c.score[0].resit_score < 60:
                gotcredit = gotcredit + c.credit
    GPA = GPA/allcredit
    GPA = round(GPA, 2)
    credit = [allcredit, gotcredit, GPA]
    return credit

def sub_query(id, year, term):
    lists = []
    stu = Student.query.filter(Student.id == id).first()
    if year == 'all':
        for cla in stu.subject:
            if cla.school_term == int(term):
                lists.append(cla)
    elif term == 'all':
        for cla in stu.subject:
            if cla.school_year == year:
                lists.append(cla)
    else:
        for cla in stu.subject:
            if cla.school_term == int(term) and cla.school_year == year:
                lists.append(cla)
    credit = exts(lists)

    return credit, lists