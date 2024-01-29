# Easy way to delete a lot of tickets in Zendesk instance by few steps
All you need is:
1. Zendesk login|password
2. Zendesk Api key
3. list of tickets's id in plain text file.

I added a new variable **last_successful_ticket_id** to keep track of the ID of the last ticket that was deleted successfully.
If an error occurs during the deletion of a batch of tickets, the code will print the ID of the last successful ticket and the ID of the ticket where the error occurred.

Note that if a batch contains only one ticket and an error occurs, the code will assume that the error occurred with that ticket. Otherwise, it will check the API response to determine which ticket in the batch was not deleted successfully. If an error occurs, the code will break out of the loop and stop deleting tickets, so you will need to manually modify the list of ticket IDs to start from the last successful ticket ID and run the code again.
