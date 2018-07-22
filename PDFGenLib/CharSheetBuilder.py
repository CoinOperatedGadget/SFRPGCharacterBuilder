# -*- coding: utf-8 -*-
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch, cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import webbrowser

pdfmetrics.registerFont(TTFont('Source Sans Pro-Bold', 'fonts/SourceSansPro-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Electrolize', 'fonts/Electrolize-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Void Pixel-7', 'fonts/void_pixel-7.ttf'))

def MakeDefaultDict():
   cd = {}
   # General Info
   cd['name'] = 'Destructo Bot XJ-71'
   cd['class'] = 'Operative 1'
   cd['race'] = 'Android'
   cd['theme'] = 'Bounty Hunter'
   cd['size'] = 'medium'
   cd['speed'] = '30 ft'
   cd['gender'] = 'N/A'
   cd['homeworld'] = 'Unknown'
   cd['alignment'] = 'N'
   cd['deity'] = 'N/A'
   cd['player'] = 'Noe3'
   # AbilityScores
   cd['strscore'] = '10'
   cd['strmod'] = '0'
   cd['dexscore'] = '10'
   cd['dexmod'] = '0'
   cd['conscore'] = '10'
   cd['conmod'] = '0'
   cd['intscore'] = '10'
   cd['intmod'] = '0'
   cd['wisscore'] = '10'
   cd['wismod'] = '0'
   cd['chascore'] = '10'
   cd['chamod'] = '0'
   cd['upgradedstrscore'] = '10'
   cd['upgradedstrmod'] = '0'
   cd['upgradeddexscore'] = '10'
   cd['upgradeddexmod'] = '0'
   cd['upgradedconscore'] = '10'
   cd['upgradedconmod'] = '0'
   cd['upgradedintscore'] = '10'
   cd['upgradedintmod'] = '0'
   cd['upgradedwisscore'] = '10'
   cd['upgradedwismod'] = '0'
   cd['upgradedchascore'] = '10'
   cd['upgradedchamod'] = '0'
   # Initiative
   cd['inittotal'] = '0'
   cd['initdexmod'] = '0'
   cd['initmiscmod'] = '0'
   # Health, Stamina, and Resolve
   cd['staminapointstotal'] = '20'
   cd['staminapointscurrent'] = '0'
   cd['hitpointstotal'] = '10'
   cd['hitpointscurrent'] = '0'
   cd['resolvepointstotal'] = '4'
   cd['resolvepointscurrent'] = '0'
   # Armor Class
   cd['eactotal'] = '10'
   cd['eacarmorbonus'] = '0'
   cd['eacdexmod'] = '0'
   cd['eacmiscmod'] = '0'
   cd['kactotal'] = '10'
   cd['kacarmorbonus'] = '0'
   cd['kacdexmod'] = '0'
   cd['kacmiscmod'] = '0'
   cd['cmdtotal'] = '18'
   cd['dr'] = '0'
   cd['resistances'] = '5 Electric'
   # Saving Throws
   cd['forttotal'] = '2'
   cd['fortbase'] = '2'
   cd['fortabilitymod'] = '0'
   cd['fortmiscmod'] = '0'
   cd['reftotal'] = '2'
   cd['refbase'] = '2'
   cd['refabilitymod'] = '0'
   cd['refmiscmod'] = '0'
   cd['willtotal'] = '2'
   cd['willbase'] = '2'
   cd['willabilitymod'] = '0'
   cd['willmiscmod'] = '0'
   # BAB stuff...
   cd['bab'] = '0'
   cd['meleeattacktotal'] = '0'
   cd['meleeattackbab'] = '0'
   cd['meleeattackstrmod'] = '0'
   cd['meleeattackmiscmod'] = '0'
   cd['rangedattacktotal'] = '0'
   cd['rangedattackbab'] = '0'
   cd['rangedattackdexmod'] = '0'
   cd['rangedattackmiscmod'] = '0'
   cd['thrownattacktotal'] = '0'
   cd['thrownattackbab'] = '0'
   cd['thrownattackdexmod'] = '0'
   cd['thrownattackmiscmod'] = '0'
   cd['unencumberedbulk'] = '0'
   cd['encumberedbulk'] = '0'
   cd['overburdenedbulk'] = '0'
   # Skills
   cd['skillranksperlevel'] = '-'
   skills = ['Acrobatics','Athletics','Bluff','Computers','Culture','Diplomacy','Disguise','Engineering','Intimidate','LifeScience','Medicine','Mysticism','Perception','PhysicalScience','Piloting','Profession','Profession2','SenseMotive','SleightOfHand','Stealth','Survival']
   for skill in skills:
      cd[skill.lower()+'classskill'] = False
      cd[skill.lower()+'total'] = '0'
      cd[skill.lower()+'ranks'] = '0'
      cd[skill.lower()+'classbonus'] = '0'
      cd[skill.lower()+'abilitymod'] = '0'
      cd[skill.lower()+'miscmod'] = '0'

   cd['abilities'] = ['I HAVE NO ABILITIES :(']
   cd['feats'] = ['Deadly Aim lol']

   return cd

def drawCenteredStringHelper(c, x, y, width, height, string):
   c.drawCentredString((x + width/2)*inch, (10.875-y)*inch, string)

def drawSaveLabel(c, x, y, width, height, shortString, longString):
   c.setFont("Source Sans Pro-Bold",13)
   drawBoxText(c,x,y,width,height,shortString,yAdjustment=0.0325)
   c.setFillColor(colors.black)
   c.setFont("Electrolize",8)
   c.drawCentredString((x+width/2)*inch,(10.875-(y+.09))*inch, longString)

def drawAbilityScoreLabel(c, x, y, width, height, shortString, longString):
   c.setFont("Source Sans Pro-Bold",13)
   drawBoxText(c,x,y,width,height,shortString,yAdjustment=0.0325)
   c.setFillColor(colors.black)
   c.setFont("Electrolize",5)
   c.drawString(x*inch,(10.875-(y+.07))*inch, longString)

def drawBoxText(c,x,y,width,height,shortString,yAdjustment=0):
   c.setFillColor(colors.black)
   c.rect(x*inch, (10.875-y)*inch, width*inch, height*inch, fill=1)
   c.setFillColor(colors.white)
   # c.setFont("Source Sans Pro-Bold",13)
   drawCenteredStringHelper(c, x, y-yAdjustment, width, height, shortString)
   c.setFillColor(colors.black)

def drawACScoreLabel(c, x, y, width, height, shortString, stringArray):
   c.setFont("Source Sans Pro-Bold",13)
   drawBoxText(c,x,y,width,height,shortString,yAdjustment=0.06)
   c.setFillColor(colors.black)
   drawMultiLine(c, x+width+.02, y-height/2 - 0.035, 'Electrolize', 10, stringArray, -.5)

def drawMultiLine(c, x, y, font, size, stringArray, spaceFix=0):
   # textobject = c.beginText((5.62+.43/2)*inch, (10.875-3.55)*inch)
   textobject = c.beginText(x*inch, (10.875-y)*inch)
   textobject.setFont(font, size)
   textobject.setCharSpace(spaceFix)
   lines = stringArray
   for line in lines:
      textobject.textLine(line)
   c.drawText(textobject)
   # c.setCharSpace(0)
   textobject = c.beginText(0,0)
   textobject.setCharSpace(0)
   c.drawText(textobject)

