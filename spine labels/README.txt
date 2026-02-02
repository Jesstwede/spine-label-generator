# Spine Label Generator

A Python tool that automates the creation of library spine labels. It takes a list of ISBNs, fetches metadata (Dewey Decimal Class and Author Name) from the OpenLibrary API, and generates a formatted PDF ready for printing on 1" x 1" labels.

## Features
* **Automated Lookup:** Fetches book data using the OpenLibrary API.
* **Smart Classification:**
    * Extracts the Dewey Decimal number for non-fiction.
    * Detects Fiction (including tags like `[Fic]`) and assigns "F".
    * Generates an Author Cutter (first 3 letters of the last name).
* **Print-Ready:** Outputs a PDF sized specifically for 1-inch label printers.

## Prerequisites

You need **Python 3** installed on your computer. You also need the following Python libraries:

* `requests` (for fetching data)
* `reportlab` (for creating the PDF)

You can install them using pip:

```bash
pip install requests reportlab
