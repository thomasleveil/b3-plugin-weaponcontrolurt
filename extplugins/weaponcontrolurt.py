#
# Plugin for BigBrotherBot(B3) (www.bigbrotherbot.com)
# Copyright (C) 2008 Courgette
# 
#  Description :
#     this plugin allow to forbid the use of any weapon of Urban Terror
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# Changelog:
#
# 10/10/2008 - v0.1.0b - Courgette : 
#  -first shot, beta version. Seems to work, waiting for feedback before moving on
# 11/10/2008 - v0.2.0b - Courgette : 
#  - add weaponcontrol command to change settings in-game
#  - add control over the M4A1 (missing in the Urban Terror manual)
# 19/10/2008 -v0.2.1 - Courgette
# - just updated the config file as it was missing the command section
# 04/03/2009 - v0.3.0 - Courgette
# - Fix bug with the AK.
# - Add missing 'kevlar helmet'
# - Broadcast message when a weapon/item is allowed/disallowed
"""
Urban Terror doc on gear : http://www.urbanterror.net/urt_manual/gear.htm
"""

__version__ = '0.3.0'
__author__  = 'Courgette'

import b3, re
import b3.events
import b3.plugin


#--------------------------------------------------------------------------------------------------
class WeaponcontrolurtPlugin(b3.plugin.Plugin):
  _adminPlugin = None
  _forbiddenWeapons = []
  _forbiddenWeaponsFromConfig = []
  
  weaponCodes = {
    'Beretta 92G': 'F'
    ,'Desert Eagle': 'G'
    ,'SPAS-12': 'H'
    ,'MP5K': 'I'
    ,'UMP45': 'J'
    ,'HK69': 'K'
    ,'LR300ML': 'L'
    ,'G36': 'M'
    ,'PSG-1': 'N'
    ,'SR-8': 'Z'
    ,'AK-103': 'a'
    ,'Negev': 'c'
    ,'M4A1': 'e'
    ,'HE Grenade': 'O'
    ,'Smoke Grenade': 'Q'
    ,'Kevlar Vest': 'R'
    ,'Kevlar Helmet': 'W'
    ,'Silencer': 'U'
    ,'Laser Sight': 'V'
    ,'Medkit': 'T'
    ,'NVGs': 'S'
    ,'Extra Ammo': 'X'
  }
  
  def onStartup(self):
    # note: we are listening to client name change events as every time the parser receive a clientInfo line, 
    # the name is set again, hence raising this event.
    self.registerEvent(b3.events.EVT_CLIENT_NAME_CHANGE)
          
  def onLoadConfig(self):

    # get the admin plugin 
    self._adminPlugin = self.console.getPlugin('admin')
    if not self._adminPlugin:
      # something is wrong, can't start without admin plugin
      self.error('Could not find admin plugin')
      return False
   
    # register our commands
    if 'commands' in self.config.sections():
      for cmd in self.config.options('commands'):
        level = self.config.get('commands', cmd)
        sp = cmd.split('-')
        alias = None
        if len(sp) == 2:
          cmd, alias = sp

        func = self.getCmd(cmd)
        if func:
          self._adminPlugin.registerCommand(self, cmd, level, func, alias)
          
    for weapon in self.config.options('weapons'):
      try:
        if not self.config.getboolean('weapons', weapon):
          self._forbiddenWeapons.append(self.weaponCodes[weapon])
      except:
        self.warning('config error for weapon %s'%weapon)
    
    self.debug('forbidden weapon codes : %s'%self._forbiddenWeapons)
    self._forbiddenWeaponsFromConfig = self._forbiddenWeapons
    
        
  def onEvent(self, event):  
    if event.type == b3.events.EVT_CLIENT_NAME_CHANGE:
      self.checkClient(event.client)
       
  def getCmd(self, cmd):
    cmd = 'cmd_%s' % cmd
    if hasattr(self, cmd):
      func = getattr(self, cmd)
      return func

    return None
    
  def checkClient(self, client):
    if not hasattr(client, 'gear'):
      return
    if client.team == b3.TEAM_SPEC:
      return
      
    self.debug('gear : %s'%client.gear)
    
    problems = []
    for weap in self._forbiddenWeapons:
      if weap in client.gear:
        problems.append(find_key(self.weaponCodes, weap))
    
    if len(problems)>0:
      self.debug('%s has %s unallowed weapons : %s'%(client.name, len(problems), problems))
      self.console.write('forceteam %s %s' % (client.cid, 's'))
      client.message('sorry, weapon not allowed : %s'% (', '.join(problems)))
  
  
  def cmd_weaponcontrol(self, data, client, cmd=None):
    """\
    set resctrictions on weapon choice
    all|reset
    [+|-]ber|de|spas|mp5|ump|hk|lr|g36|psg|sr8|ak|neg|he|smoke|kev|hel|sil|laser|med|nvg|xtra
    """
    if not data:
      restrictions = []
      for weap in self._forbiddenWeapons:
        restrictions.append(find_key(self.weaponCodes, weap))
        
      if len(restrictions) == 0:
        client.message('^7No weapon restriction')
      else:
        client.message('^7Weapon restrictions: %s'% (', '.join(restrictions)))
      return True
    else:
      if not data[:4] in ('all', 'rese', 
        '+ber', '+de', '+spa', '+mp5', '+ump', '+hk', '+lr', '+g36', '+psg', '+sr8', '+ak', '+neg', '+m4', '+he', '+smo', '+kev', '+hel', '+sil', '+las', '+med', '+nvg', '+xtr',
        '-ber', '-de', '-spa', '-mp5', '-ump', '-hk', '-lr', '-g36', '-psg', '-sr8', '-ak', '-neg', '-m4', '-he', '-smo', '-kev', '-hel', '-sil', '-las', '-med', '-nvg', '-xtr'):
        if client:
          client.message('^7Invalid data, try !help weaponcontrol')
        else:
          self.debug('Invalid data sent to cmd_weaponcontrol')
        return False
        
    if data[:3] == 'all':
      self._forbiddenWeapons = []
      self.console.say('^7All weapons/items allowed')
    elif data[:3] == 'res':
      self._forbiddenWeapons = self._forbiddenWeaponsFromConfig
      restrictions = []
      for weap in self._forbiddenWeapons:
        restrictions.append(find_key(self.weaponCodes, weap))
      self.console.say('^7Weapon restrictions: %s'% (', '.join(restrictions)))
    else:
      if data[1:4] == 'ber':
        bit='F'
      elif data[1:3] == 'de':
        bit='G'
      elif data[1:4] == 'spa':
        bit='H'
      elif data[1:3] == 'mp':
        bit='I'
      elif data[1:4] == 'ump':
        bit='J'
      elif data[1:3] == 'hk':
        bit='K'
      elif data[1:3] == 'lr':
        bit='L'
      elif data[1:4] == 'g36':
        bit='M'
      elif data[1:4] == 'psg':
        bit='N'
      elif data[1:3] == 'sr':
        bit='Z'
      elif data[1:3] == 'ak':
        bit='a'
      elif data[1:4] == 'neg':
        bit='c'
      elif data[1:4] == 'm4':
        bit='e'
      elif data[1:4] == 'hel':
        bit='W'
      elif data[1:3] == 'he':
        bit='O'
      elif data[1:4] == 'smo':
        bit='Q'
      elif data[1:4] == 'kev':
        bit='R'
      elif data[1:4] == 'sil':
        bit='U'
      elif data[1:4] == 'las':
        bit='V'
      elif data[1:4] == 'med':
        bit='T'
      elif data[1:4] == 'nvg':
        bit='S'
      elif data[1:4] == 'xtr':
        bit='X'
      elif data[1:4] == 'ext':
        bit='X'
      else:
        return False
        
      if data[:1] == '-':
        if bit not in self._forbiddenWeapons:
          self._forbiddenWeapons.append(bit)
          self.console.say('^4%s^7 is now ^1disallowed'% find_key(self.weaponCodes, bit))
        else:
          client.message('^4%s^7 is already forbidden' % find_key(self.weaponCodes, bit))
      elif data[:1] == '+':
        if bit in self._forbiddenWeapons:
          try:
            self._forbiddenWeapons.remove(bit)
            self.console.say('^4%s^7 is now ^2allowed'% find_key(self.weaponCodes, bit))
          except:
            pass
        else:
          client.message('^4%s^7 is already allowed' % find_key(self.weaponCodes, bit))
      else:
        client.message('^7Invalid data, try !help weaponcontrol')
        return False
      
      self.checkConnectedPlayers()
      return True
    
  def checkConnectedPlayers(self):
    self.info("checking all connected players")
    clients = self.console.clients.getList()
    for c in clients:
      self.checkClient(c)
    
############ util ############
def find_key(dic, val):
    """return the key of dictionary dic given the value"""
    return [k for k, v in dic.items() if v == val][0]