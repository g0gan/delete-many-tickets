import requests
import time
import base64

# Replace with your Zendesk subdomain and API credentials
SUBDOMAIN = 'HERE' #add subdomain here
EMAIL = 'user@domain.com' #add email here api key here
API_KEY = '' #add api key here

# Read the ticket IDs from a text file, one ID per line
with open('ticket_ids.txt', 'r') as f:
    ticket_ids = f.read().splitlines()

# Set the maximum number of tickets to delete per API request
MAX_TICKETS_PER_REQUEST = 99

# Split the ticket IDs into batches of maximum size MAX_TICKETS_PER_REQUEST
ticket_id_batches = [ticket_ids[i:i+MAX_TICKETS_PER_REQUEST] for i in range(0, len(ticket_ids), MAX_TICKETS_PER_REQUEST)]

# Set up the API request headers with Basic authentication
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {base64.b64encode(f"{EMAIL}/token:{API_KEY}".encode("utf-8")).decode("ascii")}',
}

total_deleted_tickets = 0
last_successful_ticket_id = None

# Loop over each ticket ID batch and delete the tickets
for ticket_ids_batch in ticket_id_batches:
    # Construct the URL to delete the tickets
    url = f'https://{SUBDOMAIN}.zendesk.com/api/v2/tickets/destroy_many.json?ids={",".join(ticket_ids_batch)}'

    # Send the API request to delete the tickets with timeout of 60 seconds
    response = requests.delete(url, headers=headers, timeout=60)

    # Check if the request was successful
    if response.status_code == 200:
        num_deleted_tickets = len(ticket_ids_batch)
        total_deleted_tickets += num_deleted_tickets
        last_successful_ticket_id = ticket_ids_batch[-1]
        print(f'{num_deleted_tickets} tickets deleted successfully. Total deleted: {total_deleted_tickets}.')
    else:
        error_ticket_id = None
        if len(ticket_ids_batch) == 1:
            error_ticket_id = ticket_ids_batch[0]
        else:
            # Find the first ticket ID in the batch that was not deleted successfully
            response_json = response.json()
            for ticket_id in ticket_ids_batch:
                if str(ticket_id) not in response_json['results']:
                    error_ticket_id = ticket_id
                    break

        print(f'Error deleting tickets. Last successful ticket ID: {last_successful_ticket_id}. Error ticket ID: {error_ticket_id}. Response: {response.text}')
        break

    # Print a loader to indicate that the code is still running
    for i in range(5):
        print('.', end='', flush=True)
        time.sleep(1)
    print()

    # Wait for 10 seconds before sending the next request
    time.sleep(10)
