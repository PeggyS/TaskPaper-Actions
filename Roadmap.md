## Next Actions:
A small roadmap to keep track of what we want/need to do. This is in no way promised features.


### Input:
Possible input methods can/should be:  

- Direct Access to file;
- TaskPaper list passed via command line / URL scheme (list must be urlencoded) @done
- Debug (Uses builtin list for testing purposes) @done

### Output:
Possible output methods can/should be:  

- Print to stdout/console; @done 
- Save to origina file;
- Save to a new file

### Mark as done:

- Mark sub-tasks `@done` when parent is done; @done
- Mark parent `@done` when all sub-tasks are done; @done
- Mark all tasks as `@done` if the project/sub-project is marked as done

### Process Tasks:

- Append `@next` to next actionable tasks; @done
- Print/output only next actionable tasks without appending `@next` tag;
- Ignore tasks with a due/start date greater than today or with a set of pre-defined tags such as `@waiting`, `@hold` etc.;

## TaskPaper to HTML
Convert a TaskPaper list to html for viewing either on StatusBoard or as a simple HTML file in any web browser.

### Input
- Direct Access to file;
- TaskPaper list passed via command line / URL scheme (list must be urlencoded)

### Output:
Possible output methods can/should be:  

- Print to stdout/console; @done 
- Save to origina file;
- Save to a new file