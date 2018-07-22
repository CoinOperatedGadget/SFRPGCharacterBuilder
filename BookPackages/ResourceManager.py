# -*- coding: utf-8 -*-
import pickle
import copy
try:
   import RuleBookLib
except:
   from BookPackages import RuleBookLib

class ResourceManager:
   def __init__(self):
      self.classes = []
      self.feats = []
      self.items = []
      self.themes = []
      self.races = []
      self.abilities = []
      self.spells = []
      self.book = None
      self.copyright = None

   def add(self, item):
      if self.book != None:
         item['book'] = self.book
      if self.copyright != None:
         item['copyright'] = self.copyright
      if not('subtype' in item):
         item['subtype'] = None
      if item['type'] == 'race':
         self.races.append(item)
         return
      if item['type'] == 'class':
         RuleBookLib.processClass(item)
         self.classes.append(item)
         return
      if item['type'] == 'item':
         self.items.append(item)
         return
      if item['type'] == 'theme':
         self.themes.append(item)
         return
      if item['type'] == 'feat':
         RuleBookLib.processFeat(item)
         self.feats.append(item)
         return
      if item['type'] == 'ability':
         RuleBookLib.processAbility(item)
         self.abilities.append(item)
         return
      if item['type'] == 'spell':
         self.spells.append(item)
         return
      print(item)
      raise ValueError

   def get_item_by_name(self,name):
      for i in self.all:
         if name == i['name']:
            return self.make_new_copy_of_item(i)
            # return copy.deepcopy(i)
      return None

   def get_item_by_name_and_type(self,name,type='any'):
      for i in self.get_items_by_type_and_subtype(type=type):
         if name == i['name']:
            return self.make_new_copy_of_item(i)
            # return copy.deepcopy(i)
      return None
      
   def make_new_copy_of_item(self,item):
      newCopy = {}
      for j in item:
         newCopy[j] = item[j]
      return newCopy
      

   def get_items_by_type_and_subtype(self,type='any',subtype='any'):
      itemList = []
      searchList = self.all
      if (type == 'race'):
         searchList = self.races
      if (type == 'class'):
         searchList = self.classes
      if (type == 'item'):
         searchList = self.items
      if (type == 'theme'):
         searchList = self.themes
      if (type == 'feat'):
         searchList = self.feats
      if (type == 'ability'):
         searchList = self.abilities
      if (type == 'spell'):
         searchList = self.spells
      if (subtype == 'any'):
         return searchList

      for i in searchList:
         if (type == i['type'] or type == 'any') and (subtype == i['subtype'] or subtype == 'any'):
            itemList.append(i)
      return itemList
      
   def get_spell_list(self, name):
      spellList = []
      for spell in self.spells:
         if name in spell['spelllists']:
            spellList.append(spell)
      return spellList
      
   def get_spell_list_by_level(self, name):
      spellList = self.get_spell_list(name)
      spellListByLevel = []
      for spell in spellList:
         while spell['spelllists'][name]+1 > len(spellListByLevel):
            spellListByLevel = spellListByLevel + [[]]
         spellListByLevel[spell['spelllists'][name]].append(spell)
      return spellListByLevel

   def save(self, filename):
      file = open(filename,'wb')
      pickle.dump(self.all, file)
      file.close()

   def load(self, filename):
      file = open(filename,'rb')
      rs = pickle.load(file)
      file.close()
      for i in rs:
         self.add(i)
      # self.classes += rs.classes
      # self.feats += rs.feats
      # self.items += rs.items
      # self.themes += rs.themes
      # self.races += rs.races

   @property
   def all(self):
      return self.classes + self.feats + self.items + self.themes + self.races + self.abilities + self.spells