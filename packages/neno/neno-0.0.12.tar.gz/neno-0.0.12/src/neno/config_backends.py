import os, json
from .models import FsBackendSchema
from .util import ensure_dir
from .models import EndpointSchema, EndpointRunSchema, FsBackendSchema, ScheduledJobSchema
from werkzeug.datastructures import FileStorage

class ConfigBackend:
  """Base class for config backends
  
  A config backend is a system for storing and retrieving information about a noto cluster,
  the resources it serves, and the runs of those resources. If the backend supports clustering,
  it allows individual noto instances to discover each other and take on different roles.
  """
  def __init__(self, config):
    self.config = config
    self.role_assigned_listeners = []
  
  def list_jobs(self) -> list[ScheduledJobSchema]:
    """Get a list of scheduled jobs of a given type"""
    raise NotImplementedError()
  
  def get_endpoint(self, endpoint_name: str, method: str) -> EndpointSchema:
    """Get an endpoint by its name and method"""
    raise NotImplementedError()
  
  def save_job(self, job: ScheduledJobSchema):
    """Add a scheduled job to the config backend"""
    raise NotImplementedError()
  
  def delete_job(self, job_name: str):
    """Remove a scheduled job from the config backend"""
    raise NotImplementedError()
  
  def list_endpoints(self) -> list[EndpointSchema]:
    """Get a list of resources of a given type"""
    raise NotImplementedError()
  
  def save_endpoint(self, endpoint: EndpointSchema):
    """Add a resource to the config backend"""
    raise NotImplementedError()
  
  def delete_endpoint(self, endpoint_name: str, method: str):
    """Remove a resource from the config backend"""
    raise NotImplementedError()
  
  def list_runs(self, endpoint_name: str) -> list[EndpointRunSchema]:
    """Add a resource to the config backend"""
    raise NotImplementedError()
  
  def get_run_by_id(self, endpoint_name: str, run_id: str) -> EndpointRunSchema:
    """Get a resource by its ID"""
    raise NotImplementedError()
  
  def save_run(self, run: EndpointRunSchema):
    """Save a run of a resource"""
    raise NotImplementedError()

  def get_cluster_members(self) -> list[str]:
    """Get a list of all members in the cluster"""
    raise NotImplementedError()
  
  def has_role(self, member_id: str, role: str):
    """Check if a member has a given role"""
    raise NotImplementedError()
  
  def do_i_have_role(self, role: str):
    """Check if the current member has a given role"""
    return self.has_role(self.get_my_id(), role)
  
  def get_my_id(self) -> str:
    """Get the ID of the current member as it is known to the config backend"""
    raise NotImplementedError()
  
  def add_role_assigned_listener(self, listener: callable):
    """Add a listener for role assignment events"""
    self.role_assigned_listeners.append(listener)
  
  def bootstrap(self):
    """Perform any necessary setup tasks for the config backend"""
    pass


