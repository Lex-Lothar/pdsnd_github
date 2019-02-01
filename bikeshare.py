import numpy as np
import pandas as pd

#Dictionary for loading the .csv files (The paths refer to my local folder structure)

load_files = {1: 'chicago.csv',
              2: 'new_york_city.csv',
              3: 'washington.csv'}

#Dictionary storing text elements for user input prompts

prompts = { 'raw_trips': '\nHere are the trips {} to {}.',
            'except_error':'\nI\'m sorry, I don\'t understand the input. Please only select {}.',
            'range_error':'\nOoops, there doesn\'t seem to be a match for your input {}. Please only select {}.',
            'enter':'\n\nPlease type {}: ',            
            'success':'Thank you for choosing {}.',
            'cities':['\n\n  Chicago     [1]\n  New York    [2]\n  Washington  [3]', 
                     ['Chicago', 'New York', 'Washington'],
                     range(1,4),
                     '1, 2 or 3',
                     '\n\n\nWhich City would you like to take a closer look at?'],
            'time_filter':['\n\n  no        [1]\n  by month  [2]\n  by day    [3]\n  by both   [4]',
                          ['no time filter', 'to filter by month only', 'to filter by day only', 'to filter by month and day'],
                          range(1,5),
                          'a number between 1 and 4',
                          '\n\n\nWould you like to filter by time?'],
            'months':['\n\n  January   [1]       February  [2]       March     [3]\n  April     [4]       May       [5]       June      [6]',
                     ['January', 'February', 'March', 'April', 'May', 'June'],
                     range(1,7),
                     'a number between 1 and 6',
                     '\n\n\nWhich month would you like to filter by?'],
            'days':['\n\n  Monday     [1]       Tuesday     [2]       Wednesday  [3]\n  Thursday   [4]       Friday      [5]       Saturday   [6]\n  Sunday     [7]',
                   ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                   range(1,8),
                   'a number between 1 and 7',
                   '\n\n\nWhich day would you like to filter by?'],
            'raw_1':['\n\n  Yes  [1]\n  No   [2]',
                    ['to show individual trips', 'not to show individual trips'],
                    range(1,3),
                    '1 or 2',
                    '\n\n\nWould you like to display data for indivdual trips 5 at a time?'],
            'raw_2':['\n\n  Yes  [1]\n  No   [2]',
                    ['to show 5 more trips', 'not to show any more trips'],
                    range(1,3),
                    '1 or 2',
                    '\n\n\nWould you like to check out 5 more trips?'],
            'start_over':['\n\n  Start over  [1]\n  Stop        [2]',
                         ['to start another analysis', 'to stop for now'],
                         range(1,3),
                         '1 or 2',
                         '\n\n\nHow would you like to continue?']}

#Output text elements

pop_txt = 'The most popular {} is {}.'
time_txt = 'The {} travel time is {} {}.'
year_txt = 'The {} Birth Year is {}'
gender_txt = 'There are {} female and {} male users'
type_txt = 'There are {} subscribers and {} customers'
header_time = '\n'+'='*15+'\nTIME STATISTICS'+'\n'+'='*15
header_station = '\n'+'='*18+'\nSTATION STATISTICS'+'\n'+'='*18
header_trip = '\n'+'='*15+'\nTRIP STATISTICS'+'\n'+'='*15
header_user = '\n'+'='*19+'\nCUSTOMER STATISTICS'+'\n'+'='*19

#Defined functions

def check_input(options):
    """Checks for valid user input and handles exceptions
       Input: Text elements from the prompts dictionary
       Output: User input variable."""    
    while True: 
        try:            
            user_input = int(input('{}{}{}'.format(options[4], options[0],prompts['enter'].format(options[3]))))            
            if user_input not in options[2]: 
                print(prompts['range_error'].format(user_input, options[3]))
                continue
            print('_'*(30 + len(options[1][user_input - 1])))
            print('\n* ','{}'.format(prompts['success'].format(options[1][user_input - 1])),' *')
            print('_'*(30 + len(options[1][user_input - 1])))
            break
        except:
            print(prompts['except_error'].format(options[3]))
    return user_input

def raw_rows(start, end):
    """Function to print defined rows of raw data from a DataFrame
       Input: start and end index
       Output: start and end index increased by 5"""
    print('\nHere are the trips {} to {}.\n'.format(start + 1, end))
    print(df[start:end])
    start += 5
    end += 5
    return start, end

