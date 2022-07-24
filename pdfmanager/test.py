from reportlab.pdfgen import canvas
from reportlab.lib import colors
import io
from PyPDF2 import PdfFileReader, PdfFileWriter


textToPrint1 = 'Ea aliquip labore sit eiusmod adipisicing quis ad cillum enim. Ex exercitation proident voluptate voluptate mollit amet veniam dolor ad non exercitation ea nulla commodo. Reprehenderit commodo ex cillum fugiat sunt consequat do. Laborum ullamco esse amet reprehenderit esse elit veniam pariatur tempor. Culpa ea tempor dolor enim incididunt eu ad eu. Mollit proident enim cillum excepteur proident amet fugiat sint est occaecat amet magna do mollit. Esse laboris fugiat id aliquip aute et cillum pariatur et sint Lorem consequat nostrud.'
textToPrint2 = '\n'.join([textToPrint1[i*100:i*100+100] for i in range(len(textToPrint1)%100)])
# Canvas creation
packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=(100,100))
can.setFillColor(colors.lightgrey)
can.setStrokeColor(colors.grey)
can.rect(0,0,100,100, fill=1)
# text writing
textobject = can.beginText()
textobject.setTextOrigin(0,100)
textobject.setFont('Courier', 1.65)
textobject.setFillColor(colors.black)
textobject.textLines(textToPrint2)
can.drawText(textobject)
can.save()
packet.seek(0)

# Pdf writing
inputPdfPath = '/Users/giovannimazzobel/Downloads/Social_Security_Fraud.pdf'
outputPdfPath = '/Users/giovannimazzobel/Scripts/PDFManager/test.pdf'

output = PdfFileWriter()
new_pdf = PdfFileReader(packet)
output.addPage(new_pdf.getPage(0))
outputStream = open(outputPdfPath, "wb")
output.write(outputStream)
outputStream.close()