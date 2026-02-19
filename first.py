from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
import os

def get_user_input():
    print("===== Resume Builder =====\n")
    data = {
        "name": input("Full Name: "),
        "email": input("Email: "),
        "phone": input("Phone Number: "),
        "address": input("Address: "),
        "linkedin": input("LinkedIn Profile URL: "),
        "github": input("GitHub URL: "),
        "summary": input("Professional Summary: "),
        "skills": input("Skills (comma-separated): "),
        "photo_path": input("Enter path to profile photo (JPG or PNG): "),
        "education": [],
        "experience": []
    }

    print("\n--- Add Education Details ---")
    while True:
        edu = {
            "degree": input("Degree: "),
            "institution": input("Institution: "),
            "year": input("Year of Completion: ")
        }
        data["education"].append(edu)
        if input("Add more education? (y/n): ").lower() != 'y':
            break

    print("\n--- Add Work Experience ---")
    while True:
        exp = {
            "title": input("Job Title: "),
            "company": input("Company: "),
            "duration": input("Duration (e.g., 2021-2023): "),
            "description": input("Description: ")
        }
        data["experience"].append(exp)
        if input("Add more experience? (y/n): ").lower() != 'y':
            break

    return data

def split_text(text, max_width):
    words = text.split()
    lines = []
    line = ""

    for word in words:
        if len(line + " " + word) <= max_width:
            line += " " + word if line else word
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)

    return lines

def create_resume(data, filename="resume.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    margin = 50
    y = height - 50

    # Draw profile image
    if os.path.exists(data['photo_path']):
        try:
            image = Image.open(data['photo_path'])
            image.thumbnail((100, 100))
            temp_img_path = "temp_img.jpg"
            image.save(temp_img_path)
            c.drawImage(ImageReader(temp_img_path), width - 120, y - 100, width=80, height=80)
            os.remove(temp_img_path)
        except Exception as e:
            print("Failed to load photo:", e)

    # Header
    c.setFont("Helvetica-Bold", 20)
    c.drawString(margin, y, data["name"])
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
    y -= 18
    c.setFont("Helvetica", 12)
    for line in split_text(data["summary"], 100):
        c.drawString(margin, y, line)
        y -= 15

    # Skills
    y -= 10
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "Skills")
    y -= 18
    c.setFont("Helvetica", 12)
    skills = [skill.strip() for skill in data["skills"].split(",")]
    c.drawString(margin, y, " | ".join(skills))
    y -= 30

    # Education
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "Education")
    y -= 20
    c.setFont("Helvetica", 12)
    for edu in data["education"]:
        c.drawString(margin, y, f"{edu['degree']} - {edu['institution']} ({edu['year']})")
        y -= 15
    y -= 20

    # Experience
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "Experience")
    y -= 20
    c.setFont("Helvetica", 12)
    for exp in data["experience"]:
        c.drawString(margin, y, f"{exp['title']} at {exp['company']} ({exp['duration']})")
        y -= 15
        for line in split_text(exp['description'], 100):
            c.drawString(margin + 20, y, line)
            y -= 15
        y -= 10

    c.save()
    print(f"\n✅ Resume saved as: {filename}")

if __name__ == "__main__":
    data = get_user_input()
    create_resume(data)
