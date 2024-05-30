import atexit
import gunicorn.app.base
import random
import sys
import subprocess

from btgitserver.args import parse_args
from btgitserver.config import AppConfig
from btgitserver.defaults import \
default_app_host_address, \
default_app_port, \
default_num_threads, \
default_num_workers, \
default_preload, \
default_repo_search_paths, \
default_ondemand_repo_search_paths, \
default_verify_tls
from btgitserver.logger import Logger

from dulwich import repo
from dulwich.pack import PackStreamReader
from flask_httpauth import HTTPBasicAuth
from flask import Flask, make_response, request, abort
from pathlib import Path

if sys.version_info[0] == 2:
    from StringIO import StringIO
if sys.version_info[0] >= 3:
    from io import BytesIO


# Private variables
__author__ = 'berttejeda'
__original_author = 'stewartpark'

# Read command-line args
args = parse_args()

# Initialize logging facility
logger_obj = Logger(
    logfile_path=args.logfile_path,
    logfile_write_mode=args.logfile_write_mode)
logger = logger_obj.init_logger('app')

verify_tls = args.no_verify_tls or default_verify_tls

# Flask
auth = HTTPBasicAuth()

# Initialize Config Readers
app_config = AppConfig().initialize(
  args=vars(args),
  verify_tls=verify_tls
)

git_ondemand_search_paths = args.ondemand_repo_search_paths or app_config.get('app.ondemand.search_paths', default_ondemand_repo_search_paths)
git_search_paths = args.repo_search_paths or app_config.get('app.search_paths', default_repo_search_paths)
git_search_paths = git_search_paths + git_ondemand_search_paths
app_host_address = args.host_address or app_config.get('app.listen', default_app_host_address)
app_port = args.port or app_config.get('app.port', default_app_port)
gunicorn_preload = args.preload or app_config.get('app.gunicorn.preload', default_preload)
gunicorn_threads = args.threads or app_config.get('app.gunicorn.threads', default_num_threads)
gunicorn_workers = args.workers or app_config.get('app.gunicorn.workers', default_num_workers)

authorized_users = app_config.auth.users
users = [u[0] for u in authorized_users.items()]


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

def get_repos(org, search_paths):
    repo_map = {}

    for git_search_path in search_paths:
        fq_git_search_path = Path(git_search_path).expanduser().joinpath(org)
        logger.debug(f'Building git repo map ...')
        logger.debug(f'Adding git repos under {fq_git_search_path}')
        for p in Path(fq_git_search_path).glob("*"):
            dotgit = Path(p).joinpath(".git")
            if dotgit.is_dir():
                git_directory = p.as_posix()
                git_directory_name = p.name
                if git_directory_name:
                    repo_map[git_directory_name] = git_directory
    logger.debug(f'Finished building git repo map!')
    numrepos = len(list(repo_map.keys()))
    logger.debug(f'Found {numrepos} repo(s)')
    return repo_map


def interrupt():
  logger.info("Stop API")

