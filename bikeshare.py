import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'data/chicago.csv',
              'new york city': 'data/new_york_city.csv',
              'washington': 'data/washington.csv' }

DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

DATA_COLUMNS = []

def get_filters(city = '', month = '', day = ''):
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    print('At any prompt you may enter [restart] to restart')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city == '':
        allowed_cities = {'CHI': 'Chicago', 'NYC': 'New York City', 'WDC': 'Washington'}
        user_input = input('What city would you like to analyze? [CHI, NYC, WDC].\n').upper()

        if user_input == 'RESTART':
            get_filters()

        city = ''

        if user_input in allowed_cities:
            city = allowed_cities[user_input]
        else:
            print("\n\nPlease enter a valid city.")

        
    # get user input for month (all, january, february, ... , june)
    while month == '':
        #allowed months including zero index 'ALL' for no filter
        allowed_months = {'ALL': 'All', 'JAN': 'January', 'FEB': 'February', 'MAR': 'March', 'APR': 'April', 'MAY': 'May', 'JUN': 'June'}
        print('\nWhat month would you like to analyze?')
        print('- Whole Month Name: March')
        print('- Three Character Abbreviation: MAR')
        print('- Month Number: 3')
        user_input = input('- 0 or ALL for All Available Months\n')

        try:
            user_input = int(user_input)
        except:
            user_input = user_input.upper()

        if isinstance(user_input, str):
            if user_input == 'RESTART':
                get_filters()

        # if input is a string check the allowed months
            user_input = user_input[:3]
            if user_input in allowed_months:
                month = allowed_months[user_input]

        else: 
        # if user input is less than 12 and less than the array of available months
            if user_input <= 12 and user_input < len(allowed_months):
                month = allowed_months[list(allowed_months)[user_input]]
        
        if month == '':
            print("\n\nPlease enter a valid month.")
            
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day == '':
        #allowed days of the week including zero index 'ALL' for no filter
        allowed_days = {'ALL': 'All', 'MON': 'Monday', 'TUES': 'Tuesday', 'WED': 'Wednesday', 'THU': 'Thursday', 'FRI': 'Friday', 'SAT': 'Saturday', 'SUN': 'Sunday'}
        print('\nWhat day of the week like to analyze?')
        print('- Whole Day Name: Wednesday')
        print('- Three Character Abbreviation: WED')
        print('- Weekday Number [Starting on Monday as 1]: 3')
        user_input = input('- 0 or all for All Available Weekdays\n')

        try:
            user_input = int(user_input)
        except:
            user_input = user_input.upper()

        if isinstance(user_input, str):
            if user_input == 'RESTART':
                get_filters()

            # if input is a string check the allowed weekdays
            user_input = user_input[:3]
            if user_input in allowed_days:
                day = allowed_days[user_input]

        else: 
        # if user input is less than 7 and less than the array of available days
            if user_input <= 7 and user_input < len(allowed_days):
                day = allowed_days[list(allowed_days)[user_input]]

        if day == '':
            print("\n\nPlease enter a valid day of the week.")


    print('-'*40)
    print('\nYou selected: City: {}, Month: {}, Day: {}\n'.format(city, month, day))
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

    print('\nGathering data...')
    city = city.lower()
    month = month.lower()
    day = day.lower()

    df = pd.read_csv(CITY_DATA[city])
    df.fillna(0)

    
    # convert the Start and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month)
    
        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe

        day = DAYS.index(day)
        df = df[df['day_of_week']==day]

    
    for c in list(df.columns):
        DATA_COLUMNS.append(c)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('-'*40)
    print('\nCalculating The Most Frequent Times of Travel...\n')    
    start_time = time.time()

    print('\nThe Most Frequent Times of Travel are:\n')

    # display the most common month
    if 'month' in DATA_COLUMNS:
        frequent_month = df['month'].mode()[0]
        print('Most Common Month: {}'.format(MONTHS[frequent_month].title()))

    # display the most common day of week
    frequent_day = df['day_of_week'].mode()[0]
    print('Most Common Day of the Week: {}'.format(DAYS[frequent_day].title()))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    frequent_hour = df['hour'].mode()[0]
    print('Most Common Hour: {}'.format(frequent_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    input('\nEnter to continue...')



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('-'*40)
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print('\nThe Most Frequent Popular Stations Are:\n')

    col = ''

    col = 'Start Station'
    if col in DATA_COLUMNS:
        # display most commonly used start station
        print('Most Popular Starting Station: {}'.format(df[col].mode()[0]))
    else:
        print('{} Data is Not Available'.format(col))
    
    # display most commonly used end station
    col = 'End Station'
    if col in DATA_COLUMNS:
        # display most commonly used ending station
        print('Most Popular Ending Station: {}'.format(df[col].mode()[0]))
    else:
        print('{} Data is Not Available'.format(col))

    # display most frequent combination of start station and end station trip

    if 'Start Station' in DATA_COLUMNS and 'End Station' in DATA_COLUMNS:
        df['End Points'] = df['Start Station'] + ' ' + df['End Station']
        frequent_end_points = df['End Points'].mode()[0]
        print('Most Popular End Points: {}'.format(frequent_end_points))
    else:
        print('Start and End Station Data is Not Available')


    print("\nThis took %s seconds." % (time.time() - start_time))
    input('\nEnter to continue...')

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('-'*40)
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    col = ''

    col = 'Trip Duration'
    if col in DATA_COLUMNS:
        print('Total Travel Time of All Trips: {} seconds'.format(df[col].sum()))

        # display mean travel time
        print('Mean Average Travel Time of All Trips: {} seconds'.format(df[col].mean()))
    else:
        print('{} Data is Not Available'.format(col))


    print('\nThis took %s seconds.' % (time.time() - start_time))

    input('\nEnter to continue...')


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('-'*40)
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    col = ''

    # Display counts of user types
    col = 'User Type'
    if col in DATA_COLUMNS:
        print('Count of Users by Type')
        print(df[col].value_counts())
    else:
        print('{} Data is Not Available'.format(col))

    # Display counts of gender
    col = 'Gender'
    if col in DATA_COLUMNS:
        print('Count of Users by {}'.format(col))
        print(df[col].value_counts())
    else:
        print('{} Data is Not Available'.format(col))

    # Display earliest, most recent, and most common year of birth
    col = 'Birth Year'
    if col in DATA_COLUMNS:
        print('Youngest User Was Born In {}'.format(df[col].max()))
        print('Oldest User Was Born In {}'.format(df[col].min()))
        print('Our Users Are Most Commonly Born In {}'.format(df[col].mode()[0]))
    else:
        print('{} Data is Not Available'.format(col))

    print("\nThis took %s seconds." % (time.time() - start_time))
    input('\nEnter to continue...')

def output_control(df):
    output_display = 5

    print('Would you like to view the raw data?')
    user_input = input('- "Yes" to Display raw data [Default No]:')  
    if len(user_input) > 0 and user_input[0].upper() == 'Y':
        print('\nTruncate data output?')
        user_input = input('- Rows of data to display [Default 10]:')
    
        if len(user_input) > 0:
            try:
                user_input = int(user_input)
            except:
                user_input = user_input[0].upper()

            if isinstance(user_input, int):
                output_display = user_input



        pd.set_option('display.max_rows', output_display)
        pd.set_option('display.max_columns', None)
        print(df)



def main():
    while True:
        df = ''
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        output_control(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if len(restart) == 0 or restart[0].upper() != 'Y':
            break


if __name__ == "__main__":
	main()
