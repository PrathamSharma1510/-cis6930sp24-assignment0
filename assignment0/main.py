# main.py
import argparse
import urllib.request
import os
import PyPDF2
# from assignment0 import datafetch as data_fetch
def fetchincidents(url):
    # Specify the user agent to avoid blocking by some websites
    url = ("https://www.normanok.gov/sites/default/files/documents/"
       "2024-01/2024-01-01_daily_incident_summary.pdf")
    headers = {'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}

    # Create a request object with the given URL and headers
    request = urllib.request.Request(url, headers=headers)

    # Use urllib to open the URL and read the data
    response = urllib.request.urlopen(request)
    data = response.read()
    # print(data)
    # Define the path for saving the PDF, using /tmp for temporary storage
    file_path = '/tmp/incident_report.pdf'

    # Write the downloaded PDF to a file
    with open(file_path, 'wb') as file:
        file.write(data)
    # Read the PDF content using PyPDF2
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text_content = []
        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text_content.append(page.extract_text())
        
        # Combine the text from all pages into a single string
        all_text = '\n'.join(text_content)
        
        # Print the first 500 characters to verify
        print(all_text[:500])
    # Return the path of the saved file for further processing
    return file_path
def main(url):
    # Download data
    incident_data = fetchincidents(url)
    # Extract data
    # incidents = assignment0.extract_incidents(incident_data)
    
    # # Create new database
    # db = assignment0.create_db()
    
    # # Insert data
    # assignment0.populate_db(db, incidents)
    
    # # Print incident counts
    # assignment0.print_status(db)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process incident data.")
    parser.add_argument("--incidents", type=str, required=True, help="URL to the incident summary PDF.")
    
    args = parser.parse_args()
    main(args.incidents)
