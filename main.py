# -*- coding: utf-8 -*-
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty, ObjectProperty
from kivy.lang import Builder
from os.path import dirname, join
from kivy.clock import Clock
from BookPackages.ResourceManager import ResourceManager
from CharacterLib.CharBuilder import StarfinderCharacterObject
import pickle
from PDFGenLib import CharSheetBuilder
import cProfile

class LoadDialog(FloatLayout):
   load = ObjectProperty(None)
   cancel = ObjectProperty(None)

class SaveDialog(FloatLayout):
   save = ObjectProperty(None)
   text_input = ObjectProperty(None)
   cancel = ObjectProperty(None)

class LicenseDialog(FloatLayout):
   licenselabel = ObjectProperty(None)
   cancel = ObjectProperty(None)

class TabScreen(Screen):
   fullscreen = BooleanProperty(False)
   def __init__(self, *args):
      self.rm = App.get_running_app().rm
      self.character = App.get_running_app().character
      return super(TabScreen, self).__init__(*args)

   def refresh_screen(self, *args):
      pass

   def add_widget(self, *args):
      if 'content' in self.ids:
         return self.ids.content.add_widget(*args)
      return super(TabScreen, self).add_widget(*args)

class EquipmentScreen(TabScreen):
   fullscreen = BooleanProperty(False)
   def __init__(self, *args):
      return super(EquipmentScreen, self).__init__(*args)

class ChoicePopup(Popup):
   def __init__(self, cb, validChoices, invalidChoices, defaultChoice, *args):
      self.rm = App.get_running_app().rm
      self.character = App.get_running_app().character
      self.validChoices = validChoices
      self.invalidChoices = invalidChoices
      self.defaultChoice = defaultChoice
      self.cb = cb
      self.currentChoice = defaultChoice
      self.choiceButtonList = []
      self.activeButtonList = []
      self.currentChoiceButton = None
      self.choiceLabel = None
      super(ChoicePopup, self).__init__(*args)
      Clock.schedule_once(self._setup_options)
   def _setup_options(self, *args):
      for i in range(256):
         self._addButton()
      self.refresh()
      self.choiceLabel = Label(text='',size_hint_y=None)
      self.choiceLabel.bind(width=lambda s, w:
            s.setter('text_size')(s,(w,None)))
      self.choiceLabel.bind(texture_size=self.choiceLabel.setter('size'))
   def refresh(self):
      # Remove old stuff...
      print(self.currentChoiceButton)
      if not(self.currentChoiceButton == None):
         self.currentChoiceButton.background_color = (1.0, 1.0, 1.0, 1.0)
         if not(self.currentChoiceButton.valid):
            self.currentChoiceButton.background_color = (1.0, 0.0, 0.0, 1.0)
      if not(self.choiceLabel == None):
         self.ids.choicelist.remove_widget(self.choiceLabel)
      # Calculate new sizes and stuff...
      newLength = len(self.validChoices)+len(self.invalidChoices)
      if (newLength < len(self.activeButtonList)):
         for i in self.activeButtonList[newLength:]:
            self.ids.choicelist.remove_widget(i)
      if (newLength > len(self.activeButtonList)):
         for i in self.choiceButtonList[len(self.activeButtonList):newLength]:
            self.ids.choicelist.add_widget(i)
      # Reseting active button list
      self.activeButtonList = []
      # Change new stuff!!
      for i in self.validChoices:
         self.add_choice(i,True)
      for i in self.invalidChoices:
         self.add_choice(i,False)
   def _addButton(self):
      button = Button()
      button.size_hint_y = None
      button.bind(texture_size=button.setter('size'))
      button.bind(on_press = self.select_choice)
      self.choiceButtonList.append(button)
   def add_choice(self, choice, valid, index=0):
      if (len(self.choiceButtonList) == len(self.activeButtonList)):
         self._addButton()
      button = self.choiceButtonList[len(self.activeButtonList)]
      button.text = choice['name']
      button.choice = choice
      self.activeButtonList.append(button)
      if not(valid):
         button.background_color = (1.0, 0.0, 0.0, 1.0)
      # self.ids.choicelist.add_widget(button)
      if (choice == self.currentChoice):
         button.background_color = (0.0, 1.0, 1.0, 1.0)
         self.currentChoiceButton = button
      button.valid = valid
   def select_choice(self, choiceButton):
      if (choiceButton == self.currentChoiceButton):
         return
      if not(self.choiceLabel == None):
         self.ids.choicelist.remove_widget(self.choiceLabel)
      self.currentChoice = choiceButton.choice
      choiceButton.background_color = (0.0, 1.0, 1.0, 1.0)
      if not(self.currentChoiceButton == None):
         self.currentChoiceButton.background_color = (1.0, 1.0, 1.0, 1.0)
         if not(self.currentChoiceButton.valid):
            self.currentChoiceButton.background_color = (1.0, 0.0, 0.0, 1.0)
      self.currentChoiceButton = choiceButton
      self.choiceLabel.text = self.character.get_obj_description_string(self.currentChoice)
      self.ids.choicelist.add_widget(self.choiceLabel,self.ids.choicelist.children.index(choiceButton))
   def confirm_choice(self):
      self.cb(self.currentChoice)
      self.dismiss()
   def cancel(self):
      self.cb(self.defaultChoice)
      self.dismiss()
   def clear_choice(self):
      self.cb(None)
      self.dismiss()

