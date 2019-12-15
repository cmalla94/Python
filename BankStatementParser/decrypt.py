# Decrypt the bank statements and move to Unsecured_Statements directory

import os
import glob
import pikepdf
import shutil

# change to Secured_Statements directory to access the statements to be decrypted
os.chdir('./Secured_Statements')

def decrypt(year):

    for file in glob.glob('*{}*.pdf'.format(year)):
        # decrypt

        pdf = pikepdf.open(file)
        new_name = 'Dcrptd_{}'.format(file)
        pdf.save(new_name)

        # move file
        shutil.move(new_name, '../Unsecured_Statements/{}'.format(year))
        print("file: {} moved \n".format(new_name))

# decrypt(2014)
# decrypt(2015)
# decrypt(2016)
# decrypt(2017)
# decrypt(2018)
# decrypt(2019)

