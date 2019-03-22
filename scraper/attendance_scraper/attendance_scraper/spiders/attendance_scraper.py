import re

import pandas as pd
import scrapy


class AttendanceSpider(scrapy.Spider):
    """Get the information about all the games we need."""

    name = "attendance"
    base_url = 'https://www.baseball-reference.com'

    def __init__(self, file_name, **kwargs):
        """Load the Correct Games file."""
        self.file_name = file_name
        super().__init__(**kwargs)

    def start_requests(self):
        """Load the game list and scrape each game result page."""
        games = pd.read_json(
            path_or_buf='../../data/' + self.file_name + '.jl', lines=True)
        # the >1000 drops playoff games that are breaking things :(
        for slug in (games[games.date > 1000].boxscore_link).unique():
            yield scrapy.Request(url=self.base_url+slug,
                                 callback=self.parse)

    def parse(self, response):
        """Extract stats from the game pages."""
        boxscore_link = response.url.replace(self.base_url, '')
        messy_html_blob = response.css('div.section_wrapper')[
            2].css('*')[0].get()
        html_lines = messy_html_blob.split("\n")
        # I ran into some weird blockers dealing with the HTML object where
        # the good stuff was located so please pardon this janky/ugly regex
        if len(html_lines) == 17:
            offset = 0
        else:
            offset = 1
        try:
            attendance = re.findall('\d+(?:,\d+)*(?:\.\d+)?',
                                    html_lines[10 + offset])[0].replace(',', '')
        except IndexError:
            attendance = 'Not Given'
        try:
            start_time = re.findall(
            '(?<=Time of Game:</strong> )(.*)(?=.<)', html_lines[9 + offset])[0]
        except IndexError:
            start_time = ''
        try:
            field_condition = re.findall('(?<=<div><strong>Field Condition:</strong> )(.*)(?=.<)',
                                         html_lines[11 + offset])[0]
        except IndexError:
            field_condition = ''
        try:
            temperature = re.findall('\\d+', html_lines[12 + offset])[0]
        except IndexError:
            temperature = ''
        try:
            weather_description = re.findall(
                '(?=,)(.*)(?=.</div>)', html_lines[12 + offset])[0].split(', ')[-1]
        except IndexError:
            weather_description = ''
        yield {
            'boxscore_link': boxscore_link,
            'attendance': attendance,
            'start_time': start_time,
            'field_condition': field_condition,
            'temperature': temperature,
            'weather_description': weather_description,
        }
