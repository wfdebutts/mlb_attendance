I was curious to see if there was good dataset to try to understand MLB attendance, my basic google searches only found data at the season level and not the game level.  I felt like it could be an interesting dataset to play around in so I wrote a scraper for baseballrefference.com which nicely has information for the attendance for every MLB game since the 40s.  <b>I am not sure if this is a "okay" legal use of the baseball-refference data so please do no resell or use this data for business purposes without checking with the owners of baseball-refference.com </b>

<h2> Analysis </h2>
I didn't have time to try to make an attendance prediction model but my first thought would be to use some some combination of the following features:

<p></p>

<ul> - Stadium Capacity: Obviously we could expect higher attendance at larger statiums </ul>
<ul> - Weather: for teams with outdoor stadiums we could expect extreme temperatures, rain, or other factors to play a big role in how many go to game. </ul>

<ul> - Home and away team payroll.  This is effectively a proxy of both market size and star power which could determine interest in the game, it might be better to include basic census style economic data about the city is located in.  This sort of data could also be interesting in predicting ticket prices ... or creating some form of "deal score" for after market ticket prices</ul>

<ul> - Home team standings of the current seasons and the past season.  My guess would be people don't want to see games from teams out of playoff contention and or very bad or underwhelming teams.  There also could be interesting interaction effects with the payroll data.</ul>


<h2> Scraper </h2>

Inside of the scraper directory you will find the attendance_scraper directory that contains the Scrapy project used to extract attendence and game data from baseballrefference.com.  It has the following directory structure, a lot of this is Scrapy broiler plate most of my work is in /spiders
'''
scrapy.cfg            # deploy configuration file

attendance_scraper/             # project's Python module, you'll import your code from here
    __init__.py

    items.py          # project items definition file

    middlewares.py    # project middlewares file

    pipelines.py      # project pipelines file

    settings.py       # project settings file

    spiders/          # actual scraping spiders
        __init__.py

In order to generate the list of games the following command from `scraper/attendance_scraper`

`scrapy crawl games -a start_year=<desired start year> -o ../../data/games_list.jl`

I checked and the data goes back to MLBs founding in 1903! However attendance data only started getting added in the mid 1930's so I wouldn't go back any farther than about 1935.

the -o file will decide what format your output will be in and what directory it lives in. The current command will place a JSON lines file in /data.

In order to get the game attendance out of for these games run
`scrapy crawl attendance -a file_name=games_list.jl -o ../../data/<output_name>.jl`

This might take a few minutes to run.  For your convience all games from the 2010 to 2018 seasons are already in the 2019s_attendence.jl file.

<h2> Tests </h2>

Tests are important.  While mocking a lot of the Scarpy objects and callback seemed a bit over the top for this sort of project.  In practice taking the time for doing this sort of thing is very important. 
