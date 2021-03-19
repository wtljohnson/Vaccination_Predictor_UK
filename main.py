import time
from selenium import webdriver
import re
from datetime import date
from datetime import timedelta


def main():
    data = get_data()
    clean_data = data_cleaner(data)
    calculator(clean_data, 31800000, 2286572)  # Goal currently top 4 categories, will amend for whole pop.
    print("\n")


def get_data():
    data_list = []
    driver_path = "A:/ProgramData/chromedriver_win32/chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get("https://coronavirus.data.gov.uk/details/vaccinations")
    time.sleep(1)  # Wait for page to load
    driver.find_element_by_css_selector("button[aria-label='Data']").click()  # Click data button to load table
    time.sleep(1)  # Wait for table to load
    full_table = driver.find_element_by_tag_name("tbody")
    table_rows = full_table.find_elements_by_tag_name("tr")
    for row in table_rows:
        all_data = row.find_elements_by_tag_name("td")
        specific_data = all_data[1].text  # Second row is all the data needed
        data_list.append(specific_data)
    del data_list[-1]  # Removed as first day was N/A
    driver.quit()
    return data_list


def data_cleaner(raw_data):
    temp_data = []
    for value in raw_data:
        no_commas = re.sub(",", "", value)
        int_value = int(no_commas)
        temp_data.append(int_value)
    return temp_data


def calculator(clean_data, goal, start):
    total_daily_sum = 0
    for value in clean_data:
        total_daily_sum += value
    amended_goal = goal - start - total_daily_sum

    # Yesterday's rate
    yesterday_rate = clean_data[0]
    yesterday_days_until_complete = amended_goal // yesterday_rate

    yesterdays_dates = date_adder(yesterday_days_until_complete)
    printer("yesterday's daily", yesterdays_dates[0], yesterdays_dates[1], "Yesterday's", yesterday_rate)

    # Total average daily rate
    tda_rate = total_daily_sum / len(clean_data)

    average_days_until_complete = amended_goal // tda_rate

    average_days_dates = date_adder(average_days_until_complete)
    printer("the total average daily", average_days_dates[0], average_days_dates[1], "Total daily average", tda_rate)

    # Last week's daily average rate
    last_week_sum = 0
    for i in range(7):
        last_week_sum += clean_data[i]
    week_dr = last_week_sum / 7

    week_dav_until_complete = amended_goal // week_dr

    week_dav_dates = date_adder(week_dav_until_complete)
    printer("last week's daily average", week_dav_dates[0], week_dav_dates[1], "Last week's daily average", week_dr)
    print(f"\tLast week's vaccinations: {last_week_sum:,}")



def date_adder(days_to_add):
    day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    completed_by = date.today() + timedelta(days=days_to_add)
    str_completed_by = completed_by.strftime("%d %b, %Y")
    weekday = day_name[completed_by.weekday()]
    return weekday, str_completed_by


def printer(rate_description, weekday, date_done, presented_data_description, presented_data):
    print("\n")
    print(f"If vaccinations continue at {rate_description} rate, they will be finished by: \n"
          f"\t{weekday}, {date_done}\n"
          f"\t{presented_data_description} vaccinations: {presented_data:,}")


main()
