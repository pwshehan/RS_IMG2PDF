import sys
import re
import os

from fpdf import FPDF
from progress.bar import ChargingBar

listFile = open('list.txt', 'r')
files = listFile.readlines()

images = []
for file in files:
    listLine = file.split("\n")[0]
    title = listLine.split(".")[0] if len(
        listLine.split("|")) == 1 else listLine.split("|")[1]
    filepath = listLine.split("|")[0]
    newPage = False
    if title[-1] == "*":
        newPage = True
        title = title[:-1]

    if not os.path.exists("img/"+filepath):
        print(title + " does not exit.")
        sys.exit()

    images.append({
        "title": title,
        "filepath": "img/"+filepath,
        "newPage": newPage
    })

bar = ChargingBar('Creating PDF', max=len(images))

pages = []

pages.append([images.pop(0)])

while (len(images)):
    page = []
    image1 = images.pop(0)
    page.append(image1)
    if image1["newPage"]:
        pages.append(page)
        continue

    if (len(images)):
        image2 = images.pop(0)
        if image1["newPage"]:
            pages.append(page)
            page = [image2]
        else:
            page.append(image2)
    pages.append(page)

index_no = input('Enter your Index Number: ')
name = input("Name with initials: ")
prac_num = input("Enter Practical Number: ")
prac_name = input("Enter Practical Name: ")
sub_date = input("Enter Submission Date: ")

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=15)
pdf.set_text_color(0, 0, 0)
pdf.text(15, 20, txt="Module Code: ER2034")
pdf.text(15, 30, txt="Module Name: Principles of Remote Sensing and GIS")
pdf.text(15, 40, txt=f"Practical No: {prac_num}")
pdf.text(15, 50, txt=f"Practical Name: {prac_name}")
pdf.text(15, 60, txt=f"Name: {name}")
pdf.text(15, 70, txt=f"Index No: {index_no}")
pdf.text(15, 80, txt=f"Submission Date: {sub_date}")

pdf.set_font("Arial", size=10)
image1 = pages.pop(0)[0]
pdf.text(15, 100, txt=image1["title"])
pdf.image(image1["filepath"], x=15, y=105, w=180)
bar.next()

for page in pages:
    pdf.add_page()

    image = page.pop(0)
    pdf.text(15, 20, txt=image["title"])
    pdf.image(image["filepath"], x=15, y=25, w=180)
    bar.next()

    if not len(page):
        continue

    image = page.pop(0)
    pdf.text(15, 150, txt=image["title"])
    pdf.image(image["filepath"], x=15, y=155, w=180)
    bar.next()

bar.finish()
output = f"RS_practical{prac_num}_{index_no}.pdf"
pdf.output(output)


print("Done.")
