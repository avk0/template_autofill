import src

PPT_TEMPLATE_PATH = 'template.pptx'
DATA_PATH = 'data.xlsx'
OUT_FILE_PATH = 'out.pptx'

pres = src.read_presentation(PPT_TEMPLATE_PATH)
data = src.read_data(DATA_PATH)

new_pres = src.fill_pres_with_data(pres, data)

src.save_presentation(new_pres, OUT_FILE_PATH)
