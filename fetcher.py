import datetime
from exceptions import PokeApiException

favorite_uris = ['https://pokeapi.co/api/v2/pokemon/25',    # pikachu
                 'https://pokeapi.co/api/v2/pokemon/132',   # ditto
                 'https://pokeapi.co/api/v2/pokemon/143',   # snorlax
                 'https://pokeapi.co/api/v2/pokemon/35',    # clefairy
                 'https://pokeapi.co/api/v2/pokemon/413']  # wormadam-plant


class Fetcher(object):
    def __init__(self, requester, cache_timeout_seconds=300):
        """
        Instantiate a fetcher that holds a list of favorite Pokémon in memory
        :param requester:  The request protocol to use for url actions
        :param cache_timeout_seconds: How many seconds should the cache remain before being refreshed
        """
        self.requester = requester  # inject dependency for testability.
        self.last_fetched = None
        self.pokemon = None
        self.cache_timeout_seconds = cache_timeout_seconds

    def fetch_all(self):
        """
        Fetches a copy of the favorite Pokémon data and keeps it in memory for quick access
        :return:
        """
        self.pokemon = {}
        for uri in favorite_uris:
            fetched_pokemon = self.get_resource(uri)
            species = self.get_resource(fetched_pokemon['species']['url'])

            # Format information to what we want in our api
            data = {
                'name': fetched_pokemon['name'],
                'height': fetched_pokemon['height'],
                'weight': fetched_pokemon['weight'],
                'color': species['color']['name'],
                'moves': fetched_pokemon['moves'],
                'base_happiness': {
                    'average': species['base_happiness'],
                    'mean': species['base_happiness'],
                    'median': species['base_happiness'],
                }
            }
            name = data['name']
            self.pokemon[name] = data
        self.last_fetched = datetime.datetime.now()

    def get_resource(self, url):
        request = self.requester.get(url, auth={})
        if request.status_code != 200:
            print('Request to pokeapi failed, url: {}, content: {}'.format(url, request.content))
            raise PokeApiException('invalid request to pokeapi, {}'.format(url))
        return request.json()

    def favorites(self):
        """
        Lazy fetch the favorite Pokémon, or fetch if the cache should be busted
        :return:
        """
        if self.pokemon is None or self.cache_bust():
            self.fetch_all()
        return self.pokemon

    def cache_bust(self):
        """
        Cache should be busted if either we have never fetched or if the fetch is too old.
        :return:
        """
        if self.last_fetched is None:
            return True
        if (datetime.datetime.now() - self.last_fetched).seconds > self.cache_timeout_seconds:
            return True
        return False
