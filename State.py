#Importing packages
import cloudscraper
from statistics import mean
import json

# Class to call and organize the data of each state
class State():

# Initiizer. Data retrieval is also called.
    def __init__(self, name, url):
        self.name = name
        self.url = url
        scraper = cloudscraper.create_scraper()
        response = scraper.get(self.url)
        self.data = response.json()

        # Code for retrieving json files
        # filename = f"data5500_mycode/hw5/json_file/{self.name}.json"
        # with open(filename, 'w', encoding='utf-8') as f:
        # json.dump(self.data, f, indent=2, ensure_ascii=False)

# Prints data in desired format.
    def print_data(self):
        print("Name: " + self.name)
        print("Average number of new cases per day: " + str(round(self.daily_avg())))
        print("Date with the highest number of new cases: " + str(self.new_cases_max()))
        print("Date of last day with no new cases: " + str(self.last_no_new_cases_date()))
        print("The month and year that had the highest new cases: " + str(self.highest_new_cases_month()))
        print("The month and year that had the lowest new cases: " + str(self.lowest_new_cases_month()))

#Calculate daily average
    def daily_avg(self):
        
        daily_increases = []

        for day in self.data:
            daily_increases.append(day["positiveIncrease"])

        return mean(daily_increases)

#Find day with highest new cases
    def new_cases_max(self):
        highest = 0
        highest_day = 0
        for day in self.data:
            if (day["positiveIncrease"] > highest):
                highest = day["positiveIncrease"]
                highest_day = day["date"]
        return highest_day

#Find most recent day in data with no new cases
    def last_no_new_cases_date(self):
        last_day = 0
        for day in self.data:
            if (day["positiveIncrease"] == 0):
                last_day = day["date"]
        return last_day

#Find highest new casess month
    def highest_new_cases_month(self):
        cases_by_month = []
        cases = 0
        month = str(202103) #the starting month

        for day in self.data:
            if (str(day["date"])[:6] < month):
                cases_by_month.append(dict(cases = cases, monthDate = day["date"]))
                month = str(day["date"])[:6]
                cases = 0
            cases += day["positiveIncrease"]
        
        highest = 0
        highest_month = 0
        for month in cases_by_month:
            if (month["cases"] > highest):
                highest_month = month["monthDate"]
                highest = month["cases"]
        return str(highest_month)[:6]

#Find lowest new casess month
    def lowest_new_cases_month(self):
        cases_by_month = []
        cases = 0
        month = str(202103) #the starting month

        for day in self.data:
            if (str(day["date"])[:6] < month):
                cases_by_month.append(dict(cases = cases, monthDate = day["date"]))
                month = str(day["date"])[:6]
                cases = 0
            cases += day["positiveIncrease"]

        lowest = cases_by_month[1]["cases"]
        lowest_month = 0
        for month in cases_by_month:
            if (month["cases"] < lowest):
                lowest_month = month["monthDate"]
                lowest = month["cases"]
        return str(lowest_month)[:6]