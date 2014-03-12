pyBrew
====================
pyBrew is an open source cross-platform homebrewing program built with 
wxPython.

It is tested in Windows (Vista and 7) and Ubuntu, but should work in any 
platform that wxPython works in.

Check out some screenshots in the screenshots folder to see how the interface
looks.

Installation
--------------------------------------------

### Ubuntu

Make sure python 2.7.x is installed (type <code>python --version</code> 
at the terminal) then install wxPython with

    sudo apt-get install python-wxgtk2.8

Clone this repo to a folder on your computer with

    git clone git://github.com/tgvoskuilen/pyBrew.git
    
Run the <code>runPyBrew.py</code> script to open the program.

### Windows 7

First install python 2.7 for [Windows](http://www.python.org/download/), 
then install wxPython 2.8 with the appropriate
[Windows binary](http://www.wxpython.org/download.php)

Then download the source files for 
[pyBrew](http://www.github.com/tgvoskuilen/pyBrew/archive/master.zip) and
unzip them to a folder anywhere on your computer. Double click on 
<code>runPyBrew.py</code> to start the program.

### Mac OSX and Others

Follow the instructions for Windows 7, but choose the Mac installers instead.
I have not tested this.


Usage Guide
--------------------------------------------

### Home
pyBrew manages your projects and recipes. The Home panel shows all your
current ones. You can add new ones with the top menus. All your projects are
stored in the UserData folder in readable text files.
   
### Projects
This is the project explorer, which shows the details of each project.
Use the tabs on the left to navigate categories and as you add your ingredients
the calculated values will show up. This can be handy if you want to 'wing it'
while making a batch.
  
### Recipes
Upload your recipes here. A potential future feature would be to auto-load
a recipe into a new project.
    
    
