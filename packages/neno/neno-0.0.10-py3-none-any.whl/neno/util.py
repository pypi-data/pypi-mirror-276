import os, venv, subprocess

def ensure_dir(path: str):
  """Ensure that a directory exists and is readable and writable. If the path exists and is not a directory, raise an error."""
  if os.path.exists(path) and not os.path.isdir(path):
    raise ValueError('Path {} already exists and is not a directory'.format(path))
  if not os.path.exists(path):
    print('Creating directory', path)
    os.makedirs(path)
  if not os.access(path, os.R_OK | os.W_OK):
    raise ValueError('Path {} must readable and writable'.format(path))

def _get_venvs_base_dir():
  return os.path.join(os.path.expanduser('~'), '.neno', 'venvs')

def _get_venv_dir(key):
  venvs_dirs = _get_venvs_base_dir()
  return os.path.join(venvs_dirs, key)

def ensure_venv(key):
  """Create a virtual environment if it doesn't exist and install papermill in it."""
  venvs_dirs = _get_venvs_base_dir()
  ensure_dir(venvs_dirs)
  venv_dir = _get_venv_dir(key)
  if not os.path.exists(venv_dir):
    print(f"Creating venv {venv_dir}")
    venv.create(venv_dir, with_pip=True)
    # install papermill in the venv
    print(f"venv {venv_dir} created. Installing papermill...")
    result = subprocess.run([f"{venv_dir}/bin/pip", "install", "papermill", "ipykernel"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
      result.check_returncode()
    except subprocess.CalledProcessError as e:
      print(e.stderr.decode())
      raise e
    print(f"Installing ipykernel in {venv_dir}...")
    result = subprocess.run([f"{venv_dir}/bin/python", "-m", "ipykernel", "install", "--user"])
    try:
      result.check_returncode()
    except subprocess.CalledProcessError as e:
      print(e.stderr.decode())
      raise e
    print("papermill installed. Venv ready.")

def run_in_venv(key, args: list[str]):
  ensure_venv(key)
  venv_dir = _get_venv_dir(key)
  # call python in the venv with the given args
  python_path = os.path.join(venv_dir, 'bin', 'python')
  command_str = f"{venv_dir}/bin/python {' '.join(args)}"
  print(f"Calling {command_str}...")
  result = subprocess.run([python_path] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  result.check_returncode()
  return result