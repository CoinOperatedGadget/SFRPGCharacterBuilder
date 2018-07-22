# -*- coding: utf-8 -*-
import math
import pickle

class StarfinderCharacterObject:
   def __init__(self):
      print('Making starfinder character...')
      self.name = 'Starfinder Character'
      self._classes = []
      self.effects = {}
      self._race = None
      self._theme = None
      self._speed = 30
      self.gender = 'M/F'
      self.homeworld = ''
      self.alignment = 'N'
      self.deity = ''
      self.player = ''
      self.description = 'This is my character!'
      self._strScore = 0
      self._strBaseScore = 10
      self.strMod = 0
      self._dexScore = 0
      self._dexBaseScore = 10
      self.dexMod = 0
      self._conScore = 0
      self._conBaseScore = 10
      self.conMod = 0
      self._intScore = 0
      self._intBaseScore = 10
      self.intMod = 0
      self._wisScore = 0
      self._wisBaseScore = 10
      self.wisMod = 0
      self._chaScore = 0
      self._chaBaseScore = 10
      self.chaMod = 0
      self.dr = 0
      self.resistances = {}
      self._setLevel = 1
      self._feats = []
      self._abilities = []
      # Oooops all these lists are the same object!!!  Rookie mistake!
      # self._spells = [{}]*20
      self._spells = [{} for _ in range(20)]
      self._addBonusesToEffectsFromObj(self._createNormalFeatArray())
      self._skills = {'Acrobatics':[0]*20,'Athletics':[0]*20,'Bluff':[0]*20,'Computers':[0]*20,'Culture':[0]*20,'Diplomacy':[0]*20,'Disguise':[0]*20,'Engineering':[0]*20,'Intimidate':[0]*20,'LifeScience':[0]*20,'Medicine':[0]*20,'Mysticism':[0]*20,'Perception':[0]*20,'PhysicalScience':[0]*20,'Piloting':[0]*20,'Profession':[0]*20,'Profession2':[0]*20,'SenseMotive':[0]*20,'SleightOfHand':[0]*20,'Stealth':[0]*20,'Survival':[0]*20}
      self._skillAbilities = {'Acrobatics':'dex','Athletics':'str','Bluff':'cha','Computers':'int','Culture':'int','Diplomacy':'cha','Disguise':'cha','Engineering':'int','Intimidate':'cha','LifeScience':'int','Medicine':'int','Mysticism':'wis','Perception':'wis','PhysicalScience':'int','Piloting':'dex','Profession':'wis','Profession2':'wis','SenseMotive':'wis','SleightOfHand':'dex','Stealth':'dex','Survival':'wis'}
      self._addBonusesToEffectsFromObj(self._createAbilityBonusArray())
      self.rm = None

   def _createNormalFeatArray(self):
      self.featProgression = {}
      self.featProgression['type'] = 'other'
      self.featProgression['name'] = 'Norman Feat Progression'
      self.featProgression['bonus'] = []
      for i in range(1,20,2):
         self.featProgression['bonus'].append({'type':'feat','value': None,'lvl':i})
      return self.featProgression

   def _createAbilityBonusArray(self):
      self.featProgression = {}
      self.featProgression['type'] = 'others'
      self.featProgression['name'] = 'Leveling Ability Bonus'
      self.featProgression['bonus'] = []
      for i in range(5,21,5):
         self.featProgression['bonus'].append({'type':'abilitychoice','value': 'Leveling Ability Bonus','lvl':i})
         self.featProgression['bonus'].append({'type':'abilitychoice','value': 'Leveling Ability Bonus','lvl':i})
         self.featProgression['bonus'].append({'type':'abilitychoice','value': 'Leveling Ability Bonus','lvl':i})
         self.featProgression['bonus'].append({'type':'abilitychoice','value': 'Leveling Ability Bonus','lvl':i})
      return self.featProgression

   def _statGet(self,base,bonusTypeStr):
      bonus = 0
      if (bonusTypeStr in self.effects):
         for i in self.effects[bonusTypeStr]:
            if i['type'] == bonusTypeStr:
               bonus += i['value']
      return base+bonus

   def _getNumericSumOfEffectsAtLevel(self,level,stringList):
      sum = 0
      for i in stringList:
         if (i in self.effects):
            for j in self.effects[i]:
               if j['type'] == i and self._getEffectLevel(j) <= level:
                  sum += j['value']
      return sum

   def _getNumericSumOfGreatestOfEffectsAtLevel(self,level,stringList):
      sum = 0
      effectList = {}
      for i in stringList:
         if (i in self.effects):
            for j in self.effects[i]:
               if j['type'] == i and self._getEffectLevel(j) <= level:
                  if not(i in effectList):
                     effectList[i] = j['value']
                  if j['value'] > effectList[i]:
                     effectList[i] = j['value']
      for i in effectList:
         sum += effectList[i]
      return sum

   def _getNumericSumOfEffectsOnlyAtLevel(self,level,stringList):
      sum = 0
      for i in stringList:
         if (i in self.effects):
            for j in self.effects[i]:
               if j['type'] == i and self._getEffectLevel(j) == level:
                  sum += j['value']
      return sum

   def _getEffectLevel(self,effect):
      if 'lvl' in effect:
         return effect['lvl']
      # TODO: STUB!!!
      if 'classlvl' in effect:
         return 0
      print('EFFECT HAS NO LEVEL!!',effect)
      return 0
      
   def _getObjLevel(self, obj):
      if 'lvl' in obj:
         return obj['lvl']
      return 0

   def _getCountCommonEffectsAtLevel(self,level,stringList):
      sum = 0
      for i in stringList:
         if (i in self.effects):
            for j in self.effects[i]:
               if j['type'] == i and self._getEffectLevel(j) <= level:
                  sum += 1
      return sum

   def _getEffectsAtLevel(self,level,stringList):
      list = []
      for i in stringList:
         if (i in self.effects):
            for j in self.effects[i]:
               if j['type'] == i and self._getEffectLevel(j) <= level:
                  list.append(j)
      return list

   # We should do something about classlvl and lvl...
   def _addBonusesToEffectsFromObj(self, obj):
      for bonus in obj['bonus']:
         if 'class' in bonus:
            bonus['lvl'] = self._getLvlOfClassLvl(bonus['class'],bonus['classlvl'])
            if ('minlvl' in bonus):
               bonus['lvl'] = max(bonus['lvl'],bonus['minlvl'])
            if not('class' in self.effects):
               self.effects['class'] = []
            self.effects['class'].append(bonus)
         if not(bonus['type'] in self.effects):
            self.effects[bonus['type']] = []
         self.effects[bonus['type']].append(bonus)
         if (bonus['type'] == 'bonusfeat' or bonus['type'] == 'feat'):
            bonus['static'] = False
            if (isinstance(bonus['value'],str)):
               self.add_feat(self.rm.get_item_by_name(bonus['value']), bonus)
               bonus['static'] = True
         if (bonus['type'] == 'bonusfeatbysubtype'):
            bonus['static'] = False
         if (bonus['type'] == 'abilitychoice'):
            self.add_ability(None,bonus)
         if (bonus['type'] == 'ability'):
            self.add_ability(self.rm.get_item_by_name(bonus['value']), bonus)

   def _removeObjectBonusFromEffects(self, obj):
      for bonus in obj['bonus']:
         self.effects[bonus['type']].remove(bonus)
         if (bonus['type'] == 'bonusfeat' or bonus['type'] == 'feat'):
            if (isinstance(bonus['value'],str)):
               self.remove_feat(bonus)
         if (bonus['type'] == 'ability' or bonus['type'] == 'abilitychoice'):
            self.remove_ability(bonus)

   def _meetsPrerequisits(self, obj, lvl=None):
      if (lvl == None):
         lvl = self.level
      self.setLevel = lvl
      for prereqList in obj['prerequisites']:
         met = False
         for prereq in prereqList:

            # Feat prereq
            if prereq['type'] == 'feat':
               for feat in self.feats:
                  if feat['name'] == prereq['value']:
                     met = True
                     break

            # Does not have feat prereq
            if prereq['type'] == 'nofeat':
               met = True
               for feat in self.feats:
                  if feat['name'] == prereq['value']:
                     met = False
                     break

            # Ability prereq
            if prereq['type'] == 'ability':
               for ability in self.abilities:
                  if ability['name'] == prereq['value']:
                     met = True
                     break

            # Does not have ability prereq
            if prereq['type'] == 'noability':
               met = True
               for ability in self.abilities:
                  if ability['name'] == prereq['value']:
                     met = False
                     break

            # Does not have ability prereq
            if prereq['type'] == 'noabilitysamelevel':
               met = True
               for ability in self.abilities:
                  if ability['name'] == prereq['value']:
                     if  self._getObjLevel(ability) == lvl:
                        met = False
                        break

            # BAB prereq
            if prereq['type'] == 'bab':
               if self.bab >= prereq['value']:
                  met = True

            # Level prereq
            if prereq['type'] == 'lvl':
               if lvl >= prereq['value']:
                  met = True

            # Base Save prereq
            if prereq['type'] == 'fortbase':
               if self.fortBase > prereq['value']:
                  met = True
            if prereq['type'] == 'refbase':
               if self.refBase > prereq['value']:
                  met = True
            if prereq['type'] == 'willbase':
               if self.willBase > prereq['value']:
                  met = True

            # Does not have feat prereq
            if prereq['type'] == 'combatfeat':
               combatCount = 0
               for feat in self.feats:
                  if feat['subtype'] == 'Combat':
                     combatCount += 1
               if combatCount >= prereq['value']:
                  met = True

            # Ability Score prereq
            abilityScoreStrings = ['str','dex','con','int','wis','cha']
            for ass in abilityScoreStrings:
               if (prereq['type'] == ass):
                  if (self._getAbilityScoreByString(ass) >= prereq['value']):
                     met = True

            # Key Ability Score prereq
            if (prereq['type'] == 'keyabilityscore'):
               if (self._getAbilityScoreByString(self.keyAbilityScore) >= prereq['value']):
                  met = True

            # Class level prereq
            if prereq['type'] == 'classlvl':
               classObj = self.rm.get_item_by_name(prereq['class'])
               if self.get_class_level(classObj,lvl) >= prereq['value']:
                     met = True

            # Lack of class prereq
            if prereq['type'] == 'noclass':
               classObj = self.rm.get_item_by_name(prereq['value'])
               if self.get_class_level(classObj,lvl) == 0:
                  met = True

            # Skill prereqs
            if 'skillrank' in prereq['type']:
               for skill in self.skillStringList:
                  if (prereq['type'] == 'skillrank'+skill.lower()):
                     if (self.skillRanks[skill] >= prereq['value']):
                        met = True
         if not met:
            self.setLevel = self.level
            return False
      self.setLevel = self.level
      return True

   def _getAbilityScoreByString(self, string):
      if string == 'str':
         return self.strScore
      if string == 'dex':
         return self.dexScore
      if string == 'con':
         return self.conScore
      if string == 'int':
         return self.intScore
      if string == 'wis':
         return self.wisScore
      if string == 'cha':
         return self.chaScore

   def _getAbilityModByString(self, string):
      score = self._getAbilityScoreByString(string)
      return math.floor((score-10)/2)

   def get_obj_description_string(self, obj):
      descriptionString = ''
      # if obj['type'] == 'feat':
      if 'description' in obj:
         if len(obj['description']) > 0:
            first = True
            for line in obj['description']:
               if not(line == ''):
                  if not(first):
                     descriptionString += '\n'
                     descriptionString += '\n'
                  first = False
                  descriptionString += line
      if obj['type'] == 'spell':
         descriptionString += obj['name'].upper()
         descriptionString += '\n'
         if ('shortdescription' in obj):
            descriptionString += '\n'
            # descriptionString += '\n'
            descriptionString += obj['shortdescription']
         if ('castingtime' in obj):
            descriptionString += '\n'
            # descriptionString += '\n'
            descriptionString += 'Casting Time: '
            descriptionString += obj['castingtime']
         if ('range' in obj):
            descriptionString += '\n'
            # descriptionString += '\n'
            descriptionString += 'Range: '
            descriptionString += obj['range']
         if ('area' in obj):
            descriptionString += '\n'
            # descriptionString += '\n'
            descriptionString += 'Area: '
            descriptionString += obj['area']
         if ('effect' in obj):
            descriptionString += '\n'
            # descriptionString += '\n'
            descriptionString += 'Effect: '
            descriptionString += obj['effect']
         if ('targets' in obj):
            descriptionString += '\n'
            # descriptionString += '\n'
            descriptionString += 'Targets: '
            descriptionString += obj['targets']
         if ('duration' in obj):
            descriptionString += '\n'
            # descriptionString += '\n'
            descriptionString += 'Duration: '
            descriptionString += obj['duration']
         if ('savingthrow' in obj):
            descriptionString += '\n'
            # descriptionString += '\n'
            descriptionString += 'Saving Throw: '
            descriptionString += obj['savingthrow']
         if ('spellresistance' in obj):
            descriptionString += '\n'
            # descriptionString += '\n'
            descriptionString += 'Spell Reistance: '
            descriptionString += obj['spellresistance']
         if ('longdescription' in obj):
            descriptionString += '\n'
            descriptionString += '\n'
            descriptionString += obj['longdescription']
      if descriptionString == '':
         descriptionString += 'No Description Available.'
      if 'copyright' in obj:
         descriptionString += '\n'
         descriptionString += '\n'
         descriptionString += obj['copyright']
      return descriptionString

   def get_spells_known_dict_at_level(self, lvl):
      spell_arrays = self._getEffectsAtLevel(lvl,['spellsknown'])
      spells_known_dict = {}
      for sa in spell_arrays:
         if not(sa['spelllist'] in spells_known_dict):
            spells_known_dict[sa['spelllist']] = [0]*10
         for i in range(len(sa['value'])):
            spells_known_dict[sa['spelllist']][i] += sa['value'][i]
      return spells_known_dict

   def get_spells_per_day_dict_at_level(self, lvl):
      spell_arrays = self._getEffectsAtLevel(lvl,['spellsperday'])
      spells_known_dict = {}
      for sa in spell_arrays:
         if not(sa['spelllist'] in spells_known_dict):
            spells_known_dict[sa['spelllist']] = [0]*10
         for i in range(len(sa['value'])):
            spells_known_dict[sa['spelllist']][i] += sa['value'][i]
      bonus_spell_effects = self._getEffectsAtLevel(lvl,['bonusspellsperdaystat'])
      for bse in bonus_spell_effects:
         bonus_spell_array = self.get_bonus_spells_per_day_at_level(bse['value'],lvl)
         if bse['spelllist'] in spells_known_dict:
            for i in range(len(bonus_spell_array)):
               if spells_known_dict[bse['spelllist']][i] > 0:
                  spells_known_dict[bse['spelllist']][i] += bonus_spell_array[i]
      return spells_known_dict
      
   def get_bonus_spells_per_day_at_level(self,statStr,lvl):
      self.setLevel = lvl
      abilityScore = self._getAbilityScoreByString(statStr)
      bonusSpellsPerDay = [0,0,0,0,0,0,0]
      if abilityScore >= 12:
         bonusSpellsPerDay[1] += 1
      if abilityScore >= 14:
         bonusSpellsPerDay[2] += 1
      if abilityScore >= 16:
         bonusSpellsPerDay[3] += 1
      if abilityScore >= 18:
         bonusSpellsPerDay[4] += 1
      if abilityScore >= 20:
         bonusSpellsPerDay[5] += 1
         bonusSpellsPerDay[1] += 1
      if abilityScore >= 22:
         bonusSpellsPerDay[6] += 1
         bonusSpellsPerDay[2] += 1
      if abilityScore >= 24:
         bonusSpellsPerDay[3] += 1
      if abilityScore >= 26:
         bonusSpellsPerDay[4] += 1
      if abilityScore >= 28:
         bonusSpellsPerDay[5] += 1
         bonusSpellsPerDay[1] += 1
      if abilityScore >= 30:
         bonusSpellsPerDay[6] += 1
         bonusSpellsPerDay[2] += 1
      self.setLevel = self.level
      return bonusSpellsPerDay
      
   def get_bonus_spells_known_dict_at_level(self,lvl):
      bonus_spells = self._getEffectsAtLevel(lvl,['bonusspellknown'])
      bonus_spells_known_dict = {}
      for spell in bonus_spells:
         if not(spell['spelllist'] in bonus_spells_known_dict):
            bonus_spells_known_dict[spell['spelllist']] = [[],[],[],[],[],[],[],[],[],[],]
         spellItem = self.rm.get_item_by_name_and_type(spell['value'],'spell')
         spellLevel = 0
         if (spellItem != None):
            if spell['spelllist'] in spellItem['spelllists']:
               spellLevel = spellItem['spelllists'][spell['spelllist']]
            if 'spelllevel' in spell:
               spellLevel = spell['spelllevel']
            bonus_spells_known_dict[spell['spelllist']][spellLevel].append(spellItem)
      return bonus_spells_known_dict
         

   ##########################################################################
   ###################################TODO###################################
   ##########################################################################
   # I need to combine add/edit/remove/get ability/feat.  They are the same #
   # logic and I don't want to have to edit both every change I make...     #
   ##########################################################################
   def add_ability(self,ability,abilityBonus):
      if not ('abilityLink' in abilityBonus):
         abilityBonus['abilityLink'] = None
      if abilityBonus['abilityLink'] != None:
         self.remove_ability(abilityBonus)
      if (ability == None):
         return
      abilityBonus['abilityLink'] = ability
      self._abilities.append(ability)
      if ('abilityclasslvloffset' in abilityBonus):
         for bonus in ability['bonus']:
            bonus['classlvl'] += abilityBonus['abilityclasslvloffset']
      if 'lvl' in abilityBonus:
         ability['lvl'] = abilityBonus['lvl']
      for bonus in ability['bonus']:
         if not('classlvl' in bonus) and not('lvl' in bonus):
            bonus['lvl'] = ability['lvl']
         bonus['minlvl'] = ability['lvl']
         if 'lvl' in bonus:
            if bonus['lvl'] < bonus['minlvl']:
               bonus['lvl'] = bonus['minlvl']
      if 'classlvl' in abilityBonus:
         # TODO: STUB!!!
         ability['lvl'] = 0
      self._addBonusesToEffectsFromObj(ability)
   def get_valid_abilities(self,abilityBonus):
      abilityList = self.rm.get_items_by_type_and_subtype(type='ability',subtype=abilityBonus['value'])
      lvl = abilityBonus['lvl']
      valid = []
      invalid = []
      for ability in abilityList:
         if (self._meetsPrerequisits(ability, lvl=lvl)):
            valid.append(ability)
         else:
            invalid.append(ability)
      return (valid,invalid)
   def edit_ability(self,feat,featBonus):
      if not ('abilityLink' in featBonus):
         featBonus['abilityLink'] = None
      pass
   def remove_ability(self,featBonus):
      if not ('abilityLink' in featBonus):
         featBonus['abilityLink'] = None
      if featBonus['abilityLink'] == None:
         return
      self._removeObjectBonusFromEffects(featBonus['abilityLink'])
      self._abilities.remove(featBonus['abilityLink'])
      featBonus['abilityLink'] = None
   def get_ability(self,featBonus):
      if not ('abilityLink' in featBonus):
         featBonus['abilityLink'] = None
      return featBonus['abilityLink']
   def get_ability_subtype(self,featBonus):
      ability = self.get_ability(featBonus)
      if ability == None:
         return None
      if not('subtype' in ability):
         return None
      return ability['subtype']


   def add_feat(self,feat,featBonus):
      if not ('featLink' in featBonus):
         featBonus['featLink'] = None
      if featBonus['featLink'] != None:
         self.remove_feat(featBonus)
      if (feat == None):
         return
      featBonus['featLink'] = feat
      self._feats.append(feat)
      if 'lvl' in featBonus:
         feat['lvl'] = featBonus['lvl']
      if 'classlvl' in featBonus:
         # TODO: STUB!!!
         feat['lvl'] = 0
      self._addBonusesToEffectsFromObj(feat)
   def edit_feat(self,feat,featBonus):
      if not ('featLink' in featBonus):
         featBonus['featLink'] = None
      pass
   def remove_feat(self,featBonus):
      if not ('featLink' in featBonus):
         featBonus['featLink'] = None
      if featBonus['featLink'] == None:
         return
      self._removeObjectBonusFromEffects(featBonus['featLink'])
      self._feats.remove(featBonus['featLink'])
      featBonus['featLink'] = None
   def get_feat(self,featBonus):
      if not ('featLink' in featBonus):
         featBonus['featLink'] = None
      return featBonus['featLink']
   def get_valid_feats(self,featBonus,featList):
      valid = []
      invalid = []
      lvl = featBonus['lvl']
      newFeatList = featList
      if (featBonus['type'] == 'bonusfeatbysubtype'):
         newFeatList = self._getFeatsBySubtype(featBonus['value'],featList)
      for feat in newFeatList:
         if (self._meetsPrerequisits(feat,lvl=lvl)):
            valid.append(feat)
         else:
            invalid.append(feat)
      return (valid,invalid)

   def get_display_name(self,obj):
      subString = ''
      if 'displaydice' in obj:
         if obj['displaydice']:
            [dice,numDice,addition] = self._getObjDisplayDice(obj)
            subString += ' '+str(numDice)+'d'+str(dice)
            if addition > 0:
               subString += '+'+str(addition)
            if addition < 0:
               subString += str(addition)
      return obj['name']+subString

   def _getObjDisplayDice(self,obj):
      effects = self._getEffectsAtLevel(self.setLevel,[obj['name']+'dice'])
      maxdice = 0
      maxdicenum = 0
      addition = 0
      for e in effects:
         if 'addition' in e:
            addition += e['addition']
         if 'dice' in e and 'numdice' in e:
            newaverage = float(e['dice'])/2*e['numdice']
            oldaverage = float(maxdice)/2*maxdicenum
            if newaverage > oldaverage:
               maxdice = e['dice']
               maxdicenum = e['numdice']

      return [maxdice,maxdicenum,addition]

   def _getFeatsBySubtype(self, subtype, featList):
      subtypeFeatList = []
      for feat in featList:
         if feat['subtype'] == subtype:
            subtypeFeatList.append(feat)
      return subtypeFeatList

   def edit_class(self, lvl, newClass):
      oldClass = self.classes[lvl-1]
      classesToRemove = self.classes[lvl-1:]
      classesToAdd = []
      for ctr in classesToRemove:
         cta = self.rm.get_item_by_name(ctr['name'])
         classesToAdd.append(cta)
      classesToAdd[0] = newClass
      for i in reversed(range(len(classesToRemove))):
         self.remove_class(i+lvl)
      for cta in classesToAdd:
         self.add_class(cta)
   def add_class(self, newClass):
      classLvl = self.get_class_level(newClass)
      newClassAtLevel = self._getClassObjectForLevel(newClass,classLvl+1,self.level+1)
      self.classes.append(newClassAtLevel)
      self._addBonusesToEffectsFromObj(newClassAtLevel)
      self._updateLvlsOfClassBasedSkills()
      self.setLevel = self.level
   def remove_class(self, lvl):
      if (self.classes[lvl-1] != None):
         self._removeObjectBonusFromEffects(self.classes[lvl-1])
         self.chosenSpells[lvl-1] = {}
      self.classes.remove(self.classes[lvl-1])
      self._updateLvlsOfClassBasedSkills()
      self.setLevel = self.level
   def get_class_level(self, newClass, maxLevel=None):
      if maxLevel == None:
         maxLevel = self.level
      levelCount = 0
      for c in self.classes[:maxLevel]:
         if c['name'] == newClass['name']:
            levelCount += 1
      return levelCount
   def _getClassObjectForLevel(self, classObj, classLvl, charLvl):
      newClassObj = {}
      newClassObj['type'] = classObj['type']
      newClassObj['name'] = classObj['name']
      newClassObj['bonus'] = []
      for bonus in classObj['bonus']:
         if bonus['classlvl'] == classLvl or bonus['classlvl'] == 0:
            bonus['lvl'] = charLvl
            newClassObj['bonus'].append(bonus)
      return newClassObj
   def _updateLvlsOfClassBasedSkills(self):
      if 'class' in self.effects:
         for bonus in self.effects['class']:
            if 'class' in bonus:
               bonus['lvl'] = self._getLvlOfClassLvl(bonus['class'],bonus['classlvl'])
   def _getLvlOfClassLvl(self, className, classLvl):
      classObj = self.rm.get_item_by_name(className)
      if (self.get_class_level(classObj) < classLvl):
         return self.level+1
      for i in range(self.level):
         if (self.get_class_level(classObj,i+1) == classLvl):
            return i+1
      return None

   def can_add_skillpoint(self, skillName, lvl):
      if (lvl == 0):
         lvl = self.level
      if self.skillPoints > 0 and self.skillRanks[skillName] < lvl:
         return True
      return False

   def can_add_skillpoint_at_level(self, skillName, lvl):
      if (lvl == None):
         lvl = self.level
      skillRanks = self.get_skill_ranks_at_level(skillName,lvl)
      if self.get_remaining_skillpoints_at_level(lvl) > 0 and skillRanks < lvl:
         return True
      return False

   def get_skill_ranks_at_level(self, skillName, lvl):
      if (lvl == None):
         lvl = self.level
      return sum(self.skillRanksByLevel[skillName][0:lvl])

   def get_remaining_skillpoints_at_level(self,lvl):
      if (lvl == None):
         lvl = self.level
      srbl = self.skillRanksByLevel
      skillPointsUsed = 0
      for skill in srbl:
         skillPointsUsed += srbl[skill][lvl-1]
      return self.get_total_skillpoints_at_level(lvl)-skillPointsUsed

   def get_total_skillpoints_at_level(self,lvl):
      if (lvl == None):
         lvl = self.level
      skillPoints = max(1,self._getNumericSumOfEffectsOnlyAtLevel(lvl,['skillpoints']) + self._getAbilityModByString('int'))
      return skillPoints

   @property
   def classes(self):
      return self._classes
   @classes.setter
   def classes(self, value):
      print('setting classes...')
      for i in self._classes:
         self._removeObjectBonusFromEffects(i)
      self._classes = value
      for i in self.classes:
         self._addBonusesToEffectsFromObj(i)

   @property
   def uniqueClasses(self):
      classNames = []
      classList = []
      for c in self.classes:
         if not(c['name'] in classNames):
            classList.append(c)
            classNames.append(c['name'])
      return classList

   @property
   def classString(self):
      classString = ''
      for c in self.uniqueClasses:
         classString += c['name']
         classString += ' '
         classString += str(self.get_class_level(c))
         classString += ' '
      classString.strip()
      return classString

   @property
   def race(self):
      return self._race
   @race.setter
   def race(self,value):
      if (self._race != None):
         if (self.race['name'] == value['name']):
            return
         self._removeObjectBonusFromEffects(self.race)
      self._race = value
      self._addBonusesToEffectsFromObj(self.race)

   @property
   def theme(self):
      return self._theme
   @theme.setter
   def theme(self,value):
      if (self.theme != None):
         if (self.theme['name'] == value['name']):
            return
         self._removeObjectBonusFromEffects(self.theme)
      self._theme = value
      self._addBonusesToEffectsFromObj(self.theme)

   @property
   def strScore(self):
      strScore = self.strBaseScore+self._strScore
      lvlBonusEffects = self._getEffectsAtLevel(self.setLevel,['strbaselvlbonus'])
      for i in lvlBonusEffects:
         if strScore < 17:
            strScore += 1
         strScore += 1
      strBonuses = self._getNumericSumOfEffectsAtLevel(self.setLevel,['strbonus'])
      return strScore+strBonuses
   @strScore.setter
   def strScore(self,value):
      self._strScore = value
   @property
   def dexScore(self):
      dexScore = self.dexBaseScore+self._dexScore
      lvlBonusEffects = self._getEffectsAtLevel(self.setLevel,['dexbaselvlbonus'])
      for i in lvlBonusEffects:
         if dexScore < 17:
            dexScore += 1
         dexScore += 1
      dexBonuses = self._getNumericSumOfEffectsAtLevel(self.setLevel,['dexbonus'])
      return dexScore+dexBonuses
   @dexScore.setter
   def dexScore(self,value):
      self._dexScore = value
   @property
   def conScore(self):
      conScore = self.conBaseScore+self._conScore
      lvlBonusEffects = self._getEffectsAtLevel(self.setLevel,['conbaselvlbonus'])
      for i in lvlBonusEffects:
         if conScore < 17:
            conScore += 1
         conScore += 1
      conBonuses = self._getNumericSumOfEffectsAtLevel(self.setLevel,['conbonus'])
      return conScore+conBonuses
   @conScore.setter
   def conScore(self,value):
      self._conScore = value
   @property
   def intScore(self):
      intScore = self.intBaseScore+self._intScore
      lvlBonusEffects = self._getEffectsAtLevel(self.setLevel,['intbaselvlbonus'])
      for i in lvlBonusEffects:
         if intScore < 17:
            intScore += 1
         intScore += 1
      intBonuses = self._getNumericSumOfEffectsAtLevel(self.setLevel,['intbonus'])
      return intScore+intBonuses
   @intScore.setter
   def intScore(self,value):
      self._intScore = value
   @property
   def wisScore(self):
      wisScore = self.wisBaseScore+self._wisScore
      lvlBonusEffects = self._getEffectsAtLevel(self.setLevel,['wisbaselvlbonus'])
      for i in lvlBonusEffects:
         if wisScore < 17:
            wisScore += 1
         wisScore += 1
      wisBonuses = self._getNumericSumOfEffectsAtLevel(self.setLevel,['wisbonus'])
      return wisScore+wisBonuses
   @wisScore.setter
   def wisScore(self,value):
      self._wisScore = value
   @property
   def chaScore(self):
      chaScore = self.chaBaseScore+self._chaScore
      lvlBonusEffects = self._getEffectsAtLevel(self.setLevel,['chabaselvlbonus'])
      for i in lvlBonusEffects:
         if chaScore < 17:
            chaScore += 1
         chaScore += 1
      chaBonuses = self._getNumericSumOfEffectsAtLevel(self.setLevel,['chabonus'])
      return chaScore+chaBonuses
   @chaScore.setter
   def chaScore(self,value):
      self._chaScore = value

   @property
   def strBaseScore(self):
      return self._statGet(self._strBaseScore,'strbasebonus')
   @strBaseScore.setter
   def strBaseScore(self,value):
      self._strBaseScore = value
   @property
   def dexBaseScore(self):
      return self._statGet(self._dexBaseScore,'dexbasebonus')
   @dexBaseScore.setter
   def dexBaseScore(self,value):
      self._dexBaseScore = value
   @property
   def conBaseScore(self):
      return self._statGet(self._conBaseScore,'conbasebonus')
   @conBaseScore.setter
   def conBaseScore(self,value):
      self._conBaseScore = value
   @property
   def intBaseScore(self):
      return self._statGet(self._intBaseScore,'intbasebonus')
   @intBaseScore.setter
   def intBaseScore(self,value):
      self._intBaseScore = value
   @property
   def wisBaseScore(self):
      return self._statGet(self._wisBaseScore,'wisbasebonus')
   @wisBaseScore.setter
   def wisBaseScore(self,value):
      self._wisBaseScore = value
   @property
   def chaBaseScore(self):
      return self._statGet(self._chaBaseScore,'chabasebonus')
   @chaBaseScore.setter
   def chaBaseScore(self,value):
      self._chaBaseScore = value

   @property
   def strPoints(self):
      return self._strScore
   @property
   def dexPoints(self):
      return self._dexScore
   @property
   def conPoints(self):
      return self._conScore
   @property
   def intPoints(self):
      return self._intScore
   @property
   def wisPoints(self):
      return self._wisScore
   @property
   def chaPoints(self):
      return self._chaScore

   @property
   def pointBuy(self):
      return self._strScore+self._dexScore+self._conScore+self._intScore+self._wisScore+self._chaScore

   @property
   def level(self):
      return len(self.classes)

   @property
   def setLevel(self):
      return self._setLevel
   @setLevel.setter
   def setLevel(self, value):
      self._setLevel = value

   @property
   def hitPointsTotal(self):
      return self._getNumericSumOfEffectsAtLevel(self.setLevel,['hpbonus'])

   @property
   def staminaPointsTotal(self):
      staminaBonusTotal = self._getNumericSumOfEffectsAtLevel(self.setLevel,['staminabonus'])
      staminaConBonus = self.setLevel*self._getAbilityModByString('con')
      return staminaBonusTotal+staminaConBonus

   @property
   def resolvePointsTotal(self):
      return max(1,max(1,int(self.setLevel/2))+self._getAbilityModByString(self.keyAbilityScore))

   @property
   def featSlots(self):
      return self._getCountCommonEffectsAtLevel(self.setLevel,['feat','bonusfeat','bonusfeatbysubtype'])

   @property
   def featBonuses(self):
      return self._getEffectsAtLevel(self.setLevel,['feat','bonusfeat','bonusfeatbysubtype'])

   @property
   def feats(self):
      return self._feats

   @property
   def abilities(self):
      return self._abilities

   @property
   def abilityBonuses(self):
      return self._getEffectsAtLevel(self.setLevel,['ability','abilitychoice'])

   @property
   def skillStringList(self):
      return list(self._skills.keys())

   @property
   def skillRanksByLevel(self):
      return self._skills

   @property
   def skillRanks(self):
      skillDict = {}
      for skill in self._skills:
         skillDict[skill] = 0
         for i in range(len(self._skills[skill])):
            skillDict[skill] += self._skills[skill][i]
      return skillDict

   @property
   def classSkills(self):
      classSkills = []
      classSkillBonuses = self._getEffectsAtLevel(self.setLevel,['classskill'])
      for csb in classSkillBonuses:
         classSkills.append(csb['value'])
      for skill in self.skillStringList:
         skillFirstLevelClassSkillBonusStr = skill.lower().replace(' ','')+'firstlevelclassskillbonus'
         if ((self._getNumericSumOfGreatestOfEffectsAtLevel(self.setLevel,[skillFirstLevelClassSkillBonusStr,])) > 0 and not(skill in classSkills)):
            classSkills.append(skill)
      return classSkills

   @property
   def firstLevelClassSkills(self):
      classSkills = []
      classSkillBonuses = self._getEffectsAtLevel(1,['classskill'])
      for csb in classSkillBonuses:
         classSkills.append(csb['value'])
      return classSkills

   @property
   def skillBonuses(self):
      skillDict = {}
      csb = self.classSkillBonuses
      msb = self.miscSkillBonuses
      for skill in self.skillStringList:
         skillDict[skill] = 0
         skillDict[skill] += msb[skill]
         skillDict[skill] += csb[skill]
      return skillDict

   @property
   def miscSkillBonuses(self):
      skillDict = {}
      noRankBonus =  self._getNumericSumOfEffectsAtLevel(self.setLevel,['norankskillbonus'])
      skillRanks = self.skillRanks
      csb = self.classSkillBonuses
      firstLevelClassSkills = self.firstLevelClassSkills
      for skill in self.skillStringList:
         skillBonusStr = skill.lower().replace(' ','')+'bonus'
         skillInsightBonusStr = skill.lower().replace(' ','')+'insightbonus'
         skillRacialBonusStr = skill.lower().replace(' ','')+'racialbonus'
         skillFirstLevelClassSkillBonusStr = skill.lower().replace(' ','')+'firstlevelclassskillbonus'
         skillDict[skill] =  self._getNumericSumOfEffectsAtLevel(self.setLevel,[skillBonusStr])
         skillDict[skill] +=  self._getNumericSumOfGreatestOfEffectsAtLevel(self.setLevel,[skillInsightBonusStr,skillRacialBonusStr,])
         if (skillRanks[skill] == 0):
            skillDict[skill] += noRankBonus
         if (skill in firstLevelClassSkills):
            skillDict[skill] +=  self._getNumericSumOfGreatestOfEffectsAtLevel(self.setLevel,[skillFirstLevelClassSkillBonusStr,])
      return skillDict

   @property
   def classSkillBonuses(self):
      skillDict = {}
      for skill in self.skillStringList:
         skillDict[skill] = 0
         if (skill in self.classSkills and self.get_skill_ranks_at_level(skill,self.setLevel) > 0):
            skillDict[skill] += 3
      return skillDict

   @property
   def skillAbilityMods(self):
      skillDict = {}
      for skill in self.skillStringList:
         skillDict[skill] = self._getAbilityModByString(self._skillAbilities[skill])
      return skillDict

   @property
   def skillTotals(self):
      skillDict = {}
      srbl = self.skillRanksByLevel
      sb = self.skillBonuses
      sam = self.skillAbilityMods
      for skill in self.skillStringList:
         skillDict[skill] = sum(srbl[skill][0:self.setLevel])+sb[skill]+sam[skill]
      return skillDict

   @property
   def skillPoints(self):
      return self._getNumericSumOfEffectsAtLevel(self.setLevel,['skillpoints'])-sum(self.skillRanks.values())

   @property
   def abilityStringList(self):
      list = []
      for i in self.abilities:
         display = True
         if 'display' in i:
            display = i['display']
         if display:
            list.append(self.get_display_name(i))
      return list

   @property
   def featStringList(self):
      list = []
      for i in self.feats:
         display = True
         if 'display' in i:
            display = i['display']
         if display:
            list.append(self.get_display_name(i))
      return list

   @property
   def bab(self):
      return self._getNumericSumOfEffectsAtLevel(self.setLevel,['babbonus'])

   @property
   def fortBase(self):
      return self._getNumericSumOfEffectsAtLevel(self.setLevel,['fortbasebonus'])
   @property
   def fortAbilityMod(self):
      return self._getAbilityModByString('con')
   @property
   def fortMiscMod(self):
      return self._getNumericSumOfEffectsAtLevel(self.setLevel,['fortbonus'])
   @property
   def fortTotal(self):
      return self.fortBase + self.fortAbilityMod + self.fortMiscMod

   @property
   def refBase(self):
      return self._getNumericSumOfEffectsAtLevel(self.setLevel,['refbasebonus'])
   @property
   def refAbilityMod(self):
      return self._getAbilityModByString('dex')
   @property
   def refMiscMod(self):
      return self._getNumericSumOfEffectsAtLevel(self.setLevel,['refbonus'])
   @property
   def refTotal(self):
      return self.refBase + self.refAbilityMod + self.refMiscMod

   @property
   def willBase(self):
      return self._getNumericSumOfEffectsAtLevel(self.setLevel,['willbasebonus'])
   @property
   def willAbilityMod(self):
      return self._getAbilityModByString('wis')
   @property
   def willMiscMod(self):
      return self._getNumericSumOfEffectsAtLevel(self.setLevel,['willbonus'])
   @property
   def willTotal(self):
      return self.willBase + self.willAbilityMod + self.willMiscMod

   @property
   def speed(self):
      baseSpeed = 30
      # Should only be one of these based on race...
      baseSpeedEffects = self._getEffectsAtLevel(self.setLevel,['basespeed'])
      for effect in baseSpeedEffects:
         baseSpeed = effect['value']
      speedBonus = self._getNumericSumOfEffectsAtLevel(self.setLevel,['speedbonus'])
      speed = baseSpeed + speedBonus
      return str(speed) + ' ft.'

   @property
   def initiativeMisc(self):
      insightBonus = self._getNumericSumOfGreatestOfEffectsAtLevel(self.setLevel,['initiativeinsightbonus'])
      return self._getNumericSumOfEffectsAtLevel(self.setLevel,['initiativebonus']) + insightBonus

   @property
   def initiativeTotal(self):
      return self._getAbilityModByString('dex') + self.initiativeMisc

   @property
   def keyAbilityScore(self):
      options = self._getEffectsAtLevel(self.setLevel,['keyabilityscore'])
      if (len(options) == 0):
         return 'dex'
      kas = options[0]['value']
      for stat in options:
         if (self._getAbilityModByString(stat['value']) > self._getAbilityModByString(kas)):
            kas = stat['value']
      return kas

   @property
   def eacTotal(self):
      return 10 + self.eacArmorBonus + self._getAbilityModByString('dex') + self.eacMiscMod
   @property
   def eacArmorBonus(self):
      return 0
   @property
   def eacMiscMod(self):
      return self._getNumericSumOfEffectsAtLevel(self.setLevel,['kacbonus','acbonus'])

   @property
   def kacTotal(self):
      return 10 + self.kacArmorBonus + self._getAbilityModByString('dex') + self.kacMiscMod
   @property
   def kacArmorBonus(self):
      return 0
   @property
   def kacMiscMod(self):
      return self._getNumericSumOfEffectsAtLevel(self.setLevel,['kacbonus','acbonus'])

   @property
   def cmacTotal(self):
      return 8+self.kacTotal

   @property
   def meleeAttackTotal(self):
      return self.bab + self.meleeAttackMiscMod + self.meleeAttackAbilityMod
   @property
   def meleeAttackMiscMod(self):
      attackInsightBonus = self._getNumericSumOfGreatestOfEffectsAtLevel(self.setLevel,['attackinsightbonus'])
      return self._getNumericSumOfEffectsAtLevel(self.setLevel,['meleeattackbonus','attackbonus']) + attackInsightBonus
   @property
   def meleeAttackAbilityMod(self):
      return self._getAbilityModByString('str')

   @property
   def rangedAttackTotal(self):
      return self.bab + self.rangedAttackMiscMod + self.rangedAttackAbilityMod
   @property
   def rangedAttackMiscMod(self):
      attackInsightBonus = self._getNumericSumOfGreatestOfEffectsAtLevel(self.setLevel,['attackinsightbonus'])
      print('attackinsightbonus',attackInsightBonus)
      return self._getNumericSumOfEffectsAtLevel(self.setLevel,['rangedattackbonus','attackbonus']) + attackInsightBonus
   @property
   def rangedAttackAbilityMod(self):
      return self._getAbilityModByString('dex')

   @property
   def thrownAttackTotal(self):
      return self.bab + self.thrownAttackMiscMod + self.thrownAttackAbilityMod
   @property
   def thrownAttackMiscMod(self):
      attackInsightBonus = self._getNumericSumOfGreatestOfEffectsAtLevel(self.setLevel,['attackinsightbonus'])
      return self._getNumericSumOfEffectsAtLevel(self.setLevel,['thrownattackbonus','attackbonus']) + attackInsightBonus
   @property
   def thrownAttackAbilityMod(self):
      return self._getAbilityModByString('dex')

   @property
   def unencumberedBulk(self):
      return 0
   @property
   def encumberedBulk(self):
      strbonus = self._getNumericSumOfEffectsAtLevel(self.setLevel,['strbulkbonus'])
      return int((self.strScore+strbonus)/2)
   @property
   def overburdenedBulk(self):
      strbonus = self._getNumericSumOfEffectsAtLevel(self.setLevel,['strbulkbonus'])
      return self.strScore + strbonus

   @property
   def chosenSpells(self):
      return self._spells

   @property
   def spells(self):
      spells = {}
      bonusSpellDict = self.get_bonus_spells_known_dict_at_level(self.setLevel)
      for spellList in self.chosenSpells[self.setLevel-1]:
         if not(spellList in spells):
            spells[spellList] = [[],[],[],[],[],[],[],[],[],[],]
         for spellLevel in range(len(self.chosenSpells[self.setLevel-1][spellList])):
            for spell in self.chosenSpells[self.setLevel-1][spellList][spellLevel]:
               spells[spellList][spellLevel].append(spell)
      for spellList in bonusSpellDict:
         if not(spellList in spells):
            spells[spellList] = [[],[],[],[],[],[],[],[],[],[],]
         for spellLevel in range(len(bonusSpellDict[spellList])):
            for spell in bonusSpellDict[spellList][spellLevel]:
               spells[spellList][spellLevel].append(spell)
      return spells

   @property
   def size(self):
      size = 'Medium'
      sizeEffects = self._getEffectsAtLevel(self.setLevel,['size'])
      if (len(sizeEffects) > 0):
         size = sizeEffects[0]['value']
      return size

   def get_pdf_array(self):
      cd = {}
      # General Info
      cd['name'] = self.name
      cd['class'] = self.classString
      cd['race'] = self.race['name']
      cd['theme'] = self.theme['name']
      cd['size'] = self.size
      cd['speed'] = self.speed
      cd['gender'] = self.gender
      cd['homeworld'] = self.homeworld
      cd['alignment'] = self.alignment
      cd['deity'] = self.deity
      cd['player'] = self.player
      # AbilityScores
      cd['strscore'] = self.strScore
      cd['strmod'] = self._getAbilityModByString('str')
      cd['dexscore'] = self.dexScore
      cd['dexmod'] = self._getAbilityModByString('dex')
      cd['conscore'] = self.conScore
      cd['conmod'] = self._getAbilityModByString('con')
      cd['intscore'] = self.intScore
      cd['intmod'] = self._getAbilityModByString('int')
      cd['wisscore'] = self.wisScore
      cd['wismod'] = self._getAbilityModByString('wis')
      cd['chascore'] = self.chaScore
      cd['chamod'] = self._getAbilityModByString('cha')
      cd['upgradedstrscore'] = self.strScore
      cd['upgradedstrmod'] = self._getAbilityModByString('str')
      cd['upgradeddexscore'] = self.dexScore
      cd['upgradeddexmod'] = self._getAbilityModByString('dex')
      cd['upgradedconscore'] = self.conScore
      cd['upgradedconmod'] = self._getAbilityModByString('con')
      cd['upgradedintscore'] = self.intScore
      cd['upgradedintmod'] = self._getAbilityModByString('int')
      cd['upgradedwisscore'] = self.wisScore
      cd['upgradedwismod'] = self._getAbilityModByString('wis')
      cd['upgradedchascore'] = self.chaScore
      cd['upgradedchamod'] = self._getAbilityModByString('cha')
      # Initiative
      cd['inittotal'] = self.initiativeTotal
      cd['initdexmod'] = self._getAbilityModByString('dex')
      cd['initmiscmod'] = self.initiativeMisc
      # Health, Stamina, and Resolve
      cd['staminapointstotal'] = self.staminaPointsTotal
      cd['staminapointscurrent'] = self.staminaPointsTotal
      cd['hitpointstotal'] = self.hitPointsTotal
      cd['hitpointscurrent'] = self.hitPointsTotal
      cd['resolvepointstotal'] = self.resolvePointsTotal
      cd['resolvepointscurrent'] = self.resolvePointsTotal
      # Armor Class
      cd['eactotal'] = self.eacTotal
      cd['eacarmorbonus'] = self.eacArmorBonus
      cd['eacdexmod'] = self._getAbilityModByString('dex')
      cd['eacmiscmod'] = self.eacMiscMod
      cd['kactotal'] = self.kacTotal
      cd['kacarmorbonus'] = self.kacArmorBonus
      cd['kacdexmod'] = self._getAbilityModByString('dex')
      cd['kacmiscmod'] = self.kacMiscMod
      cd['cmdtotal'] = self.cmacTotal
      cd['dr'] = self.dr
      cd['resistances'] = ''
      # Saving Throws
      cd['forttotal'] = self.fortTotal
      cd['fortbase'] = self.fortBase
      cd['fortabilitymod'] = self.fortAbilityMod
      cd['fortmiscmod'] = self.fortMiscMod
      cd['reftotal'] = self.refTotal
      cd['refbase'] = self.refBase
      cd['refabilitymod'] = self.refAbilityMod
      cd['refmiscmod'] = self.refMiscMod
      cd['willtotal'] = self.willTotal
      cd['willbase'] = self.willBase
      cd['willabilitymod'] = self.willAbilityMod
      cd['willmiscmod'] = self.willMiscMod
      # BAB stuff...
      cd['bab'] = self.bab
      cd['meleeattacktotal'] = self.meleeAttackTotal
      cd['meleeattackbab'] = self.bab
      cd['meleeattackstrmod'] = self.meleeAttackAbilityMod
      cd['meleeattackmiscmod'] = self.meleeAttackMiscMod
      cd['rangedattacktotal'] = self.rangedAttackTotal
      cd['rangedattackbab'] = self.bab
      cd['rangedattackdexmod'] = self.rangedAttackAbilityMod
      cd['rangedattackmiscmod'] = self.rangedAttackMiscMod
      cd['thrownattacktotal'] = self.thrownAttackTotal
      cd['thrownattackbab'] = self.bab
      cd['thrownattackdexmod'] = self.thrownAttackAbilityMod
      cd['thrownattackmiscmod'] = self.thrownAttackMiscMod
      # Bulk Stuff
      cd['unencumberedbulk'] = self.unencumberedBulk
      cd['encumberedbulk'] = self.encumberedBulk
      cd['overburdenedbulk'] = self.overburdenedBulk
      # Skills
      cd['skillranksperlevel'] = '-'
      skills = ['Acrobatics','Athletics','Bluff','Computers','Culture','Diplomacy','Disguise','Engineering','Intimidate','LifeScience','Medicine','Mysticism','Perception','PhysicalScience','Piloting','Profession','Profession2','SenseMotive','SleightOfHand','Stealth','Survival']
      for skill in skills:
         cd[skill.lower()+'total'] = self.skillTotals[skill]
         cd[skill.lower()+'ranks'] = self.skillRanks[skill]
         cd[skill.lower()+'classbonus'] = self.classSkillBonuses[skill]
         cd[skill.lower()+'abilitymod'] = self.skillAbilityMods[skill]
         cd[skill.lower()+'miscmod'] = self.miscSkillBonuses[skill]

      for key, value in cd.items():
         cd[key] = str(value)
      cd['abilities'] = self.abilityStringList
      cd['feats'] = self.featStringList
      for skill in skills:
         cd[skill.lower()+'classskill'] = (skill in self.classSkills)
      cd['spells'] = self.spells
      cd['spellsknown'] = self.get_spells_known_dict_at_level(self.setLevel)
      cd['spellsperday'] = self.get_spells_per_day_dict_at_level(self.setLevel)
      return cd

   def save(self, filename):
      pass
   def load(self, filename):
      pass

   def save(self, filename):
      saveDict = {}
      saveDict['name'] = self.name
      saveDict['_classes'] = self._classes
      saveDict['effects'] = self.effects
      saveDict['_race'] = self._race
      saveDict['_theme'] = self._theme
      saveDict['_speed'] = self._speed
      saveDict['_spells'] = self._spells
      saveDict['gender'] = self.gender
      saveDict['homeworld'] = self.homeworld
      saveDict['alignment'] = self.alignment
      saveDict['deity'] = self.deity
      saveDict['player'] = self.player
      saveDict['description'] = self.description
      saveDict['_strScore'] = self._strScore
      saveDict['_strBaseScore'] = self._strBaseScore
      saveDict['strMod'] = self.strMod
      saveDict['_dexScore'] = self._dexScore
      saveDict['_dexBaseScore'] = self._dexBaseScore
      saveDict['dexMod'] = self.dexMod
      saveDict['_conScore'] = self._conScore
      saveDict['_conBaseScore'] = self._conBaseScore
      saveDict['conMod'] = self.conMod
      saveDict['_intScore'] = self._intScore
      saveDict['_intBaseScore'] = self._intBaseScore
      saveDict['intMod'] = self.intMod
      saveDict['_wisScore'] = self._wisScore
      saveDict['_wisBaseScore'] = self._wisBaseScore
      saveDict['wisMod'] = self.wisMod
      saveDict['_chaScore'] = self._chaScore
      saveDict['_chaBaseScore'] = self._chaBaseScore
      saveDict['chaMod'] = self.chaMod
      saveDict['dr'] = self.dr
      saveDict['resistances'] = self.resistances
      saveDict['_setLevel'] = self._setLevel
      saveDict['_feats'] = self._feats
      saveDict['_abilities'] = self._abilities
      saveDict['_skills'] = self._skills
      saveDict['_skillAbilities'] = self._skillAbilities
      file = open(filename,'wb')
      pickle.dump(saveDict, file)
      file.close()

   def load(self, filename):

      file = open(filename,'rb')
      saveDict = pickle.load(file)
      file.close()
      self.name = saveDict['name']
      self._classes = saveDict['_classes']
      self.effects = saveDict['effects']
      self._race = saveDict['_race']
      self._theme = saveDict['_theme']
      self._speed = saveDict['_speed']
      self._spells = saveDict['_spells']
      self.gender = saveDict['gender']
      self.homeworld = saveDict['homeworld']
      self.alignment = saveDict['alignment']
      self.deity = saveDict['deity']
      self.player = saveDict['player']
      self.description = saveDict['description']
      self._strScore = saveDict['_strScore']
      self._strBaseScore = saveDict['_strBaseScore']
      self.strMod = saveDict['strMod']
      self._dexScore = saveDict['_dexScore']
      self._dexBaseScore = saveDict['_dexBaseScore']
      self.dexMod = saveDict['dexMod']
      self._conScore = saveDict['_conScore']
      self._conBaseScore = saveDict['_conBaseScore']
      self.conMod = saveDict['conMod']
      self._intScore = saveDict['_intScore']
      self._intBaseScore = saveDict['_intBaseScore']
      self.intMod = saveDict['intMod']
      self._wisScore = saveDict['_wisScore']
      self._wisBaseScore = saveDict['_wisBaseScore']
      self.wisMod = saveDict['wisMod']
      self._chaScore = saveDict['_chaScore']
      self._chaBaseScore = saveDict['_chaBaseScore']
      self.chaMod = saveDict['chaMod']
      self.dr = saveDict['dr']
      self.resistances = saveDict['resistances']
      self._setLevel = saveDict['_setLevel']
      self._feats = saveDict['_feats']
      self._abilities = saveDict['_abilities']
      self._skills = saveDict['_skills']
      self._skillAbilities = saveDict['_skillAbilities']

def main():
   print('test script initialize...')


if __name__ == "__main__":
   main()