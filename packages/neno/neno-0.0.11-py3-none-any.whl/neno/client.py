import typer
import zipfile, tempfile
import datetime
from .app import create_flask_app
from .server import gunicorn_run
from prettytable import PrettyTable
import requests
from requests.exceptions import ConnectionError
from .models import EndpointSchema, EndpointRunSchema
from typing_extensions import Annotated
import os, json

def get_neno_server_url():
  url = os.getenv("NENO_SERVER_URL", "http://127.0.0.1:5000")
  if not url.startswith("http://") and not url.startswith("https://"):
    url = "http://" + url # Assume http if no protocol is specified
  return url

def get_endpoints():
  response = requests.get(f"{get_neno_server_url()}/manage/endpoints")
  if response.status_code == 200:
    return [EndpointSchema().load(e) for e in response.json()]
  else:
      raise Exception(f"Failed to get endpoints: {response.status_code} {response.text}")

def print_connection_error(err: ConnectionError):
  print(f"Failed to connect to neno server at {get_neno_server_url()}")
  print(f"Make sure the server is running and the client is able to reach it. Raw error is: {err}")

def get_runs(endpoint_name: str):
  response = requests.get(f"{get_neno_server_url()}/manage/runs/" + endpoint_name)
  runs = response.json()
  if response.status_code == 200:
    return [EndpointRunSchema().load(r) for r in runs]
  else:
    raise Exception(f"Failed to get runs for {endpoint_name}: {response.status_code} {response.text}")

cliApp = typer.Typer()
getApp = typer.Typer()
addApp = typer.Typer()
cliApp.add_typer(getApp, name="get", short_help="Get information on various resources.")
cliApp.add_typer(addApp, name="add", short_help="Add resources to the noto server.")

@cliApp.command(short_help="Start neno server.",
                help="""Start the neno server and begin serving endpoints. Be sure to first install the server dependencies by running `pip install \"neno[server]\"`.
                This command will look for a config.yaml file in the current directory and use it to configure the server.
                The server will listen on 0.0.0.0:<port>, where port is 5000 by default.
                """, name="serve")
def serve(config_file: Annotated[str, typer.Option(help="The path to the config file to use. If not specified, will look for a config.yaml in the current folder.")] = "config.yaml"):
  app, config = create_flask_app(config_file)
  print(f"Starting server on {config['host']}:{config['port']}...")
  try:
    gunicorn_run(app, port=config['port'])
  except ImportError as e:
    print("Failed to start server. Make sure you have installed neno[server]. You can do so by running `pip install \"neno[server]\"`.")
    print(f"Raw error: {e}")

@getApp.command(short_help="List installed endpoints.")
def endpoints(show_curl: Annotated[bool, typer.Option(help="Generate a curl command")] = False):
  endpoint = []
  try:
    endpoints = get_endpoints()
  except ConnectionError as e:
    print_connection_error(e)
    return
  table = PrettyTable()
  field_names = ["Method", "URI", "Content Type"]
  if show_curl:
    field_names.append("curl Command")
  table.field_names = field_names
  for endpoint in endpoints:
    row = [endpoint.get('method'), "/api/" + endpoint.get('name'), endpoint.get('content_type')]
    if show_curl:
      row.append(f"curl -X {endpoint.get('method')} {get_neno_server_url()}/api/{endpoint.get('name')}")
    table.add_row(row)
  if show_curl:
    print("Note: You may pass additional parameters by appending them as query parameters to the URI in the curl command.")
  print(table)

@getApp.command(short_help="Get runs for an endpoint.")
def runs(endpoint_name: str, limit: int = 10):
  runs = []
  try:
    runs = get_runs(endpoint_name)
  except ConnectionError as e:
    print_connection_error(e)
    return
  table = PrettyTable()
  table.field_names = ["ID", "Success", "Timestamp", "Error Message"]
  runs.sort(key=lambda x: float(x.get('timestamp') or 0), reverse=True)
  runs = runs[:limit]
  for run in runs[::-1]:
    ts = "Unknown"
    if run.get('timestamp') is not None:
      ts = datetime.datetime.fromtimestamp(run.get('timestamp')).strftime('%Y-%m-%d %H:%M:%S')
    err = run.get('error_message')[0:50] + "..." if run.get('error_message') is not None else None
    table.add_row([run.get('id'), run.get('success'), ts, err])
  print(table)