def start_api(**kwargs):
  """API functions.
  This function defines the API routes and starts the API Process.
  """
  app = Flask(__name__)
  # app.config['MAX_CONTENT_LENGTH'] = 1600 * 1024 * 1024 # 16GB
  # app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB

  @auth.get_password
  def get_pw(username):
      if username in users:
          credential = authorized_users.get(username).password
          return credential
      else:
          return None

  @app.route('/<string:org_name>/<string:project_name>/info/refs')
  @auth.login_required
  def info_refs(org_name, project_name):
      git_repo_map = get_repos(org_name, git_search_paths)
      available_repos = list(git_repo_map.keys())
      service = request.args.get('service')
      if service[:4] != 'git-':
          abort(500)

      logger.info(f'Receiving {org_name}/{project_name}')
      
      if project_name in available_repos:
          return info_refs_header(
              git_repo_map=git_repo_map,
              project_name=project_name,
              service=service
          )
      else:
          logger.info(f'Repo at {org_name}/{project_name} does not currently exist, processing as on-demand')
          ondemand_search_path = random.choice(git_ondemand_search_paths)
          ondemand_org_path = Path(ondemand_search_path).expanduser().joinpath(org_name)
          try:
              if not ondemand_org_path.is_dir():
                  logger.info(f'Creating on-demand repo org path at {ondemand_org_path}')
                  ondemand_org_path.mkdir(parents=True)
              ondemand_project_path = ondemand_org_path.joinpath(project_name).as_posix()
              logger.info(f'Initializing on-demand repo {ondemand_project_path}')
              project_repo = repo.Repo.init(ondemand_project_path, mkdir=True)
              project_repo_config = project_repo.get_config()
              project_repo_config.set("receive", "denyCurrentBranch", "updateInstead")
              project_repo_config.write_to_path()
              logger.info(f'Initialization complete for {ondemand_project_path}')
              git_repo_map = get_repos(org_name, git_search_paths)
              return info_refs_header(
                  git_repo_map=git_repo_map,
                  project_name=project_name,
                  service=service
              )
          except Exception as e:
              logger.error(f"Could not create on-demand project path at {ondemand_project_path}, error was {e}")
              abort(501)

  def info_refs_header(**kwargs):
    git_repo_map = kwargs['git_repo_map']
    project_name = kwargs['project_name']
    service = kwargs['service']
    project_path = [v for k, v in git_repo_map.items() if k == project_name][0]
    p = subprocess.Popen([service, '--stateless-rpc', '--advertise-refs', project_path], stdout=subprocess.PIPE)
    packet = '# service=%s\n' % service
    length = len(packet) + 4
    _hex = '0123456789abcdef'
    prefix = ''
    prefix += _hex[length >> 12 & 0xf]
    prefix += _hex[length >> 8 & 0xf]
    prefix += _hex[length >> 4 & 0xf]
    prefix += _hex[length & 0xf]
    data = prefix + packet + '0000'
    data = data.encode() + p.stdout.read()
    res = make_response(data)
    res.headers['Expires'] = 'Fri, 01 Jan 1980 00:00:00 GMT'
    res.headers['Pragma'] = 'no-cache'
    res.headers['Cache-Control'] = 'no-cache, max-age=0, must-revalidate'
    res.headers['Content-Type'] = 'application/x-%s-advertisement' % service
    p.wait()
    return res

  @app.route('/<string:org_name>/<string:project_name>/git-receive-pack', methods=('POST',))
  @auth.login_required
  def git_receive_pack(org_name, project_name):
      git_repo_map = get_repos(org_name, git_search_paths)
      available_repos = list(git_repo_map.keys())
      if project_name in available_repos:
          project_path = [v for k,v in git_repo_map.items() if k == project_name][0]
          p = subprocess.Popen(['git-receive-pack', '--stateless-rpc', project_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
          data_in = request.data
          pack_file = data_in[data_in.index(b'PACK'):]

          if sys.version_info[0] == 2:
              objects = PackStreamReader(StringIO(pack_file).read)
          if sys.version_info[0] >= 3:
              objects = PackStreamReader(BytesIO(pack_file).read)

          for obj in objects.read_objects():
              if obj.obj_type_num == 1: # Commit
                  logger.debug(obj)
          p.stdin.write(data_in)
          data_out = p.communicate()
          res = make_response(data_out)
          res.headers['Expires'] = 'Fri, 01 Jan 1980 00:00:00 GMT'
          res.headers['Pragma'] = 'no-cache'
          res.headers['Cache-Control'] = 'no-cache, max-age=0, must-revalidate'
          res.headers['Content-Type'] = 'application/x-git-receive-pack-result'
          p.wait()
          logger.info(f'Finished receiving {org_name}/{project_name}')
          return res
      else:
          abort(501)

  @app.route('/<string:org_name>/<string:project_name>/git-upload-pack', methods=('POST',))
  @auth.login_required
  def git_upload_pack(org_name, project_name):
      git_repo_map = get_repos(org_name, git_search_paths)
      available_repos = list(git_repo_map.keys())
      if project_name in available_repos:
          project_path = [v for k,v in git_repo_map.items() if k == project_name][0]
          p = subprocess.Popen(['git-upload-pack', '--stateless-rpc', project_path],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE)
          p.stdin.write(request.data)
          p.stdin.close()
          data = p.stdout.read()
          res = make_response(data)
          res.headers['Expires'] = 'Fri, 01 Jan 1980 00:00:00 GMT'
          res.headers['Pragma'] = 'no-cache'
          res.headers['Cache-Control'] = 'no-cache, max-age=0, must-revalidate'
          res.headers['Content-Type'] = 'application/x-git-upload-pack-result'
          p.wait()
          return res
      else:
          abort(501)

  logger.info("Start API")

  options = {
      'bind': f'{app_host_address}:{app_port}',
      'preload': gunicorn_preload,
      'threads': gunicorn_threads,
      'workers': gunicorn_workers,
  }

  atexit.register(interrupt)
  if args.dev_server:
    app.run(host=app_host_address, port=app_port)
  else:
    StandaloneApplication(app, options).run()    

if __name__ == '__main__':
  start_api()
