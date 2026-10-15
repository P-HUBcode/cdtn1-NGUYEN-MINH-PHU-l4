import os
import win32com.client
import sys

docx_path = os.path.abspath(r"D:\CDTN 1\docs\BT1_2374802013447_NguyenMinhPhu.docx")
pdf_path = os.path.abspath(r"D:\CDTN 1\docs\BT1_2374802013447_NguyenMinhPhu.pdf")

print("Converting:", docx_path, "->", pdf_path)
word = win32com.client.Dispatch("Word.Application")
word.Visible = False

try:
    doc = word.Documents.Open(docx_path)
    # wdFormatPDF = 17
    doc.SaveAs(pdf_path, FileFormat=17)
    page_count = doc.ComputeStatistics(2) # 2 = wdStatisticPages
    doc.Close()
    print(f"SUCCESS: Exported PDF with {page_count} pages.")
except Exception as e:
    print("Error during conversion:", e)
finally:
    word.Quit()