def upload_endpoint(endpoint_name: str,
                    notebook_file: str,
                    additional_resources: list[str],
                    method: str = 'GET',
                    content_type: str = 'application/json',
                    kernel: str = 'python3',
                    keep_runs: str = 'failed'):
  manifest = {
    'name': endpoint_name,
    'method': method,
    'notebook': notebook_file,
    'content_type': content_type,
    'kernel': kernel,
    'keep_runs': keep_runs,
  }
  files = {
    'manifest': json.dumps(manifest),
  }
  files[notebook_file] = open(notebook_file, 'rb')
  for res in additional_resources:
    files[res] = open(res, 'rb')
  response = None
  try:
    response = requests.post(f"{get_neno_server_url()}/manage/endpoints", files=files)
  except ConnectionError as e:
    print_connection_error(e)
    return
  if response.status_code != 200:
    raise Exception(f"Failed to upload endpoint: {response.status_code} {response.text}")
  
@addApp.command(short_help="Upload a new endpoint to the noto server.")
def endpoint(name: Annotated[str, typer.Argument(..., help="The name of the endpoint to create.")],
             notebook: Annotated[str, typer.Option(..., help="The notebook to run when this endpoint is called.")],
             file: Annotated[list[str], typer.Option(..., help="Additional files to upload with the endpoint. The files will be available in the notebook's working directory.")] = [],
             content_type: Annotated[str, typer.Option(help="The content type of the response. If you choose application/json MAKE SURE that you notebook's output is valid JSON.")] = 'text/plain',
             keep_runs: Annotated[str, typer.Option(help="When to keep the output of runs for this endpoint. Options: always, failed, none.")] = 'failed',
             kernel: Annotated[str, typer.Option(help="The kernel to use when running the notebook.")] = 'python3',
             method: str = "GET"):
  try:
    upload_endpoint(name, notebook, file, method=method, keep_runs=keep_runs, kernel=kernel, content_type=content_type)
  except ConnectionError as e:
    print_connection_error(e)
    return
  print(f"Uploaded endpoint {name}.")

kernelsApp = typer.Typer()
cliApp.add_typer(kernelsApp, name="kernels", short_help="Get information about the kernels installed on the noto instance.")

@kernelsApp.command(short_help="List installed kernels.")
def list():
  response = None
  try:
    response = requests.get(f"{get_neno_server_url()}/manage/kernels")
  except ConnectionError as e:
    print_connection_error(e)
    return
  if response.status_code == 200:
    kernels = response.json()
    table = PrettyTable()
    table.field_names = ["Kernel ID", "Display Name", "Language"]
    for kernel_key in kernels.get("kernelspecs"):
      kernel = kernels.get("kernelspecs").get(kernel_key)
      spec = kernel.get('spec') if kernel is not None else None
      table.add_row([kernel_key, spec.get('display_name') if spec is not None else "???", spec.get('language') if spec is not None else "???"])
    print(table)
  else:
    raise Exception(f"Failed to get kernels: {response.status_code} {response.text}")

fetchApp = typer.Typer()
cliApp.add_typer(fetchApp, name="fetch", short_help="Download resources from the noto server.")
@fetchApp.command(short_help="Download the output of a run.")
def run(endpoint_name: str, run_id: str, inspect: bool = False):
  """Save the zipped output of a run to the current directory."""
  download_url = f"{get_neno_server_url()}/manage/runs/{endpoint_name}/{run_id}/data"
  response = None
  try:
    response = requests.get(download_url)
  except ConnectionError as e:
    print_connection_error(e)
    return
  temp_zip_file = tempfile.mktemp() + ".zip"
  if response.status_code == 200:
    with open(temp_zip_file, "wb") as file:
      file.write(response.content)
      print(f"Downloaded {temp_zip_file}")
  else:
    raise Exception(f"Failed to download run data: {response.status_code} {response.text}")
  
  if inspect:
    tempdir = tempfile.mkdtemp()
    with zipfile.ZipFile(temp_zip_file, 'r') as zip_ref:
      zip_ref.extractall(tempdir)
    print(f"Extracted {temp_zip_file} to {tempdir}. Will now start a Jupyter notebook server in this directory.")
    os.system(f"jupyter lab --notebook-dir={tempdir}")

deleteApp = typer.Typer()
cliApp.add_typer(deleteApp, name="delete", short_help="Delete resources from the noto server.")

@deleteApp.command(name="endpoint", short_help="Delete an endpoint.")
def delete_endpoint(name: Annotated[str, typer.Argument(help="The name of the endpoint to delete.")],
                    method: Annotated[str, typer.Argument(help="Method of the endpoint to delete.")] = "GET",):
  response = None
  try:
    response = requests.delete(f"{get_neno_server_url()}/manage/endpoints/" + name)
  except ConnectionError as e:
    print_connection_error(e)
    return
  if response.status_code < 200 or response.status_code >= 400:
    raise Exception(f"Failed to delete endpoint: {response.status_code} {response.text}")
  print(f"Deleted endpoint {name}.")