class AbilitySelector(BoxLayout):
   def __init__(self, abilityBonus, refresh_cb, *args):
      self.rm = App.get_running_app().rm
      self.character = App.get_running_app().character
      self.abilityBonus = abilityBonus
      self.refresh_cb = refresh_cb
      super(AbilitySelector, self).__init__(*args)
      Clock.schedule_once(self._setup_options)
   def _setup_options(self, *args):
      self.abilityWidget = Label()
      if self.abilityBonus['type'] == 'abilitychoice':
         self.abilityWidget = Button()
         self.abilityWidget.bind(on_press = self.open_feat_popup)
         self.abilityWidget.background_color = (1.0, 1.0, 0.0, 1.0)
         self.abilityWidget.text = 'Select '
      self.abilityWidget.text = self.abilityWidget.text+self.abilityBonus['value']
      if (self.abilityBonus['abilityLink'] != None):
         self.abilityWidget.text = self.character.get_display_name(self.character.get_ability(self.abilityBonus))
         self.abilityWidget.background_color = (1.0, 1.0, 1.0, 1.0)
      self.add_widget(self.abilityWidget)
   def open_feat_popup(self,abilityBonus):
      default = self.character.get_ability(self.abilityBonus)
      (valid, invalid) = self.character.get_valid_abilities(self.abilityBonus)
      popup = ChoicePopup(cb=self.ability_popup_cb, validChoices=valid, invalidChoices=invalid, defaultChoice=default )
      popup.open()
   def ability_popup_cb(self, ability):
      self.abilityWidget.text = 'Select '+self.abilityBonus['value']
      self.abilityWidget.background_color = (1.0, 1.0, 0.0, 1.0)
      if (ability != None):
         self.abilityWidget.text = ability['name']
         self.abilityWidget.background_color = (1.0, 1.0, 1.0, 1.0)
      self.character.add_ability(ability,self.abilityBonus)
      self.refresh_cb()

class FeatSelector(BoxLayout):
   def __init__(self, popup, *args):
      self.rm = App.get_running_app().rm
      self.character = App.get_running_app().character
      super(FeatSelector, self).__init__(*args)
      Clock.schedule_once(self._setup_options)
      self.popup = popup
   def _setup_options(self, *args):
      feat = self.character.get_feat(self.featBonus)
      if (not self.featBonus['static']):
         self.featname = 'Select a feat'
         if feat != None:
            self.featname = self.character.get_display_name(feat)
      if (self.featBonus['static']):
         self.ids.featbutton.background_color = (0.0, 0.0, 0.0, 1.0)
         self.ids.featbutton.text = self.character.get_display_name(feat)
         # This doesn't work for some reason...  Maybe have to manually bind to do this, handling in function for now...
         # self.ids.featbutton.funbind('on_release', self.open_feat_popup)
   def open_feat_popup(self):
      if not(self.featBonus['static']):
         defaultFeat = self.character.get_feat(self.featBonus)
         self.character.remove_feat(self.featBonus)
         (validFeats,invalidFeats) = self.character.get_valid_feats(self.featBonus,self.rm.feats)
         if (self.popup == None):
            self.popup = ChoicePopup(cb=self.feat_popup_cb, validChoices=validFeats, invalidChoices=invalidFeats, defaultChoice = defaultFeat)
         self.popup.cb=self.feat_popup_cb
         self.popup.validChoices=validFeats
         self.popup.invalidChoices=invalidFeats
         self.popup.defaultChoice=defaultFeat
         self.popup.currentChoice=defaultFeat
         self.popup.refresh()
         self.popup.open()
   def feat_popup_cb(self, feat):
      self.featname = 'Select a feat'
      if (feat != None):
         self.featname = feat['name']
      self.character.add_feat(feat,self.featBonus)
   @property
   def featname(self):
      return self.ids.featbutton.text
   @featname.setter
   def featname(self,value):
      self.ids.featbutton.text = value

