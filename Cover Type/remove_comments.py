import json
import os
import re

def remove_comments_from_notebook(notebook_path):
    """Remove all Python comments from a Jupyter notebook."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    modified = False
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            source = cell.get('source', [])
            if isinstance(source, str):
                source = [source]
            
            new_source = []
            for line in source:
                stripped = line.strip()
                if stripped.startswith('#'):
                    modified = True
                    continue
                line_without_comment = re.sub(r'\s+#.*$', '', line)
                if line_without_comment != line:
                    modified = True
                new_source.append(line_without_comment)
            
            cell['source'] = new_source
    
    if modified:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1, ensure_ascii=False)
        return True
    return False

notebooks = [
    r'eda\01_exploratory_data_analysis.ipynb',
    r'forest-cover-type-preprocessing-eda.ipynb',
    r'logistic_regression\01_preprocessing.ipynb',
    r'logistic_regression\02_training.ipynb',
    r'neural_network\01_preprocessing.ipynb',
    r'neural_network\02_training.ipynb',
    r'svm\01_preprocessing.ipynb',
    r'svm\02_training.ipynb'
]

base_dir = os.getcwd()
print(f"Working directory: {base_dir}\n")

for notebook in notebooks:
    notebook_path = os.path.join(base_dir, notebook)
    if os.path.exists(notebook_path):
        print(f"Processing: {notebook}")
        if remove_comments_from_notebook(notebook_path):
            print(f"  ✓ Comments removed")
        else:
            print(f"  - No comments found")
    else:
        print(f"  ✗ File not found: {notebook}")

print("\nDone!")
