#!/usr/bin/env python

# This represents the amount of search results we get for this words
# The word in this case will be dataisbig
DATA_IS_BIG = {
    'd': 1000,
    'da': 1100,
    'dat': 1000,
    'data': 100000, # Winner!!!
    'datai': 100,
    'datais': 4000,
    'dataisb': 2000,
    'dataisbi': 3000,
    'dataisbig': 3000
}

def guess_the_word(phrase):
    """
    Take a guess on the word in a big string

    >>> guess_the_word("dataisbig")
    'data'
    """
    winner = phrase[0]

    for i in range(1, len(phrase)):
        if DATA_IS_BIG[winner] < DATA_IS_BIG[phrase[0:i]]:
            winner = phrase[0:i]

    return winner

if __name__ == '__main__':
    import doctest
    doctest.testmod()
