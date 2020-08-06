from tpo.models import Test, TestWriting, TestSpeaking, TestReading, TestListening, Reading,\
    Listening, Speaking, Writing, WritingTimes, SpeakingTimes, ListeningTimes

tpos = [(f'tpo{i}', i) for i in range(1, 54)]

for (tpo, i) in tpos:
    test = Test()
    test.title = 'TPO ' + str(i)
    test.code = tpo
    test.mode = 'T'

    test.reading_time = 3600
    test.save()

    listening_times = ListeningTimes()
    listening_times.test = test
    listening_times.number = 1
    listening_times.time = 600
    listening_times.save()

    listening_times = ListeningTimes()
    listening_times.test = test
    listening_times.number = 2
    listening_times.time = 600
    listening_times.save()

    writing_times = WritingTimes()
    writing_times.test = test
    writing_times.number = 1
    writing_times.time = 1200
    writing_times.reading_time = 180
    writing_times.save()

    writing_times = WritingTimes()
    writing_times.test = test
    writing_times.number = 2
    writing_times.time = 1800
    writing_times.save()

    speaking_times = SpeakingTimes()
    speaking_times.test = test
    speaking_times.number = 1
    speaking_times.preparation_time = 15
    speaking_times.answering_time = 45
    speaking_times.save()

    speaking_times = SpeakingTimes()
    speaking_times.test = test
    speaking_times.number = 2
    speaking_times.preparation_time = 15
    speaking_times.answering_time = 45
    speaking_times.save()

    speaking_times = SpeakingTimes()
    speaking_times.test = test
    speaking_times.number = 3
    speaking_times.preparation_time = 30
    speaking_times.answering_time = 60
    speaking_times.reading_time = 45
    speaking_times.save()

    speaking_times = SpeakingTimes()
    speaking_times.test = test
    speaking_times.number = 4
    speaking_times.preparation_time = 30
    speaking_times.answering_time = 60
    speaking_times.reading_time = 45
    speaking_times.save()

    speaking_times = SpeakingTimes()
    speaking_times.test = test
    speaking_times.number = 5
    speaking_times.preparation_time = 30
    speaking_times.answering_time = 60
    speaking_times.reading_time = 45
    speaking_times.save()

    speaking_times = SpeakingTimes()
    speaking_times.test = test
    speaking_times.number = 6
    speaking_times.preparation_time = 30
    speaking_times.answering_time = 60
    speaking_times.reading_time = 45
    speaking_times.save()

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
        if item.phase > 3:
            listening_test.phase = 2
            listening_test.part = item.phase - 3
        else:
            listening_test.phase = 1
            listening_test.part = item.phase
        listening_test.save()

    for item in speaking_tpo:
        speaking_test = TestSpeaking()
        speaking_test.test = test
        speaking_test.speaking = item
        speaking_test.part = item.number
        speaking_test.save()

    for item in writing_tpo:
        writing_test = TestWriting()
        writing_test.test = test
        writing_test.writing = item
        writing_test.part = item.section
        writing_test.save()
