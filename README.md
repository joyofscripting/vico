# vico 👩‍💻
***

vico helps to transform a list of text items in a way that it can be easily used in programming.

Steve Jobs  
Tim Cook  
Carver Mead  
Tim O'Reilly  
=> "Steve Jobs", "Tim Cook", "Carver Mead", "Tim O''Reilly'"

***

botelo currently supports:

* Python 3.7.8 (and higher)
* pyperclip 1.8.2 (and higher)
* PySimpleGUI 4.60.3 (and higher)

![vico](http://www.schoolscout24.de/img/vico/vico_gui.png).

## Background
In my daily job as a data analyst I often get list of text items from business which I need to use in my programming or SQL code. Sometimes I get a long list of ids, sometimes a long list of artist or band names.

In the past I copied those lists into an Excel sheet and then tried to add the prefixes, suffixes and delimiters that were necessary to use the information in my Python or SQL code. When I needed the informationen transformed into a single line of text, even more work was needed. Quoting? Another tedious task.

As my colleagues faced the same challenges I finally decided to write a tool for the team. At first it was a command line tool that would transform the text currently available in the clipboard. But then some time ago I discovered [PySimpleGUI](https://www.pysimplegui.org) and immediately decided to make a GUI based tool.

Well, and that is how vico came alive.

## Quick start

I recommend the following approach:

1. Download the source files to your computer
2. Install a new Python environment on your computer (venv)
3. Use the requirements.txt to install the necessary packages (PySimpleGUI and pyperclip) with pip
4. Run vico using "/path/to/your/Python/python /path/to/your/vico_folder/vico.py"

If you are an advanced user and use Windows then you can also create a vico.exe with the help of [auto-py-to-exe](https://pypi.org/project/auto-py-to-exe/). That is how I use it on my work laptop. If you are currently using macOS Monterey then please note that there is currently a [bug](https://github.com/PySimpleGUI/PySimpleGUI/issues/4900), which results in PySimpleGUI displaying a black window.

## Presets
vico will let you create presets with your favourite transform settings. You can also set a surrounding text for the transformed text in a preset:

![vico - Example of surrounding text in a preset](http://www.schoolscout24.de/img/vico/vico_sur_text.png).

Use the format code "{0}" to specify where the transformed text should be placed.

The presets are loaded during application start and saved when the application quits. They are located in a JSON file named vico_settings.json.



## Yes, vico trims every line!
Currently vico trims whitespace from every line. So don't be surprised about that. Maybe I will make trimming optional in the future. Who knows.

## History

### Version 1.0.1 (2022-09-21)
* Now you can also include a surrounding text in presets

### Initial version (2022-09-05)
The initial version featuring presets was released.