# Chrome for Testing Manager

![PyPI - Version](https://img.shields.io/pypi/v/chrome-for-testing-manager)
![Github license](https://img.shields.io/github/license/sukaiyi/chrome-for-testing-manager-python)

Thanks to the [Chrome for Testing](https://developer.chrome.com/blog/chrome-for-testing) project for resolving the issue
of mismatch between Chrome and Chromedriver versions in browser automation, witch is caused by Chrome automatic updates.

But we still need to manually download and manage Chrome and Chromedriver.

So `Chrome for Testing Manager`: A Python project that automatic download and manage Chrome and Chromedriver, and
ensures
that their versions match.

## Usage

1. Install

```bash
pip install chrome-for-testing-manager
```

2. Just call `chrome_for_testing_manager.init`, which will download and return the local path of chrome & chromedriver.

```python
from chrome_for_testing_manager import init

chrome_path, chromedriver_path = init()

# and then init selenium or any other ... ⬇️
# options = Options()
# options.binary_location = chrome_path
# service = Service(executable_path=chromedriver_path)
# driver = webdriver.Chrome(options, service)
```

## Optional Configuration

```python
from chrome_for_testing_manager import init

chrome_path, chromedriver_path = init(
    version="125.0.6422.78",
    path="path/to/download",
    force_download=False
)

```

| configuration  | description                                                                                                                                                                                                                                                |
|----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| version        | Witch version of chrome & chromedriver to download, latest version of the stable channel by default. [Available versions](https://googlechromelabs.github.io/chrome-for-testing/)                                                                          |
| path           | The local path to download chrome & chromedriver, `~/.chrome-manager` by default.                                                                                                                                                                          |
| forceDownload  | Download chrome & chromedriver even if the local file exists. `false` by default.                                                                                                                                                                          |


