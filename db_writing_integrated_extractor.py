import sqlite3
from tpo.models import Writing
import re
from django.core.files import File


conn = sqlite3.connect('ylk.db')
for paper_id in range(1, 85):
    e = conn.cursor()
    e.execute(f"SELECT paperName FROM tbl_toefl_paper WHERE paperID={paper_id}")
    related = ''
    for item in e:
        related = item[0]
    if related == '':
        continue
    elif related[0] == 't':
        c = conn.cursor()
        d = conn.cursor()
        c.execute("SELECT questionContent"
                  f" FROM tbl_toefl_question WHERE paperID={paper_id} AND btype=4 AND seqno=1")
        d.execute(f"SELECT yu_duan, paragraphDetail "
                  f"FROM tbl_toefl_paragraph WHERE btype=4 AND phaseid=1 AND paperID={paper_id}")
        writings = ''
        for item in c:
            writings = item[0]
        new_writing = Writing()
        for item in d:
            writing_reading = item[0]
            writing_listening_transcript = item[1]

        writing_listening_transcript = re.sub(r'\{\[.\|.+?\]\}', '', writing_listening_transcript)
        writing_listening_transcript = re.sub(r'<m_p>', '', writing_listening_transcript)
        writing_listening_transcript = re.sub(r'<\/m_p>', '', writing_listening_transcript)
        writing_file_name = f'{related}_writing1_passage.mp3'
        new_writing.writing_listening.save(f'{writing_file_name}',
                                           File(open(f'Material/Tpo/{related}/{writing_file_name}', 'rb')))
        try:
            new_writing.writing_image.save(f"{related}_writing.jpg",
                                           File(open(f'Material/Tpo/{related}/{related}_writing.jpg', 'rb')))
        except FileNotFoundError:
            new_writing.writing_image.save(f"{related}_writing.jpg",
                                           File(open(f'tpo21_writing.jpg', 'rb')))

        new_writing.related = related
        new_writing.writing_question = writings
        new_writing.type = 'Integrated'
        new_writing.writing_listening_transcript = writing_listening_transcript
        new_writing.writing_reading = writing_reading
        new_writing.sections = 4
        new_writing.section = 1

        new_writing.save()
