#터미널에서 python MovieRatingData.py 100 실행
#파이참 터미널로 실행하지 않으면 sys.argv[1]이 지정되지 않기 때문에 오류 발생함

import time
from datetime import datetime
import random
from time import sleep
import sys

def convert_unixtime(date_time):
	unixtime = time.mktime(datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S').timetuple())
	return unixtime

data_amount = sys.argv[1]
data_destination = time.strftime("kinesis.log")

with open(data_destination, "w") as f:
	for i in range(int(data_amount)):
		user_id = str(random.randrange(1, 101))
		movie_id = str(random.randrange(1, 101))
		rating = str(random.randrange(1,6))
		date_time = time.strftime('%Y-%m-%d %H:%M:%S')

		tiemstamp = round(convert_unixtime(date_time),3)

		log = user_id + " " + movie_id + " " + rating + " " + "{0:.0f}".format(tiemstamp) + "\n"
		f.write(log)
		sleep(0.00001)
	print("Complete")