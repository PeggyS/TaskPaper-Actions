	# -*- coding: utf-8 -*-

SCRIPT_NAME = 'TaskPaper Tasks to Reminders'
DESCRIPTION = 'Send tasks tagged with @remind to Reminders'

import re
import argparse
import urllib2
import codecs
import os
import subprocess
import datetime
import fileinput


DEFAULT_TIME = "10:00"
DEFAULT_LIST = "Inbox"
ADD_NOTES = True	# True: Aditional tags and task notes will be added to notes
				# False: Just the task will be added with no extra information.



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
	
	# AppleScript uses a date format of the type DD-MM-YYYY or MM-DD-YY so we need to switch it around 
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



def addTask(task,dt):
	"""Add the task to Reminders using AppleSript"""
	
	# TODO: Check for duplicate Reminders
	# TODO: Remove @remind tag after adding task to Reminders.
	
	command = '''set dDate to date("%s %s") 
	tell application "Reminders" to make new reminder in list "%s" with properties \
	{%s, remind me date:dDate}''' %(str(dt[0]),str(dt[1]), DEFAULT_LIST, task)
	
	p = subprocess.Popen(['osascript', '-e', command], stdin=None, stdout=None, stderr=None)
	p.communicate()

	
	
def main():
	parser = argparse.ArgumentParser(description="Sends tasks tagged with @remind to iCloud Reminders")
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-f', '--file', help="TaskPaper file to read.", nargs='+')
	group.add_argument('-l', '--list', help="URL encoded list passed via command line.", nargs='+')
	args = parser.parse_args()
	
	
	if args.file:
		if os.path.exists(args.file[0]):
			f = codecs.open(args.file[0], encoding="utf-8")
			arg = f.read()
	if args.list:
		arg = urllib2.unquote(args.list[0]).decode('string-escape')
	
	
	# Isolate tasks with @remind tag
	tp_remind = re.findall("((?!.*@done).*remind.*(\n*\t*(?!\w.*:$)\w.*)*)", arg, re.M)

	# Iterate over every task tagged and process it.
	for match in tp_remind:
		
		# Process Task
		src_task = re.sub("- ","",re.search("^-.*", match[0].strip()).group())
		task = re.sub('\s{1}@\w+(\(\d{4}-\d{2}-\d{2}\s*((|\d{2}:\d{2}))\)|)','',src_task,re.M)
		

			
		# Process task time
		dt =  taskTime(src_task)
		
		# Prepate notes if NOTES == True, else ommit notes from Reminder.
		if ADD_NOTES:
			# Get list of tags from task without remind tag
			tag_str = ' '.join([tag for tag in stripTags(src_task) if stripTags(src_task)])
			
			# Prepare Notes
			notes = (re.sub("^-.*\n*|\t","", match[0].strip())).strip()
			
			# Create body of task
			if tag_str and notes:
				task_str = 'name:"%s", body:"%s"' %(task, notes.strip()+'\n'+tag_str.strip())
			elif tag_str and not notes:
				task_str = 'name:"%s", body:"%s"' %(task, tag_str.strip())
			elif notes and not tag_str:
				task_str = 'name:"%s", body:"%s"' %(task, notes.strip())
			else:
				task_str = 'name:"%s"' %(task)
				
		else:
			task_str = 'name:"%s"' %(task)	
		
		# Add the task to Reminders.
		addTask(task_str,dt)


		
if __name__ == '__main__':
	main()