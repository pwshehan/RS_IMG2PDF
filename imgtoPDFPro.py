import sys
import re
import os
import json

from fpdf import FPDF
from progress.bar import ChargingBar
import tabulate


def getFileListText(fileList):
    files = []
    for i in range(len(fileList)):
        files.append(f"{i} | {fileList[i]}")
    return "\n".join(files)


def getNumberInput(question, min, max, default):
    while True:
        inputLine = input(f"{question} ({default}): ")
        if not inputLine:
            return default

        try:
            num = int(inputLine)
        except:
            continue

        if min != False and num < min:
            continue

        if max != False and num > max:
            continue

        return num


def getTextInput(question, default):
    inputLine = input(f"{question} ({default}): ")
    if not inputLine:
        return default

    return inputLine


def getBoolInput(question, default):
    while True:
        inputLine = input(f"{question} y/n ({default}): ")

        if not inputLine:
            inputLine = default

        if inputLine == "y":
            return True

        if inputLine == "n":
            return False


def createImages():
    for i in range(len(fileList)):
        print(getFileListText(fileList))

        fileIndex = getNumberInput(
            "Which file do you select", 0, len(fileList) - 1, 0)
        fileName = fileList.pop(fileIndex)

        title = getTextInput("title", fileName.split(".")[0])

        newPage = getBoolInput("New Page", "n")

        images.append({
            "title": title,
            "filepath": "img/"+fileName,
            "newPage": newPage
        })

    header = images[0].keys()
    rows = [x.values() for x in images]
    print(tabulate.tabulate(rows, header, tablefmt="presto"))

    f = open("images.json", "w")
    f.write(json.dumps(images))
    f.close()


imageLocation = "img/"
fileList = os.listdir(imageLocation)

images = []

if os.path.exists("images.json"):
    f = open("images.json", "r")
    imageList = json.loads(f.read())
    f.close()

    header = imageList[0].keys()
    rows = [x.values() for x in imageList]
    print(tabulate.tabulate(rows, header, tablefmt="presto"))

    if (getBoolInput("Do you need to continue with these images?", "y")):
        images = imageList
    else:
        createImages()
else:
    createImages()

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
    pdf.text(15, 15, txt=image["title"])
    pdf.image(image["filepath"], x=15, y=20, w=180)
    bar.next()

    if not len(page):
        continue

    image = page.pop(0)
    pdf.text(15, 155, txt=image["title"])
    pdf.image(image["filepath"], x=15, y=160, w=180)
    bar.next()

bar.finish()
output = f"RS_practical{prac_num}_{index_no}.pdf"
pdf.output(output)


print("Done.")
