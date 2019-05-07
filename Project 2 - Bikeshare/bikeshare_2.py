import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

def get_filters():

    print('Hello! Let\'s explore some US bikeshare data!')
    city = input('Enter City name: ').lower()

    while city not in ('new york city', 'washington', 'chicago'):
        print("OPS! Wrong input (Chicago/Washington/NewYork)")
        city = input('Enter City name: ').lower()
    # get user input for month (all, january, february, ... , june)
    month = input('Enter Month: ').lower()

    while month not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
        print("OPS! Invalid input")
        month = input('Enter Month: ').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Enter Day: ').lower()

    while day not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
        print("OPS! Invalid input")
        day = input('Enter Day: ').lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most Common Month:', common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most Common Day of Week:', common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour= df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station:', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most Common End Station:', common_end_station)

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'].str.cat(df['End Station'], sep=' - ')
    common_trip = df['Trip'].mode()[0]
    print('Most Common Trip Stations:', common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    total_time_in_hrs = (total_time/60).round(2)
    print("Total travel time(in hours):", total_time_in_hrs)

    # display mean travel time
    average_time = df['Trip Duration'].mean().round(2)
    print("Average travel time(in minutes):", average_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Users Types Number: \n", user_types)

    # Display counts of gender
    if(city != 'washington'):
        user_gender = df['Gender'].value_counts()
        print("User Gender Number: \n", user_gender)

    # Display earliest, most recent, and most common year of birth
        earliest_year = df['Birth Year'].min()
        print("Earliest Birth Year: ", earliest_year)

        recent_year = df['Birth Year'].max()
        print("Most Recent Birth Year: ", recent_year)

        common_year = df['Birth Year'].mode()
        print("Most Common Birth Year: ", common_year)

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


def display_data(df):
    data = input('\nDo you want to see raw data? Enter yes or no.\n')
    i = 0
    while data.lower() != 'no':
        print(df.iloc[i:i+5])
        i += 5
        data = input('\nDo you want to see raw data? Enter yes or no.\n')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
