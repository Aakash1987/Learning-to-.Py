import csv


def main():
    actor_Db = create_actors_Db('movies.txt')
    ratings_Db = create_ratings_Db('moviescores.csv')

    play_again_2 = 'y'
    while play_again_2 != 'n':
        choice = get_choice()
        if choice == 1:
            actor_name = verify_actor_input(actor_Db)
            print select_where_actor_is(actor_name,actor_Db)
            play_again_2 = play_again()

        elif choice == 2:    
            movie_name = verify_movie_input(actor_Db)
            print select_where_movie_is(movie_name,actor_Db)
            play_again_2 = play_again()

        elif choice == 3:
            targeted_rating = input("What is your target rating. Please enter a number between 1 and 100 \n")
            is_critic = input("Press 0 for using audience rating, or 1 for critics rating \n")
            comparison = raw_input("Do you want movies above(Press >), below (Press <), or equal (Press =) to the target rating \n")
            print select_where_rating_is(comparison, targeted_rating, is_critic, ratings_Db)
            play_again_2 = play_again()

        elif choice == 4:
            actor_name = verify_actor_input(actor_Db)
            print get_co_actors(actor_name,actor_Db)
            play_again_2 = play_again()

        elif choice == 5:
            print "Choose first actor \n"
            actor1 = verify_actor_input(actor_Db)
            print "Choose second actor \n"
            actor2 = verify_actor_input(actor_Db)
            print get_common_movie(actor1, actor2, actor_Db)
            play_again_2 = play_again()

        elif choice == 6:
            print "Actor(s) with the highest average critics ratings:\n"
            print critics_darling(actor_Db, ratings_Db)
            play_again_2 = play_again()

        elif choice == 7:
            print "Actor(s) with the highest average audience ratings:\n"
            print audience_darling(actor_Db, ratings_Db)
            play_again_2 = play_again()

        elif choice == 8:
            print "Movies with high critics and audience ratings are: \n"
            print good_movies(ratings_Db)
            play_again_2 = play_again()

        elif choice == 9:
            print "Choose first movie \n"
            movie1 = verify_movie_input(actor_Db)
            print "Choose second movie \n"
            movie2 = verify_movie_input(actor_Db)
            print get_common_actors(movie1,movie2,actor_Db)
            play_again_2 = play_again()

        elif choice == 10:
            actor_name = verify_actor_input(actor_Db)
            print get_bacon(actor_name,actor_Db)
            play_again_2 = play_again()

    if play_again_2 == 'n':
        print "Thanks for using the database!\n"


def insert_actor_info(actor, movies, movie_Db):
    '''Inserts/updates the actor_Db database'''
    if movie_Db.get(actor,0) == 0:
        #If actor does not exist in the database, add the actor and the movies
        movie_Db[actor] = movies
    else:
        #If actor exists in the database, update his movies list
        movies_in_database = movie_Db[actor]
        movie_Db[actor] = movies_in_database.union(movies)

def insert_rating(movie, ratings, ratings_Db):
    '''Inserts/Updates the ratings_Db database'''
    ratings_Db[movie] = ratings

def delete_movie(movie, actor_Db, ratings_Db):
    '''Deletes a movie from both actor_Db and ratings_Db databases'''
    #Delete the movie key from the movies database
    del ratings_Db[movie]
    
    #Find the sets containing the movie in the values of the actor database, and remove them
    for actor, movie_list in actor_Db.iteritems():
        if movie in movie_list:
            movie_list.remove(movie)
            actor_Db[actor] = movie_list

def select_where_actor_is(actor_name,movie_Db):
    '''Returns a list of movies an actor has worked in'''
    list_of_actor_movies = list(movie_Db[actor_name])
    return list_of_actor_movies

def select_where_movie_is(movie_name,movie_Db):
    '''Returns a list of actors in a given movie'''
    list_of_movie_actors = []
    for actor, movie_list in movie_Db.iteritems():
        if movie_name in movie_list:
            list_of_movie_actors.append(actor)
    return dedupe(list_of_movie_actors)

