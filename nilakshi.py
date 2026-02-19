from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
import os

def get_user_input():
    print("Enter your resume details:")
    data = {
        "name": input("Full Name: "),
        "email": input("Email: "),
        "phone": input("Phone: "),
        "address": input("Address: "),
        "linkedin": input("LinkedIn URL: "),
        "github": input("GitHub URL: "),
        "summary": input("Professional Summary: "),
        "skills": input("Skills (comma-separated): "),
        "education": [],
        "experience": [],
        "photo_path": input("Path to profile photo (JPG/PNG): ")
    }

    print("\n--- Education ---")
    while True:
        edu = {
            "degree": input("Degree: "),
            "school": input("School/University: "),
            "year": input("Year of completion: ")
        }
        data["education"].append(edu)
        cont = input("Add another education? (y/n): ")
        if cont.lower() != 'y':
            break

    print("\n--- Experience ---")
    while True:
        exp = {
            "title": input("Job Title: "),
            "company": input("Company: "),
            "duration": input("Duration (e.g. 2020-2023): "),
            "description": input("Job Description: ")
        }
        data["experience"].append(exp)
        cont = input("Add another experience? (y/n): ")
        if cont.lower() != 'y':
            break

    return data

def create_resume(data, filename="resume.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    margin = 40
    y = height - margin

    # Draw photo
    if os.path.exists(data['photo_path']):
        try:
            image = Image.open(data['photo_path'])
            image.thumbnail((100, 100))
            img_path = "temp_profile_img.jpg"
            image.save(img_path)
            c.drawImage(ImageReader(img_path), width - 120, y - 100, width=80, height=80)
        except Exception as e:
            print("Error loading photo:", e)
    else:
        print("Photo not found. Skipping.")

    # Header
    c.setFont("Helvetica-Bold", 20)
    c.drawString(margin, y, data['name'])
    y -= 25

    c.setFont("Helvetica", 12)
    c.drawString(margin, y, f"Email: {data['email']} | Phone: {data['phone']}")
    y -= 15
    c.drawString(margin, y, f"Address: {data['address']}")
    y -= 15
    c.drawString(margin, y, f"LinkedIn: {data['linkedin']} | GitHub: {data['github']}")
    y -= 30

    # Summary
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "Professional Summary")
    y -= 15
    c.setFont("Helvetica", 12)
    for line in split_text(data['summary'], 100):
        c.drawString(margin, y, line)
        y -= 15

    # Skills
    y -= 10
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "Skills")
    y -= 15
    c.setFont("Helvetica", 12)
    c.drawString(margin, y, ", ".join(data['skills'].split(',')))
    y -= 30

    # Education
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "Education")
    y -= 15
    c.setFont("Helvetica", 12)
    for edu in data['education']:
        c.drawString(margin, y, f"{edu['degree']} - {edu['school']} ({edu['year']})")
        y -= 15

    y -= 20

    # Experience
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "Work Experience")
    y -= 15
    c.setFont("Helvetica", 12)
    for exp in data['experience']:
        c.drawString(margin, y, f"{exp['title']} at {exp['company']} ({exp['duration']})")
        y -= 15
        for line in split_text(exp['description'], 100):
            c.drawString(margin + 20, y, line)
            y -= 15
        y -= 10

    c.save()
    print(f"\nResume saved as {filename}")

    # Clean up temp image
    if os.path.exists("temp_profile_img.jpg"):
        os.remove("temp_profile_img.jpg")

def split_text(text, max_chars):
    words = text.split()
    lines = []
    line = ""
    for word in words:
        if len(line + " " + word) <= max_chars:
            line += " " + word if line else word
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

if __name__ == "__main__":
    user_data = get_user_input()
    create_resume(user_data)
