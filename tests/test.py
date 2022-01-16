import sys
import os
sys.path.append(os.path.join('template_autofill'))

import src

PPT_TEMPLATE_PATH = os.path.join('tests', 'test_data', 'Certificate_test.pptx')
DATA_PATH = os.path.join('tests', 'test_data', 'data_test.xlsx')
OUT_FILE_PATH = os.path.join('tests', 'out_dir', 'out.pptx')
OUT_DIR = os.path.join('tests', 'out_dir')

pres = src.read_presentation(PPT_TEMPLATE_PATH)
data = src.read_data(DATA_PATH)

new_pres = src.fill_pres_with_data(pres, data)
src.save_presentation(new_pres, OUT_FILE_PATH)


src.fill_sep_pres_with_data(pres, data, os.path.join('tests', 'out_dir'))
src.save_files_as_zip(os.path.join('tests', 'out_dir'), os.path.join('tests', 'out_zip'))
