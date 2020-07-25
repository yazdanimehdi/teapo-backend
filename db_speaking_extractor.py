import sqlite3
from tpo.models import Speaking
import re
from django.core.files import File

conn = sqlite3.connect('ylk.db')
for paper_id in range(1, 85):
    for section in range(1, 7):

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
                      f" FROM tbl_toefl_question WHERE paperID={paper_id} AND btype=3 AND seqno={section}")
            d.execute(f"SELECT yu_duan, paragraphDetail "
                      f"FROM tbl_toefl_paragraph WHERE btype=3 AND phaseid={section} AND paperID={paper_id}")
            for item in d:
                speaking_reading = item[0]
                speaking_listening_transcript = item[1]

            for item in c:
                question = item[0]
            new_speaking = Speaking()
            if section == 3 or section == 4:
                speaking_listening_transcript = re.sub(r'\{\[.\|.+?\]\}', '', speaking_listening_transcript)
                speaking_listening_transcript = re.sub(r'<m_p>', '', speaking_listening_transcript)
                speaking_listening_transcript = re.sub(r'<\/m_p>', '', speaking_listening_transcript)
                speaking_question_file_name = f'{related}_speaking{section}_question{section}.mp3'
                speaking_guide_file_name = f"{related}_speaking{section}_question{section}_qd.mp3"
                speaking_beforereading_file_name = f"{related}_speaking{section}_question{section}_beforeread.mp3"
                speaking_audio_file_name = f"{related}_speaking{section}_question{section}_dialog.mp3"
                speaking_image_file_name = f"{related}_speaking_{section}.jpg"
                new_speaking.number = section
                new_speaking.related = related
                new_speaking.speaking_question = question
                new_speaking.speaking_reading = speaking_reading
                new_speaking.speaking_prepare_time = 30
                new_speaking.sections = 4
                new_speaking.speaking_time = 60
                try:
                    new_speaking.speaking_image.save(speaking_image_file_name,
                                                     File(open(
                                                         f'Material/Tpo/{related}/{speaking_image_file_name}',
                                                         'rb')))
                except:
                    new_speaking.speaking_image.save(speaking_question_file_name,
                                                     File(open(
                                                         f'tpo21_writing.jpg',
                                                         'rb')))
                new_speaking.speaking_question_audio_file.save(speaking_question_file_name,
                                                               File(open(
                                                                   f'Material/Tpo/{related}/{speaking_question_file_name}',
                                                                   'rb')))
                new_speaking.speaking_question_guide_audio_file.save(
                    f'{speaking_guide_file_name}',
                    File(open(
                        f'Material/Tpo/{related}/{speaking_guide_file_name}',
                        'rb')))
                new_speaking.speaking_question_before_read_audio.save(f'{speaking_beforereading_file_name}',
                                                                      open(
                                                                          f'Material/Tpo/{related}/{speaking_beforereading_file_name}',
                                                                          'rb'))
                new_speaking.speaking_audio_file.save(f'{speaking_audio_file_name}',
                                                      open(f'Material/Tpo/{related}/{speaking_audio_file_name}', 'rb'))
                new_speaking.speaking_audio_file_transcript = speaking_listening_transcript
                new_speaking.save()

            elif section == 1 or section == 2:
                new_speaking.number = section
                new_speaking.related = related
                new_speaking.speaking_question = question
                new_speaking.speaking_question_audio_file.save(f'{related}_speaking{section}_question{section}.mp3',
                                                               File(open(
                                                                   f'Material/Tpo/{related}/{related}_speaking{section}_question{section}.mp3',
                                                                   'rb')))
                new_speaking.speaking_question_guide_audio_file.save(
                    f'{related}_speaking{section}_question{section}_qd.mp3',
                    File(open(
                        f'Material/Tpo/{related}/{related}_speaking{section}_question{section}_qd.mp3',
                        'rb')))
                new_speaking.speaking_prepare_time = 15
                new_speaking.speaking_time = 45
                new_speaking.sections = 2
                new_speaking.save()
            else:
                speaking_listening_transcript = re.sub(r'\{\[.\|.+?\]\}', '', speaking_listening_transcript)
                speaking_listening_transcript = re.sub(r'<m_p>', '', speaking_listening_transcript)
                speaking_listening_transcript = re.sub(r'<\/m_p>', '', speaking_listening_transcript)
                speaking_question_file_name = f'{related}_speaking{section}_question{section}.mp3'
                speaking_guide_file_name = f"{related}_speaking{section}_question{section}_qd.mp3"
                speaking_audio_file_name = f"{related}_speaking{section}_question{section}_dialog.mp3"
                speaking_image_file_name = f"{related}_speaking_{section}.jpg"
                new_speaking.number = section
                new_speaking.related = related
                new_speaking.sections = 3
                new_speaking.speaking_question = question
                new_speaking.speaking_prepare_time = 30
                new_speaking.speaking_time = 60
                try:
                    new_speaking.speaking_image.save(speaking_image_file_name,
                                                     File(open(
                                                         f'Material/Tpo/{related}/{speaking_image_file_name}',
                                                         'rb')))
                except:
                    new_speaking.speaking_image.save(speaking_question_file_name,
                                                     File(open(
                                                         f'tpo21_writing.jpg',
                                                         'rb')))
                new_speaking.speaking_question_audio_file.save(speaking_question_file_name,
                                                               File(open(
                                                                   f'Material/Tpo/{related}/{speaking_question_file_name}',
                                                                   'rb')))
                new_speaking.speaking_question_guide_audio_file.save(
                    f'{speaking_guide_file_name}',
                    File(open(
                        f'Material/Tpo/{related}/{speaking_guide_file_name}',
                        'rb')))

                new_speaking.speaking_audio_file.save(f'{speaking_audio_file_name}',
                                                      open(f'Material/Tpo/{related}/{speaking_audio_file_name}', 'rb'))
                new_speaking.speaking_audio_file_transcript = speaking_listening_transcript
                new_speaking.save()

# todo: add time
