import urllib.request
import os

def fetchincidents(url):
    # Specify the user agent to avoid blocking by some websites
    headers = {'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}

    # Create a request object with the given URL and headers
    request = urllib.request.Request(url, headers=headers)

    # Use urllib to open the URL and read the data
    response = urllib.request.urlopen(request)
    data = response.read()

    # Define the path for saving the PDF, using /tmp for temporary storage
    file_path = '/tmp/incident_report.pdf'

    # Write the downloaded PDF to a file
    with open(file_path, 'wb') as file:
        file.write(data)
    
    # Return the path of the saved file for further processing
    return file_path