#----------------------------------------------------------------------
# runPyBrew.py
#
# Created 10/28/2011
#
# Author: Tyler Voskuilen
#
#----------------------------------------------------------------------


# TASKS (Pythonic, Bugs, and Features)
# P   Update names (consistent case, Grain vs Ferm, etc...)
# P   Improve documentation
# B   Fix loading bugs in Windows 7
# F   Add "Show Recipe" functionality to project
# F   Add build from recipe option for projects
#
# B   Still some bugs with no projects... but hardly seems like a big issue
# B   Fix icons in Windows

# New/BeerSmith Features
#  Timeline
#   temperature/time graph ?
#  Build project from recipe
#  Show projects based on this recipe
#  Boil-off calculations built in
#   "Advanced Settings" panel
#  Range bars to show position in ranges
#  Add multiple yeasts to a project
#  Design full-screen
#  All ingredients together, count IBU of grains?
#  Brew date calandar dropdown
#  Export all/export selection
#  Formatted export (to pdf for paper filing) or raw export (csv)
#  Add a "tools" menu
#  Add fermentation profiles, but don't lock projects to them
#  Add an "Ingredients" view and don't hard-code ingredients any more
#
#
# MAJOR TASKS
#  1. Calander view
#      Add more dates to each project (bottle time, etc)
#      Add date dropdown on BrewDate entry
#      Add calander view
#      Get "event" icons for major events, mouseover or click for event text
#
#  2. Ingredients view (then styles view)
#       Remove hard coding of ingredients and styles (pickle)
#
#  3. Multiple yeasts per project (combine attributes by averaging?)
#
#  4. Make "fancy" range bars for all ranges
#
#  5. Add more to "about" menu  
#
#
# BUG LIST
#  Double clicking on a project or recipe doesn't load it (load data not called)
#
#

import wx
import pyBrew

app = wx.App()
pyBrew.MainFrame()
app.MainLoop()
    
