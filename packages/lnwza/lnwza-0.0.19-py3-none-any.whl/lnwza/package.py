import json
from urllib.request import urlopen

def get_latest_package_version(package):
  with urlopen(f'https://pypi.org/pypi/{package.__name__}/json') as response:
      data = json.load(response)
  return data['info']['version']

def get_current_package_version(package):
  return package.__version__

def current_is_latest_package_version(package):
  return get_current_package_version(package) == get_latest_package_version(package)

if __name__ == '__main__':
  import requests

  print(requests.__name__)
  print('current vertion :', get_current_package_version(requests))
  print('last version :', get_latest_package_version(requests))
  print('current is latest version :', current_is_latest_package_version(requests))
