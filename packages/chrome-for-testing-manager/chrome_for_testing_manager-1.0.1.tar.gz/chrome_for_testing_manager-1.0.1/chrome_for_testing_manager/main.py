from pathlib import Path
import os
import platform
import requests
import shutil
import json
import zipfile


def init(path=None, version=None, force_download=False):
    if path is None or len(path) == 0:
        path = os.path.join(str(Path.home()), ".chromedriver-manager")
    if not os.path.exists(path):
        os.mkdir(path)
    chrome_path, chromedriver_path = _resolve_chrome_path(path, version)
    if (not force_download and chrome_path is not None and os.path.exists(chrome_path) and
            chromedriver_path is not None and os.path.exists(chromedriver_path)):
        return chrome_path, chromedriver_path

    if version is None or len(version) == 0:
        version = _resolve_latest_version()
    print(f"Chrome version to download: {version}")

    target_dir = os.path.join(path, version)
    if os.path.exists(target_dir) and len(os.listdir(target_dir)) > 0:
        shutil.rmtree(target_dir)
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    chrome_version = _resolve_chrome_version_source(version)
    _download_chromedriver(target_dir, chrome_version)
    _download_chrome(target_dir, chrome_version)
    return _resolve_chrome_path(path, version)


def _download_chromedriver(target_dir, chrome_version):
    system_suffix = _system_suffix()
    downloads = chrome_version.get("downloads").get("chromedriver")
    chromedriver = [f for f in downloads if f.get('platform') == system_suffix][0]
    url = chromedriver.get('url')
    target_file = os.path.join(target_dir, f"chromedriver-{system_suffix}.zip")
    _download_and_extract(url, target_file, target_dir)


def _download_chrome(target_dir, chrome_version):
    system_suffix = _system_suffix()
    downloads = chrome_version.get("downloads").get("chrome")
    chrome = [f for f in downloads if f.get('platform') == system_suffix][0]
    url = chrome.get('url')
    target_file = os.path.join(target_dir, f"chrome-{system_suffix}.zip")
    _download_and_extract(url, target_file, target_dir)


def _download_and_extract(url, target_file, extract_dir):
    file_name = os.path.basename(target_file)

    response = requests.get(url, stream=True)
    content_length = int(response.headers['content-length'])
    data_count = 0
    print(f"\r[    0%] Downloading {file_name}: {url}0%", end="")
    with open(target_file, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
                data_count = data_count + len(chunk)
            progress = round(data_count / content_length * 100, 2)
            print(f"\r[{str(progress).rjust(5)}%] Downloading {file_name}: {url}", end="")
    print(end="\n")
    _extract(target_file, extract_dir)
    os.remove(target_file)


def _resolve_chrome_version_source(version):
    content = requests.get(
        "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json",
        headers={
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
        }
    ).content
    data = json.loads(content)
    versions = data.get("versions")
    version_matched = [v for v in versions if v.get("version") == version]
    return version_matched[0] if len(version_matched) > 0 else None


def _resolve_latest_version():
    content = requests.get("https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE", headers={
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
    }).content
    return content.decode("utf-8")


def _resolve_chrome_path(path, version):
    if path is None or len(path) == 0:
        return None, None
    if not os.path.exists(path):
        return None, None
    files = os.listdir(path)
    if len(files) == 0:
        return None, None
    if version is None or len(version) == 0:
        version = max(files)

    system_suffix = _system_suffix()
    chrome_path = os.path.join(path, version, f"chrome-{system_suffix}")
    if system_suffix.startswith("win"):
        chrome_path = os.path.join(chrome_path, "chrome.exe")
    elif system_suffix.startswith("mac"):
        chrome_path = os.path.join(
            chrome_path, "Google Chrome for Testing.app", "Contents", "MacOS", "Google Chrome for Testing"
        )
    else:
        chrome_path = os.path.join(chrome_path, "chrome")
    chromedriver_path = os.path.join(path, version, f"chromedriver-{system_suffix}",
                                     f"chromedriver{'.exe' if system_suffix.startswith('win') else ''}")
    return chrome_path, chromedriver_path


def _system_suffix():
    system_info = platform.uname()
    if system_info.system == 'Darwin':
        return "mac-arm64" if system_info.machine == 'arm64' else "mac-x64"
    if system_info.system == 'Linux':
        return "linux64"
    if system_info.system == 'Windows':
        return "win64" if system_info.machine == 'AMD64' else "win32"
    return "linux64"


def _extract(zip_file, target):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        for zip_info in zip_ref.infolist():
            extracted_path = zip_ref.extract(zip_info, target)

            # 处理符号链接
            is_symlink = (zip_info.external_attr >> 16) & 0o120000 == 0o120000
            if is_symlink:
                with open(extracted_path) as f:
                    symlink_target = f.read()
                os.remove(extracted_path)
                os.symlink(symlink_target, extracted_path)
            # 处理文件权限
            if not is_symlink and not zip_info.is_dir():
                mode = zip_info.external_attr >> 16 & 0xFFFF
                os.chmod(extracted_path, mode)


if __name__ == "__main__":
    print(init(force_download=True))
