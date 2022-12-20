from datetime import datetime, timedelta

def get_time(current_time):
	waiting_time = timedelta(seconds = 60*60*4)
	
	if current_time < current_time.replace(hour=1, minute=00, second=0):
		waiting_time = current_time.replace(hour=1, minute=00, second=0) - current_time
		return "Dusk", waiting_time, "Night"
		
	if current_time < current_time.replace(hour=5, minute=00, second=0):
		waiting_time = current_time.replace(hour=5, minute=00, second=0) - current_time
		return "Night", waiting_time, "Dawn"
		
	if current_time < current_time.replace(hour=7, minute=00, second=0):
		waiting_time = current_time.replace(hour=7, minute=00, second=0) - current_time
		return "Dawn", waiting_time, "Day"

	if current_time < current_time.replace(hour=11, minute=00, second=0):
		waiting_time = current_time.replace(hour=11, minute=00, second=0) - current_time
		return "Day", waiting_time, "Dusk"

	if current_time < current_time.replace(hour=13, minute=00, second=0):
		waiting_time = current_time.replace(hour=13, minute=00, second=0) - current_time
		return "Dusk", waiting_time, "Night"

	if current_time < current_time.replace(hour=17, minute=00, second=0):
		waiting_time = current_time.replace(hour=17, minute=00, second=0) - current_time
		return "Night", waiting_time, "Dawn"

	if current_time < current_time.replace(hour=19, minute=00, second=0):
		waiting_time = current_time.replace(hour=19, minute=00, second=0) - current_time
		return "Dawn", waiting_time, "Day"

	if current_time < current_time.replace(hour=11, minute=00, second=0):
		waiting_time = current_time.replace(hour=23, minute=00, second=0) - current_time
		return "Day", waiting_time, "Dusk"

	return "Day", waiting_time, "Dusk"