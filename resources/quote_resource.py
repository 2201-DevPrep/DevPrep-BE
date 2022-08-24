from app import cache
from flask_restful import Resource
import random, csv

class QuoteResource(Resource):
    def get(self):
        # checks if a current quote of the day exists
        cached_quote = cache.get('quote_of_the_day')
        if cached_quote:
            return cached_quote, 200
        else:
            # if not, reads the CSV and caches a random quote
            with open('data/quotes.csv', newline='') as f:
                fdicts = csv.DictReader(f.read().splitlines(), skipinitialspace=True)

                csv_dicts = [{k: v for k, v in row.items()} for row in fdicts]

            quote = random.choice(csv_dicts)
            cache.set('quote_of_the_day', quote, timeout=86400)

            return quote, 200