#Loop to restart if requested at the end of the process
again = 1
while again == 1:

#Step 1: Define city based on user input
    city = check_input(prompts['cities'])

    #Create DataFrame based on user selection. Add required columns.
    df = pd.read_csv(load_files.get(city))
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day of week'] = df['Start Time'].dt.weekday
    df['Hour of day'] = df['Start Time'].dt.hour
    df['Trip'] = 'from ' + df['Start Station'] +' to ' + df['End Station']

    #Text elements and data for the output statistics with a condition for the unavailable data for Washington
    pop_m = ('month', prompts.get('months')[1][df['Month'].mode()[0] - 1])
    pop_d = ('day of the week', prompts.get('days')[1][df['Day of week'].mode()[0] - 1])
    pop_hr = ('hour of the day', df['Hour of day'].mode()[0])
    pop_sst = ('start station', df['Start Station'].mode()[0])
    pop_est = ('end station', df['End Station'].mode()[0])
    pop_tr = ('trip', df['Trip'].mode()[0])
    t_time = ('total', int((df['Trip Duration'].sum() / 3600)), 'hours')
    a_time = ('average', int((df['Trip Duration'].mean() / 60)), 'minutes')
    if city != 3:
        min_y = ('earliest', int(df['Birth Year'].min()))
        max_y = ('most recent', int(df['Birth Year'].max()))
        avg_y = ('average', int(df['Birth Year'].mean()))
        m_count = df['Gender'].value_counts()[0]
        f_count = df['Gender'].value_counts()[1]
    s_count = df['User Type'].value_counts()[0]
    c_count = df['User Type'].value_counts()[1]
    
#Step 2 a: Checks for time filter preferences
    time_filter = check_input(prompts['time_filter'])

    month = None
    day = None

#Step 2 b: Based on filter preferences user is asked to set time filters and the DataFrame is filtered accordingly
    if time_filter == 2:
        month = check_input(prompts['months'])
        df = df[df['Month'] == month - 1]
        filter_prompt = '\nTime filter applied: month = {}.'.format(prompts['months'][1][month - 1])  
    elif time_filter == 3:
        day = check_input(prompts['days'])
        df = df[df['Day of week'] == day - 1]
        filter_prompt = '\nTime filter applied: day of the week = {}.'.format(prompts['days'][1][day - 1])     
    elif time_filter == 4:
        month = check_input(prompts['months'])
        day = check_input(prompts['days'])
        df = df[(df['Month'] == month - 1) & (df['Day of week'] == day - 1)]
        filter_prompt = '\nTime filter applied: month = {}, day of the week = {}.'.format(prompts['months'][1][month - 1], prompts['days'][1][day - 1])     
    else:
        filter_prompt = '\nNo time filter applied'

    #Printing statistics based on the filtered DataFrame    
    print('\n'*5 + filter_prompt)
    print(header_time + '\n')
    if not month:
        print(pop_txt.format(pop_m[0], pop_m[1]))
    if not day:
        print(pop_txt.format(pop_d[0], pop_d[1]))
    print(pop_txt.format(pop_hr[0], pop_hr[1]))
    print(header_station + '\n')
    print(pop_txt.format(pop_sst[0], pop_sst[1]))
    print(pop_txt.format(pop_est[0], pop_est[1]))
    print(pop_txt.format(pop_tr[0], pop_tr[1]))        
    print(header_trip + '\n')
    print(time_txt.format(t_time[0], t_time[1], t_time[2]))
    print(time_txt.format(a_time[0], a_time[1], a_time[2]))
    print(header_user + '\n')
    if city != 3:
        print(gender_txt.format(f_count, m_count))
    print(type_txt.format(s_count, c_count))
    if city != 3:
        print(year_txt.format(min_y[0], min_y[1]))
        print(year_txt.format(max_y[0], max_y[1]))
        print(year_txt.format(avg_y[0], avg_y[1]))
         
#Step 3: Raw data is printed based on user preference
    start, end = 0, 5   
    if check_input(prompts['raw_1']) == 1 and end < df['Start Time'].count():
        start, end = raw_rows(start, end)              
        while check_input(prompts['raw_2']) == 1:            
            start, end = raw_rows(start, end)   

#Step 4: User selection to end or restart
    again = check_input(prompts['start_over'])