def select_where_rating_is(comparison, targeted_rating, is_critic, ratings_Db):
    '''Returns the movies as per specified ratings criteria'''
    #critics-audience
    movie_list = []
    for movies, ratings in ratings_Db.iteritems():
        critics_ratings = int(ratings[0])
        audience_ratings = int(ratings[1])
        if comparison == '<':
            if is_critic == 1:
                if critics_ratings < targeted_rating:
                    movie_list.append(movies)
            else:
                if audience_ratings < targeted_rating:
                    movie_list.append(movies)

        if comparison == '>':
            if is_critic == 1:
                if critics_ratings > targeted_rating:
                    movie_list.append(movies)
            else:
                if audience_ratings > targeted_rating:
                    movie_list.append(movies)

        if comparison == '=':
            if is_critic == 1:
                if critics_ratings == targeted_rating:
                    movie_list.append(movies)
            else:
                if audience_ratings == targeted_rating:
                    movie_list.append(movies)

    return dedupe(movie_list)

def get_co_actors(actor_name,movie_Db):
    '''Finds the list of all co-actors that an actor has worked with'''
    list_of_co_actors = []
    movies_acted = list(movie_Db[actor_name])
    for movie_name in movies_acted:
        for actor, movie_list in movie_Db.iteritems():
            if movie_name in movie_list:
                list_of_co_actors.append(actor)

    while actor_name in list_of_co_actors:
        list_of_co_actors.remove(actor_name)

    return dedupe(list_of_co_actors)

def get_common_movie(actor1, actor2, movie_db):
    '''Finds common movies between two actors'''
    actor1_movies = movie_db[actor1]
    actor2_movies = movie_db[actor2]
    common_movies = list(actor1_movies.intersection(actor2_movies))
    return dedupe(common_movies)

def critics_darling(movie_Db, ratings_Db):
    '''Finds actor(s) who have the highest average critics ratings'''
    critics_ratings_list = []
    current_high = 0
    critics_darling = {}
    critics_darling_actors = []
    high_score = 0

    #Find all the movies of a given actor
    for actor in movie_Db.keys():
        list_of_movies = list(movie_Db[actor])
        #Store ratings of each of the actor's movie in a list
        for movie in list_of_movies:
            critics_ratings = ratings_Db.get(movie)
            if critics_ratings is not None:
                critics_ratings = int(critics_ratings[0])
                critics_ratings_list.append(critics_ratings)
            else:
                continue
                #Find average rating the actor has received
        if len(critics_ratings_list)>0:
            average_critics_rating = sum(critics_ratings_list) / len(critics_ratings_list)

            if average_critics_rating >= current_high:
                current_high = average_critics_rating
                #Store high scoring actors in a dictionary with their scores as value
                critics_darling[actor] = average_critics_rating
        critics_ratings_list = []

    #Find the actor(s) with the highest score
    for actor, score in critics_darling.iteritems():
        if score >= high_score:
            high_score = score

    for actor, score in critics_darling.iteritems():
        if score == high_score:
            critics_darling_actors.append(actor)

    return critics_darling_actors


def audience_darling(movie_Db, ratings_Db):
    '''Finds actor(s) who have the highest average critics ratings'''
    audience_ratings_list = []
    current_high = 0
    audience_darling = {}
    audience_darling_actors = []
    high_score = 0

    #Find all the movies of a given actor
    for actor in movie_Db.keys():
        list_of_movies = list(movie_Db[actor])
        #Store ratings of each of the actor's movie in a list
        for movie in list_of_movies:
            audience_ratings = ratings_Db.get(movie)
            if audience_ratings is not None:
                audience_ratings = int(audience_ratings[1])
                audience_ratings_list.append(audience_ratings)
            else:
                continue
                #Find average rating the actor has received
        if len(audience_ratings_list)>0:
            average_audience_rating = sum(audience_ratings_list) / len(audience_ratings_list)

            if average_audience_rating >= current_high:
                current_high = average_audience_rating
                #Store high scoring actors in a dictionary with their scores as value
                audience_darling[actor] = average_audience_rating
        audience_ratings_list = []

    #Find the actor(s) with the highest score
    for actor, score in audience_darling.iteritems():
        if score >= high_score:
            high_score = score

    for actor, score in audience_darling.iteritems():
        if score == high_score:
            audience_darling_actors.append(actor)

    return audience_darling_actors

def good_movies(ratings_Db):
    '''Returns a set of movies with high audience and critics ratings'''
    good_critics_movie = set(select_where_rating_is('>', 84, True, ratings_Db))
    good_audience_movie = set(select_where_rating_is('>', 84, False, ratings_Db))
    good_movies = good_critics_movie.intersection(good_audience_movie)

    return dedupe(good_movies)

