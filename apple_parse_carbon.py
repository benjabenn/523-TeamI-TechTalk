import os
import csv
import pymupdf
import re


def extract_text_from_pdf(pdf_path):
    with pymupdf.open(pdf_path) as doc:
        # We usually only need the first 2-3 pages for the total footprint
        text = ""
        for page in doc:
            text += page.get_text("text") + " "
    # Clean the text: replace newlines/tabs with spaces and normalize whitespace
    text = " ".join(text.split())
    return text


def extract_carbon_value(text):
    # Normalize text: Remove newlines and double spaces to make it one clean string
    clean_text = " ".join(text.split())

    patterns = [
        # Modern Format: "89 kg Net GHG emissions (CO 2e)3"
        r"(?i)([\d,.]+)\s*kg\s*Net\s*GHG\s*emissions\s*\(?CO\s*2\s*e\)?\d*",
        # Occasional Formats: "44 kg Net emissions"
        r"(?i)([\d,.]+)\s*kg\s*Net\s*emissions\s*\d*",
        r"(?i)([\d,.]+)\s*kg\s*Total\s*product\s*emissions\s*\d*",
        r"(?i)([\d,.]+)\s*kg\s*Carbon\s*emissions\s*\d*",
        r"(?i)([\d,.]+)\s*kg\s*Carbon\s*\d*",
        # Emissions First Format: "Total greenhouse gas emissions: 65 kg CO2e"
        r"(?i)emissions(?::|of)?\s*([\d,.]+)\s*kg\s*CO\s*2\s*e",
        # Standard Format: "54 kg CO2e"
        r"(?i)([\d,.]+)\s*kg\s*CO\s*2\s*e",
    ]

    for pattern in patterns:
        match = re.search(pattern, clean_text)
        if match:
            # Extract the first capture group (the number)
            val = match.group(1).replace(",", "")
            try:
                return float(val)
            except ValueError:
                continue

    return None


# --- Main Loop ---
pdf_directory = "apple/"
csv_directory = "out/"
csv_file_path = os.path.join(csv_directory, "apple.csv")
os.makedirs(csv_directory, exist_ok=True)
all_maps = []

for file_name in os.listdir(pdf_directory):
    if file_name.lower().endswith(".pdf"):
        text = extract_text_from_pdf(os.path.join(pdf_directory, file_name))
        pcf = extract_carbon_value(text)

        all_maps.append({"Filename": file_name, "PCF_kg_CO2e": pcf})

# Export to CSV (Standard logic)
with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=all_maps[0].keys())
    writer.writeheader()
    for data_map in all_maps:
        writer.writerow(data_map)
