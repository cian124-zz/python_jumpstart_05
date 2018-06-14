import collections
import requests
import bs4

Weather = collections.namedtuple('Weather', 'temp, scale, condition, location')
Location = collections.namedtuple('Location', 'country, state, city')


def draw_header():
    print('--------------------')
    print('    WEATHER APP')
    print('--------------------')
    print('')


def get_location():
    country = input('Please enter a country code: ')
    if country == 'us':
        state = input('Please enter the state code: ')
    else:
        state = None
    city = input('Please enter a city: ')
    city = city.replace(' ', '-').lower()
    loc = Location(country, state, city)
    return loc


def get_weather(loc):

    if loc.state:
        req = requests.get('https://www.wunderground.com/weather/{}/{}/{}'.format(loc.country, loc.state, loc.city))
    else:
        req = requests.get('https://www.wunderground.com/weather/{}/{}'.format(loc.country, loc.city))
    soup = bs4.BeautifulSoup(req.text, "html.parser")

    temp = soup.find(class_='wu-unit-temperature').find(class_='wu-value').get_text()
    scale = soup.find(class_='wu-unit-temperature').find(class_='wu-label').get_text()
    scale = cleanup_text(scale)
    condition = soup.find(class_='condition-icon').get_text()
    condition = cleanup_text(condition)
    city = soup.find(class_='region-content-header').find('h1').get_text()
    city = cleanup_text(city)

    weather_info = Weather(temp, scale, condition, city)
    return weather_info


def print_weather(weather):
    print("Looks like it's {}{} and {} in {}".format(weather.temp, weather.scale, weather.condition, weather.location))
    return


def cleanup_text(text: str):
    if not text:
        return text

    text = text.strip()
    return text


def main():
    draw_header()
    loc = get_location()
    weather_info = get_weather(loc)
    print_weather(weather_info)
    return


if __name__ == '__main__':
    main()
