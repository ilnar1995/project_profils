import requests
import imdb
import time


def getMovieRating(key):
    start_time = time.time()
    ia = imdb.Cinemagoer()
    movierating = ia.get_movie_vote_details(key)
    print("--- %s seconds ---" % (time.time() - start_time))
    return movierating['data']['demographics']['ttrt fltr imdb users']['rating']

