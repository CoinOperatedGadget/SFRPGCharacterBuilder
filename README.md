# SFRPGCharacterBuilder
This project was created to create a Kivy based character generator for the SFRPG.  I am currently working on getting it to a state where I'll be able to release under both Android and Windows.

In it's current state it builds in both environments, but does not have enough features to warrant releasing.  Currently finished:
  - Feats
  - Abilities for the following classes:
    - Soldier
    - Envoy
    - Operative
  - Skills
  - Basic stats
  - PDF Character Sheet Generation

What needs to get done before releasing v1.0
  - All other classes need to be imported
  - Weapons and other equipment
  - Spells
  - Companions (AKA Mechanic)
  
I'm sure there are currently many bugs in the features that do exist.  The effort right now is to get basic functionality and polish afterwards.


# Running from source
If you'd like to run everthing from python, there are a few things to keep in mind.  First is dependencies.  Currently the only dependencies are Kivy and reportlab.  Everything is written with python 3.x in mind and is untested with 2.7.x, including the pickels used to import rulebook data (these will not work with 2.7.x).  For installing Kivy, follow the instructions at the following link (Given for Windows below, the site also has instructions for Linux and Mac):

https://kivy.org/docs/installation/installation-windows.html 

A special note on reportlab.  Using the following command you can install reportlab:

python -m pip install reportlab

Note that there are some issues with the current version of reportlab and the editable fields that the character builder generates for the PDF.  This can be fixed by using the latest version of reportlab from the following:

https://bitbucket.org/rptlab/reportlab

Once dependencies are installed navigate to the root directory of the source and use the following command to run:

python main.py