def MakeSFCS(CharacterDict):
   cd = CharacterDict
   c = canvas.Canvas('cs.pdf', (8.375*inch, 10.875*inch))#pagesize=letter)

   c.setFillColor(colors.white)
   c.rect(0.33*inch, (10.875-3.88)*inch, 3.60*inch, 2.06*inch, fill=1)

   c.rect(4.21*inch, (10.875-3.11)*inch, 3.92*inch, 0.87*inch, fill=1)

   c.rect(4.21*inch, (10.875-4.74)*inch, 3.92*inch, 1.38*inch, fill=1)
   c.line(4.23*inch,(10.875-3.845)*inch,8.11*inch,(10.875-3.845)*inch)
   c.line(4.23*inch,(10.875-4.165)*inch,8.11*inch,(10.875-4.165)*inch)
   c.line(4.23*inch,(10.875-4.48)*inch,8.11*inch,(10.875-4.48)*inch)

   c.rect(4.21*inch, (10.875-6.07)*inch, 3.92*inch, 1.06*inch, fill=1)

   c.rect(4.21*inch, (10.875-7.74)*inch, 3.92*inch, 1.35*inch, fill=1)
   c.line(4.23*inch,(10.875-6.825)*inch,8.11*inch,(10.875-6.825)*inch)
   c.line(4.23*inch,(10.875-7.275)*inch,8.11*inch,(10.875-7.275)*inch)

   c.setFillColor(colors.white)
   c.setFont("Void Pixel-7",22)
   # DRAW THE IMAGES/TEXT HEADERS
   # Character Name
   c.drawImage('cs_resources/titleoverlay.jpg', 0.25*inch, (10.875-0.47)*inch, 1.89*inch, 0.21*inch,mask='auto')
   # c.drawCentredString((0.25 + 1.89/2)*inch, (10.875-(0.47-.04))*inch, 'CHARACTER NAME')
   c.drawString((0.25+.15)*inch, (10.875-(0.47-.04))*inch, 'CHARACTER NAME')
   # Description
   c.drawImage('cs_resources/titleoverlay.jpg', 5.63*inch, (10.875-0.55)*inch, 1.89*inch, 0.20*inch,mask='auto')
   # c.drawCentredString((5.63 + 1.89/2)*inch, (10.875-(0.55-.04))*inch, 'DESCRIPTION')
   c.drawString((5.63+.15)*inch, (10.875-(0.55-.04))*inch, 'DESCRIPTION')
   # Ability Score
   c.drawImage('cs_resources/titleoverlay.jpg', 0.22*inch, (10.875-1.82)*inch, 2.00*inch, 0.22*inch,mask='auto')
   # c.drawCentredString((0.22 + 2.00/2)*inch, (10.875-(1.82-.04))*inch, 'ABILITY SCORE')
   c.drawString((0.22 + .15)*inch, (10.875-(1.82-.04))*inch, 'ABILITY SCORE')
   #Skills
   c.drawImage('cs_resources/titleoverlay.jpg', 0.22*inch, (10.875-4.22)*inch, 1.99*inch, 0.22*inch,mask='auto')
   # c.drawCentredString((0.22 + 1.99/2)*inch, (10.875-(4.22-.04))*inch, 'SKILLS')
   c.drawString((0.22 + .15)*inch, (10.875-(4.22-.04))*inch, 'SKILLS')
   # Initiative
   c.drawImage('cs_resources/titleoverlay.jpg', 4.10*inch, (10.875-1.96)*inch, 1.99*inch, 0.22*inch,mask='auto')
   # c.drawCentredString((4.10 + 1.99/2)*inch, (10.875-(1.96-.04))*inch, 'INITIATIVE')
   c.drawString((4.10 +.15)*inch, (10.875-(1.96-.04))*inch, 'INITIATIVE')
   # Health/Resolve
   c.drawImage('cs_resources/titleoverlay.jpg', 4.10*inch, (10.875-2.24)*inch, 2.31*inch, 0.22*inch,mask='auto')
   # c.drawCentredString((4.10 + 2.31/2)*inch, (10.875-(2.24-.04))*inch, 'HEALTH AND RESOLVE')
   c.drawString((4.10 + .15)*inch, (10.875-(2.24-.04))*inch, 'HEALTH AND RESOLVE')
   # Armor Class
   c.drawImage('cs_resources/titleoverlay.jpg', 4.10*inch, (10.875-3.36)*inch, 1.99*inch, 0.22*inch,mask='auto')
   # c.drawCentredString((4.10 + 1.99/2)*inch, (10.875-(3.36-.04))*inch, 'ARMOR CLASS')
   c.drawString((4.10 + .15)*inch, (10.875-(3.36-.04))*inch, 'ARMOR CLASS')
   # Saving Throws
   c.drawImage('cs_resources/titleoverlay.jpg', 4.10*inch, (10.875-5.01)*inch, 1.99*inch, 0.22*inch,mask='auto')
   # c.drawCentredString((4.10 + 1.99/2)*inch, (10.875-(5.01-.04))*inch, 'SAVING THROWS')
   c.drawString((4.10 + .15)*inch, (10.875-(5.01-.04))*inch, 'SAVING THROWS')
   # Attack Bonuses
   c.drawImage('cs_resources/titleoverlay.jpg', 4.10*inch, (10.875-6.39)*inch, 1.99*inch, 0.22*inch,mask='auto')
   # c.drawCentredString((4.10 + 1.99/2)*inch, (10.875-(6.39-.04))*inch, 'ATTACK BONUSES')
   c.drawString((4.10 + .15)*inch, (10.875-(6.39-.04))*inch, 'ATTACK BONUSES')
   # Weapons
   c.drawImage('cs_resources/titleoverlay.jpg', 4.10*inch, (10.875-8.05)*inch, 1.99*inch, 0.22*inch,mask='auto')
   # c.drawCentredString((4.10 + 1.99/2)*inch, (10.875-(8.05-.04))*inch, 'WEAPONS')
   c.drawString((4.10 + .15)*inch, (10.875-(8.05-.04))*inch, 'WEAPONS')
   c.setFillColor(colors.black)

   c.setFont("Electrolize",8)
   c.drawCentredString((1.42)*inch,(10.875-(2.03))*inch, 'SCORE')
   c.drawCentredString((2.08)*inch,(10.875-(2.03))*inch, 'MODIFIER')
   c.drawCentredString((2.74)*inch,(10.875-(1.93))*inch, 'UPGRADED')
   c.drawCentredString((2.74)*inch,(10.875-(2.03))*inch, 'SCORE')
   c.drawCentredString((3.38)*inch,(10.875-(1.93))*inch, 'UPGRADED')
   c.drawCentredString((3.38)*inch,(10.875-(2.03))*inch, 'MODIFIER')
   drawAbilityScoreLabel(c, 0.47, 2.25, 0.38, 0.19, 'STR', 'STRENGTH')
   drawAbilityScoreLabel(c, 0.47, 2.55, 0.38, 0.19, 'DEX', 'DEXTERITY')
   drawAbilityScoreLabel(c, 0.47, 2.85, 0.38, 0.19, 'CON', 'CONSTITUTION')
   drawAbilityScoreLabel(c, 0.47, 3.15, 0.38, 0.19, 'INT', 'INTELLIGENCE')
   drawAbilityScoreLabel(c, 0.47, 3.44, 0.38, 0.19, 'WIS', 'WISDOM')
   drawAbilityScoreLabel(c, 0.47, 3.73, 0.38, 0.19, 'CHA', 'CHARISMA')

   c.setFont("Electrolize",8)
   c.drawCentredString((6.455)*inch,(10.875-(1.68))*inch, 'TOTAL')
   c.drawCentredString((7.055)*inch,(10.875-(1.58))*inch, 'DEX')
   c.drawCentredString((7.055)*inch,(10.875-(1.68))*inch, 'MODIFIER')
   c.drawCentredString((7.655)*inch,(10.875-(1.58))*inch, 'MISC')
   c.drawCentredString((7.655)*inch,(10.875-(1.68))*inch, 'MODIFIER')
   c.setFont("Electrolize",10)
   c.drawCentredString((6.755)*inch,(10.875-(1.89))*inch, '=')
   c.drawCentredString((7.355)*inch,(10.875-(1.89))*inch, '+')

   c.setFont("Electrolize",8)
   c.drawString(0.25*inch,(10.875-(0.78+.1))*inch, 'CLASS/LEVEL')
   c.drawString(2.96*inch,(10.875-(0.78+.1))*inch, 'RACE')
   c.drawString(4.33*inch,(10.875-(0.78+.1))*inch, 'THEME')
   c.drawString(0.25*inch,(10.875-(1.11+.1))*inch, 'SIZE')
   c.drawString(1.27*inch,(10.875-(1.11+.1))*inch, 'SPEED')
   c.drawString(2.28*inch,(10.875-(1.11+.1))*inch, 'GENDER')
   c.drawString(2.79*inch,(10.875-(1.11+.1))*inch, 'HOME WORLD')
   c.drawString(0.25*inch,(10.875-(1.42+.1))*inch, 'ALIGNMENT')
   c.drawString(0.94*inch,(10.875-(1.42+.1))*inch, 'DEITY')
   c.drawString(3.31*inch,(10.875-(1.42+.1))*inch, 'PLAYER')

   c.setFont("Electrolize",10)
   c.drawRightString(4.94*inch,(10.875-(2.60))*inch, 'TOTAL')
   c.drawRightString(4.94*inch,(10.875-(2.95))*inch, 'CURRENT')
   c.setFont("Electrolize",8)
   c.drawCentredString((5.00+0.70/2)*inch,(10.875-(2.39))*inch, 'STAMINA POINTS')
   c.drawCentredString((5.93+0.70/2)*inch,(10.875-(2.39))*inch, 'HIT POINTS')
   c.drawCentredString((6.88+0.70/2)*inch,(10.875-(2.39))*inch, 'RESOLVE POINTS')

   drawACScoreLabel(c, 4.26, 3.79, 0.38, 0.25, 'EAC', ['ENERGY','ARMOR CLASS'])
   drawACScoreLabel(c, 4.26, 4.13, 0.38, 0.25, 'KAC', ['KINETIC','ARMOR CLASS'])
   drawMultiLine(c,4.26,4.28,'Electrolize',10,['AC VS.','COMBAT MANEUVERS'],-.75)
   drawBoxText(c, 6.45, 4.45, 0.38, 0.25, 'KAC', yAdjustment=0.06)

   c.setFont("Electrolize",8)
   c.drawCentredString((5.62+0.43/2)*inch,(10.875-(3.54))*inch, 'TOTAL')

   c.drawCentredString((6.44+0.43/2)*inch,(10.875-(3.455))*inch, 'ARMOR')
   c.drawCentredString((6.44+0.43/2)*inch,(10.875-(3.54))*inch, 'BONUS')

   c.drawCentredString((6.97+0.43/2)*inch,(10.875-(3.455))*inch, 'DEX')
   c.drawCentredString((6.97+0.43/2)*inch,(10.875-(3.54))*inch, 'MOD')

   c.drawCentredString((7.50+0.43/2)*inch,(10.875-(3.455))*inch, 'MISC')
   c.drawCentredString((7.50+0.43/2)*inch,(10.875-(3.54))*inch, 'MOD')

   c.setFont("Electrolize",10)
   c.drawCentredString(6.245*inch,(10.875-(3.73))*inch, '= 10+')
   c.drawCentredString(6.92*inch,(10.875-(3.73))*inch, '+')
   c.drawCentredString(7.45*inch,(10.875-(3.73))*inch, '+')
   c.drawCentredString(6.245*inch,(10.875-(4.06))*inch, '= 10+')
   c.drawCentredString(6.92*inch,(10.875-(4.06))*inch, '+')
   c.drawCentredString(7.45*inch,(10.875-(4.06))*inch, '+')
   c.drawCentredString(6.245*inch,(10.875-(4.37))*inch, '= 8 +')
   c.drawString(4.26*inch,(10.875-(4.69))*inch, 'DR')
   c.drawString(5.60*inch,(10.875-(4.69))*inch, 'RESIST')

   c.setFont("Electrolize",8)
   c.drawCentredString(5.66*inch,(10.875-(5.12))*inch, 'TOTAL')
   c.drawCentredString(6.35*inch,(10.875-(5.12))*inch, 'BASE SAVE')
   c.drawCentredString(7.04*inch,(10.875-(5.12))*inch, 'ABILITY MOD')
   c.drawCentredString(7.73*inch,(10.875-(5.12))*inch, 'MISC MOD')

   c.setFont("Electrolize",10)
   drawSaveLabel(c, 4.36, 5.31, 0.90, 0.19, 'FORTITUDE', '(CONSTITUTION)')
   drawSaveLabel(c, 4.36, 5.62, 0.90, 0.19, 'REFLEX', '(DEXTERITY)')
   drawSaveLabel(c, 4.36, 5.93, 0.90, 0.19, 'WILL', '(WISDOM)')

   c.drawCentredString(6.005*inch,(10.875-(5.32))*inch, '=')
   c.drawCentredString(6.695*inch,(10.875-(5.32))*inch, '+')
   c.drawCentredString(6.695*inch,(10.875-(5.32))*inch, '+')
   c.drawCentredString(7.385*inch,(10.875-(5.32))*inch, '+')
   c.drawCentredString(6.005*inch,(10.875-(5.61))*inch, '=')
   c.drawCentredString(6.695*inch,(10.875-(5.61))*inch, '+')
   c.drawCentredString(6.695*inch,(10.875-(5.61))*inch, '+')
   c.drawCentredString(7.385*inch,(10.875-(5.61))*inch, '+')
   c.drawCentredString(6.005*inch,(10.875-(5.91))*inch, '=')
   c.drawCentredString(6.695*inch,(10.875-(5.91))*inch, '+')
   c.drawCentredString(6.695*inch,(10.875-(5.91))*inch, '+')
   c.drawCentredString(7.385*inch,(10.875-(5.91))*inch, '+')

   c.setFont("Electrolize",8.5)
   c.drawString(4.30*inch,(10.875-(6.72))*inch, 'MELEE ATTACK')
   c.drawString(4.30*inch,(10.875-(7.16))*inch, 'RANGED ATTACK')
   c.drawString(4.30*inch,(10.875-(7.62))*inch, 'THROWN ATTACK')

   c.setFont("Electrolize",8)
   c.drawCentredString(5.64*inch,(10.875-(6.50))*inch, 'TOTAL')
   c.drawCentredString(6.36*inch,(10.875-(6.50))*inch, 'BAB')
   c.drawCentredString(7.07*inch,(10.875-(6.50))*inch, 'STR MOD')
   c.drawCentredString(7.77*inch,(10.875-(6.50))*inch, 'MISC MOD')
   c.setFont("Electrolize",10)
   c.drawCentredString(6.00*inch,(10.875 -(6.71))*inch, '=')
   c.drawCentredString(6.715*inch,(10.875-(6.71))*inch, '+')
   c.drawCentredString(7.42*inch,(10.875 -(6.71))*inch, '+')
   c.setFont("Electrolize",8)
   c.drawCentredString(5.64*inch,(10.875-(6.94))*inch, 'TOTAL')
   c.drawCentredString(6.36*inch,(10.875-(6.94))*inch, 'BAB')
   c.drawCentredString(7.07*inch,(10.875-(6.94))*inch, 'DEX MOD')
   c.drawCentredString(7.77*inch,(10.875-(6.94))*inch, 'MISC MOD')
   c.setFont("Electrolize",10)
   c.drawCentredString(6.00*inch,(10.875 -(7.15))*inch, '=')
   c.drawCentredString(6.715*inch,(10.875-(7.15))*inch, '+')
   c.drawCentredString(7.42*inch,(10.875 -(7.15))*inch, '+')
   c.setFont("Electrolize",8)
   c.drawCentredString(5.64*inch,(10.875-(7.39))*inch, 'TOTAL')
   c.drawCentredString(6.36*inch,(10.875-(7.39))*inch, 'BAB')
   c.drawCentredString(7.07*inch,(10.875-(7.39))*inch, 'DEX MOD')
   c.drawCentredString(7.77*inch,(10.875-(7.39))*inch, 'MISC MOD')
   c.setFont("Electrolize",10)
   c.drawCentredString(6.00*inch,(10.875 -(7.60))*inch, '=')
   c.drawCentredString(6.715*inch,(10.875-(7.60))*inch, '+')
   c.drawCentredString(7.42*inch,(10.875 -(7.60))*inch, '+')

   c.setFont("Electrolize",8)
   c.drawRightString(3.35*inch,(10.875-4.10)*inch, 'SKILL RANKS')
   c.drawRightString(3.35*inch,(10.875-4.20)*inch, 'PER LEVEL')

   c.setFont("Electrolize",7)
   c.drawCentredString(2.005*inch,(10.875-4.51)*inch, 'TOTAL')
   c.drawCentredString(2.455*inch,(10.875-4.51)*inch, 'RANKS')
   c.drawCentredString(2.885*inch,(10.875-4.41)*inch, 'CLASS')
   c.drawCentredString(2.885*inch,(10.875-4.51)*inch, 'BONUS')
   c.drawCentredString(3.325*inch,(10.875-4.41)*inch, 'ABILITY')
   c.drawCentredString(3.325*inch,(10.875-4.51)*inch, 'MOD')
   c.drawCentredString(3.765*inch,(10.875-4.41)*inch, 'MISC')
   c.drawCentredString(3.765*inch,(10.875-4.51)*inch, 'MOD')

   c.setFont("Electrolize",7)
   c.drawString(0.25*inch,(10.875-(9.86))*inch, '¤ Trained Only')
   c.drawString(1.25*inch,(10.875-(9.86))*inch, 'Class Skill      *Armor check penalty applies')

   c.acroForm.checkbox(name="example_checkbox",
      x=1.15*inch, y=(10.875-9.86)*inch,
      checked=True,
      buttonStyle='check',
      shape='square',
      fieldFlags=1<<0,
      size=0.08*inch,
      )

   c.setFont("Void Pixel-7",22)
   c.drawString(0.25*inch,(10.875-(10.15))*inch, 'SKILL NOTES')

   # General Info!
   # Line 1
   c.acroForm.textfield(name='CharacterName',
      value = cd['name'],
      x=2.17*inch, y=(10.875-0.47)*inch,
      borderStyle='underlined',
      forceBorder=True,
      width=3.44*inch,
      height=0.2*inch,
      fontSize=10,
      )

   # Line 2
   c.acroForm.textfield(name='ClassLevel',
      value = cd['class'],
      x=0.25*inch, y=(10.875-0.78)*inch,
      borderStyle='underlined',
      forceBorder=True,
      width=2.63*inch,
      height=0.2*inch,
      fontSize=10,
      )

   c.acroForm.textfield(name='Race',
      value = cd['race'],
      x=2.96*inch, y=(10.875-0.78)*inch,
      borderStyle='underlined',
      forceBorder=True,
      width=1.3*inch,
      height=0.2*inch,
      fontSize=10,
      )

   c.acroForm.textfield(name='Theme',
      value = cd['theme'],
      x=4.33*inch, y=(10.875-0.78)*inch,
      borderStyle='underlined',
      forceBorder=True,
      width=1.28*inch,
      height=0.2*inch,
      fontSize=10,
      )

   # Line 3
   c.acroForm.textfield(name='Size',
      value = cd['size'],
      x=0.25*inch, y=(10.875-1.11)*inch,
      borderStyle='underlined',
      forceBorder=True,
      width=0.95*inch,
      height=0.2*inch,
      fontSize=10,
      )

   c.acroForm.textfield(name='Speed',
      value = cd['speed'],
      x=1.27*inch, y=(10.875-1.11)*inch,
      borderStyle='underlined',
      forceBorder=True,
      width=0.95*inch,
      height=0.2*inch,
      fontSize=10,
      )

   c.acroForm.textfield(name='Gender',
      value = cd['gender'],
      x=2.28*inch, y=(10.875-1.11)*inch,
      borderStyle='underlined',
      forceBorder=True,
      width=0.43*inch,
      height=0.2*inch,
      fontSize=10,
      )

   c.acroForm.textfield(name='Homeworld',
      value = cd['homeworld'],
      x=2.79*inch, y=(10.875-1.11)*inch,
      borderStyle='underlined',
      forceBorder=True,
      width=2.83*inch,
      height=0.2*inch,
      fontSize=10,
      )

   # Line 4
   c.acroForm.textfield(name='Alignment',
      value = cd['alignment'],
      x=0.25*inch, y=(10.875-1.42)*inch,
      borderStyle='underlined',
      forceBorder=True,
      width=0.62*inch,
      height=0.2*inch,
      fontSize=10,
      )

   c.acroForm.textfield(name='Deity',
      value = cd['deity'],
      x=0.94*inch, y=(10.875-1.42)*inch,
      borderStyle='underlined',
      forceBorder=True,
      width=2.31*inch,
      height=0.2*inch,
      fontSize=10,
      )

   c.acroForm.textfield(name='Player',
      value = cd['player'],
      x=3.31*inch, y=(10.875-1.42)*inch,
      borderStyle='underlined',
      forceBorder=True,
      width=2.31*inch,
      height=0.2*inch,
      fontSize=10,
      )

   for i in range(4):
      c.acroForm.textfield(name='DescriptionLine'+str(i),
         value = '',
         x=5.69*inch, y=(10.875-(0.78+i*.2))*inch,
         borderStyle='underlined',
         forceBorder=True,
         width=2.44*inch,
         height=0.2*inch,
         fontSize=10,
         )

   # Ability Scores
   # Str
   c.acroForm.textfield(name='StrScore',
      value = cd['strscore'],
      x=1.13*inch, y=(10.875-2.34)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.58*inch,
      height=0.28*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='StrMod',
      value = cd['strmod'],
      x=1.79*inch, y=(10.875-2.34)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.58*inch,
      height=0.28*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='StrUpScore',
      value = cd['upgradedstrscore'],
      x=2.45*inch, y=(10.875-2.34)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.58*inch,
      height=0.28*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='StrUpMod',
      value = cd['upgradedstrmod'],
      x=3.09*inch, y=(10.875-2.34)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.58*inch,
      height=0.28*inch,
      fontSize=10,
      )
   # Dex
   c.acroForm.textfield(name='DexScore',
      value = cd['dexscore'],
      x=1.13*inch, y=(10.875-2.63)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.58*inch,
      height=0.28*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='DexMod',
      value = cd['dexmod'],
      x=1.79*inch, y=(10.875-2.63)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.58*inch,
      height=0.28*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='DexUpScore',
      value = cd['upgradeddexscore'],
      x=2.45*inch, y=(10.875-2.63)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.58*inch,
      height=0.28*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='DexUpMod',
      value = cd['upgradeddexmod'],
      x=3.09*inch, y=(10.875-2.63)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.58*inch,
      height=0.28*inch,
      fontSize=10,
      )
   # Con
   c.acroForm.textfield(name='ConScore',
      value = cd['conscore'],
      x=1.13*inch, y=(10.875-2.93)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.58*inch,
      height=0.28*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='ConMod',
      value = cd['conmod'],
      x=1.79*inch, y=(10.875-2.93)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.58*inch,
      height=0.28*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='ConUpScore',
      value = cd['upgradedconscore'],
      x=2.45*inch, y=(10.875-2.93)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.58*inch,
      height=0.28*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='ConUpMod',
      value = cd['upgradedconmod'],
      x=3.09*inch, y=(10.875-2.93)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.58*inch,
      height=0.28*inch,
      fontSize=10,
      )
   # Int
   c.acroForm.textfield(name='IntScore',
      value = cd['intscore'],
      x=1.13*inch, y=(10.875-3.23)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.58*inch,
      height=0.28*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='IntMod',
      value = cd['intmod'],
      x=1.79*inch, y=(10.875-3.23)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.58*inch,
      height=0.28*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='IntUpScore',
      value = cd['upgradedintscore'],
      x=2.45*inch, y=(10.875-3.23)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.58*inch,
      height=0.28*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='IntUpMod',
      value = cd['upgradedintmod'],
      x=3.09*inch, y=(10.875-3.23)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.58*inch,
      height=0.28*inch,
      fontSize=10,
      )
   # Wis
   c.acroForm.textfield(name='WisScore',
      value = cd['wisscore'],
      x=1.13*inch, y=(10.875-3.52)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.58*inch,
      height=0.28*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='WisMod',
      value = cd['wismod'],
      x=1.79*inch, y=(10.875-3.52)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.58*inch,
      height=0.28*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='WisUpScore',
      value = cd['upgradedwisscore'],
      x=2.45*inch, y=(10.875-3.52)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.58*inch,
      height=0.28*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='WisUpMod',
      value = cd['upgradedwismod'],
      x=3.09*inch, y=(10.875-3.52)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.58*inch,
      height=0.28*inch,
      fontSize=10,
      )
   # Cha
   c.acroForm.textfield(name='ChaScore',
      value = cd['chascore'],
      x=1.13*inch, y=(10.875-3.81)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.58*inch,
      height=0.28*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='ChaMod',
      value = cd['chamod'],
      x=1.79*inch, y=(10.875-3.81)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.58*inch,
      height=0.28*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='ChaUpScore',
      value = cd['upgradedchascore'],
      x=2.45*inch, y=(10.875-3.81)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.58*inch,
      height=0.28*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='ChaUpMod',
      value = cd['upgradedchamod'],
      x=3.09*inch, y=(10.875-3.81)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.58*inch,
      height=0.28*inch,
      fontSize=10,
      )

   # Initiative
   c.acroForm.textfield(name='InitiativeTotal',
      value = cd['inittotal'],
      x=6.24*inch, y=(10.875-1.97)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.43*inch,
      height=0.26*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='InitiativeDexMod',
      value = cd['initdexmod'],
      x=6.84*inch, y=(10.875-1.97)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.43*inch,
      height=0.26*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='InitiativeMiscMod',
      value = cd['initmiscmod'],
      x=7.44*inch, y=(10.875-1.97)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.43*inch,
      height=0.26*inch,
      fontSize=10,
      )

   # Health and Resolve
   # Stamina
   c.acroForm.textfield(name='StaminaPointsTotal',
      value = cd['staminapointstotal'],
      x=5.00*inch, y=(10.875-2.71)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.70*inch,
      height=0.29*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='StaminaPointsCurrent',
      value = cd['staminapointscurrent'],
      x=5.00*inch, y=(10.875-3.04)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.70*inch,
      height=0.29*inch,
      fontSize=10,
      )
   # Hit Points
   c.acroForm.textfield(name='HitPointsTotal',
      value = cd['hitpointstotal'],
      x=5.93*inch, y=(10.875-2.71)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.70*inch,
      height=0.29*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='HitPointsCurrent',
      value = cd['hitpointscurrent'],
      x=5.93*inch, y=(10.875-3.04)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.70*inch,
      height=0.29*inch,
      fontSize=10,
      )
   # Resolve
   c.acroForm.textfield(name='ResolvePointsTotal',
      value = cd['resolvepointstotal'],
      x=6.88*inch, y=(10.875-2.71)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.70*inch,
      height=0.29*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='ResolvePointsCurrent',
      value = cd['resolvepointscurrent'],
      x=6.88*inch, y=(10.875-3.04)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.70*inch,
      height=0.29*inch,
      fontSize=10,
      )

   # Armor Class
   # EAC
   c.acroForm.textfield(name='eacTotal',
      value = cd['eactotal'],
      x=5.62*inch, y=(10.875-3.81)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.43*inch,
      height=0.26*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='eacArmorBonus',
      value = cd['eacarmorbonus'],
      x=6.44*inch, y=(10.875-3.81)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.43*inch,
      height=0.26*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='eacDexMod',
      value = cd['eacdexmod'],
      x=6.97*inch, y=(10.875-3.81)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.43*inch,
      height=0.26*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='eacMiscMod',
      value = cd['eacmiscmod'],
      x=7.50*inch, y=(10.875-3.81)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.43*inch,
      height=0.26*inch,
      fontSize=10,
      )
   # KAC
   c.acroForm.textfield(name='kacTotal',
      value = cd['kactotal'],
      x=5.62*inch, y=(10.875-4.14)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.43*inch,
      height=0.26*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='kacArmorBonus',
      value = cd['kacarmorbonus'],
      x=6.44*inch, y=(10.875-4.14)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.43*inch,
      height=0.26*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='kacDexMod',
      value = cd['kacdexmod'],
      x=6.97*inch, y=(10.875-4.14)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.43*inch,
      height=0.26*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='kacMiscMod',
      value = cd['kacmiscmod'],
      x=7.50*inch, y=(10.875-4.14)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.43*inch,
      height=0.26*inch,
      fontSize=10,
      )
   # CMD
   c.acroForm.textfield(name='cmdTotal',
      value = cd['cmdtotal'],
      x=5.62*inch, y=(10.875-4.45)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.43*inch,
      height=0.26*inch,
      fontSize=10,
      )
   # DR
   c.acroForm.textfield(name='DR',
      value = cd['dr'],
      x=4.48*inch, y=(10.875-4.70)*inch,
      borderStyle='bevelled',
      forceBorder=False,
      width=1.08*inch,
      height=0.20*inch,
      fontSize=10,
      )
   # Resistances
   c.acroForm.textfield(name='Resistances',
      value = cd['resistances'],
      x=6.44*inch, y=(10.875-4.70)*inch,
      borderStyle='bevelled',
      forceBorder=False,
      width=1.64*inch,
      height=0.20*inch,
      fontSize=10,
      )

   # Saving Throws
   # Fort
   c.acroForm.textfield(name='FortTotal',
      value = cd['forttotal'],
      x=5.36*inch, y=(10.875-5.41)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.60*inch,
      height=0.26*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='FortBaseSave',
      value = cd['fortbase'],
      x=6.05*inch, y=(10.875-5.41)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.60*inch,
      height=0.26*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='FortAbilityMod',
      value = cd['fortabilitymod'],
      x=6.74*inch, y=(10.875-5.41)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.60*inch,
      height=0.26*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='FortMiscMod',
      value = cd['fortmiscmod'],
      x=7.43*inch, y=(10.875-5.41)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.60*inch,
      height=0.26*inch,
      fontSize=10,
      )
   # Ref
   c.acroForm.textfield(name='RefTotal',
      value = cd['reftotal'],
      x=5.36*inch, y=(10.875-5.70)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.60*inch,
      height=0.26*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='RefBaseSave',
      value = cd['refbase'],
      x=6.05*inch, y=(10.875-5.70)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.60*inch,
      height=0.26*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='RefAbilityMod',
      value = cd['refabilitymod'],
      x=6.74*inch, y=(10.875-5.70)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.60*inch,
      height=0.26*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='RefMiscMod',
      value = cd['refmiscmod'],
      x=7.43*inch, y=(10.875-5.70)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.60*inch,
      height=0.26*inch,
      fontSize=10,
      )
   # Will
   c.acroForm.textfield(name='WillTotal',
      value = cd['willtotal'],
      x=5.36*inch, y=(10.875-6.01)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.60*inch,
      height=0.26*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='WillBaseSave',
      value = cd['willbase'],
      x=6.05*inch, y=(10.875-6.01)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.60*inch,
      height=0.26*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='WillAbilityMod',
      value = cd['willabilitymod'],
      x=6.74*inch, y=(10.875-6.01)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.60*inch,
      height=0.26*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='WillMiscMod',
      value = cd['willmiscmod'],
      x=7.43*inch, y=(10.875-6.01)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.60*inch,
      height=0.26*inch,
      fontSize=10,
      )

   # Attack Bonus
   c.acroForm.textfield(name='BaB',
      value = cd['bab'],
      x=7.47*inch, y=(10.875-6.36)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.62*inch,
      height=0.26*inch,
      fontSize=10,
      )
   # Melee
   c.acroForm.textfield(name='MeleeAttackTotal',
      value = cd['meleeattacktotal'],
      x=5.33*inch, y=(10.875-6.79)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.62*inch,
      height=0.26*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='MeleeAttackBaB',
      value = cd['meleeattackbab'],
      x=6.05*inch, y=(10.875-6.79)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.62*inch,
      height=0.26*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='MeleeStrMod',
      value = cd['meleeattackstrmod'],
      x=6.76*inch, y=(10.875-6.79)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.62*inch,
      height=0.26*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='MeleeMiscMod',
      value = cd['meleeattackmiscmod'],
      x=7.46*inch, y=(10.875-6.79)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.62*inch,
      height=0.26*inch,
      fontSize=10,
      )
   # Ranged
   c.acroForm.textfield(name='RangedAttackTotal',
      value = cd['rangedattacktotal'],
      x=5.33*inch, y=(10.875-7.23)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.62*inch,
      height=0.26*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='RangedAttackBaB',
      value = cd['rangedattackbab'],
      x=6.05*inch, y=(10.875-7.23)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.62*inch,
      height=0.26*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='RangedDexMod',
      value = cd['rangedattackdexmod'],
      x=6.76*inch, y=(10.875-7.23)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.62*inch,
      height=0.26*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='RangedMiscMod',
      value = cd['rangedattackmiscmod'],
      x=7.46*inch, y=(10.875-7.23)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.62*inch,
      height=0.26*inch,
      fontSize=10,
      )
   # Thrown
   c.acroForm.textfield(name='ThrownAttackTotal',
      value = cd['thrownattacktotal'],
      x=5.33*inch, y=(10.875-7.68)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.62*inch,
      height=0.26*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='ThrownAttackBaB',
      value = cd['thrownattackbab'],
      x=6.05*inch, y=(10.875-7.68)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.62*inch,
      height=0.26*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='ThrownDexMod',
      value = cd['thrownattackdexmod'],
      x=6.76*inch, y=(10.875-7.68)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.62*inch,
      height=0.26*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='ThrownMiscMod',
      value = cd['thrownattackmiscmod'],
      x=7.46*inch, y=(10.875-7.68)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.62*inch,
      height=0.26*inch,
      fontSize=10,
      )

   # Skills
   c.acroForm.textfield(name='SkillRanksPerLevel',
      value = cd['skillranksperlevel'],
      x=3.42*inch, y=(10.875-4.25)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.46*inch,
      height=0.29*inch,
      fontSize=10,
      )
   skills = ['Acrobatics','Athletics','Bluff','Computers','Culture','Diplomacy','Disguise','Engineering','Intimidate','LifeScience','Medicine','Mysticism','Perception','PhysicalScience','Piloting','Profession','Profession2','SenseMotive','SleightOfHand','Stealth','Survival']
   skillsString = ['ACROBATICS* (DEX)','ATHLETICS* (STR)','BLUFF (CHA)','COMPUTERS (INT)','CULTURE (INT)','DIPLOMACY (CHA)','DISGUISE (CHA)','ENGINEERING (INT)','INTIMIDATE (CHA)','LIFE SCIENCE (INT)','MEDICINE (INT)','MYSTICISM (WIS)','PERCEPTION (WIS)','PHYSICAL SCIENCE (INT)','PILOTING (DEX)','PROFESSION','PROFESSION','SENSEMOTIVE (WIS)','SLEIGHT OF HAND* (DEX)','STEALTH* (DEX)','SURVIVAL (WIS)']
   skillsOffsetsY = [4.77,4.99,5.22,5.45,5.67,5.90,6.12,6.35,6.58,6.80,7.03,7.26,7.48,7.71,7.94,8.16,8.63,9.02,9.25,9.48,9.71]
   for i in range(len(skills)):
      c.setFont("Electrolize",8)
      c.drawString(0.47*inch,(10.875-(skillsOffsetsY[i]-.05))*inch, skillsString[i])
      c.drawCentredString(2.23*inch,(10.875-(skillsOffsetsY[i] -.07))*inch, '=')
      c.drawCentredString(2.67*inch,(10.875-(skillsOffsetsY[i] -.07))*inch, '+')
      c.drawCentredString(3.105*inch,(10.875-(skillsOffsetsY[i]-.07))*inch, '+')
      c.drawCentredString(3.545*inch,(10.875-(skillsOffsetsY[i]-.07))*inch, '+')
      c.acroForm.checkbox(name=skills[i]+'ClassSkill',
         x=0.36*inch, y=(10.875-(skillsOffsetsY[i]-.04))*inch,
         checked = cd[skills[i].lower()+'classskill'],
         buttonStyle='check',
         shape='square',
         size=0.10*inch,
         )
      c.acroForm.textfield(name=skills[i]+'Total',
         value = cd[skills[i].lower()+'total'],
         x=1.83*inch, y=(10.875-skillsOffsetsY[i])*inch,
         borderStyle='bevelled',
         forceBorder=True,
         width=0.35*inch,
         height=0.23*inch,
         fontSize=10,
         )
      c.acroForm.textfield(name=skills[i]+'Ranks',
         value = cd[skills[i].lower()+'ranks'],
         x=2.28*inch, y=(10.875-skillsOffsetsY[i])*inch,
         borderStyle='bevelled',
         forceBorder=True,
         width=0.35*inch,
         height=0.23*inch,
         fontSize=10,
         )
      c.acroForm.textfield(name=skills[i]+'ClassBonus',
         value = cd[skills[i].lower()+'classbonus'],
         x=2.71*inch, y=(10.875-skillsOffsetsY[i])*inch,
         borderStyle='bevelled',
         forceBorder=True,
         width=0.35*inch,
         height=0.23*inch,
         fontSize=10,
         )
      c.acroForm.textfield(name=skills[i]+'AbilityMod',
         value = cd[skills[i].lower()+'abilitymod'],
         x=3.15*inch, y=(10.875-skillsOffsetsY[i])*inch,
         borderStyle='bevelled',
         forceBorder=True,
         width=0.35*inch,
         height=0.23*inch,
         fontSize=10,
         )
      c.acroForm.textfield(name=skills[i]+'MiscMod',
         value = cd[skills[i].lower()+'miscmod'],
         x=3.59*inch, y=(10.875-skillsOffsetsY[i])*inch,
         borderStyle='bevelled',
         forceBorder=True,
         width=0.35*inch,
         height=0.23*inch,
         fontSize=10,
         )
   c.acroForm.textfield(name='Profession0Name',
      value = '',
      x=0.49*inch, y=(10.875-(skillsOffsetsY[15]+.23))*inch,
      borderStyle='underlined',
      forceBorder=True,
      width=1.28*inch,
      height=0.15*inch,
      fontSize=8,
      )
   c.acroForm.textfield(name='Profession1Name',
      value = '',
      x=0.49*inch, y=(10.875-(skillsOffsetsY[16]+.23))*inch,
      borderStyle='underlined',
      forceBorder=True,
      width=1.28*inch,
      height=0.15*inch,
      fontSize=8,
      )
   c.setFillColor(colors.black)
   c.setFont("Electrolize",7)
   c.drawString(0.25*inch,(10.875-(5.45-.05))*inch, '¤')
   c.drawString(0.25*inch,(10.875-(5.67-.05))*inch, '¤')
   c.drawString(0.25*inch,(10.875-(6.35-.05))*inch, '¤')
   c.drawString(0.25*inch,(10.875-(6.80-.05))*inch, '¤')
   c.drawString(0.25*inch,(10.875-(7.03-.05))*inch, '¤')
   c.drawString(0.25*inch,(10.875-(7.26-.05))*inch, '¤')
   c.drawString(0.25*inch,(10.875-(7.71-.05))*inch, '¤')
   c.drawString(0.25*inch,(10.875-(8.16-.05))*inch, '¤')
   c.drawString(0.25*inch,(10.875-(8.16-.05))*inch, '¤')
   c.drawString(0.25*inch,(10.875-(8.63-.05))*inch, '¤')
   c.drawString(0.25*inch,(10.875-(9.25-.05))*inch, '¤')
   c.setFont("Electrolize",8)
   c.drawString(0.47*inch,(10.875-(skillsOffsetsY[15]+.05))*inch, '(CHA, INT, OR WIS)')
   c.drawString(0.47*inch,(10.875-(skillsOffsetsY[16]+.05))*inch, '(CHA, INT, OR WIS)')

   # Weapons
   weaponYLocations=[8.33,8.99,9.65,10.30]
   for i in range(len(weaponYLocations)):
      c.setFillColor(colors.white)
      c.rect(4.21*inch, (10.875-(weaponYLocations[i]+.30))*inch, 3.92*inch, 0.58*inch, fill=1)
      c.setFillColor(colors.black)
      c.setFont("Electrolize",6)
      c.drawString(4.22*inch,(10.875-(weaponYLocations[i]-.21))*inch, 'WEAPON')
      c.drawString(6.19*inch,(10.875-(weaponYLocations[i]-.21))*inch, 'LEVEL')
      c.drawString(6.59*inch,(10.875-(weaponYLocations[i]-.21))*inch, 'ATTACK BONUS')
      c.drawString(7.23*inch,(10.875-(weaponYLocations[i]-.21))*inch, 'DAMAGE')
      c.drawString(4.22*inch,(10.875-(weaponYLocations[i]+.29-.21))*inch, 'CRITICAL')
      c.drawString(5.07*inch,(10.875-(weaponYLocations[i]+.29-.21))*inch, 'RANGE')
      c.drawString(5.44*inch,(10.875-(weaponYLocations[i]+.29-.21))*inch, 'TYPE')
      c.drawString(6.19*inch,(10.875-(weaponYLocations[i]+.29-.21))*inch, 'AMMO/USAGE')
      c.drawString(7.23*inch,(10.875-(weaponYLocations[i]+.29-.21))*inch, 'SPECIAL')
      c.acroForm.textfield(name='Weapon'+str(i)+'Name',
         value = '0',
         x=4.22*inch, y=(10.875-weaponYLocations[i])*inch,
         borderStyle='bevelled',
         borderWidth=0,
         forceBorder=True,
         width=1.96*inch,
         height=0.20*inch,
         fontSize=10,
         )
      c.acroForm.textfield(name='Weapon'+str(i)+'Lvl',
         value = '0',
         x=6.19*inch, y=(10.875-weaponYLocations[i])*inch,
         borderStyle='bevelled',
         borderWidth=0,
         forceBorder=True,
         width=0.39*inch,
         height=0.20*inch,
         fontSize=10,
         )
      c.acroForm.textfield(name='Weapon'+str(i)+'AttackBonus',
         value = '0',
         x=6.59*inch, y=(10.875-weaponYLocations[i])*inch,
         borderStyle='bevelled',
         borderWidth=0,
         forceBorder=True,
         width=0.63*inch,
         height=0.20*inch,
         fontSize=10,
         )
      c.acroForm.textfield(name='Weapon'+str(i)+'Damage',
         value = '0',
         x=7.23*inch, y=(10.875-weaponYLocations[i])*inch,
         borderStyle='bevelled',
         borderWidth=0,
         forceBorder=True,
         width=0.88*inch,
         height=0.20*inch,
         fontSize=10,
         )
      c.acroForm.textfield(name='Weapon'+str(i)+'Critical',
         value = '0',
         x=4.22*inch, y=(10.875-(weaponYLocations[i]+.29))*inch,
         borderStyle='bevelled',
         borderWidth=0,
         forceBorder=True,
         width=0.84*inch,
         height=0.20*inch,
         fontSize=10,
         )
      c.acroForm.textfield(name='Weapon'+str(i)+'Range',
         value = '0',
         x=5.07*inch, y=(10.875-(weaponYLocations[i]+.29))*inch,
         borderStyle='bevelled',
         borderWidth=0,
         forceBorder=True,
         width=0.36*inch,
         height=0.20*inch,
         fontSize=10,
         )
      c.acroForm.textfield(name='Weapon'+str(i)+'Type',
         value = '0',
         x=5.44*inch, y=(10.875-(weaponYLocations[i]+.29))*inch,
         borderStyle='bevelled',
         borderWidth=0,
         forceBorder=True,
         width=0.74*inch,
         height=0.20*inch,
         fontSize=10,
         )
      c.acroForm.textfield(name='Weapon'+str(i)+'AmmoUsage',
         value = '0',
         x=6.19*inch, y=(10.875-(weaponYLocations[i]+.29))*inch,
         borderStyle='bevelled',
         borderWidth=0,
         forceBorder=True,
         width=1.03*inch,
         height=0.20*inch,
         fontSize=10,
         )
      c.acroForm.textfield(name='Weapon'+str(i)+'Special',
         value = '0',
         x=7.23*inch, y=(10.875-(weaponYLocations[i]+.29))*inch,
         borderStyle='bevelled',
         borderWidth=0,
         forceBorder=True,
         width=0.88*inch,
         height=0.20*inch,
         fontSize=10,
         )

   c.acroForm.textfield(name='SkillNotes0',
      value = '',
      x=1.40*inch, y=(10.875-(10.19))*inch,
      borderStyle='underlined',
      forceBorder=True,
      width=2.53*inch,
      height=0.2*inch,
      fontSize=10,
      )
   for i in range(2):
      c.acroForm.textfield(name='SkillNotes'+str(i+1),
         value = '',
         x=0.25*inch, y=(10.875-(10.39+i*.2))*inch,
         borderStyle='underlined',
         forceBorder=True,
         width=3.68*inch,
         height=0.2*inch,
         fontSize=10,
         )

   c.showPage()
   #####################################################################################################
   ############################################# NEXT PAGE #############################################
   #####################################################################################################
   c.setFillColor(colors.white)
   c.setFont("Void Pixel-7",22)
   # DRAW THE IMAGES/TEXT HEADERS
   # Abilities
   c.drawImage('cs_resources/titleoverlay.jpg', 0.20*inch, (10.875-0.50)*inch, 2.10*inch, 0.21*inch,mask='auto')
   c.drawString((0.20+.15)*inch, (10.875-(0.50-.04))*inch, 'ABILITIES')
   # Languages
   c.drawImage('cs_resources/titleoverlay.jpg', 0.20*inch, (10.875-9.85)*inch, 2.10*inch, 0.21*inch,mask='auto')
   c.drawString((0.20+.15)*inch, (10.875-(9.85-.04))*inch, 'LANGUAGES')
   # Carrying Capacity
   c.drawImage('cs_resources/titleoverlay.jpg', 2.53*inch, (10.875-9.48)*inch, 2.10*inch, 0.21*inch,mask='auto')
   c.drawString((2.53+.15)*inch, (10.875-(9.48-.04))*inch, 'CARRYING CAPACITY')
   # Experience
   c.rect(2.61*inch, (10.875-10.65)*inch, 2.87*inch, 0.38*inch, fill=1)
   c.drawImage('cs_resources/titleoverlay.jpg', 2.53*inch, (10.875-10.27)*inch, 2.10*inch, 0.21*inch,mask='auto')
   c.drawString((2.53+.15)*inch, (10.875-(10.27-.04))*inch, 'EXPERIENCE POINTS')
   # Feats and Proficiencies
   c.drawImage('cs_resources/titleoverlay.jpg', 0.20*inch, (10.875-5.08)*inch, 2.20*inch, 0.42*inch,mask='auto')
   c.drawString((0.20+.15)*inch, (10.875-(5.08-.23))*inch, 'FEATS AND')
   c.drawString((0.20+.15)*inch, (10.875-(5.08-.08))*inch, 'PROFICIENCIES')
   # Spells Known
   c.drawImage('cs_resources/titleoverlay.jpg', 5.44*inch, (10.875-0.66)*inch, 2.20*inch, 0.21*inch,mask='auto')
   c.drawString((5.44+.15)*inch, (10.875-(0.66-.04))*inch, 'SPELLS KNOWN')
   # EQUIPMENT
   c.drawImage('cs_resources/titleoverlay.jpg', 2.54*inch, (10.875-5.04)*inch, 2.10*inch, 0.21*inch,mask='auto')
   c.drawString((2.54+.15)*inch, (10.875-(5.04-.04))*inch, 'EQUIPMENT')
   c.setFillColor(colors.black)

   # for i in range(20):
   for i in range(len(cd['abilities'])):
      c.acroForm.textfield(name='Ability'+str(i),
         value = cd['abilities'][i],
         x=0.25*inch, y=(10.875-(0.72+i*.2))*inch,
         borderStyle='underlined',
         forceBorder=True,
         width=5.14*inch,
         height=0.2*inch,
         fontSize=10,
         )

   # for i in range(22):
   for i in range(len(cd['feats'])):
      c.acroForm.textfield(name='Feat'+str(i),
         value = cd['feats'][i],
         x=0.25*inch, y=(10.875-(5.33+i*.2))*inch,
         borderStyle='underlined',
         forceBorder=True,
         width=2.20*inch,
         height=0.2*inch,
         fontSize=10,
         )

   # Equipment/Wealth
   c.setFont("Electrolize",7)
   c.drawCentredString(4.825*inch,(10.875-(5.04))*inch, 'LVL')
   c.drawCentredString(5.225*inch,(10.875-(5.04))*inch, 'BULK')
   for i in range(15):
      c.acroForm.textfield(name='Equipment'+str(i),
         value = '',
         x=2.6*inch, y=(10.875-(5.33+i*.2))*inch,
         borderStyle='underlined',
         forceBorder=True,
         width=2.00*inch,
         height=0.2*inch,
         fontSize=10,
         )
      c.acroForm.textfield(name='EquipmentLvl'+str(i),
         value = '',
         x=4.65*inch, y=(10.875-(5.33+i*.2))*inch,
         borderStyle='underlined',
         forceBorder=True,
         width=0.35*inch,
         height=0.2*inch,
         fontSize=10,
         )
      c.acroForm.textfield(name='EquipmentBulk'+str(i),
         value = '',
         x=5.05*inch, y=(10.875-(5.33+i*.2))*inch,
         borderStyle='underlined',
         forceBorder=True,
         width=0.35*inch,
         height=0.2*inch,
         fontSize=10,
         )

   c.setFont("Electrolize",10)
   c.drawString(2.60*inch,(10.875-(8.50))*inch, 'CREDITS')
   c.drawRightString(5.00*inch,(10.875-(8.30))*inch, 'TOTAL')
   c.drawRightString(5.00*inch,(10.875-(8.50))*inch, 'BULK')
   # c.drawCentredString(5.065*inch,(10.875-(9.60))*inch, 'OVERBURDENED')
   c.acroForm.textfield(name='Credits',
      value = '',
      x=3.20*inch, y=(10.875-8.52)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=1.32*inch,
      height=0.35*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='TotalBulk',
      value = '',
      x=5.03*inch, y=(10.875-8.52)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.38*inch,
      height=0.35*inch,
      fontSize=10,
      )

   # Carrying Capacity
   c.setFont("Electrolize",7)
   c.drawCentredString(3.045*inch,(10.875-(9.60))*inch, 'UNENCUMBERED')
   c.drawCentredString(4.105*inch,(10.875-(9.60))*inch, 'ENCUMBERED')
   c.drawCentredString(5.065*inch,(10.875-(9.60))*inch, 'OVERBURDENED')
   c.acroForm.textfield(name='UnencumberedBulk',
      value = cd['unencumberedbulk'],
      x=2.63*inch, y=(10.875-9.99)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.83*inch,
      height=0.35*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='EncumberedBulk',
      value = cd['encumberedbulk'],
      x=3.69*inch, y=(10.875-9.99)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.83*inch,
      height=0.35*inch,
      fontSize=10,
      )
   c.acroForm.textfield(name='OverburdenedBulk',
      value = cd['overburdenedbulk'],
      x=4.65*inch, y=(10.875-9.99)*inch,
      borderStyle='bevelled',
      forceBorder=True,
      width=0.83*inch,
      height=0.35*inch,
      fontSize=10,
      )

   c.setFont("Electrolize",10)
   c.drawString(2.60*inch,(10.875-(8.75))*inch, 'OTHER WEALTH')
   for i in range(2):
      c.acroForm.textfield(name='OtherWealth'+str(i),
         value = '',
         x=2.60*inch, y=(10.875-(8.99+i*.2))*inch,
         borderStyle='underlined',
         forceBorder=True,
         width=2.80*inch,
         height=0.2*inch,
         fontSize=10,
         )

   c.setFont("Electrolize",8)
   c.drawString(2.74*inch,(10.875-(10.53))*inch, 'XP')
   c.drawString(2.74*inch,(10.875-(10.63))*inch, 'EARNED')
   c.drawString(3.98*inch,(10.875-(10.53))*inch, 'NEXT')
   c.drawString(3.98*inch,(10.875-(10.63))*inch, 'LEVEL')

   for i in range(4):
      c.acroForm.textfield(name='Language'+str(i),
         value = '',
         x=0.25*inch, y=(10.875-(10.06+i*.2))*inch,
         borderStyle='underlined',
         forceBorder=True,
         width=2.20*inch,
         height=0.2*inch,
         fontSize=10,
         )

   # Spells
   SpellSpaceNumber = [6,6,6,6,5,4,4]
   SpellsKnown = [0,0,0,0,0,0,0]
   SpellsPerDay = [0,0,0,0,0,0,0]
   SpellNames = [[],[],[],[],[],[],[],]
   for spellList in cd['spellsknown']:
      for i in range(min(len(cd['spellsknown'][spellList]),7)):
         SpellsKnown[i] += cd['spellsknown'][spellList][i]
   for spellList in cd['spellsperday']:
      for i in range(min(len(cd['spellsperday'][spellList]),7)):
         SpellsPerDay[i] += cd['spellsperday'][spellList][i]
   for spellList in cd['spells']:
      for i in range(min(len(cd['spells'][spellList]),7)):
         for j in range(min(len(cd['spells'][spellList][i]),7)):
            SpellNames[i].append(cd['spells'][spellList][i][j]['name'])
   print(cd['spells'])
   print(SpellNames)
   SpellLabel = ['0','1ST','2ND','3RD','4TH','5TH','6TH']
   ylevel = 0.93
   for i in range(7):
      c.setFont("Electrolize",10)
      c.drawString(5.62*inch,(10.875-(ylevel))*inch, SpellLabel[i])
      if not(i == 0):
         c.setFont("Electrolize",5)
         c.drawCentredString(6.315*inch,(10.875-(ylevel-.275))*inch, 'SPELLS KNOWN')
         c.drawCentredString(6.995*inch,(10.875-(ylevel-.275))*inch, 'SPELLS PER DAY')
         c.drawCentredString(7.705*inch,(10.875-(ylevel-.275))*inch, 'SPELL SLOTS USED')
         c.acroForm.textfield(name='SpellsKnownLvl'+str(i),
            value = str(SpellsKnown[i]),
            x=6.01*inch, y=(10.875-ylevel)*inch,
            borderStyle='bevelled',
            forceBorder=True,
            width=0.61*inch,
            height=0.25*inch,
            fontSize=10,
            )
         c.acroForm.textfield(name='SpellsPerDayLvl'+str(i),
            value = str(SpellsPerDay[i]),
            x=6.69*inch, y=(10.875-ylevel)*inch,
            borderStyle='bevelled',
            forceBorder=True,
            width=0.61*inch,
            height=0.25*inch,
            fontSize=10,
            )
         c.acroForm.textfield(name='SpellSlotsUsedLvl'+str(i),
            value = '',
            x=7.40*inch, y=(10.875-ylevel)*inch,
            borderStyle='bevelled',
            forceBorder=True,
            width=0.61*inch,
            height=0.25*inch,
            fontSize=10,
            )
      if (i == 0):
         c.setFont("Electrolize",8)
         c.drawRightString(6.65*inch,(10.875-(ylevel))*inch, 'SPELLS KNOWN')
         c.acroForm.textfield(name='SpellsKnownLvl'+str(i),
            value = str(SpellsKnown[i]),
            x=6.69*inch, y=(10.875-ylevel)*inch,
            borderStyle='bevelled',
            forceBorder=True,
            width=0.61*inch,
            height=0.25*inch,
            fontSize=10,
            )

      ylevel += .23
      for j in range(SpellSpaceNumber[i]):
         spellname = ''
         if len(SpellNames[i]) > j:
            spellname = SpellNames[i][j]
         c.acroForm.textfield(name='SpellSlotLevel'+str(i)+'Slot'+str(j),
            value = spellname,
            x=5.62*inch, y=(10.875-ylevel)*inch,
            borderStyle='underlined',
            forceBorder=True,
            width=2.51*inch,
            height=0.2*inch,
            fontSize=10,
            )
         ylevel += .2
      ylevel += .15

   c.save()
   webbrowser.open_new("cs.pdf")


def main():
   print('test script initialize...')
   MakeSFCS(MakeDefaultDict())


if __name__ == "__main__":
   main()