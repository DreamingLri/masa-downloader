import json
import os
from pathlib import Path

import questionary
import requests
from tqdm import tqdm


CONFIG_FILE = "config.json"

def init_config(): # 初始化配置文件
    config = {
        "repositories": [
        {
            "owner": "sakura-ryoko",
            "repo": "litematica",
            "version": "1.21.4"
        },
        {
            "owner": "sakura-ryoko",
            "repo": "malilib",
            "version": "1.21.4"
        },
        {
            "owner": "sakura-ryoko",
            "repo": "tweakeroo",
            "version": "1.21.4"
        },
        {
            "owner": "sakura-ryoko",
            "repo": "minihud",
            "version": "1.21.4"
        },
        {
            "owner": "sakura-ryoko",
            "repo": "itemscroller",
            "version": "1.21.4"
        },
        {
            "owner": "sakura-ryoko",
            "repo": "syncmatica",
            "version": "1.21.4"
        },
        ],
        "download_dir": None
    }

    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def load_config(): # 加载配置文件
    try:
        with open(CONFIG_FILE) as f:
            config = json.load(f)


        download_dir = config.get('download_dir', None)
        if len(download_dir) > 0:
            path_obj = Path(download_dir).expanduser()
            path_obj = path_obj.resolve()
        else:
            path_obj = Path(str(Path.home() / "Downloads"))

        path_obj.mkdir(parents=True, exist_ok=True)
        config['download_dir'] = str(path_obj)

        return config
    except Exception as e:
        init_config()
        print(f"Error loading config: {e}, initializing new config file.")
        exit(1)

def select_repos(repos): # 选择仓库
    choices = [
        questionary.Choice(
            f"{repo['owner']}/{repo['repo']}-{repo['version']}",
            value=repo
        ) for repo in repos
    ]
    
    selected = questionary.checkbox(
        "请用 ↑ ↓ 选择仓库（空格选中，回车确认）",
        choices=choices,
        validate=lambda x: True
    ).ask()
    
    return selected or []

def get_latest_release(owner, repo, version): # 获取最新Release信息
    try:
        response = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}/releases"
        )
        response.raise_for_status()
        releases = response.json()

        for release in releases:
            if release['tag_name'].split("-")[0] == version:
                return release 

    except requests.exceptions.HTTPError as e:
        print(f"Error fetching release: {e.response.status_code} {e.response.reason}")
        return None
    
def download_file(url, save_path): # 下载文件
    download = requests.get(url, stream=True)
    download.raise_for_status()

    save_path = Path(save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)

    total_size = int(download.headers.get('content-length', 0))
    with open(save_path, 'wb') as f, tqdm(
        desc=os.path.basename(save_path),
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in download.iter_content(chunk_size=8192):
            f.write(chunk)
            bar.update(len(chunk))

def main():
    config = load_config()
    selected_repos = select_repos(config['repositories'])
    if not selected_repos:
        print("No repositories selected.")
        exit()

    delete_old = questionary.confirm("是否删除旧版本？", default=True).ask()
    
    for repo in selected_repos:
        owner = repo['owner']
        repo_name = repo['repo']
        version = repo['version']

        print(f"Fetching latest release for {owner}/{repo_name}...")
        release = get_latest_release(owner, repo_name, version)
        if not release:
            continue

        download_path = Path(config['download_dir'])
        os.makedirs(download_path, exist_ok=True)
 
        assets = release['assets']
        browser_url = assets[0]['browser_download_url']
        name = assets[0]['name']

        print(f"Downloading {release['name']}...")

        if delete_old:
            existing_files = list(download_path.glob(name.split("-")[0] + "*"))
            if existing_files:
                for file in existing_files:
                    try:
                        os.remove(file)
                    except Exception as e:
                        print(f"Error deleting {file}: {e}")
        try: 
            download_file(browser_url, os.path.join(download_path, name))
        except Exception as e:
            print(f"Error downloading {name}: {e}")

if __name__ == "__main__":
    main()
    
