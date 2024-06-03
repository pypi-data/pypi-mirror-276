import papermill as pm
import uuid
import os
import traceback
import json
import base64
from .util import run_in_venv

def run_notebook(pm_notebook_path, pm_parameters):
  random_id = uuid.uuid4().hex
  temp_dir = os.path.join(os.getcwd(), random_id)
  output_path = os.path.join(temp_dir, f"output.ipynb")

  output_dir = temp_dir
  notebook_dir = os.path.dirname(pm_notebook_path)

  # create temp directory if it doesn't exist
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)
  
  # iterate over every file in notebook_dir and create a symlink in temp_dir to it
  for file in os.listdir(notebook_dir):
    os.symlink(os.path.join(notebook_dir, file), os.path.join(temp_dir, file))
  
  base64_params = base64.b64encode(json.dumps(pm_parameters).encode()).decode()
  # TODO: use a better key generation method (e.g. endpoint name + method)
  # create a key for a virtual environment that is unique to the notebook path
  # this way, we can reuse the same venv for multiple runs of the same notebook
  venv_key = str(hash(pm_notebook_path))

  try:
    run_in_venv(venv_key, ["-m", "papermill", pm_notebook_path, output_path, "-b", base64_params, "--cwd", temp_dir])
    response = None
    with open(output_path, 'r') as f:
      output_nb = json.load(f)
      # find cell tagged "response" and return its output as string
      for cell in output_nb['cells']:
        if 'tags' in cell['metadata'] and 'response' in cell['metadata']['tags']:
          response = [output['text'] for output in cell['outputs'] if output['output_type'] == 'stream']
          flattened = ['\n'.join(texts) for texts in response]
          response = '\n'.join(flattened)
      # if no cell tagged "response" found, return the output of the last cell
      if response is None:
        response = output_nb['cells'][-1]['outputs']
        flattened = ['\n'.join(texts) for texts in response]
        response = '\n'.join(flattened)
    return response, random_id, None, output_dir
  except Exception as e:
    traceback.print_exc()
    return None, random_id, repr(e), output_dir
  

  
