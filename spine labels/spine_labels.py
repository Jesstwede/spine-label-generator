import requests
from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas


LABEL_SIZE = 1 * inch


def get_book_data(isbn):
    url = f"https://openlibrary.org/isbn/{isbn}.json"
    r = requests.get(url)

    if r.status_code != 200:
        return None

    data = r.json()

    # Get author last name
    author_last = "UNK"
    authors = data.get("authors", [])
    if authors:
        author_key = authors[0].get("key")
        if author_key:
            a = requests.get(f"https://openlibrary.org{author_key}.json")
            if a.status_code == 200:
                name = a.json().get("name", "")
                author_last = name.split()[-1][:3].upper()

    # Get Dewey (if available)
    dewey = data.get("dewey_decimal_class")
    
    if dewey:
        # Grab the first classification found
        raw_call = dewey[0]
        
        # CLEANUP LOGIC:
        # If it contains "Fic" (like "[Fic]" or "Fic"), force it to "F"
        if "fic" in raw_call.lower():
            call_number = "F"
        else:
            call_number = raw_call
    else:
        # If the field is totally empty, assume F
        call_number = "F"

    return call_number, author_last
    # Get Dewey (if available)
    dewey = data.get("dewey_decimal_class")
    if dewey:
        call_number = dewey[0]
    else:
        call_number = "F"

    return call_number, author_last


def generate_labels(isbn_list, output_file="spine_labels.pdf"):
    c = canvas.Canvas(output_file, pagesize=(LABEL_SIZE, LABEL_SIZE))

    for isbn in isbn_list:
        result = get_book_data(isbn)
        if not result:
            continue

        call_number, author = result

        # Top line (Call number or F)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(LABEL_SIZE / 2, 0.65 * inch, call_number)

        # Bottom line (Author cutter)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(LABEL_SIZE / 2, 0.35 * inch, author)

        c.showPage()  # NEW PAGE = NEW LABEL

    c.save()

def load_isbns(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip()]

if __name__ == "__main__":
    isbn_list = load_isbns("isbns.txt")
    generate_labels(isbn_list)