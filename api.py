import requests as req


class Api:
	def __init__(self, api_key: str):
		self.api_key = api_key
		self.s = req.Session()

		self.api_url = "https://api.dicolink.com/v1"


	def get_random_word(self):
		r = self.request(
			"/mots/motauhasard",
			params={
				"avecdef": "false",
				"minlong": 1,
				"maxlong": -1,
				"verbeconjugue": "false"
			}
		)

		word = r['mot']
		return word

	def get_word_definition(self, word: str):
		r = self.request(
			f"/mot/{word}/definitions",
			params={
				"limite": 5,
				"source": ["granddico"]

			}
		)

		word_def = r['definition']
		return word_def


	def request(self, path: str, params: dict):
		params['api_key'] = self.api_key
		full_path = self.api_url + path

		r = self.s.get(full_path, params=params).json()
		return r
