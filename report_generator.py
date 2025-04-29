import csv
from fpdf import FPDF

# Step 1: Read CSV with Name, Percent, Reg.No.
def read_data(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        data = []
        for row in reader:
            name = row['Name']
            reg_no = row['Reg.No.']
            percent = float(row['Percent'].strip())
            data.append({'Name': name, 'Reg.No.': reg_no, 'Percent': percent})
        return data

# Step 2: Analyze percentages
def analyze_data(data):
    scores = [entry['Percent'] for entry in data]
    return {
        'Total Students': len(scores),
        'Average Percent': round(sum(scores) / len(scores), 2),
        'Highest Percent': max(scores),
        'Lowest Percent': min(scores)
    }

# Step 3: Define PDF layout
class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Student Performance Report", ln=True, align="C")

    def student_table(self, data):
        self.set_font("Arial", "B", 12)
        self.cell(60, 10, "Name", border=1)
        self.cell(40, 10, "Reg.No.", border=1)
        self.cell(40, 10, "Percent", border=1)
        self.ln()
        self.set_font("Arial", "", 12)
        for entry in data:
            self.cell(60, 10, entry['Name'], border=1)
            self.cell(40, 10, entry['Reg.No.'], border=1)
            self.cell(40, 10, f"{entry['Percent']}%", border=1)
            self.ln()

    def summary_table(self, summary):
        self.ln(10)
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Summary", ln=True)
        self.set_font("Arial", "", 12)
        for key, value in summary.items():
            suffix = "%" if "Percent" in key else ""
            self.cell(0, 10, f"{key}: {value}{suffix}", ln=True)

# Step 4: Generate the PDF
def generate_pdf(data, summary, output_filename="student_report.pdf"):
    pdf = PDFReport()
    pdf.add_page()
    pdf.student_table(data)
    pdf.summary_table(summary)
    pdf.output(output_filename)
    print(f"Report saved as {output_filename}")

# Step 5: Main execution
if __name__ == "__main__":
    data = read_data("data.csv")  # Ensure your CSV file uses the correct column headers
    summary = analyze_data(data)
    generate_pdf(data, summary)

