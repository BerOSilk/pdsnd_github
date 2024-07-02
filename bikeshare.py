import time
import pandas as pd
import numpy as np

# the city data that we will be using in this project
CITY_DATA = { 'chicago'       : 'chicago.csv',
              'new york city' : 'new_york_city.csv',
              'washington'    : 'washington.csv' 
            }

def input_month():

    """
    Asks user to specify the month

    Returns: 
        (str) month - name of the month to filter by, or "all" to apply no month filter

    """

    month = None

    while True:
    
        print('Which month would you like to see for? ', ['All','January', 'February', 'March', 'April', 'May', 'June'], ' - the input is case insensitive')
        month = input().lower()
        if month in ['all','january', 'february', 'march', 'april', 'may', 'june']:
            break
        print('Invalid input')
    
    return month

def input_day():

    """
        Asks user to specify the day

        Returns: 
            (str) day - name of the day of week to filter by, or "all" to apply no day filter

    """

    day = None

    while True:
    
        print('Which day would you like to see for? ', ['All', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], ' - the input is case insensitive')
        day = input().lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        print('Invalid input')
    return day

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    city = None

    while True:
    
        print('Which city would you like to see for ? ',['Chicago', 'New york city', 'Washington'], ' - the input is case insensitive')
        city = input().lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        print('Invalid input')

    # Asks user to choose between filtring the data by month, day, both, or none of them.
    time_filter = None

    while True:

        print('Would you like to filter by month, day, both, or none? - the input is case insensitive')
        time_filter = input().lower()
        if time_filter in ['month', 'day', 'both', 'none']:
            break
        print('Invalid input')

    month = None
    day = None

    if time_filter == 'month':
        month = input_month()
    elif time_filter == 'day':
        day = input_day()
    elif time_filter == 'both':
        month = input_month()
        day = input_day()

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

    # Convert the day into a specific number so pandas dataframe can understand it.
    days = {'sunday': 1, 'monday': 2, 'tuesday': 3,'wednesday': 4, 'thursday': 5, 'friday': 6, 'saturday': 7}

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_of_week


    if month != 'all' and month != None:
        months = ['january', 'february','march', 'april','may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all' and day != None:
        df = df[df['day_of_week'] == days[day]]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The most common month: ', df['month'].mode()[0])

    # display the most common day of week
    df['day'] = df['Start Time'].dt.day
    print('The most common day: ', df['day'].mode()[0])

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('The most common hour: ', df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].value_counts().sort_values(ascending=False)
    print('The most common used start station: ', common_start_station.index[0], ' count: ', common_start_station.iloc[0])

    # display most commonly used end station
    common_end_Station = df['End Station'].value_counts().sort_values(ascending=False)
    print('The most common used end station: ', common_end_Station.index[0], ' count: ', common_end_Station.iloc[0])

    # display most frequent combination of start station and end station trip
    df['combined_start_end_stations'] = df['Start Station'] + ' | ' + df['End Station']
    common_start_end_station = df['combined_start_end_stations'].value_counts().sort_values(ascending=False)
    print('The most frequent combination of start and end station: ', common_start_end_station.index[0], ' count: ', common_start_end_station.iloc[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['hour'] = df['Start Time'].dt.hour
    df['minute'] = df['Start Time'].dt.minute
    df['second'] = df['Start Time'].dt.second

    # display total travel time
    total_travel_time = np.sum(df['hour']) * 3600 + np.sum(df['minute']) * 60 + np.sum(df['second'])
    print('total travel time: ', total_travel_time, ' second')
    # display mean travel time
    mean_travel_time = np.mean(total_travel_time)
    print('mean travel time: ', mean_travel_time, ' second')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_types = df['User Type'].value_counts()
    print('\nCount of User Types: \n')
    print(count_user_types)
    print()

    if city != 'washington':
        # Display counts of gender
        count_gender = df['Gender'].value_counts()
        print('\nCount of Gender: \n')
        print(count_gender)
        print()

        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = df['Birth Year'].min()
        recent_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].value_counts().sort_values(ascending=False)

        print('earliest birth year: ', earliest_birth_year)
        print('most recent birth year: ', recent_birth_year)
        print('common birth year: ', common_birth_year.index[0], ' count: ', common_birth_year.iloc[0])
    else:
        print('Washington does not support gender or birth year\n')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_data(df):
    print('\n Would you like to view 5 rows of data? Enter yes or no')
    start_index = 0
    while True:
        check = input().lower()
        if check == 'no':
            break
        elif check == 'yes':
            print(df.iloc[start_index:start_index+5])
            print('-'*40)
            print('\n Would you like to view the next 5 rows of data? Enter yes or no')
            start_index += 5
            continue
        else:
            print('Invalid input')
            continue

def main():

    restart = 'yes'
    df = None
    while restart == 'yes':
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
    
    view_data(df)


if __name__ == "__main__":
	main()
    

   

