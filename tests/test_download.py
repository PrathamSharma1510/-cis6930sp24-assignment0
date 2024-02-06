import os
import unittest
from assignment0.main import download_pdf



class TestDownloadPDF(unittest.TestCase):

    def test_pdf_download(self):
        """Test the download_pdf function to ensure a PDF is downloaded correctly."""
        test_url = 'https://www.normanok.gov/sites/default/files/documents/2024-01/2024-01-07_daily_incident_summary.pdf'
        expected_file_path = '/tmp/incident_report.pdf'
        
        # Call the download function
        result_path = download_pdf(test_url, expected_file_path)
        
        # Check if the file exists in the specified path
        self.assertTrue(os.path.exists(result_path))
        
        # Clean up - remove the downloaded file after the test
        if os.path.exists(result_path):
            os.remove(result_path)

if __name__ == '__main__':
    unittest.main()
