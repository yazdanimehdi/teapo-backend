import sqlite3
from tpo.models import Listening, ListeningQuestions, ListeningAnswers

from django.core.files import File

conn = sqlite3.connect('ylk.db')
for paper_id in range(1, 85):
    for phase in range(1, 7):
        e = conn.cursor()
        e.execute(f"SELECT paperName FROM tbl_toefl_paper WHERE paperID={paper_id}")
        related = ''
        for item in e:
            related = item[0]
        if related == '':
            continue
        elif related[0] == 't':
            d = conn.cursor()
            d.execute(f"SELECT yu_duan, title, paragraphID "
                      f"FROM tbl_toefl_paragraph WHERE btype=2 AND phaseid={phase} AND paperID={paper_id}")

            new_listening = Listening()
            new_listening.phase = phase
            new_listening.related = related
            for item in d:
                listening_transcript = item[0]
                listening_title = item[1]
                paragraph_id = item[2]
            new_listening.title = listening_title
            new_listening.transcript = listening_transcript
            if phase == 1 or phase == 4:
                new_listening.type = 'Conversation'
            else:
                new_listening.type = 'Lecture'
            listening_passage_file_name = f'{related}_listening{phase}_passage.mp3'
            new_listening.listening.save(f'{listening_passage_file_name}',
                                         File(open(f'Material/Tpo/{related}/{listening_passage_file_name}', 'rb')))
            try:
                new_listening.listening_image.save(f"{related}_listening_{phase}.jpg",
                                                   File(open(f'Material/Tpo/{related}/{related}_listening_{phase}.jpg',
                                                             'rb')))
            except FileNotFoundError:
                if phase == 1 or phase == 4:
                    new_listening.listening_image.save(f"{related}_listening_{phase}.jpg",
                                                       File(open(
                                                           f'tpo30_listening_1.jpg',
                                                           'rb')))
                else:
                    new_listening.listening_image.save(f"{related}_listening_{phase}.jpg",
                                                       File(open(
                                                           f'tpo21_writing.jpg',
                                                           'rb')))
            new_listening.save()

            d.execute(f"SELECT questionID, seqno"
                      f" FROM tbl_toefl_topic WHERE paragraphID={paragraph_id}")
            for q in d:
                listening_question = ListeningQuestions()
                listening_question.listening = new_listening
                listening_question.number = q[1]
                c = conn.cursor()
                question_all = c.execute(f"SELECT questionContent, choiceA, choiceB, choiceC, choiceD, choiceE,"
                                         f" choiceF, answer, ques_type, repeataudiourl"
                                         f" FROM tbl_toefl_question WHERE questionID={q[0]}")
                for co in question_all:
                    if co[8] < 8:
                        question = co[0]
                        choices = []
                        for choice in co[1:7]:
                            if choice != '':
                                choices.append(choice)
                        correct_answer = ''
                        for ca in co[7]:
                            if ca == 'A':
                                correct_answer += '1 '
                            if ca == 'B':
                                correct_answer += '2 '
                            if ca == 'C':
                                correct_answer += '3 '
                            if ca == 'D':
                                correct_answer += '4 '
                            if ca == 'E':
                                correct_answer += '5 '
                            if ca == 'F':
                                correct_answer += '6 '

                        correct_answer = correct_answer.strip()
                        listening_question.right_answer = correct_answer
                        listening_question.question = question
                        listening_question_audio_file_name = f'{related}_listening{phase}_question{q[1]}.mp3'
                        listening_question.listening_question_audio_file.save(listening_question_audio_file_name,
                                                                              File(open(
                                                                                  f'Material/Tpo/{related}'
                                                                                  f'/{listening_question_audio_file_name}',
                                                                                  'rb')))
                        if (co[9] is not None) and (len(co[9]) != 0):
                            listening_question.quote = True
                            listening_question_quote_file_name = f'{related}_listening{phase}_question{q[1]}_repeat.mp3'
                            listening_question.quote_audio_file.save(listening_question_quote_file_name,
                                                                     File(open(
                                                                         f'Material/Tpo/{related}'
                                                                         f'/{listening_question_quote_file_name}',
                                                                         'rb')))

                        elif co[9] is None or len(co[9]) == 0:
                            listening_question.quote = False

                        listening_question.save()

                        l = 1
                        for ans in choices:
                            answer = ListeningAnswers()
                            answer.question = listening_question
                            answer.answer = ans
                            answer.code = l
                            answer.save()
                            l += 1
