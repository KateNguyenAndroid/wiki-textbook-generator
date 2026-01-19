# Wiki Textbook Generator

A Python project that generates a wiki-style textbook from user-defined topics, helping users self-study step-by-step any skill they need.

## Features

- Fetch content from Wikipedia for multiple topics.
- Generate a combined Markdown file with links to each topic's Wikipedia page.
- User-friendly web interface built with Flask.
- Error handling for non-existent Wikipedia pages.

## Requirements

- Python 3.x
- Flask
- wikipedia-api

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/wiki-textbook-generator.git
   cd wiki-textbook-generator
2. Install the required packages:
   pip install -r requirements.txt
3. Running the Project
   To run the project, execute:
   python main.py
   Open your web browser and go to http://127.0.0.1:5000/ to access the Wiki Textbook Generator.
4. Usage
   Enter multiple topics separated by commas in the input box.
   Click on "Generate Textbook."
   If successful, a link to the generated Markdown file will be displayed.
5. Contributing
   Feel free to fork the repository and submit pull requests for improvements or bug fixes.

Add Features to Implement:
1. User Authentication: Using Flask-Login.
2. Textbook Management: Allow users to view and delete textbooks.
3. Export Options: Export textbooks as PDF.
4. Search Functionality: Allow users to search for Wikipedia topics.
5. Feedback and Rating System: Allow users to rate textbooks.
