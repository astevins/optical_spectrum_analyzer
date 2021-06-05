# Optical Spectrum Analyzer GUI
The OSA GUI provides an interface for downloading and plotting spectrums from the virtual OSA at http://flaskosa.herokuapp.com/

## Installation Instructions
* A standalone Windows executable file can be downloaded from releases.
* To run the app from source code with Python (assumes the latest versions of Python and pip are installed).
  * Clone the source code
  * Run command prompt in the root directory of the project:
    * (optional) Start a virtual environment for the dependency installation.
    * `pip install -r requirements.txt` to install dependencies.
    * `python -m main` to start the app.

## Features
* Retrieve and plot single traces, or continously update plot with new traces at 1 Hz.
* Display x-axis in units of wavelength or frequency.
  * Note: Conversion from wavelength to frequency assumes the waves travel at the speed of light (c).
* Save an image of the currently displayed plot with the menu: File > Save
  * Change the directory where plot images are saved with File > Set directory

## Dependencies
* Main dependency is PyQt5, which was used to create the GUI and plot.

## What could be improved 
If this was a bigger project, these are main improvements I would want to make:
* More logging of communications between app and server.
* I included some unit tests, but ideally I would include more unit tests (such as tests for the UI) and integration tests.
