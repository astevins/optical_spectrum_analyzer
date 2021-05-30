# Optical Spectrum Analyzer GUI
The OSA GUI provides an interface for downloading and plotting spectrums from the virtual OSA at http://flaskosa.herokuapp.com/

# Installation Instructions
* A standalone Windows executable file can be downloaded from releases
* To run the app from source code with Python (assumes the latest versions of Python and pip are installed)
  * Clone the source code
  * Run command prompt as administrator in the root directory of the project:
    * `pip install -r requirements.txt` to install dependencies
    * `python setup.py install` to install the osa package
    * `start_osa_gui` to run the gui

# Features
* Retrieve and plot single traces, or continously update plot with new traces at 1 Hz
* Display x-axis in units of wavelength or frequency
  * Note: Conversion from wavelength to frequency assumes the waves travel at the speed of light (c)
* Save an image of the currently displayed plot with the menu: File > Save
  * Change the directory where plot images are saved with File > Set directory

Built with Python and PyQt5 
