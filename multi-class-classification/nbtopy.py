from nbformat import read, NO_CONVERT

with open("multi-label-classification.ipynb") as fp:
    notebook = read(fp, NO_CONVERT)
cells = notebook['cells']
code_cells = [c for c in cells if c['cell_type'] == 'code']
for cell in code_cells:
    print(cell['source'])