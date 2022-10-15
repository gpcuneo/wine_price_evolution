import pdfplumber
from datetime import datetime, timedelta
import locale
from glob import glob
import pandas as pd


def getInfoPDF(pdf_file):
    print(pdf_file)
    title_raw = pdf_file[pdf_file.rfind('\\') + 1 :pdf_file.find('.pdf')]
    title = title_raw[:title_raw.find('Dupont_') + 7]
    date_raw = title_raw[title_raw.find('Dupont_') + 7:]
    date = datetime.strptime(date_raw,'%B_%Y')
    title_in_CSV = title[title.rfind('/'):] + date.strftime("%Y-%m")
    print(title_in_CSV)
    with pdfplumber.open(pdf_file) as pdf :
        data = []
        for page in pdf.pages:
            content = page.extract_text()
            rows = content.split('\n')
            if content.find('Vinos importados') != -1 or content.find("Whisky + Copas") != -1 or content.find("Aceites de oliva") != -1:
                break
            for row in rows:
                if row.find('Vinos de Autor') != -1 or row.find('Página') != -1:
                    continue
                if row.find('Caja') != -1:
                    bodega = row[:row.find('Caja') -1]
                    bodega = bodega.strip()
                else:
                    name = row[:row.find('$') -1]
                    if name.find("(caja") != -1:
                        name = name[:name.find("(caja")]
                        name = name.strip()
                        precio = row[row.rfind('$') +1:row.rfind('\n')]
                        precio = precio.replace(' ', '')
                        precio = precio.replace('.', '')
                        precio = precio[:precio.find(',')]
                        precio = precio.strip()
                        try:
                            precio = int(precio)
                        except:
                            continue
                        info = {
                        'vino': name,
                        'bodega': bodega,
                        'precio': precio,
                        'fecha': date
                        }
                        data.append(info)
    return [title_in_CSV, data]


### START EXECUTION ###
directory_pdfs = 'pdfs/'
direcotry_vinos_csvs = 'csvs/'
locale.setlocale(locale.LC_TIME, 'es_ES')

listPDF = glob(directory_pdfs + "*pdf")

count = 0
for file in listPDF:
  # VINOS #
  listContent = getInfoPDF(file)
  print(listContent[0])
  df = pd.DataFrame(listContent[1])
  print(df)
  df.to_csv(direcotry_vinos_csvs + listContent[0] + ".csv", index = False)