def get_common_actors(movie1,movie2,movies_Db):
    '''Returns a list of actors who acted in both of given two movies'''
    actors_in_movie1 = []
    actors_in_movie2 = []
    for actor,movies_list in movies_Db.iteritems():
        if movie1 in movies_list:
            actors_in_movie1.append(actor)
        if movie2 in movies_list:
            actors_in_movie2.append(actor)

    common_actors = set(actors_in_movie1).intersection(set(actors_in_movie2))

    return dedupe(list(common_actors))


def verify_actor_input(actor_Db):
    '''Gets and verifies whether the user input(actor) is in database'''
    actor_name = raw_input("Which actor do you want to choose? \n")
    actor_name = sanitize_input(actor_name)
    while actor_name not in actor_Db.keys():
        actor_name = raw_input("Actor not in database, choose another actor \n")
        actor_name = sanitize_input(actor_name)
    return actor_name

def verify_movie_input(actor_Db):
    '''Gets and verifies whether the user input(movie) is in database'''
    counter = 0
    while counter == 0:
        movie_name = raw_input("Which movie do you want to choose? \n")
        movie_name = sanitize_input(movie_name)
        movies = actor_Db.values()
        for movie_list in movies:
            if movie_name in movie_list:
                counter = 1
                break
            else:
                counter = 0
    return movie_name

def get_choice():
    '''Prints welcome message and asks user for an initial choice'''
    print '''Welcome to the most awesome movie trivia database! \n This database containsa information on actors and the movies they have been a part of. It also contains information on critics ratings and audience ratings of movies. Using this data, we have developed some unique ways for you to get info/insights from the database. Here are some things you can ask our database: \n
    1. List of movies for an actor
    2. List of actors in a given movie
    3. List of movies with a given ratings criteria
    4. List of all co-actors that an actor has worked with
    5. List of common movies between two actors
    6. Actor(s) who have the highest average critics ratings
    7. Actor(s) who have the highest average audience ratings
    8. List of movies with high audience and critics ratings (>=85 each)
    9. List of actors who acted in both of two given movies
    10. Find the Bacon number of an actor
    '''
    choice = input("Press a number corresponding to what you want to know (Between 1 and 10) \n")
    while (choice < 1 or choice > 10):
        choice = input("Press a number corresponding to what you want to know (Between 1 and 10) \n")
    return choice

def sanitize_input(input):
    '''Returns an input of type 'Abc Abc' given any case combination like 'ABC ABC', 'abc abc'''
    sanitized_input = ''
    name = input.split()
    for words in name:
        words = words[0].upper() + words[1:].lower()
        sanitized_input = sanitized_input + ' ' + words

    sanitized_input = sanitized_input[1:]
    return sanitized_input

def dedupe(given_list):
    '''Removes duplicate values in a list'''
    set_list = set(given_list)
    dedupe_list = list(set_list)
    return dedupe_list

def play_again():
    play_again = raw_input ("Do you want to explore more? Type y for Yes and n for No\n")
    while play_again is not "y" and play_again is not "n":  
        #if the user put in wrong inputs
        play_again = raw_input ("Wrong input. Do you want to explore more? Type y for Yes and n for N \n")
    return play_again


def get_bacon(actor, movie_Db):
    '''Gets the Bacon number for a given actor'''
    Bacon_number = 1
    new_co_actors = []
    counter = 0

    co_actors = get_co_actors(actor,movie_Db)

    if actor == 'Kevin Bacon':
        return 0
    if 'Kevin Bacon' in co_actors:
        return 1

    while 'Kevin Bacon' not in new_co_actors:
        for actors in co_actors:
            new_co_actors.extend(get_co_actors(str(actors),movie_Db))
        
        Bacon_number = Bacon_number + 1
        counter = counter + 1
        dedupe(new_co_actors)

        co_actors = dedupe(new_co_actors)
        
        if 'Kevin Bacon' in co_actors:
            return Bacon_number
        if counter > 5:
            return "Not enough data to find the Bacon Number"


def create_actors_Db(actor_file):
    '''Create a dictionary keyed on actors from a text file'''
    f = open(actor_file)
    movieInfo = {}
    for line in f:
        line = line.rstrip().lstrip()
        actorAndMovies = line.split(',')
        actor = actorAndMovies[0]
        movies = [x.lstrip().rstrip() for x in actorAndMovies[1:]]
        movieInfo[actor] = set(movies)
    f.close()
    return movieInfo

def create_ratings_Db(ratings_file):
    '''make a dictionary from the rotten tomatoes csv file'''
    scores_dict = {}
    with open(ratings_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        reader.next()
        for row in reader:
            scores_dict[row[0]] = [row[1], row[2]]
    return scores_dict

    
if __name__ == '__main__':
    main()