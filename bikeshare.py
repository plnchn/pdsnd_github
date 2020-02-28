"""
Script file used to launch analysis of bike sharing data
Udacity Nano Degree
2020-02
"""
import time
import pandas as pd
import numpy as np
import re  ## Regexp

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
WEEKDAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city = ''
    while not city:
        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city = input("Which city do you want data for: 1) Chicago, 2) New York City or 3) Washington\n?  ")
        if re.match('\d',city):
            if city == '1':
                city = 'Chicago'
            elif city == '2':
                city = 'New York City'
            elif city == '3':
                city = 'Washington'
        city = city.lower()
        if city not in CITY_DATA:
            print('Unknown city',city,'!? Try Again...')
            city = ''  # make empty to provoke WHILE loop iteration
        #else:
        #    # Good this looks like a city for which we have data
        #    #print('DEBUG: Found city',city) # DEBUG do nothing

    # get user input for month (all, january, february, ... , june)
    month = ''
    while not month:
        month = input("Which month to analyse (all, January, February, ..., June)\n?  ")
        month = month.lower()
        if not month:
            print('Month left empty - assuming no filtering desired.')
            month = 'all'
        elif month != 'all':
            if re.match('\d+',month):
                # Convert numeric month to string
                numMon = int(month)
                if numMon <= len(MONTHS):
                    month = MONTHS[numMon-1] ## Months are 1-based
                    print('Mapped num month',numMon,'to string',month)
            if month not in MONTHS:
                print('Unknown month',month,'. Leave empty or type "all" if no filtering desired')
                month = ''  # make empty to provoke WHILE loop iteration
        #print('DEBUG: Month is',month)


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while not day:
        day = input("Which day of week to analyse (all, Monday, Tuesday...)\n?  ")
        day = day.lower()
        if not day:
            print('Weekday left empty - assuming no filtering desired.')
            day = 'all'
        elif day != 'all':
            if day not in WEEKDAYS:
                # try and match to shortname
                WEEKDAYSshort = [ x[0:3] for x in WEEKDAYS ]  # 'mon', 'tue', ...
                if day[0:3] in WEEKDAYSshort:
                    idxday = WEEKDAYSshort.index(day[0:3])
                    day = WEEKDAYS[idxday]
                else:
                    day = ''  # make empty to provoke WHILE loop iteration
        #print('DEBUG: Day is',day)

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
    print('Importing sharing data for:',city.title())
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month  ## 1:Jan, 2:Feb, ... 6:Jun
    df['day_of_week'] = df['Start Time'].dt.dayofweek  # 0:Mo, 1:Tu, ... 6:Su


    # filter by month if applicable
    month = month.lower()
    if month != 'all':
        # use the index of the months list to get the corresponding int
        idxmonth = MONTHS.index(month) + 1  # add one because January is "1" in pd
        # filter by month to create the new dataframe
        df = df[ df['month']==idxmonth ]
        print('Month filtering active and set to',month.title())
    else:
        print('Month filtering inactive.')

    # filter by day of week if applicable
    #day = day.lower()[0:3]
    if day != 'all':
        idxday = WEEKDAYS.index(day)
        # filter by day of week to create the new dataframe
        df = df[ df['day_of_week']==idxday ]
        print('Week-day filtering active and set to',WEEKDAYS[idxday].title())
    else:
        print('Week-day filtering inactive.')

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    monthMost = df['month'].mode()[0]

    print('Most travels in month:',MONTHS[monthMost-1].title())

    # display the most common day of week
    dayweekMost = df['day_of_week'].mode()[0]
    print('Most travels on following week day:',WEEKDAYS[dayweekMost].title())

    # display the most common start hour
    df_startHour = pd.to_datetime(df['Start Time']).dt.hour
    strtHrMost = df_startHour.mode()[0]
    print('Most travels in this hour:',strtHrMost)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    # prefStart = df['Start Station'].mode()[0]
    #print('Most used Start Station:',prefStart)
    prefStart = df['Start Station'].value_counts()
    print('Most used Start Station: "{}" ({} times)'.format(
          prefStart.idxmax(),
          prefStart.max()
          ) )

    # display most commonly used end station
    #prefEnd = df['End Station'].mode()[0]
    #print('Most used End Station:',prefEnd)
    prefEnd = df['End Station'].value_counts()
    print('Most used End Station: "{}" ({} times)'.format(
          prefEnd.idxmax(),
          prefEnd.max()
          ) )

    # display most frequent combination of start station and end station trip
    StartStopSerie = df.groupby(['Start Station','End Station']).size()
    StartStopSerie_maxStations = StartStopSerie.idxmax()
    StartStopSerie_maxCount = StartStopSerie.max()
    print('Most common ride is "{}" --> "{}" ({} times)'.format(
            StartStopSerie_maxStations[0],
            StartStopSerie_maxStations[1],
            StartStopSerie_maxCount)
         )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travelTimeTot = df['Trip Duration'].sum()
    print('Total travel time is:',prettyprint_duration(travelTimeTot))

    # display mean travel time
    travelTimeMean = df['Trip Duration'].mean()
    print('Mean travel time is:',prettyprint_duration(travelTimeMean))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def prettyprint_duration(mytime):
    """Converts given integer argument "mytime" in seconds to a string HH:MM:SS"""
    days, rem = divmod(mytime, 3600*24)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)
    out = ''
    if days > 0:
        out = "{}days ".format(int(days))
    out = out + "{:0>2}h {:0>2}min {:0>2}sec".format(int(hours),int(minutes),int(seconds))
    return out


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('This is how often each User Type has used the service:')
    #print(df['User Type'].value_counts())
    prettyprint_series(df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df:
        print('This is how often each Gender has used the service:')
        prettyprint_series(df['Gender'].value_counts())
    else:
        print('There is no Gender information in the given data set')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        df_birthyear = df['Birth Year']  # float
        print("Birth year, oldest: {}".format(int(df_birthyear.min())))
        print("Birth year, most recent: {}".format(int(df_birthyear.max())))
        print("Birth year, most found: {}".format(int(df_birthyear.mode()[0])))
    else:
        print('There is no Birth Year information in the given data set')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def prettyprint_series(myseries):
    for counter, value in enumerate(myseries):
        print(" - ",myseries.axes[0][counter], ":", value)

def main():
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        city, month, day = get_filters()
        # Use following line for test purposes without user interaction
        # city,month,day = 'chicago','april','all'
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOK, you want to stop. That's fine with me.")
    else:
        print('Hope you enjoyed the analysis and found no flaws ;-)')