class ClassSelector(BoxLayout):
   def __init__(self, *args):
      self.rm = App.get_running_app().rm
      self.character = App.get_running_app().character
      self._level = 0
      super(ClassSelector, self).__init__(*args)
      Clock.schedule_once(self._setup_options)
   def _setup_options(self, *args):
      self.ids.classsel.values = [d['name'] for d in self.rm.classes]
   def class_change(self):
      self.character.edit_class(self.level,self.rm.get_item_by_name(self.classname))
   @property
   def classname(self):
      return self.ids.classsel.text
   @classname.setter
   def classname(self, value):
      self.ids.classsel.text = value
   @property
   def level(self):
      return self._level
   @level.setter
   def level(self, value):
      self.ids.classlabel.text = 'Level '+str(value)+' Class:'
      self._level = value

class AbilityScreen(TabScreen):
   def __init__(self, *args):
      self.widgetList = []
      super(AbilityScreen, self).__init__(*args)
      Clock.schedule_once(self._setup_options)

   def _setup_options(self, *args):
      self.update_ability_widgets()

   def update_ability_widgets(self):
      for i in self.widgetList:
         self.ids.abilitycontainer.remove_widget(i)
      self.widgetList = []
      for lvl in range(1,self.character.level+1):
         label = Label()
         label.text = 'Level '+str(lvl)+':'
         self.ids.abilitycontainer.add_widget(label)
         self.widgetList.append(label)
         for ab in self.character.abilityBonuses:
            if (ab['lvl'] == lvl or (ab['lvl'] == 0 and lvl == 1)):
               if (self.character.get_ability_subtype(ab) != 'Racial') or (self.ids.racialcheckbox.active):
                  absel = AbilitySelector(abilityBonus=ab, refresh_cb=self.refresh_screen)
                  self.ids.abilitycontainer.add_widget(absel)
                  self.widgetList.append(absel)

   def racial_switch_toggle(self, active, *args):
      self.update_ability_widgets()

   def refresh_screen(self, *args):
      self.update_ability_widgets()

class SkillLevelSelect(BoxLayout):
   def __init__(self, level, skillPopup, *args):
      self.rm = App.get_running_app().rm
      self.character = App.get_running_app().character
      self.level = level
      self.skillPopup = skillPopup
      super(SkillLevelSelect, self).__init__(*args)
      Clock.schedule_once(self._setup_options)
   def _setup_options(self, *args):
      self.ids.skilllevellabel.text = 'Level '+str(self.level)
   def refresh(self):
      self.ids.skilllevelbutton.text = str(self.character.get_remaining_skillpoints_at_level(self.level))+'/'+str(self.character.get_total_skillpoints_at_level(self.level))

   def open_popup(self, *args):
      self.skillPopup.level = self.level
      self.skillPopup.refresh()
      self.skillPopup.open()

class SkillDisplay(GridLayout):
   def __init__(self, skillName, refresh_cb, *args):
      self.rm = App.get_running_app().rm
      self.character = App.get_running_app().character
      self.refresh_cb = refresh_cb
      self.skillName = skillName
      super(SkillDisplay, self).__init__(*args)
      Clock.schedule_once(self._setup_options)
   def _setup_options(self, *args):
      self.ids.skillnamelabel.text = self.skillName
   def add_rank(self):
      if not(self.character.can_add_skillpoint_at_level(self.skillName,self.level)):
         return
      self.character.skillRanksByLevel[self.skillName][self.level-1] += 1
      self.refresh()
      self.refresh_cb()
   def remove_rank(self):
      if (self.character.skillRanksByLevel[self.skillName][self.level-1] == 0):
         return
      self.character.skillRanksByLevel[self.skillName][self.level-1] -= 1
      self.refresh()
      self.refresh_cb()
   def refresh(self,miscBonuses=None,totals=None):
      if miscBonuses == None:
         self.character.setLevel = self.level
         miscBonuses = self.character.skillBonuses
         self.character.setLevel = self.character.level
      if totals == None:
         self.character.setLevel = self.level
         totals = self.character.skillTotals
         self.character.setLevel = self.character.level
      self.ids.skillranklabel.text = str(self.character.get_skill_ranks_at_level(self.skillName,self.level))
      self.ids.skillmiscbonus.text = str(miscBonuses[self.skillName])
      self.ids.skilltotal.text = str(totals[self.skillName])

