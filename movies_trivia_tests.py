
#Import everything from the file with functions to be tested
from movies_trivia import *
#Use this line in every unit testing file
import unittest



class Test_movies_trivia(unittest.TestCase):
	#self is a keyword, can't change
	def setUp(self):
		self.actor_Db = create_actors_Db('movies.txt')
		self.ratings_Db = create_ratings_Db('moviescores.csv')

	def test_insert_actor_info(self):
		'''Tests the function insert_actor_info'''
		# Testing for an existing actor entry in the database
		insert_actor_info ('Tom Hanks',set(['XYZ','ABC']),self.actor_Db)
		a = self.actor_Db['Tom Hanks']
		counter = 0
		for movie in a:
			if movie == 'XYZ':
				counter = counter + 1
			if movie == 'ABC':
				counter = counter + 1
		self.assertEqual(2,counter, 'print lsterror message')
		#Testing for a new actor entry
		insert_actor_info('Tam Hunks',set(['XYZ','ABC']),self.actor_Db)
		a = self.actor_Db['Tam Hunks']
		counter = 0
		for movie in a:
			if movie == 'XYZ':
				counter = counter + 1
			if movie == 'ABC':
				counter = counter + 1
		self.assertEqual(2,counter, 'print lsterror message')

	def test_insert_rating(self):
		'''Tests the function insert_rating'''
		#Testing for updating an existing entry
		insert_rating('Casablanca',(10,50),self.ratings_Db)
		rating = self.ratings_Db['Casablanca']
		self.assertEqual((10,50),rating, 'print lsterror message')

		#Testing for inserting a new movie and its ratings
		insert_rating('Test',(10,50),self.ratings_Db)
		rating = self.ratings_Db['Test']
		self.assertEqual((10,50),rating, 'print lsterror message')

	def test_delete_movie(self):
		'''Tests the function delete_movie'''
		delete_movie('Casablanca',self.actor_Db,self.ratings_Db)
		
		#Testing whether the movie got deleted from the ratings database
		self.assertEqual(0,self.ratings_Db.get('Casablanca',0), 'print lsterror message')
		
		#Testing whether the movie got deleted from the actor database
		movies_in_actor_Db = self.actor_Db.values()
		for movie_list in movies_in_actor_Db:
			if 'Casablanca' in movie_list:
				counter = 1
			else:
				counter = 0

		self.assertEqual(0, counter, 'print lsterror message')

	def test_select_where_actor_is(self):
		'''Tests the function select_where_actor_is'''
		Mel_Gibson_movies = set(select_where_actor_is('Mel Gibson', self.actor_Db))
		self.assertEqual(set(['Braveheart', 'Lethal Weapon']), Mel_Gibson_movies, 'print lsterror message')
		
		Charlize_Theron_movies = set(select_where_actor_is('Charlize Theron', self.actor_Db))
		self.assertEqual(set(['Mad Max: Fury Road', 'Monster']), Charlize_Theron_movies, 'print lsterror message')


	def test_select_where_movie_is(self):
		'''Tests the function select_where_movie_is'''
		My_cousin_Vinny_actors = select_where_movie_is('My Cousin Vinny', self.actor_Db)
		self.assertEqual(['Ralph Macchio','Joe Pesci'], My_cousin_Vinny_actors, 'print lsterror message')
		Goodfellas_actors = select_where_movie_is('Goodfellas',self.actor_Db)
		self.assertEqual(['Joe Pesci','Robert DeNiro','Ray Liotta'], Goodfellas_actors, 'print lsterror message')

	def test_select_where_rating_is(self):
		'''Tests the function test_select_where_rating_is'''
		all_movies = set(self.ratings_Db.keys())
		return_from_function = set(select_where_rating_is('>', 0, True,self.ratings_Db))
		self.assertEqual(all_movies, return_from_function, 'print lsterror message')	

	def test_get_co_actors(self):
		'''Tests the function get_co_actors'''
		co_actors_joe_pesci = set(['Robert DeNiro', 'Ralph Macchio','Ray Liotta'])
		return_from_function = set(get_co_actors('Joe Pesci',self.actor_Db))
		self.assertEqual(co_actors_joe_pesci, return_from_function, 'print lsterror message')	
		
	def test_get_common_movie(self):
	    '''Tests the function get_common_movie'''
	    common_movie = set(['Goodfellas'])
	    return_from_function = set(get_common_movie('Joe Pesci','Robert DeNiro',self.actor_Db))
	    self.assertEqual(common_movie, return_from_function, 'print lsterror message')	

	def test_critics_darling(self):
		'''Tests the function critics_darling'''
		actor_Db_critics = {'X':["A", "B", "C"], 'Y':["D", "E", "F"], 'Z':["G", "H", "I"] }
		rating_Db_critics = {"A": (1,1), "B":(2,2), "C":(3,3), "D":(4,4), "E":(5,5), "F":(6,6), "G":(7,7), "H":(8,8)}
		self.assertEqual(['Z'], critics_darling(actor_Db_critics, rating_Db_critics), 'print lsterror message')			

	def test_audience_darling(self):
		'''Tests the function audience_darling'''	
		actor_Db_critics = {'X':["A", "B", "C"], 'Y':["D", "E", "F"], 'Z':["G", "H", "I"] }
		rating_Db_critics = {"A": (1,1), "B":(2,2), "C":(3,3), "D":(4,4), "E":(5,5), "F":(6,6), "G":(7,7), "H":(8,8)}
		self.assertEqual(['Z'], audience_darling(actor_Db_critics, rating_Db_critics), 'print lsterror message')				

	def test_good_movies(self):
		'''Tests the function good_movies'''
		counter1 = 0
		counter2 = 0
		if 'The Godfather' in good_movies(self.ratings_Db):
			counter1 = 1
		if 'Cobra' in good_movies(self.ratings_Db):
			counter2 = 1
		self.assertEqual(1, counter1, 'print lsterror message')
		self.assertEqual(0, counter2, 'print lsterror message')

	def test_get_common_actors(self):
		'''Tests the function get_common_actors'''
		return_from_function = get_common_actors('Silver Linings Playbook','American Hustle',self.actor_Db)
		common_actors = ['Bradley Cooper', 'Jennifer Lawrence']
		self.assertEqual(common_actors, return_from_function, 'print lsterror message')	

	def test_sanitize_input(self):
		'''Tests the function sanitize_input'''
		self.assertEqual('Abc Def', sanitize_input('abc def'), 'print lsterror message')
		self.assertEqual('Abc Def', sanitize_input('ABC def'), 'print lsterror message')
		self.assertEqual('Abc', sanitize_input('aBC'), 'print lsterror message')

	def test_dedupe(self):
		'''Tests the function dedupe'''
		self.assertEqual([1,2,3], dedupe([1,2,2,3,3,3]), 'print lsterror message')

	def test_get_bacon(self):
		'''Tests the function get_bacon'''
		self.assertEqual(0,get_bacon('Kevin Bacon',self.actor_Db), 'print lsterror message')
		self.assertEqual(1,get_bacon('Kevin Costner',self.actor_Db), 'print lsterror message')
		self.assertEqual(2,get_bacon('Shirley Maclaine',self.actor_Db), 'print lsterror message')


unittest.main()
