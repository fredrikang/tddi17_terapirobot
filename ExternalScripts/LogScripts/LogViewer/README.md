# Log Viewer
Used to read and export logs created in a human readable format.
## Running
 - Linux:
   - Make sure python3 is installed
   - Make sure pip3 is installed
   - run the ```run_linux.sh``` file

 - Windows:
   - Run the ```run_windows.bat``` file

## Python Requirements
 - tkinter
 - fpdf

## Usage
![Important Sections](resource/desc.png?raw=true "Important Sections")

The program will read all logs from /user/FurhatLogs (i.e. the user's home folder). The available logs will be presented in a list in the left corner, see (1.).
Clicking a timestamp will present the interaction between the user and robot for that log, see (2.).

To export a file navigate to ```File - Export```, see (3.), and select either ```Export PDF``` or ```Export Text```.