class SkillScreen(TabScreen):
   def __init__(self, *args):
      self.widgetList = []
      self.activeWidgets = []
      self.skillPopup = None
      super(SkillScreen, self).__init__(*args)
      Clock.schedule_once(self._setup_options)

   def _setup_options(self, *args):
      self.widgetList = []
      self.skillPopup = SkillPopup(cb=self.update_skill_level_widgets)
      for i in range(1,21):
         sls = SkillLevelSelect(level=i,skillPopup=self.skillPopup)
         self.widgetList.append(sls)
         # self.ids.skilllevelcontainer.add_widget(sls)

   def update_skill_level_widgets(self):
      for i in range(len(self.activeWidgets)):
         self.activeWidgets[i].refresh()

   def refresh_screen(self, *args):
      for i in range(len(self.activeWidgets)):
         self.ids.skilllevelcontainer.remove_widget(self.activeWidgets[i])
      self.activeWidgets = []
      for i in range(self.character.level):
         self.ids.skilllevelcontainer.add_widget(self.widgetList[i])
         self.activeWidgets.append(self.widgetList[i])
      self.update_skill_level_widgets()


class SkillPopup(Popup):
   def __init__(self, cb, *args):
      self.widgetList = []
      self.rm = App.get_running_app().rm
      self.character = App.get_running_app().character
      self._level = 1
      self.cb = cb
      super(SkillPopup, self).__init__(*args)
      Clock.schedule_once(self._setup_options)

   def _setup_options(self, *args):
      self.widgetList = []
      for skill in self.character.skillStringList:
         sd = SkillDisplay(skillName=skill, refresh_cb=self.update_skillpoints)
         sd.level = self.level
         self.ids.skillcontainer.add_widget(sd)
         self.widgetList.append(sd)
      self.update_skill_widgets()
      self.refresh()

   def update_skill_widgets(self):
      self.character.setLevel = self.level
      miscBonuses = self.character.skillBonuses
      totals = self.character.skillTotals
      self.character.setLevel = self.character.level
      for w in self.widgetList:
         w.refresh(miscBonuses=miscBonuses,totals=totals)

   def refresh(self, *args):
      self.update_skill_widgets()
      self.update_skillpoints()

   def update_skillpoints(self):
      self.ids.skillpointslabel.text = 'Skill Points Remaining: '+str(self.character.get_remaining_skillpoints_at_level(self.level))
   def cancel(self):
      self.cb()
      self.dismiss()
   @property
   def level(self):
      return self._level
   @level.setter
   def level(self, value):
      self._level = value
      for w in self.widgetList:
         w.level = value


class ClassScreen(TabScreen):
   def __init__(self, *args):
      self.widgetList = []
      self.allWidgets = []
      super(ClassScreen, self).__init__(*args)
      Clock.schedule_once(self._setup_options)

   def _setup_options(self, *args):
      for i in range(20):
         widget = ClassSelector()
         widget.level = i+1
         widget.className = ''
         self.allWidgets.append(widget)
      self.refresh_class_levels(len(self.character.classes))

   def refresh_screen(self, *args):
      self.refresh_class_levels(len(self.character.classes))
      super(ClassScreen, self).refresh_screen(*args)

   # Refreshes the class levels etc
   def refresh_class_levels(self, numLevels):
      # Update widget names
      for i in range(len(self.widgetList)):
         if not(self.widgetList[i].classname == self.character.classes[i]):
            self.widgetList[i].classname = self.character.classes[i]['name']
      if len(self.widgetList) < numLevels:
         for i in range(numLevels-len(self.widgetList)):
            name = ''
            widget = self.allWidgets[len(self.widgetList)]
            if (len(self.widgetList) > 0):
               name = self.widgetList[-1].classname
            self.widgetList.append(widget)
            widget.level = len(self.widgetList)

            if (len(self.widgetList) <= self.character.level):
               name = self.character.classes[len(self.widgetList)-1]['name']
            if (len(self.widgetList) > self.character.level):
               self.character.add_class(self.rm.get_item_by_name(name))
            widget.classname = name

            self.ids.classcontainer.add_widget(widget)
      if len(self.widgetList) > numLevels:
         for i in range(-numLevels+len(self.widgetList)):
            self.ids.classcontainer.remove_widget(self.widgetList[-1])
            self.widgetList = self.widgetList[:-1]
            self.character.remove_class(self.character.level)

