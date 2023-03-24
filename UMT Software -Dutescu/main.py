

# In the document we had some missing ' for certain intervals,
# but I supposed that every interval should be ['xx:xx','xx:xx']
# so I wrote some additional ' here and there where the text was not good formatted.
# Also when I copied the input from the pdf, the intervals were
# separated by , and a " " blank space so that is the format of the data
# that I used [['xx:xx','xx:xx'], ['xx:xx','xx:xx']].
# We start by reading the text of the file.
f=open("input.txt","r")
lineCount=0

# In freeIntervals we will have 1440 total values that can either be 0 or 1.
# A 1 value means that the minute is not free for a meeting.
# The position in the array will mean the hour:minute at which we are and we try to use
# And 0 in vector will mean that minute is usable and 1 will mean that minute is already used.
# For example are at freeIntervals[1000] this means
# that we are talking about 1000/60:1000%60 hour, respectively the time is 16:40.
# So if freeIntervals[1000] = 1. This means 16:40 is already used and a meeting cannot include this minute.
freeIntervals=[]
# In startAvailability we will store from where to start looking for empty times.
startAvailability=0
# In endAvailability we will store the end of the interval in which we can put a meeting.
endAvailability=2000
for i in range(24*60):
    freeIntervals.append(0)

for line in f.readlines():
    # With this flag we will know if we are reading a bookedCalendar or a calendarRangeLimits.
    lineCount+=1
    line=line.strip()
    # We then split the intervals
    intervals=line.split()
    # Now we need to split the beginning and ending of an interval.
    # We need a try-except in order to find out when we read all intervals and we need to just read
    # An integer value for the meeting time.
    try:
        if lineCount%2==1:
            # Here we are working with a bookedCalendar because these occur on odd indexed lines
            for i in intervals:
                hour = i.split("'")
                start = hour[1]
                end = hour[3]
                # Now we need to modify the freeIntervals vector according to already booked hours.
                # We split the start and end hour from 9:00 into 2 numbers 9 and 0.
                pos = start.split(":")
                hourStartInt = int(pos[0])
                minutesStartInt = int(pos[1])
                pos = end.split(":")
                hourEndInt = int(pos[0])
                minutesEndInt = int(pos[1])
                # Now we need to turn the time, into array positions.
                startInterval=hourStartInt*60+minutesStartInt
                endInterval=hourEndInt*60+minutesEndInt
                for j in range(startInterval,endInterval):
                    freeIntervals[j] = 1

        else:
            # Here we are working with a calendarRangeLimits because these occur on even indexed lines
            # Here we need to find the maximum between the starting hours
            # eg. for 9:00 10:00 we need to start counting only from 10:00.
            # And we need to find the minimum of ending hours
            # eg. for 20:00 and 18:30 we need to count only up to 18:30.
            for i in intervals:
                hour = i.split("'")
                start = hour[1]
                end = hour[3]
                pos = start.split(":")
                hourStartInt = int(pos[0])
                minutesStartInt = int(pos[1])
                pos = end.split(":")
                hourEndInt = int(pos[0])
                minutesEndInt = int(pos[1])
                # We obtain the starting and ending hours for every calendarRangeLimits as above
                if hourStartInt*60+minutesStartInt>startAvailability:
                    startAvailability = hourStartInt*60+minutesStartInt
                if hourEndInt*60+minutesEndInt<endAvailability:
                    endAvailability = hourEndInt*60+minutesEndInt
                # Now we have the interval in which we need to find all possible meeting times.
                # The interval will be between startAvailability and endAvailability,
                # which are 2 positions of the vector.
    except:
        # When we need to read the meetingTime, the program will raise an error
        # Because we try to do splits and operations on a string without "," or anything
        # And that will mean that we need to read the meetingTime because all intervals have been read.
        meetingTime=int(line)

# Now we will go through the established range limits and find out where meetings can be fit.
answer=[]
stringAnswer=[]
partialString=[]
counter=0
possibleStart=0
possibleEnd=0
for i in range(startAvailability, endAvailability+1):
    # We need to start counting how many 0 values we have between 1-s values
    # If we have 1, 1, 1, 0, 0, 0, 1 this means here we can fit a 3 minute meeting
    # While we have 0, we keep counting how many minutes can the meeting have
    if freeIntervals[i] == 0:
        if counter == 0:
            possibleStart = i
        counter += 1
    else:
        # When we reach a 1 value, means the meeting should end here
        # We check if the possible meeting has the target meeting value time
        if counter >= meetingTime:
            # If yes, we append in a list, the positions from where to where we can fit a meeting
            possibleEnd = i
            answer.append([possibleStart, possibleEnd])
        counter = 0

# We need to check one more time for the last length,
# because if the array ends in 0, the condition of appending a new answer, won't be called above
if counter-1 >= meetingTime:
    possibleEnd = endAvailability
    answer.append([possibleStart, possibleEnd])
    counter = 0
# Now we need to transform from integers values, to time ['xx:xx','xx:xx']
for i in answer:
    partialString=[]
    for j in i:
        hour=str(int(j/60))
        minutes=str(int(j%60))
        if len(minutes) == 1:
            minutes = "0"+minutes
        partialString.append(hour+":"+minutes)
    # Now we just append the strings to the final answer.
    stringAnswer.append(partialString)

print(stringAnswer)

# We need to pay attention to the format of the input txt, if it changes slightly, the splits will be done wrong
# and wrong answers will occur.




