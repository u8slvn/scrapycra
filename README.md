# ScraPyCra

Python web scraper for automated timesheet reporting (CRA, "Compte Rendu d'Activité" in French).

## Installation

### Install geckodriver:

ScraPyCra uses selenium as scraper with [geckodriver](https://github.com/mozilla/geckodriver) (Firefox).

```sh
wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
sudo sh -c 'tar -x geckodriver -zf geckodriver-v0.24.0-linux64.tar.gz -O > /usr/bin/geckodriver'
sudo chmod +x /usr/bin/geckodriver
rm geckodriver-v0.24.0-linux64.tar.gz
```

### Install wkhtmltopdf:

Allow to convert html to pdf.

```sh
sudo apt-get install wkhtmltopdf
```

### Clone the project:

```sh
git clone git@github.com:u8slvn/scrapycra.git
cd scrapycra
```

### Install dependencies:

```sh
pip install -r requierements.txt
```

### Set environment variables:

**The signature image** must be a **png** file whit **transparent background** and a size of **300x100** pixels.

```sh
export SCRAPYCRA_URL=https://timetracking.url
export SCRAPYCRA_LOGIN=username
export SCRAPYCRA_PASSWORD=password
export SCRAPYCRA_SIGNATURE=/home/user/my_signature.png
```

You can also copy `settings.env.dist` to `settings.env` fill it with your credentials and information and then use `source`. 

```sh
cp settings.env.dist settings.env
source settings.env
```

## How to run ScraPyCra:

```sh
python -m scrapycra --happiness 1 --motivation 4
```

|    options   | shortcut | description                                                                                 |
|:--------------:|:----------:|---------------------------------------------------------------------------------------------|
|  `--happiness` |    `-hn`   | [1-4] Your happiness on the last month. `1` is 'very good', `4` is 'very bad'.              |
| `--motivation` |    `-mv`   | [1-4] Your motivation on the last month. `1` is 'very interesting', `4` is 'very annoying'. |
|  `--headless`  |   ` -hl`   | Run ScraPyCra without head.                                                                 |

For more usage information:

```sh
python -m scrapycra --help
```
