# USEFUL UTILITY FUNCTIONS FOR RUNNER CODE
import os
import time

# sets the current time if timezone is provided
# prints the optiooal prompt plus the current time
# ============
# sample usage:
# import useful_functions as util
# util.print_time_cur(timezone='US/Eastern')
def print_time_cur( prompt=None, timezone='US/Pacific' ):
    # set the current clock to PST 
    try:
        if os.environ['TZ']!=timezone:
            os.environ['TZ']=timezone
            time.tzset()
    except KeyError:
        os.environ['TZ']=timezone
        time.tzset()
    print '%s%s' %( prompt + ' ' if prompt != None else '', time.strftime("%I:%M:%S"))

    
# prints the optional prompt plus the dif between start_time and current time
def print_time_dif(start_time, prompt=None,):
    hours, rem = divmod(time.time()-start_time, 3600)
    minutes, seconds = divmod(rem, 60)
    print( '%s%s' %( prompt + ' ' if prompt != None else '', "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)))


# Designed to be called within an MRJob runner code block
# prints the number of mappers and reducers for each of the MRJob's steps
# counter_group_name is optional, and may be a single group name or a list of group
# names of custom counters
# ============
# sample usage 
# import useful_functions as util
# util.print_counter_report( runner.counters(), 'my_counter_group_name')
def print_counter_report(counterSteps, counter_group_name=None):
    counter_key_list = ['Job Counters ']
    if counter_group_name != None: 
        # convert counter_group_name to list and merge with counter_key_list
        if isinstance(counter_group_name, str):
            counter_group_name = [counter_group_name]
        counter_key_list +=counter_group_name
    for i in range(len(counterSteps)):                
        print '    Step %d:' %  (i + 1)
        counters = counterSteps[i]
        for counter_key in counter_key_list:
            if counter_key in counters:
                print '    %s:' % counter_key.strip()
                for key, val in counters[counter_key].iteritems():
                    if counter_key == 'Job Counters ':
                        if 'Launched' in key or ( 'Total time' in key and 'occupied' not in key ):
                            print '\t%s\t%s' %( key, val)
                    else:
                        print '\t%s\t%s' %( key, val)
        