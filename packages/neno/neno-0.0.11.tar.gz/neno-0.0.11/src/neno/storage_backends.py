from .models import EndpointSchema, EndpointRunSchema, FsBackendSchema
import os, json, shutil, tempfile
from werkzeug.datastructures import FileStorage
from .util import ensure_dir

class StorageBackend:
  def __init__(self, config):
    self.config = config
  
  def save_run(self, run: EndpointRunSchema):
    """Save the output of a run to the storage backend and return the URI/path to the directory containing the saved output."""
    raise NotImplementedError()
  
  def get_run_as_file(self, run_id: str):
    """Return path to the zip file containing the run output."""
    raise NotImplementedError()
  
  def list_endpoints(self) -> list[EndpointSchema]:
    raise NotImplementedError()
  
  def save_endpoint(self, endpoint: EndpointSchema, files: list[FileStorage]):
    raise NotImplementedError()
  
  def delete_endpoint(self, endpoint_name: str, method: str):
    raise NotImplementedError()

class FsBackend(StorageBackend):
  def __init__(self, config: FsBackendSchema):
    super().__init__(config)
    self.path = os.path.abspath(config['path'])
    ensure_dir(self.path)
    ensure_dir(os.path.join(self.path, 'endpoints'))
    ensure_dir(os.path.join(self.path, 'runs'))
  
  def _get_run_path(self, endpoint_name: str, run_id: str):
    runs_path = os.path.join(self.path, 'runs', endpoint_name)
    target_path = os.path.join(runs_path, run_id)
    return target_path
  
  def save_run(self, run: EndpointRunSchema):
    runs_path = os.path.join(self.path, 'runs', run['endpoint']['name'])
    target_path = os.path.join(runs_path, run['id'])
    ensure_dir(runs_path)
    source_path = os.path.dirname(run['output_notebook'])
    os.rename(source_path, target_path)
    return target_path
  
  def get_run_as_file(self, endpoint_name: str, run_id: str):
    run_path = self._get_run_path(endpoint_name, run_id)
    temp_path = tempfile.mktemp()
    archive_path = shutil.make_archive(run_path, 'zip', run_path)
    shutil.move(archive_path, temp_path)
    return temp_path
  
  def save_endpoint(self, endpoint: EndpointSchema, files: list[FileStorage]):
    endpoints_path = os.path.join(self.path, 'endpoints')
    endpoint['notebook'] = os.path.join(self.path, 'endpoints', endpoint['name'], endpoint['notebook'])
    ensure_dir(endpoints_path)
    self.save_endpoint_data(endpoint, files)
  
  def save_endpoint_data(self, endpoint: EndpointSchema, files: list[FileStorage]):
    """Store local files belonging to an endpoint in the storage backend."""
    endpoint_dir = os.path.join(self.path, 'endpoints', endpoint['name'])
    endpoint_data_dir = os.path.join(endpoint_dir)
    ensure_dir(endpoint_data_dir)
    for f in files:
      path = os.path.join(endpoint_data_dir, f.name)
      ensure_dir(os.path.dirname(path))
      f.save(path)
  
  def delete_endpoint(self, endpoint_name: str, method: str):
    # TODO: Implement method-specific deletion
    endpoint_path = os.path.join(self.path, 'endpoints', endpoint_name)
    shutil.rmtree(endpoint_path)
