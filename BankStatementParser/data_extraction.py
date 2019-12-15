# Extract the data from the bank statement pdfs with help from the tabula library

import tabula
import pikepdf
import glob
import os
import numpy as np
import pandas as pd
import shutil

for year in [2014, 2015, 2016, 2018, 2019]:
    os.chdir('./Unsecured_Statements/{}'.format(year))

    # these are the dimensions of the area I am scanning for the pdf
    top, left, height, width = 37.22, 46.59, 544.66, 306.41

    for file in glob.glob('*.pdf'):
        
        pdf = pikepdf.open(file)
        num_pages = len(pdf.pages)
        print("num_pages is {}\n range is {}".format(num_pages, range(1,num_pages-1)))
        for page in range(1,num_pages-1):

            print("page before df initiated: {}, file: {}".format(page, file))
            df = tabula.read_pdf(file, pages=page, \
                    multiple_tables=False, \
                    area=[top, left, top+height, left+width], \
                    pandas_options= {'header': None}, silent = True)

            if (str(type(df)) == "<class 'pandas.core.frame.DataFrame'>"):
                        
                assert str(type(df)) == "<class 'pandas.core.frame.DataFrame'>"
                
                num_col = df.columns.shape[0]
                df = df.drop(list(range(4, num_col)), axis=1) if num_col > 3 else ''
                df = df.drop([1], axis=1)

                df[3] = df[3].str.replace('[^0-9.-]', '')
                
                df[3] = df[3].replace("(\s*.\s*)", np.nan)
                df[3] = df[3].replace('', np.nan)
                df = df.dropna().reset_index()
                df['year'] = year
                total = df[3].dropna().astype(np.float).sum()
                print("\nfile: {} --total: {} --page: {}\n".format(file, total, page))
                print("\n{}\n".format(df))
                with open('../../data.csv', 'a') as f:
                    df.to_csv(f, header=False)
            else:
                page += 1
    os.chdir('../../')
        