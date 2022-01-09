import copy

import pandas as pd
from pptx import Presentation


def read_presentation(path):
    return Presentation(path)


def save_presentation(prs, path):
    prs.save(path)


def read_data(path):
    df = pd.read_excel(path)
    return df
    
def duplicate_slide(pres, index):
    template = pres.slides[index]
    blank_slide_layout = pres.slide_layouts[0]
    copied_slide = pres.slides.add_slide(blank_slide_layout)
    
    # remove empty shapes from slide master
    for shp in copied_slide.shapes:
        if shp.text == '':
            sp = shp._sp
            sp.getparent().remove(sp)

    for shp in template.shapes:
        el = shp.element
        newel = copy.deepcopy(el)
        copied_slide.shapes._spTree.insert_element_before(newel, 'p:extLst')
    
    return copied_slide

def fill_pres_with_data(pres, data):
    for index, row in data.iterrows():
        slide = duplicate_slide(pres, 0)
        for shape in slide.shapes:
            try:
                shape.text_frame.text = row[shape.text]
            except Exception:
                pass
    return pres
