from collections import namedtuple
from datetime import date

import twitter


DATE_TODAY = date.today().strftime("%Y-%m-%d")

City = namedtuple('City', ['name','geocode'])


class TweetMurmurs:

    _city_murmurs = list()

    _major_cities = [
        City(name='Nairobi', geocode='-1.27468,36.81170,50km'),
        City(name='Thika', geocode='-1.0420115,37.0234126,50km'),
        City(name='Mombasa', geocode='-4.0517497,39.6620736,50km'),
        City(name='Kisumu', geocode='-0.0749726,34.5980818,50km'),
        City(name='Nakuru', geocode='-0.45982,36.10068,50km'),
        City(name='Eldoret', geocode='0.4836246,35.2622765,50km')
        ]

    def __init__(self, consumer_key, consumer_secret, access_token_key, access_token_secret):
        self.twitter_api = twitter.Api(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token_key=access_token_key,
            access_token_secret=access_token_secret,
            sleep_on_rate_limit=True
        )

    def get_all_tweets(self, limit=15):
        """
        This method any tweet posted from one of the major cities listed. Have to be careful not to
        surpass Twitter's Rate Limit of 15 requests per 15 minute TimeFrame Windows.

        :param:
                limit -> Maximum number of tweets to be returned for a given city.

        :return:
                A list containing tweets.
        """
        posted_tweets = list()

        # reset the class variable first
        self._city_murmurs = list()

        for city in self._major_cities:
            city_murmurs = self.twitter_api.GetSearch(geocode=city.geocode, since=DATE_TODAY, count=limit)

            data = dict(city=city.name, tweets=[])

            if len(city_murmurs) > 0:
                for city_murmur in city_murmurs:
                    data['tweets'].append(city_murmur.text)

            posted_tweets.append(data)
        
        self._city_murmurs = posted_tweets

        return self._city_murmurs

    def save(self):
        """
        This method saves all the information stored in the instance variables to a
        database.
        """
        pass


if __name__ == '__main__':
    murmur = TweetMurmurs(
        consumer_key='VFbtuufO4wBzpfeDS6xEXd0Td',
        consumer_secret='k2Ui7lDpX8iHAgQiAOSxm3FyRvUl9CMQzKYa5ZHSNd1VUk73kj',
        access_token_key='1029806395376394240-CjX9utgkBv2IuScfqVJz7ag1govYpg',
        access_token_secret='Rikyg9UQMRYG2sDG6Ak8UGLldL52rQoJCHWqkXfnKfUep'
        )

    print(murmur.get_all_tweets())