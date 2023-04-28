import time
import pandas as pd
import numpy as np
import random
import os

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let\'s explore some US bikeshare data!\n When you get bored just type 'Quit'")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_list = ['New York City', 'Chicago', 'Washington', 'random']
    
    while True:
      city = input("\nPlease enter one of the cities "+ str(city_list[ :3]) +" .\If you want me to choose for you type 'Random'\n").title()
      
      if city == ("quit".title()):
        quit()
      elif city == ("random".title()):
        random_city = random.randint(0, 2)
        city = city_list[random_city]
        break
      elif city not in city_list:
        print("This city is not in the database. Try again")
        continue
      else:
        break

    # get user input for month (all, january, february, ... , june)
    months_list = ['January', 'February', 'March', 'April', 'May', 'June', 'All']

    while True:
      month = input("\nPlease enter one of the months or type 'All' if you want all of them "+ str(months_list) +".\If you want me to choose for you type 'Random'\n").title()
      
      if month == ("quit".title()):
        quit()
      elif month == ("random".title()):
        random_month = random.randint(0, 6)
        month = months_list[random_month]
        break
      elif month in months_list:
        break
      else:
        print("This month is not in the database. Try again")
        continue


    # get user input for day of week (all, monday, tuesday, ... sunday)
    days_list = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'All']
    
    while True:
      day = input("\nPlease enter one of the week day or type 'All' if you want all of them "+ str(days_list) +"\nor enter 'Random' if you want me to choose for you\n").title()
      
      if day == ("quit".title()):
        quit()
      elif day == ("random".title()):
        random_day = random.randint(0, 7)
        day = days_list[random_day]
        break
      elif day in days_list:
        break
      else:
        print("This day of the week is not in the database. Try again")
        continue   
    
    

    print('-'*40)
    print(" Your choices: city -",city,", month -",month, ", day of the week -",day)
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    
    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    print('Most common Month:', common_month)

    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most common day of week:', common_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most common start Hour:', common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most common start station:', common_start_station)
    
    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most common end station:', common_end_station)

    # display most frequent combination of start station and end station trip 'that was hard one :D
    common_combination = df.groupby(['Start Station','End Station']).size().sort_values(ascending=False).head(3)
    print('Top 3 Most common combination of start and end station:\n', common_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def convert_sec(seconds):
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    time_conv = "{:02d}:{:02d}:{:02d}".format(int(hours), int(minutes), int(seconds))
    return time_conv

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    from time import strftime
    from time import gmtime
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time in HH:MM:SS', convert_sec(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time in HH:MM:SS', convert_sec(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    try:
      user_types = df['User Type'].value_counts()
      print('User types:\n', user_types)
    except:
      print("\nUser types:\nNo data available for this filters.")

    # Display counts of gender
    try:
      gender_types = df['Gender'].value_counts()
      print('\nGender types:\n', gender_types)
    except:
      print("\nGender types:\nNo data available for this filters.")

    # Display earliest, most recent, and most common year of birth
    try:
      earliest_year = df['Birth Year'].min()
      print('\nEarliest year:', earliest_year)
    except:
      print("\nEarliest year:\nNo data available for this filters.")

    try:
      most_recent_year = df['Birth Year'].max()
      print('\nMost recent year:', most_recent_year)
    except:
      print("\nMost recent year:\nNo data available for this filters.")

    try:
      most_common_year = df['Birth Year'].value_counts().idxmax()
      print('\nMost common year:', most_common_year)
    except:
      print("\nMost common year:\nNo data available for this filters.")

    try:
      sum_year = df['Birth Year'].sum()
      count_year = df['Birth Year'].value_counts()
      print('\nAverage year year:', (sum_year/avg_year))
    except:
      print("\nAverage year:\nNo data available for this filters.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    row_data = input("Please enter 'Yes' if you like to view 5 rows of data?\n").title()
    x = 5
    while (row_data == 'Yes'):
        print(df.head(x))
        x = x+5
        row_data = input("Please enter 'Yes' if you like to add next 5 rows\n").title()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
        

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
