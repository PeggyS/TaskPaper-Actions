#coding: utf-8
import workflow
import re
import urllib2
import datetime

PARAMS = workflow.get_parameters()

DEFAULT_TIME = PARAMS['Time']
DEFAULT_LIST = PARAMS['List']
ADD_NOTES = PARAMS['Notes']
TAG = PARAMS['Tag']


def stripTags(task):
	"""Strip tags from a task item and return the resulting list.
	Will ommit the remind tag."""
	
	#Strip remind tag
	tp_task = re.sub('@remind(\(\d{4}-\d{2}-\d{2}\s*((|\d{2}:\d{2}))\)|)','',task,re.M)
	
	# Get list of remaining tags
	tp_task = re.finditer("\@\w+(\(\d{4}-\d{2}-\d{2}\s*((|\d{2}:\d{2}))\)|)", tp_task, re.M)
	
	return  [tags.group() for tags in tp_task]
	

def taskTime(task):
	"""Will processo the date/time value in the remind tag and create a proper
	date/time string to use when creating the task"""
	
	tp_task = re.search('(?<=@remind\().*(?=\))',task,re.M)
	dt = tp_task.group().split(" ")
	
	# Get the date
	try:
		date_str = datetime.datetime.strptime(dt[0],'%Y-%m-%d').strftime('%d-%m-%Y')
	except IndexError, errmsg:
		return "There is no valid date defined."

	# Get the time
	try:
		time_str = dt[1]
	except IndexError, errmsg:
		time_str = 	DEFAULT_TIME
	
	return (date_str, time_str)
	
def main():
	arg = workflow.get_input().encode('utf-8')
	tag_pattern = re.compile("((?!.*@done).*" + TAG +".*(\n*\t*(?!\w.*:$)\w.*)*)", re.M)
	task_pattern = re.compile('\s{1}@\w+(\(\d{4}-\d{2}-\d{2}\s*((|\d{2}:\d{2}))\)|)', re.M)
	notes_pattern = re.compile("^-.*\n*|\t")
	
	# Isolate tasks with @remind tag
	tp_remind = re.findall(tag_pattern, arg)

	# Iterate over every task tagged and process it.
	url_str = ''
	for match in tp_remind:
		
		# Process Task
		src_task = re.sub("- ","",re.search("^-.*", match[0].strip()).group())
		task = re.sub(task_pattern,'',src_task)
			
		# Process task time
		dt =  taskTime(src_task)
		
		# Prepate notes if Notes == True, else ommit notes from Reminder.
		if ADD_NOTES:
			# Get list of tags from task without remind tag
			tag_str = ' '.join([tag for tag in stripTags(src_task) if stripTags(src_task)])
			
			# Prepare Notes
			notes = (re.sub(notes_pattern,"", match[0].strip())).strip()
			
			# Create body of task
			if tag_str and notes:
				notes_str = notes.strip()+'\n'+tag_str.strip()
			elif tag_str and not notes:
				notes_str = tag_str.strip()
			elif notes and not tag_str:
				notes_str = notes.strip()
			else:
				notes_str = ''
				
		else:
			notes_str = ''

		# Add the task to Reminders.
		task_str = task + ' on ' + str(dt[0]) + ' at ' + str(dt[1]) + ' /' + DEFAULT_LIST

		if url_str == '':
			url_str += 'fantastical2://x-callback-url/parse?sentence='+urllib2.quote(task_str,'')+'&notes='+urllib2.quote(notes_str)+'&reminder=1'

		else:
			url_str = 'fantastical2://x-callback-url/parse?sentence='+urllib2.quote(task_str,'')+'&notes='+urllib2.quote(notes_str,'')+'&reminder=1&x-success='+urllib2.quote(url_str,'')

	workflow.set_output(url_str)
	
		
if __name__ == '__main__':
	main()