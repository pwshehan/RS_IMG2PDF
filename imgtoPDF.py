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

ln1 = "Module Code: ER2034"
ln2 = "Module Name: Principles of Remote Sensing and GIS"
ln3 = f"Practical {prac_num} : {prac_name}"
ln4 = f"Name: {name}"
ln5 = f"Index No: {index_no}"
ln6 = f"Submission Date: {sub_date}"

bar = ChargingBar('Creating PDF', max=len(images))

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=15)
pdf.set_text_color(0, 0, 0)
pdf.text(10, 20, txt=ln1)
pdf.text(10, 30, txt=ln2)
pdf.text(10, 40, txt=ln3)
pdf.text(10, 50, txt=ln4)
pdf.text(10, 60, txt=ln5)
pdf.text(10, 70, txt=ln6)

pdf.set_font("Arial", size=10)
image1 = pages.pop(0)[0]
pdf.text(10, 90, txt=image1["title"])
pdf.image(image1["filepath"], x=10, y=95, w=180)
bar.next()

for page in pages:
    pdf.add_page()

    image = page.pop(0)
    pdf.text(10, 20, txt=image["title"])
    pdf.image(image["filepath"], x=10, y=25, w=180)
    bar.next()

    if not len(page):
        continue

    image = page.pop(0)
    pdf.text(10, 150, txt=image["title"])
    pdf.image(image["filepath"], x=10, y=155, w=180)
    bar.next()

bar.finish()
output = f"RS_practical{prac_num}_{index_no}.pdf"
pdf.output(output)


print("Done.")
