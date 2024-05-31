import os, json, time, shutil, traceback, subprocess

def create_flask_app(config_file):
  from flask import Flask, request, jsonify, Response, request, send_file
  from .runner import run_notebook
  from flask import Flask
  from .models import EndpointSchema, NotaConfigSchema
  from .storage_backends import FsBackend
  from .config_backends import FsConfigBackend
  from .config import load_config

  def spawn_data_backend(config: NotaConfigSchema):
    if config['backends'] is None or config['backends']['dataBackend'] is None:
      raise ValueError('No data backend configuration found')
    if config['backends']['dataBackend']['filesystem'] is not None:
      return FsBackend(config['backends']['dataBackend']['filesystem'])
    raise ValueError('No valid data backend found in config file')

  def spawn_config_backend(config: NotaConfigSchema):
    if config['backends'] is None or config['backends']['dataBackend'] is None:
      raise ValueError('No data backend configuration found')
    if config['backends']['configBackend']['filesystem'] is not None:
      return FsConfigBackend(config['backends']['configBackend']['filesystem'], config['port'])
    raise ValueError('No valid config backend found in config file')

  config = load_config(config_file)

  app = Flask(__name__)

  data_backend = spawn_data_backend(config)
  config_backend = spawn_config_backend(config)

  def endpoint_key(method, name):
    return '{} {}'.format(method, name)

  def endpoint_key_from_endpoint(endpoint: EndpointSchema):
    return endpoint_key(endpoint['method'], endpoint['name'])

  def endpoint_url(endpoint: EndpointSchema) -> str:
    if config['port'] == 80:
      return '{}/api/{}'.format(config['host'], endpoint['name'])
    return '{}:{}/api/{}'.format(config['host'], config['port'], endpoint['name'])

  @app.route('/api/<endpoint_name>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD', 'TRACE'])
  def run_endpoint(endpoint_name):
    endpoint = config_backend.get_endpoint(endpoint_name, request.method)
    if endpoint is None:
      return jsonify({'status': 'error', 'message': 'Endpoint not found'}), 404

    all_args = request.args.to_dict()
    for k,v in request.form.to_dict():
      all_args[k] = v
    
    output, id, error_message, output_dir = run_notebook(endpoint['notebook'], all_args)
    # decide if we should keep the run output
    keep_runs = endpoint.get('keep_runs')
    if keep_runs == 'always' or (keep_runs == 'failed' and error_message is not None):
      run_data = {
        'id': id,
        'success': error_message is None,
        'output_notebook': f"{output_dir}/output.ipynb",
        'endpoint': endpoint,
        'error_message': error_message,
        'timestamp': time.time()
      }
      output_path = data_backend.save_run(run_data)
      run_data['output_notebook'] = output_path + '/output.ipynb'
      config_backend.save_run(run_data)

    if os.path.exists(output_dir):
      # if we haven't moved the run output somewhere else, delete it
      shutil.rmtree(output_dir)

    # try to return the output in the format requested by the endpoint
    try:
      if endpoint['content_type'] == 'application/json':
        resp = { 'status': 'success' if error_message is None else 'error', 'run_id': id }
        if output is not None:
          resp['response'] = json.loads(output)
        elif error_message is not None:
          resp['message'] = error_message
        return jsonify(resp), 200 if error_message is None else 500
      return Response(output if output else error_message, mimetype=endpoint['content_type'])
    except Exception as e:
      traceback.print_exc()
      return jsonify({'status': 'error', 'message': str(e), 'run_id': id}), 500

  # Endpoint for posting new endpoints
  @app.route('/manage/endpoints', methods=['POST'])
  def add_endpoint():
    endpoint_manifest = request.files.get('manifest')
    if endpoint_manifest is None:
      return jsonify({'status': 'error', 'message': 'Manifest file not found'}), 400
    endpoint_json = json.load(endpoint_manifest.stream)
    endpoint = EndpointSchema().load(endpoint_json)
    try:
      data_backend.save_endpoint(endpoint, [request.files[k] for k in request.files.keys() if k != 'manifest'])
      config_backend.save_endpoint(endpoint)
      return jsonify({'status': 'success', 'url': endpoint_url(endpoint)})
    except Exception as e:
      return jsonify({'status': 'error', 'message': str(e)})

  # Endpoint for listing existing endpoints
  @app.route('/manage/endpoints', methods=['GET'])
  def list_endpoints():
    return jsonify(config_backend.list_endpoints())

  # Endpoint for deleting existing endpoints
  @app.route('/manage/endpoints/<method>/<endpoint_name>', methods=['DELETE'])
  def delete_endpoint(method, endpoint_name):
    config_backend.delete_endpoint(endpoint_name, method=method)
    data_backend.delete_endpoint(endpoint_name, method=method)
    return jsonify({'status': 'success'})

  # Endpoint for displaying existing runs
  @app.route('/manage/runs/<endpoint_name>', methods=['GET'])
  def list_runs(endpoint_name):
    runs = config_backend.list_runs(endpoint_name)
    if 'success' in request.args:
      success = request.args['success'] == 'true'
      runs = [r for r in runs if r['success'] == success]
    return jsonify(runs)

  @app.route('/manage/runs/<endpoint_name>/<run_id>', methods=['GET'])
  def get_run_by_id(endpoint_name, run_id):
    run = config_backend.get_run_by_id(endpoint_name, run_id)
    if run is not None:
      return jsonify(run)
    return jsonify({'status': 'error', 'message': 'Run not found'}), 404

  @app.route('/manage/runs/<endpoint_name>/<run_id>/data', methods=['GET'])
  def get_run_data_by_id(endpoint_name, run_id):
    run = config_backend.get_run_by_id(endpoint_name, run_id)
    if run is None:
      return jsonify({'status': 'error', 'message': 'Run not found'}), 404
    file = data_backend.get_run_as_file(endpoint_name, run_id)
    # TODO: some kind of cleanup of the temp file
    return send_file(file, mimetype='application/zip', as_attachment=True, download_name=f"{run_id}.zip")
  
  @app.route('/manage/kernels', methods=['GET'])
  def list_kernels():
    # run jupyter kernelspec list
    command = ['jupyter', 'kernelspec', 'list', '--json']
    kernelspecs = json.loads(subprocess.run(command, stdout=subprocess.PIPE).stdout.decode('utf-8'))
    return jsonify(kernelspecs)
  
  return app, config
