import requests

class VoxelWorldAPI:
    def __init__(self, base_url='https://voxelworld.ru/api/'):
        self.base_url = base_url
        self.headers = {'Accept': 'application/json'}

    def get_mods(self, params=None):
        url = f'{self.base_url}mods'
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_mod_by_id(self, mod_id):
        url = f'{self.base_url}mods/{mod_id}'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def download_mod(self, mod_id, mod_version):
        url = f'{self.base_url}mods/{mod_id}/version/{mod_version}/download'
        response = requests.get(url)
        if response.status_code == 200:
            with open(f'{mod_id}_{mod_version}.zip', 'wb') as file:
                file.write(response.content)
            print(f'Mod {mod_id} version {mod_version} downloaded successfully.')
        else:
            print(f'Failed to download mod {mod_id} version {mod_version}.')
            
    def search_mod_by_name(self, mod_name):
        url = f'{self.base_url}mods'
        params = {'title': mod_name}
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None

