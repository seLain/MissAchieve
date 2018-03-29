# MissAchieve
A mission and achievement app built with Django

## Missions

### Data Model

The data model design relies on MissionPorxy to allow Many-to-Many association between User and various Missions.
This design brings two advantages:
* Decoupling of User and Missions : When expanding new Mission classes, designers can focus on Mission criteria and level design.  
* Managing User objects and Mission object state purely in MissionProxy.

<img src="http://yuml.me/diagram/plain;dir:lr;scale:80/class/[MissionProxy]<>* owner-1>[auth.models.User],[MissionProxy]<>* mission-1>[Mission],[Mission]^-[KeywordMission],[Mission]^-[TalkToMeMission]"/>

### Expand New Mission Class

To expand new Mission class, simply add a new Mission class in ``models.py``. For example, we  can create a MagicNumberMission:
```python
class MagicNumberMission(Mission):
	magic_number = models.CharField(max_length=8)
```
The MagicNumberMission extends Mission class, therefore it's also a Mission object. The ``magic_number`` field records a specific numerical string used to check if mission criteria is reached.

Also, register MagicNumberMission is your ```admin.py```.

### Create New Mission

Login the admin dashboard of your Django web server.
The MagicNumberMission is supposed to show in the admin panel.
Create an instance of MagicNumberMission with designated ``magic_number``, and copy the ``key`` of this instance.

Just like that, a new MagicNumberMission instance is created. 
Please note that, this instance is not owned by any user. 
It's more like a public practice that can be copied and performed by any user.

The client code can utilize MissAchieve API `/achievements/mission/create` to create a MissionProxy object by given user and MagicNumberMission instance.

If there are multiple MagicNumberMission instances, the same user can have them all by create multiple MissionProxy objects.

## Bots

### Mattermost Bot

Rename `mm_bot_settings.example` as `mm_bot_settings.py`, and configure `mm_bot_settings.py` for mattermost API connection.

Installing `mattermost_bot` package first.

`pip install git+https://github.com/seLain/mattermost_bot`
