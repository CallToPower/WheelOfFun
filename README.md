# WheelOfFun

WheelOfFun is the best party game ever! Spin the wheel and fulfill a user-defined task.

## Screenshot

![Screenshot](img/screenshot.png?raw=true)

## Prerequisites

* Python 3
* Windows
  * Install NSIS - http://nsis.sourceforge.net
  * Add Python to PATH variable in environment
  * Add NSIS to PATH variable in environment

## Usage

* Start shell
  * Windows
    * Start shell as administrator
    * `Set-ExecutionPolicy Unrestricted -Force`
* Create a virtual environment
  * `python -m venv venv`
* Activate the virtual environment
  * Mac/Linux
    * `source venv/bin/activate`
  * Windows
    * `.\venv\scripts\activate`
* Install the required libraries
  * `pip install -r requirements.txt`
* Run the app
  * `python src/main/python/Main.py`

## Shipping

* Freeze the app (create an executable)
  * `pyinstaller WheelOfFun.spec`

## Development

pyinstaller WheelOfFun.spec

(Initially created .spec file with: pyinstaller --windowed src/main/python/Main.py --noconfirm --name "WheelOfFun" --icon "src/main/icons/icons.icns")