class FeatScreen(TabScreen):
   def __init__(self, *args):
      self.widgetList = []
      self.lvlWidgetList = []
      super(FeatScreen, self).__init__(*args)
      Clock.schedule_once(self._setup_options)

   def _setup_options(self, *args):
      for i in range(20):
         label = Label()
         label.text = 'Level '+str(i+1)+':'
         self.lvlWidgetList.append(label)
      self.lvlWidgetList
      self.popup = ChoicePopup(cb=None, validChoices=[], invalidChoices=[], defaultChoice = None)
      self.update_feat_widgets()

   def update_feat_widgets(self):
      for i in self.lvlWidgetList:
         self.ids.featcontainer.remove_widget(i)
      for i in self.widgetList:
         self.ids.featcontainer.remove_widget(i)
      self.widgetList = []
      for lvl in range(1,self.character.level+1):
         self.ids.featcontainer.add_widget(self.lvlWidgetList[lvl-1])
         for fb in self.character.featBonuses:#range(self.character.featSlots):
            if (fb['lvl'] == lvl or (fb['lvl'] == 0 and lvl == 1)):
               fs = FeatSelector(self.popup)
               fs.featBonus = fb
               self.ids.featcontainer.add_widget(fs)
               self.widgetList.append(fs)

   def refresh_screen(self, *args):
      self.update_feat_widgets()


class GeneralScreen(TabScreen):
   def __init__(self, *args):
      self.disableUpdate = True
      super(GeneralScreen, self).__init__(*args)
      Clock.schedule_once(self._setup_options)

   def _setup_options(self, *args):
      self.ids.racespinner.values = [d['name'] for d in self.rm.races]
      self.ids.themespinner.values = [d['name'] for d in self.rm.themes]
      self.refresh_screen()

   def refresh_screen(self, updateSpinners=True):
      # This is annoying but I have to do it cause on_text causes update_screen_widget to run...
      self.disableUpdate = True
      if not (self.character.race == None):
         self.ids.racespinner.text = self.character.race['name']
      if not (self.character.theme == None):
         self.ids.themespinner.text = self.character.theme['name']
      self.ids.gender.text = self.character.gender
      self.ids.homeworld.text = self.character.homeworld
      self.ids.alignment.text = self.character.alignment
      self.ids.deity.text = self.character.deity
      self.ids.player.text = self.character.player
      self.ids.charname.text = self.character.name
      self.ids.strbase.text = str(self.character.strPoints)
      self.ids.dexbase.text = str(self.character.dexPoints)
      self.ids.conbase.text = str(self.character.conPoints)
      self.ids.intbase.text = str(self.character.intPoints)
      self.ids.wisbase.text = str(self.character.wisPoints)
      self.ids.chabase.text = str(self.character.chaPoints)
      self.disableUpdate = False
      self.update_screen_widgets()

   def update_screen_widgets(self):
      if not self.disableUpdate:
         # Updating Name
         self.character.name = self.ids.charname.text
         # Updating Race
         self.character.race = self.rm.get_item_by_name(self.ids.racespinner.text)
         # Updating Race
         self.character.theme = self.rm.get_item_by_name(self.ids.themespinner.text)
         # Updataing ability values
         self.ids.strbase.values = [str(i) for i in range(0,19-self.character.strBaseScore)]
         self.character.strScore = int(self.ids.strbase.text)
         self.ids.strtotal.text = str(self.character.strScore)
         self.ids.dexbase.values = [str(i) for i in range(0,19-self.character.dexBaseScore)]
         self.character.dexScore = int(self.ids.dexbase.text)
         self.ids.dextotal.text = str(self.character.dexScore)
         self.ids.conbase.values = [str(i) for i in range(0,19-self.character.conBaseScore)]
         self.character.conScore = int(self.ids.conbase.text)
         self.ids.contotal.text = str(self.character.conScore)
         self.ids.intbase.values = [str(i) for i in range(0,19-self.character.intBaseScore)]
         self.character.intScore = int(self.ids.intbase.text)
         self.ids.inttotal.text = str(self.character.intScore)
         self.ids.wisbase.values = [str(i) for i in range(0,19-self.character.wisBaseScore)]
         self.character.wisScore = int(self.ids.wisbase.text)
         self.ids.wistotal.text = str(self.character.wisScore)
         self.ids.chabase.values = [str(i) for i in range(0,19-self.character.chaBaseScore)]
         self.character.chaScore = int(self.ids.chabase.text)
         self.ids.chatotal.text = str(self.character.chaScore)
         # Calculate Point Buy
         self.ids.pblabel.text = 'Point Buy: '+str(self.character.pointBuy)
         self.ids.pllabel.text = 'Points Left: '+str(10-self.character.pointBuy)
         self.ids.staminalabel.text = 'Total Stamina: '+str(self.character.staminaPointsTotal)
         self.ids.hplabel.text = 'Total HP: '+str(self.character.hitPointsTotal)
         self.ids.resolvelabel.text = 'Total Resolve: '+str(self.character.resolvePointsTotal)
         # Setting other stuff...
      self.character.gender = self.ids.gender.text
      self.character.homeworld = self.ids.homeworld.text
      self.character.alignment = self.ids.alignment.text
      self.character.deity = self.ids.deity.text
      self.character.player = self.ids.player.text

   def print_stuff(self):
      print('\n\nEFFECTS!',self.character.effects)
      print('\n\nCLASSES!')
      for i in self.character.classes:
         print(i['name'])
      print()
      print('FEATS!')
      for a in self.character.feats:
         print(a['name'],a['prerequisites'])
      print()
      print('ABILITIES!')
      for a in self.character.abilities:
         print(a['name'])
      print()
      print('EFFECTS!')
      for a in self.character.effects:
         print(a['type'],a['value'])

