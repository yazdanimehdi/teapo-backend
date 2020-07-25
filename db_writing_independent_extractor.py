import sqlite3
from tpo.models import Writing

conn = sqlite3.connect('ylk.db')
for paper_id in range(1, 85):
    c = conn.cursor()
    c.execute("SELECT questionContent"
              f" FROM tbl_toefl_question WHERE paperID={paper_id} AND btype=4 AND seqno=2")
    writings = ''
    for item in c:
        writings = item[0]
    new_writing = Writing()
    e = conn.cursor()
    e.execute(f"SELECT paperName FROM tbl_toefl_paper WHERE paperID={paper_id}")
    related = ''
    for item in e:
        related = item[0]
    if related == '':
        continue
    else:
        new_writing.related = related
        new_writing.writing_question = writings
        new_writing.type = 'Independent'
        new_writing.sections = 2
        new_writing.section = 1
        new_writing.save()

