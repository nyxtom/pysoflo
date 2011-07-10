from math import sqrt

# A dictionary of movie critics and their ratings of a small # set of movies
critics = {'Claudia Puig': {'Just My Luck': 3.0,
                            'Snakes on a Plane': 3.5,
                            'Superman Returns': 4.0,
                            'The Night Listener': 4.5,
                            'You, Me and Dupree': 2.5},
           'Gene Seymour': {'Just My Luck': 1.5,
                            'Lady in the Water': 3.0,
                            'Snakes on a Plane': 3.5,
                            'Superman Returns': 5.0,
                            'The Night Listener': 3.0,
                            'You, Me and Dupree': 3.5},
           'Jack Matthews': {'Lady in the Water': 3.0,
                             'Snakes on a Plane': 4.0,
                             'Superman Returns': 5.0,
                             'The Night Listener': 3.0,
                             'You, Me and Dupree': 3.5},
           'Lisa Rose': {'Just My Luck': 3.0,
                         'Lady in the Water': 2.5,
                         'Snakes on a Plane': 3.5,
                         'Superman Returns': 3.5,
                         'The Night Listener': 3.0,
                         'You, Me and Dupree': 2.5},
           'Michael Phillips': {'Lady in the Water': 2.5,
                                'Snakes on a Plane': 3.0,
                                'Superman Returns': 3.5,
                                'The Night Listener': 4.0},
           'Mick LaSalle': {'Just My Luck': 2.0,
                            'Lady in the Water': 3.0,
                            'Snakes on a Plane': 4.0,
                            'Superman Returns': 3.0,
                            'The Night Listener': 3.0,
                            'You, Me and Dupree': 2.0},
           'Toby': {'Snakes on a Plane': 4.5,
                    'Superman Returns': 4.0,
                    'You, Me and Dupree': 1.0}}

# Returns a distance-based similarity score for person1 and person2
def sim_distance(prefs, person1, person2):
    # Get the list of shared_items
    si = {}

    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    # If they have no ratings in common, return 0
    if len(si) == 0: return 0

    # Add up the squares of all the differences
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
                          for item in prefs[person1] if item in prefs[person2]])

    return 1 / (1 + sum_of_squares)