class FsConfigBackend(ConfigBackend):
  def __init__(self, backend_config: FsBackendSchema, port: int):
    super().__init__(backend_config)
    self.path = os.path.abspath(backend_config['path'])
    self.port = port
    self.listener = f"127.0.0.1:{port}"
    ensure_dir(self.path)
    ensure_dir(os.path.join(self.path, 'endpoints'))
    ensure_dir(os.path.join(self.path, 'runs'))
  
  def list_runs(self, endpoint_name: str) -> list[EndpointRunSchema]:
    """List all runs for a given endpoint name.
    
    This method takes the name of an endpoint and returns a list of all recorded runs for that endpoint.
    """
    runs_path = os.path.join(self.path, 'runs', endpoint_name)
    ensure_dir(runs_path)
    runs = []
    for run_file in os.listdir(runs_path):
      if not run_file.endswith('.json'):
        continue
      with open(os.path.join(runs_path, run_file), 'r') as f:
        if f.name.endswith('.json'):
          run = EndpointRunSchema().load(json.load(f))
          runs.append(run)
    return runs

  def list_jobs(self) -> list[ScheduledJobSchema]:
    """List all scheduled jobs in the config backend."""
    jobs_path = os.path.join(self.path, 'jobs')
    ensure_dir(jobs_path)
    jobs = []
    for job_file in os.listdir(jobs_path):
      if not job_file.endswith('.json'):
        continue
      with open(os.path.join(jobs_path, job_file), 'r') as f:
        if f.name.endswith('.json'):
          job = ScheduledJobSchema().load(json.load(f))
          jobs.append(job)
  
  def save_job(self, job: ScheduledJobSchema):
    """Record job metadata in the config backend.
    
    This method takes an job object and saves it to the config backend."""
    jobs_path = os.path.join(self.path, 'jobs')
    ensure_dir(jobs_path)
    job_path = os.path.join(jobs_path, job['name'] + '.json')
    with open(job_path, 'w') as f:
      json.dump(job, f)
  
  def delete_job(self, job_name: str):
    """Remove a scheduled job from the config backend"""
    job_path = os.path.join(self.path, 'jobs', job_name + '.json')
    os.remove(job_path)
  
  def get_run_by_id(self, endpoint_name: str, run_id: str) -> EndpointRunSchema:
    """Get a run by its ID."""
    runs_path = os.path.join(self.path, 'runs', endpoint_name)
    run_path = os.path.join(runs_path, run_id + '.json')
    if not os.path.exists(run_path):
      return None
    with open(run_path, 'r') as f:
      return EndpointRunSchema().load(json.load(f))
  
  def save_run(self, run: EndpointRunSchema):
    """Record run metadata in the config backend.
    
    This method takes a run object and saves it to the config backend. Note that only metadata
    (e.g. the run ID, success/failure status, and error message) is saved here. The actual output
    of the run is persisted in the data backend."""
    runs_path = os.path.join(self.path, 'runs', run['endpoint']['name'])
    ensure_dir(runs_path)
    run_path = os.path.join(runs_path, run['id'] + '.json')
    with open(run_path, 'w') as f:
      json.dump(run, f)
  
  def list_endpoints(self) -> list[EndpointSchema]:
    """List all endpoints in the config backend."""
    endpoints_path = os.path.join(self.path, 'endpoints')
    ensure_dir(endpoints_path)
    endpoints = []
    for endpoint_file in os.listdir(endpoints_path):
      if not endpoint_file.endswith('.json'):
        continue
      with open(os.path.join(endpoints_path, endpoint_file), 'r') as f:
        if f.name.endswith('.json'):
          endpoint = EndpointSchema().load(json.load(f))
          endpoints.append(endpoint)
    return endpoints
  
  def save_endpoint(self, endpoint: EndpointSchema):
    """Record endpoint metadata in the config backend.
    
    This method takes an endpoint object and saves it to the config backend. Note that only metadata
    (e.g. the endpoint name, method, and content type) is saved here. The actual notebook file and any
    additional files are persisted in the data backend. This method is meant to be called in tandem with
    the `save_endpoint` method of the data backend.
    
    In a backend that supports clustering, this method is essential for ensuring that other members of
    the cluster become aware of the new endpoint."""
    endpoints_path = os.path.join(self.path, 'endpoints')
    endpoint['notebook'] = os.path.join(self.path, 'endpoints', endpoint['name'], endpoint['notebook'])
    ensure_dir(endpoints_path)
    endpoint_path = os.path.join(endpoints_path, endpoint['name'] + '.json')
    with open(endpoint_path, 'w') as f:
      json.dump(endpoint, f)
  
  # TODO: cache this
  def get_endpoint(self, endpoint_name: str, method: str) -> EndpointSchema:
    endpoints = self.list_endpoints()
    for endpoint in endpoints:
      if endpoint['name'] == endpoint_name and endpoint['method'].lower() == method.lower():
        return endpoint
  
  def delete_endpoint(self, endpoint_name: str, method: str):
    """Remove the metadata for an endpoint from the config backend.
    
    This will cause the noto server to forget about the endpoint, and it will no longer be accessible."""
    endpoint_path = os.path.join(self.path, 'endpoints', endpoint_name + '.json')
    os.remove(endpoint_path)
  
  def get_cluster_members(self) -> list[str]:
    return [self.listener] # in this simple backend, there is only one member
  
  def has_role(self, member_id: str, role: str):
    """Check if a member has a given role"""
    return True # in this simple backend, there is only one member and it has all roles
  
  def get_my_id(self) -> str:
    """Get the ID of the current member as it is known to the config backend"""
    raise [self.listener]
  
  def bootstrap(self):
    """Performs any initial post-initiation setup tasks for the config backend."""
    # We are the only member of the cluster, so we assign all roles to ourselves
    for listener in self.role_assigned_listeners:
      listener(self.listener, 'scheduler')
