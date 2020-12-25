import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def input_Check (input_str,input_type):
    while True:
        input_read = input(input_str).lower()
        try:
            if input_read in ['all','chicago','new york city','washington'] and input_type == 1:
                break
            elif input_read in ['all','january','fabruary','march', 'april','may', 'june'] and input_type == 2:
                break
            elif input_read in ['all','monday','tuesday','wednesday', 'thursday', 'friday','saturday','sunday'] and input_type == 3:
                break
            else:
                if input_type == 1:
                    print("you must choose a valid city!")
                if input_type == 2:
                    print("you must choose a valid Month!")
                if input_type == 3:
                    print("you must choose a valid Day!")
        except ValueError:
            print("invalid data... ")
    return input_read

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    city = input_Check('choose requested city: chicago, new york city or washington?',1)
    month = input_Check('requested month? or pick "all"',2)
    day = input_Check('requested week day? or pick "all"',3)

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour
    # filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    com_month = df['month'].mode()[0]
    print('- The most common month is: \n",',com_month)
    com_day = df['day_of_week'].mode()[0]
    print('- The most common day of week is: \n",',com_day)
    com_hour = df["hour"].mode()[0]
    print('- The most common hour is: \n",',com_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    st_sta=df['Start Station'].mode()[0]
    print('- most commonly used start station is: \n',st_sta)
    end_sta = df['End Station'].mode()[0]
    print('- most commonly used end station is: \n',end_sta)
    freq_comb = df.groupby(['Start Station','End Station'])
    frequent = freq_comb.size().sort_values(ascending=False).head(1)
    print ('- most frequent combination of start station and end station trip is: \n',frequent)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel = df['Trip Duration'].sum()

    total_by_hours = total_travel / (60*60)
    total_travel_days = total_by_hours // 24
    total_travel_hours = total_by_hours % 24
    print('total travel time is: \n {total_travel_days} days \n {total_travel_hours} hours')
          
    mean_travel = df['Trip Duration'].mean()
    mean_by_hours = mean_travel / (60*60)
    mean_travel_days = mean_by_hours // 24
    mean_travel_hours = mean_by_hours % 24
    print('total travel time is: \n {mean_travel_days} days \n {mean_travel_hours} hours')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df,city):
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    usr_typ = df['User Type'].value_counts()
    print('counts of user types is: \n',usr_typ)
    if city != "washington":
        print('- counts of Gender :')
        print(df['Gender'].value_counts())
        early=df['Birth Year'].min()
        print('- earliest year of birth is: ',early)
        rec= df['Birth Year'].max()
        print("most recent year of birth is: ",rec)
        common_year=df['Birth Year'].mode()[0]
        print('most common year of birth is: ',common_year)
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def display_data (df):
            print('\nCalculating display data...\n')
            start_time = time.time()
            view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
            if view_data.lower() == "yes":
                start_loc = 0
                while True:
                    print(df.iloc[start_loc:start_loc+5])
                    start_loc += 5
                    view_display = input('Do you wish to continue with next 5 rows?: Enter yes or no.\n ').lower()
                    if view_display != "yes":
                        break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data (df)
        
                        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
        main()
