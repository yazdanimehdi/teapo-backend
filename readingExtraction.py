import sqlite3
from tpo.models import Reading, ReadingQuestions, ReadingAnswers
import re
conn = sqlite3.connect('ylk.db')
for paper_id in range(1, 85):
    for phase in range(1, 4):
        c = conn.cursor()
        c.execute("SELECT paragraphID, title, paragraphIndex, paragraphDetail"
                  f" FROM tbl_toefl_paragraph WHERE paperID={paper_id} AND btype=1 AND phaseid={phase}")
        reading = [i for i in c]
        paragraph_ids = [ids[0] for ids in reading]
        new_reading = Reading()
        new_reading.phase = phase
        e = conn.cursor()
        e.execute(f"SELECT paperName FROM tbl_toefl_paper WHERE paperID={paper_id}")
        related = ''
        for item in e:
            related = item[0]
        if related == '':
            break
        else:
            new_reading.related = related
            new_reading.title = reading[0][1]
            passage = ''
            for item in reading:
                passage += item[3]

            passage = re.sub(r'\{\[.\|.+?\]\}', '', passage)
            passage = re.sub(r'{\[.\|.+?\|', '', passage)
            passage = re.sub(r'\]\}', '', passage)
            passage = re.sub(r'<\/m_p>', '</p>', passage)
            passage = re.sub(r'●', '', passage)
            passage = re.sub(r'\}', '', passage)
            passage = re.sub(r'\n', '', passage)
            passage = re.sub(r'\{', '', passage)
            passage_paragraphs = passage.split('<m_p>')
            passage_ok = ''
            j = 1
            for item in passage_paragraphs[1:]:
                passage_ok = passage_ok + f'<p id=\"{j}\">' + item
                j += 1

            new_reading.passage = passage_ok
            # print(passage_ok)
            new_reading.save()
            c = conn.cursor()
            for j in range(len(paragraph_ids)):
                for item in [paragraph_ids[j]]:
                    d = conn.cursor()
                    d.execute(f"SELECT paragraphID, paperID, questionID, seqno, relatedParagraph, highlight"
                              f" FROM tbl_toefl_topic WHERE paragraphID={item}")
                    for q in d:
                        reading_question = ReadingQuestions()
                        reading_question.reading = new_reading
                        reading_new = [parag[3] for parag in reading]
                        c = conn.cursor()
                        question_all = c.execute(f"SELECT questionContent, choiceA, choiceB, choiceC, choiceD, choiceE,"
                                                 f" choiceF, answer, ques_type"
                                                 f" FROM tbl_toefl_question WHERE questionID={q[2]}")
                        for co in question_all:
                            related_passage = None
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
                            reading_question.right_answer = correct_answer

                            if co[8] == 3:
                                reading_question.question_type = 'Summary'
                            if co[8] == 1:
                                reading_question.question_type = 'Fact'
                            if co[8] == 2:
                                reading_question.question_type = 'Insertion'
                            related_passage = ''
                            for par in reading_new:
                                related_passage += par
                            highlight = q[5]
                            related_passage = re.sub(r'\{\[2\|%i\|.*?\]\}' % (q[3]), f'<mark>{highlight}</mark>', related_passage)
                            related_passage = re.sub(r'\{\[1\|.*?\]\}', '', related_passage)
                            related_passage = re.sub(r'\{\[2\|.*?\|', '', related_passage)
                            related_passage = re.sub(r'\{\[3\|%i\|A\]\}' %(q[3]),
                                                    '<a id="insert1" class="insert">[]</a>', related_passage)
                            related_passage = re.sub(r'\{\[3\|%i\|B\]\}' %(q[3]),
                                                    '<a id="insert2" class="insert">[]</a>', related_passage)
                            related_passage = re.sub(r'\{\[3\|%i\|C\]\}' %(q[3]),
                                                    '<a id="insert3" class="insert">[]</a>', related_passage)
                            related_passage = re.sub(r'\{\[3\|%i\|D\]\}' %(q[3]),
                                                    '<a id="insert4" class="insert">[]</a>', related_passage)
                            related_passage = re.sub(r'\{\[3\|.*?\|.?\]\}', '', related_passage)
                            related_passage = re.sub(r'\<m_p\>', '<p>', related_passage)
                            related_passage = re.sub(r'<\/m_p\>', '</p>', related_passage)
                            related_passage = re.sub(r'●', '', related_passage)
                            related_passage = re.sub(r'\]\}', '', related_passage)
                            related_passage = re.sub(r'\n', '', related_passage)
                            m = 0
                            n = 1
                            for char in related_passage:
                                if char == '<' and related_passage[m + 1] == 'p':
                                    related_passage = related_passage[:m+2] + f' id=\"{n}\"' + related_passage[m+2:]
                                    m += 8
                                    n += 1
                                else:
                                    m += 1
                            char_ids = []
                            i = 0
                            for char in related_passage:
                                if char == '"' and related_passage[i + 1] == '>':
                                    char_ids.append(i + 1)
                                i += 1

                            related_passage = related_passage[
                                                 :char_ids[j] + 1] + '<i class="fas fa-arrow-right"></i>' + \
                                                 related_passage[char_ids[j] + 1:]

                            reading_question.related_passage = related_passage
                            if reading_question.question_type == 'Insertion':
                                reading_question.insertion_sentence = choices[0]

                            reading_question.question = question
                            reading_question.related_paragraph = j + 1
                            reading_question.number = q[3]
                            reading_question.related_passage_title = new_reading.title
                            reading_question.save()
                            if reading_question.question_type != 'Insertion':
                                l = 1
                                for ans in choices:
                                    answer = ReadingAnswers()
                                    answer.question = reading_question
                                    answer.answer = ans
                                    answer.code = l
                                    answer.save()
                                    l += 1