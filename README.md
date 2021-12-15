# Team *enter team name here* Small Group project

## Team members
The members of the team are:
- Leonard Marshall Afzal
- Zaid Maraqa
- Kyal Patel
- Encheng Wu
- Guneek Deol

## Project structure
The project is called `system`.  It currently consists of a single app `clubs`.

## Deployed version of the application
The deployed version of the application can be found at [URL](URL).

## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Migrate the database:

```
$ python3 manage.py migrate
```

Seed the development database with:

```
$ python3 manage.py seed
```

Run all tests with:
```
$ python3 manage.py test
```

*The above instructions should work in your version of the application.  If there are deviations, declare those here in bold.  Otherwise, remove this line.*
**We used selenium to test a large portion of our project.**

**Selenium is installed through the requirements, you will need to download and setup the webdriver for selenium**

**To do this on Windows (Chrome): Visit https://chromedriver.chromium.org/downloads and download the appropriate webdriver for your chrome version (settings -> about chrome), then extract it. Then open your command prompt, and type "setx PATH  '%PATH% {the path to the directory where your chromedriver.exe resides}' " 

**To do this on Windows (Firefox): Visit https://github.com/mozilla/geckodriver/releases and download the appropriate webdriver for your Windows machine, then extract it. Then open your command prompt, and type "setx PATH  '%PATH% {the path to the directory where your geckodriver.exe resides}' "


**To do this on MacOS (Chrome): Visit https://chromedriver.chromium.org/downloads and download the appropriate webdriver for your chrome version (settings -> about chrome) then extract the file and move 'chromedriver' to '/usr/local/bin' [using finder, click on the "go" menu then "go to folder" and paste the path]  **

**To do this on MacOS (Firefox): Visit https://github.com/mozilla/geckodriver/releases and download the appropriate webdriver for your macOS version (settings -> about chrome) then extract the file and move 'chromedriver' to '/usr/local/bin' [using finder, click on the "go" menu then "go to folder" and paste the path]**

**To do this on Linux (Chrome) : Visit https://chromedriver.chromium.org/downloads and download the appropriate webdriver for your chrome version (settings -> about chrome) then extract the file. Enter these commands in to your ubuntu terminal:
sudo mv chromedriver /usr/bin/chromedriver 
sudo chown root:root /usr/bin/chromedriver 
sudo chmod +x /usr/bin/chromedriver **

**To do this on Linux (Firefox) : Visit https://github.com/mozilla/geckodriver/releases and download the appropriate webdriver for your chrome version (settings -> about chrome) then extract the file. Enter these commands in to your ubuntu terminal:
sudo mv chromedriver /usr/bin/geckodriver 
sudo chown root:root /usr/bin/geckodriver 
sudo chmod +x /usr/bin/geckodriver**




**selenium opens up a browser window and runs through the website using automation, this is used to test many parts of our website where we couldn't use response or redirect assertions.**

**Please open the owner view and officer view tests and comment out the appropriate browser**

## Sources
The packages used by this application are specified in `requirements.txt`

*Declare are other sources here.*
