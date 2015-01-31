# TaskPaper Actions
TaskPaper Actions is growing, new scripts and actions are being added to the family in the hope that added functionality can be achieved.

## TPACTIONS
tpactions.py is the base for all others, it sanitises the TaskPaper file/list so that it can then be parsed by other scripts.

### Feature List
- Marks every subtask as `@done` if the parent task is `@done`;
- Marks every task as `@done` if all it's subtasks are `@done`;
- <s>Displays the next actions, disregarding `@done` tasks and subtasks;</s>
- Appends `@next` to next actions.

### Roadmap
- <s>Rather than display the next actions, tag them with `@next. Tag also any corresponding subtask so that it will appear in search;</s>
- Determine next action for a specific project, based on user input;
- Revision mode?

## TP2REMINDERS
tp2reminders.py simply sends tasks tagged with @remind to Apple Reminders.

### Feature List
- Sends tasks tagged with @remind(YYYY-MM-DD [hh:mm]) to Reminders;
- If no time is specified, then a default time will be used;
- Optionally add remaining tags to the notes field;
- Add any notes the task may have to the notes field

### Roadmap
- Exchange information between Reminders and TaskPaper to mark as done in one or the other depending of the tasks current state
- Anything else I may think of that comes in handy.