from random import randrange

from song_data import SongData


def generate_chart(prevEmotion: str, currEmotion: str):
    labels = ["Happy", "Excited", "Calm", "Sad", "Stressed", "Angry"]

    testdata = []

    # TODO: This is a very hacky way of doing things, fix tomorrow

    user_values = [0, 0, 0, 0, 0, 0]

    user_values[labels.index(prevEmotion)] = 10

    testdata.append(SongData('Before Listening', user_values, 220, 0, 0))

    user_values = [0, 0, 0, 0, 0, 0]

    user_values[labels.index(currEmotion)] = 10

    testdata.append(SongData('After Listening', user_values, 220, 0, 0))

    #for x in range(1, 10):
        #testdata.append(SongData(('User ' + str(x)), [randrange(10), randrange(10), randrange(10), randrange(10), randrange(10), randrange(10)], randrange(30, 255, 5), randrange(30, 255, 5), randrange(30, 255, 5)))

    return testdata
