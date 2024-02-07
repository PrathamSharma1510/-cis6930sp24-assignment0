## CIS6930SP24 - Assignment0 - Incident Report Processing

**Name:** Pratham Sharma
**UFID:** 99812068

## Assignment Description
The project aims to make managing public safety incident reports a breeze. With the help of the Python code provided, it does all the heavy lifting - grabbing PDF files from specific URLs and digging out important info like when it happened, the incident number, where it occurred, what it was about, and the incident ORI. This data gets neatly sorted out and placed into an SQLite database, so you can find it easily whenever you need. But there's more! This system is also built to whip up a nice summary of all these incidents, neatly sorted by their types. It helps folks study and figure out what's happening in the world of public safety. It's a clever way to make data easier to get to and helps folks study it better, which is a win for public safety departments and researchers.

## Installation Instructions

Ensure that you have a `pipenv` installed. If not, install it using command :- `pip install pipenv`. Now, set up the project environment with command:

```
pipenv install
```

## How to Run the code

To execute the code following command is used:

```
pipenv run python main.py --incidents [PDF URL]
```

Some example:-
**Example 1**:

```
pipenv run python assignment0/main.py --incidents "https://www.normanok.gov/sites/default/files/documents/2024-01/2024-01-04_daily_incident_summary.pdf"
```

**Example 2**:

```
pipenv run python assignment0/main.py --incidents "https://www.normanok.gov/sites/default/files/documents/2024-01/2024-01-20_daily_incident_summary.pdf"
```

## Functions Overview

- **download_pdf(url, save_path)**: Facilitates the automated retrieval of PDF documents from specified web URLs. It saves the downloaded file to a local path, ensuring that the incident reports are accessible for data extraction.

- **extract_incidents_from_pdf(pdf_path)**: This function plays a vital role in turning the content of PDF files into well-organized data. It carefully reads through the document, spotting and pulling out all the important details about public safety incidents, like timestamps, incident particulars, and location information.

- **create_db_and_table(db_path)**: It lays down the groundwork for data storage by setting up an SQLite database. Plus, it creates the essential tables where we can neatly store all the organized incident data. This makes managing data a whole lot easier, and it lets us run queries efficiently.

- **populate_db(db_path, df)**: This function acts as the link between the organized data and its storage system. It grabs the well-structured data, which is now in a DataFrame, and places it nicely into the database. It takes care to make sure that each piece of information is stored accurately and precisely.

- **print_incident_summary(db_path)**: Gives you a condensed look at the stored data, with a special focus on sorting incidents by their types. It's meant to give you a better understanding of how often different kinds of incidents happen, helping with analysis and decision-making.

## Database Development

The database structure is built to handle incident data taken from PDF reports effectively. The `incidents` table is organized like this:

```sql
CREATE TABLE incidents (
    incident_time TEXT,
    incident_number TEXT UNIQUE,
    incident_location TEXT,
    nature TEXT,
    incident_ori TEXT
);
```

This setup helps store incident data in an organized way and keeps the data clean by making sure there are no duplicates of `incident_number`. It also makes it easy to get and analyze the data because it neatly sorts incidents for easy querying.

## Bugs and Assumptions

While working on this project, I dived deep into the specifics of how incident data is formatted in PDFs. One thing that really stood out was the inconsistency in how data was laid out, especially when extra lines popped up in the `incident_location` field. This was super apparent with the "RAMP" entries, throwing off the usual structure. To tackle this, I came up with a specific way to spot and fix these issues, making sure our data extraction stayed on point. This workaround, though it seemed minor at first, really highlights the need for adaptable parsing strategies when you're dealing with the unpredictability of real-world data. I've rolled this insight into our project's assumptions, aiming for even better accuracy.

Certainly, here's an explanation of the README section for test files and how to run them:

---

## Test Filess

#### `test_download_pdf.py`

This test suite validates the functionality of the `download_pdf` function. It verifies whether the function accurately downloads a PDF file from a provided URL and saves it to the designated file path. Additionally, it confirms the existence of the downloaded file and incorporates cleanup procedures to remove the file post-test execution.

#### `test_functions.py`

Within this test suite lie unit tests for various functions associated with data extraction and database management. Included are assessments for the `extract_incidents_from_pdf`, `create_db_and_table`, and `populate_db` functions. These tests scrutinize the behavior of these functions, ensuring they perform their intended tasks effectively, encompassing tasks such as data extraction, database creation, and data population. Their execution helps uphold the reliability and correctness of the project's fundamental functionalities.

### Running Tests

To run the test files, you can use the following command:

```bash
pipenv run python -m pytest
```

This command will execute all the tests located in the test files within your project.

## Demo
[![Demo Video](https://img.youtube.com/vi/SS5tU8QzhZ4/0.jpg)](https://www.youtube.com/watch?v=SS5tU8QzhZ4)
---
