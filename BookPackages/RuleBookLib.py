# -*- coding: utf-8 -*-
def getBonuseEveryNLevelsArray(bonus, n=1, startlevel=1, lvlkey='lvl'):
   bonusArray = []
   for i in range(startlevel,21,n):
      newBonus = {}
      for key in bonus:
         newBonus[key] = bonus[key]
      newBonus[lvlkey] = i
      bonusArray.append(newBonus)
   return bonusArray

def processClass(obj):
   pass
   for bonus in obj['bonus']:
      bonus['class'] = obj['name']

def processFeat(obj):
   if not('multitake' in obj):
      obj['multitake'] = False
   if not(obj['multitake']):
      prereq = {'type':'nofeat','value': obj['name']}
      if not(prereq in obj['prerequisites']):
         obj['prerequisites'].append([prereq])

def processAbility(obj):
   if not('multitake' in obj):
      obj['multitake'] = False
   if not(obj['multitake']):
      prereq = {'type':'noability','value': obj['name']}
      if not(prereq in obj['prerequisites']):
         obj['prerequisites'].append([prereq])

def getBabArray(type):
   bonusArray = []
   if type == 'Full':
      bonus = {'type':'babbonus','value':1,'classlvl':0}
      bonusArray = getBonuseEveryNLevelsArray(bonus,n=1,startlevel=1,lvlkey='classlvl')
   if type == 'ThreeForths':
      for i in range(1,21):
         babBonus = int((i)*0.75) - int((i-1)*0.75)
         if (babBonus > 0):
            bonus = {'type':'babbonus','value':babBonus,'classlvl':i}
            bonusArray.append(bonus)
   return bonusArray

def getSaveArray(type, bonusType):
   bonusArray = []
   start = 0
   inc = 0
   if type == 'Good':
      start = 2
      inc = 0.5
   if type == 'Bad':
      start = 0
      inc = 0.33334
   for i in range(20):
      saveBonus = int((i+1)*inc) - int((i)*inc)
      if (i == 0):
         saveBonus += start
      if (saveBonus > 0):
         bonus = {'type':bonusType,'value':saveBonus,'classlvl':i+1}
         bonusArray.append(bonus)
   return bonusArray