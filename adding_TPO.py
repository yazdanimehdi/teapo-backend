from tpo.models import Test, TestWriting, TestSpeaking, TestReading, TestListening, Reading,\
    Listening, Speaking, Writing

tpos = [(f'tpo{i}', i) for i in range(1, 54)]

for (tpo, i) in tpos:
    test = Test()
    test.title = 'TPO ' + str(i)
    test.code = tpo
    test.reading_time = 3600
    test.listening_time = 1200
    test.writing_independent_time = 1800
    test.writing_integrated_time = 1200
    test.writing_reading_time = 180
    test.save()
    reading_tpo = Reading.objects.filter(related=tpo)
    listening_tpo = Listening.objects.filter(related=tpo)
    speaking_tpo = Speaking.objects.filter(related=tpo)
    writing_tpo = Writing.objects.filter(related=tpo)
    for item in reading_tpo:
        reading_test = TestReading()
        reading_test.test = test
        reading_test.reading = item
        reading_test.part = item.phase
        reading_test.save()

    for item in listening_tpo:
        listening_test = TestListening()
        listening_test.test = test
        listening_test.listening = item
        listening_test.part = item.phase
        listening_test.save()

    for item in speaking_tpo:
        speaking_test = TestSpeaking()
        speaking_test.test = test
        speaking_test.speaking = item
        speaking_test.save()

    for item in writing_tpo:
        writing_test = TestWriting()
        writing_test.test = test
        writing_test.writing = item
        writing_test.save()
