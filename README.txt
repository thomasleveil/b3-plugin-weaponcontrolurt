weaponcontrolurt plugin for Big Brother Bot (www.bigbrotherbot.com)
===================================================================

Author: Courgette
Game: Urban Terror 4.1


Description
-----------

This plugin allows to define a set of weapon not allowed on your server.


Installation
------------

 * copy weaponcontrolurt.py into b3/extplugins
 * copy plugin_weaponcontrolurt.xml into b3/extplugins/conf
 * update your main b3 config file with :
<plugin name="weaponcontrolurt" priority="18" config="@b3/extplugins/conf/plugin_weaponcontrolurt.xml"/>



Admin guide
----------- 

!help weaponcontrol : show available options

!weaponcontrol : show current restrictions
!weaponcontrol all : allow all weapons/items
!weaponcontrol reset : forbid weap/item as set in the config file

!weaponcontrol -ber : forbide Beretta
!weaponcontrol +ber : allow Beretta
!weaponcontrol -de : forbide Desert Eagle
!weaponcontrol +de : allow Desert Eagle
and so on with the following weap/item codes :
 ber : Beretta 92G
 de : Desert Eagle
 spa : SPAS-12
 mp : MP5K
 ump : UMP45
 hk : HK69
 lr : LR300ML
 g36 : G36
 psg : PSG-1
 sr : SR-8
 ak : AK-103
 neg : Negev
 m4 : M-4
 he : HE Grenade
 smo : Smoke Grenade
 kev : Kevlar Vest
 hel : Kevlar Helmet
 sil : Silencer
 las : Laser Sight
 med : Medkit
 nvg : NVGs (lunettes de vision nocturne)
 xtr ou ext: Extra Ammo
 
NOTE: 
  !weaponcontrol -sil
and
  !weaponcontrol -silencer
are equivalent. only the first 3 letters are checked to recognise the weap/item