class RootWidget(FloatLayout):
   '''This is the class representing your root widget.
      By default it is inherited from BoxLayout,
      you can use any other layout/widget depending on your usage.
   '''
   pass


class MainApp(App):
   '''This is the main class of your app.
      Define any app wide entities here.
      This class can be accessed anywhere inside the kivy app as,
      in python::

      app = App.get_running_app()
      print (app.title)

      in kv language::

      on_release: print(app.title)
      Name of the .kv file that is auto-loaded is derived from the name
      of this class::

      MainApp = main.kv
      MainClass = mainclass.kv

      The App part is auto removed and the whole name is lowercased.
   '''
   def __init__(self, *args):
      self.screenStrings = ['General','Classes','Feats','Abilities','Skills']
      super(MainApp, self).__init__(*args)
      Clock.schedule_once(self._setup_options)

   def _setup_options(self, *args):
      self.rm = ResourceManager()
      self.rm.load('./books/crb.pkl')
      self.character = StarfinderCharacterObject()
      self.character.rm = self.rm
      self.character.add_class(self.rm.get_item_by_name('Soldier'))
      self.curr_screen = ''
      self.switch_screen('Setup')
      for screen in self.screenStrings:
         self.load_screen(screen)

   def on_start(self):
      self.profile = cProfile.Profile()
      self.profile.enable()

   def on_stop(self):
      self.profile.disable()
      self.profile.dump_stats('myapp3.profile')

   def build(self):
      self.screens = {}
      return RootWidget()

   def switch_screen(self, screenid):
      if (screenid == self.curr_screen):
         return
      print('we switched it...')
      screen = self.load_screen(screenid)
      sm = self.root.ids.sm
      self.root.ids.sm.switch_to(screen, direction='left')
      self.curr_screen = screenid

   def load_screen(self, screenid):
      if screenid in self.screens:
         self.screens[screenid].refresh_screen()
         return self.screens[screenid]
      # screen = Builder.load_file(screenid)
      curdir = dirname(__file__)
      filepath = join(curdir, 'screens',screenid+'.kv')
      screen = Builder.load_file(filepath)
      self.screens[screenid] = screen
      return screen

   def export_character(self):
      CharSheetBuilder.MakeSFCS(self.character.get_pdf_array())

   def dismiss_popup(self):
      self.root._popup.dismiss()

   def show_load(self):
      content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
      self.root._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
      self.root._popup.open()

   def show_save(self):
      content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
      self.root._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
      self.root._popup.open()

   def open_license_dialog(self):
      content = LicenseDialog(cancel=self.dismiss_popup)
      file = open('LICENSE.txt','r')
      licenseStr = file.read()
      file.close()
      content.ids.licenselabel.text = licenseStr
      self.root._popup = Popup(title="License Info", content=content, size_hint=(0.9, 0.9))
      self.root._popup.open()

   def save(self, path, filename):
      self.character.save(path+'/'+filename)
      self.dismiss_popup()

   def load(self, path, filename):
      self.character.load(filename[0])
      self.dismiss_popup()
      self.screens[self.curr_screen].refresh_screen()

if '__main__' == __name__:
   MainApp().run()
