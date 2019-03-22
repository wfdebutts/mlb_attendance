import re

import scrapy


class GamesSpider(scrapy.Spider):
    """Get the information about all the games we need."""
    name = "games"

    def __init__(self, start_year=2018, **kwargs):
        """Generate the Date range needed."""
        self.years = [year for year in range(int(start_year), 2019)]
        super().__init__(**kwargs)

    def start_requests(self):
        """Get the HTML results for each year of game schedules we want."""
        urls = ["https://www.baseball-reference.com/leagues/MLB/{year}-schedule.shtml"
                .format(year=year) for year in self.years]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """Extract list of game slugs from the page."""
        for game in response.css("p.game"):
            yield {
                'away_team': game.css('a::text')[0].get(),
                'home_team': game.css('a::text')[1].get(),
                'boxscore_link': game.css('a')[2].get().split("\"")[1],
                'date': re.findall('\\d+', game.css('a')[2].get())[0][:-1]
            }
