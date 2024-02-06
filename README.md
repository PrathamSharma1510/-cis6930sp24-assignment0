# CIS6930SP24 - Assignment0 - Incident Report Processing

**Name:** Pratham Sharma
**UFID:** 99812068

## Assignment Description

The project focuses on streamlining the process of managing public safety incident reports. Leveraging the provided Python code, it automates the downloading of PDF files from specified URLs, parsing these documents to extract critical details such as the date/time, incident number, location, nature, and incident ORI. This data is meticulously extracted and structured for insertion into a SQLite database, facilitating organized storage and easy retrieval. Furthermore, the system is designed to generate a comprehensive summary of incidents, categorized by their nature, aiding in the analysis and understanding of public safety trends and patterns. This innovative approach not only enhances data accessibility but also supports efficient analysis, making it a valuable tool for public safety departments and researchers alike.

## Installation Instructions

Ensure you have `pipenv` installed. If not, install it using `pip install pipenv`. Then, set up the project environment with:

```
pipenv install
```

## How to Run

Activate the project environment:

```
pipenv shell
```

To process a report, execute:

```
pipenv run python main.py --incidents [PDF URL]
```

## Functions Overview

- **download_pdf(url, save_path)**: Facilitates the automated retrieval of PDF documents from specified web URLs. It saves the downloaded file to a local path, ensuring that the incident reports are accessible for data extraction.

- **extract_incidents_from_pdf(pdf_path)**: This function is crucial for translating the content of PDF files into structured data. It meticulously scans through the document, identifying and extracting relevant information related to public safety incidents, such as timestamps, incident specifics, and geographical details.

- **create_db_and_table(db_path)**: Sets the foundation for data storage by establishing a SQLite database. It also constructs the necessary tables that will hold the structured incident data, enabling efficient data management and query execution.

- **populate_db(db_path, df)**: Acts as the bridge between extracted data and its storage solution. This function takes the structured data, now in a DataFrame, and inserts it into the database, ensuring that each piece of information is accurately represented and stored.

- **print_incident_summary(db_path)**: Provides a synthesized view of the stored data, focusing on the categorization of incidents by their nature. It is designed to offer insights into the frequency and types of incidents, supporting analysis and decision-making processes.

## Database Development

The database schema is designed to efficiently store and manage incident data extracted from PDF reports. The `incidents` table is structured as follows:

```sql
CREATE TABLE incidents (
    incident_time TEXT,
    incident_number TEXT UNIQUE,
    incident_location TEXT,
    nature TEXT,
    incident_ori TEXT
);
```

This schema supports the structured storage of incident data, ensuring data integrity through a unique constraint on `incident_number` to prevent duplicates. It facilitates efficient data retrieval and analysis by categorizing incidents in a clear and query-friendly manner.

## Bugs and Assumptions

During the development of this project, extensive research was conducted to understand the nuances of incident data presentation within PDF reports. A notable observation was the inconsistency in data formatting, particularly with additional lines appearing in the `incident_location` field, which initially posed challenges in data extraction accuracy. This was particularly evident with entries marked as "RAMP", where an extra line disrupted the standard data structure. To address this, a specialized handling approach was implemented to effectively identify and correct such cases, ensuring the robustness of the data extraction process. This adjustment, although initially an edge case, underlines the importance of flexible parsing logic in dealing with real-world data variability and has been incorporated into the project's assumptions for improved accuracy.

## Demo

Include a GIF or a video link demonstrating the tool in action.

---
