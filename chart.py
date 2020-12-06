from random import randrange

from song_data import SongData


def generate_chart(prev_emotion: str):
    labels = ["Happy", "Excited", "Calm", "Sad", "Stressed", "Angry"]

    test_data = []

    # TODO: This is a very hacky way of doing things, fix tomorrow

    user_values = [0, 0, 0, 0, 0, 0]

    user_values[labels.index(prev_emotion)] = 10

    test_data.append(SongData('Before Listening', user_values, 220, 0, 0))

    labels = ["Happy", "Excited", "Calm", "Sad", "Stressed", "Unsure"]

    test_data = []

    user_values = [randrange(10), randrange(10), randrange(10), randrange(10), randrange(10), randrange(10)]
    print(user_values)
    test_data.append(SongData('Your Emotions', user_values, 220, 0, 0))

    for x in range(1, 10):
        test_data.append(SongData(('User ' + str(x)), [randrange(10), randrange(10), randrange(10), randrange(10), randrange(10), randrange(10)], randrange(30, 255, 5), randrange(30, 255, 5), randrange(30, 255, 5)))

    return test_data
