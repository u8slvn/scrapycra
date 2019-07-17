# ScraPyCra

Python web scraper for automated timesheet reporting.

## Installation

##### Install geckodriver:

ScraPyCra use selenium as scraper with [geckodriver](https://github.com/mozilla/geckodriver) (FireFox).

```bash
wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
sudo sh -c 'tar -x geckodriver -zf geckodriver-v0.24.0-linux64.tar.gz -O > /usr/bin/geckodriver'
sudo chmod +x /usr/bin/geckodriver
rm geckodriver-v0.24.0-linux64.tar.gz
```

##### Install wkhtmltopdf:

```bash
sudo apt-get install wkhtmltopdf
```

##### Install dependencies:

```bash
pip install -r requierements.txt
```

##### Set environment variables:

```bash
export SCRAPYCRA_URL=https://timetracking.url
export SCRAPYCRA_LOGIN=username
export SCRAPYCRA_PASSWORD=password
export SCRAPYCRA_SIGNATURE=/home/me/my_signature.png
```

You can also copy `settings.env.dist` to `settings.env` and use `source`. 

```bash
cp settings.env.dist settings.env
source settings.env
```

##### Start ScraPyCra:

```bash
python -m scrapycra --happiness 1 --motivation 4
```

|    options   | shortcut | description                                                                                 |
|:------------:|:--------:|---------------------------------------------------------------------------------------------|
|  --happiness |    -hn   | [1-4] Your happiness on the last month. `1` is 'very good', `4` is 'very bad'.              |
| --motivation |    -mv   | [1-4] Your motivation on the last month. `1` is 'very interesting', `4` is 'very annoying'. |
|  --headless  |    -hl   | Run ScraPyCra without head.                                                                 |

For more usage information:

```bash
python -m scrapycra --help
```
