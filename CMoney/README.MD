This project uses selenium webdriver to automatically head to website, scroll down to load the whole information, and expand the whole article by clicking corresponded buttons.
To cope with the anti-crawler system, the project will reload the page by changing the position and return to the original spot in 0.5 second.
After webdriver finishes its job, use beautifulsoup to load the full HTML page and seperate them into each articles.
Create lists to store the needed data and turn them into a dictionary. Finally, use pandas to reform the dictionary and read them into a csv file.
