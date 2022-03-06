from datetime import datetime
from time import mktime

from Components.config import ConfigSelection, ConfigBoolean, ConfigDateTime, ConfigSequence, ConfigInteger, ConfigIP, ConfigClock, ConfigText, ConfigSelectionNumber, ConfigNumber, ConfigSlider, ConfigSet, ConfigLocations, ConfigNothing, getConfigListEntry
from Components.ScrollLabel import ScrollLabel

from Plugins.Plugin import PluginDescriptor

from Screens.Setup import Setup

from Tools.Directories import resolveFilename, SCOPE_HDD

class NotifierTester(Setup):
	skin = ["""
	<screen name="NotifierTest" position="center,center" size="%d,%d">
		<ePixmap pixmap="skin_default/buttons/red.png" position="%d,%d" size="%d,%d" alphatest="blend" scale="1"/>
		<widget source="key_red" render="Label" position="%d,%d" zPosition="1" size="%d,%d" font="Regular;%d" halign="center" valign="center" backgroundColor="#9f1313" transparent="1"/>
		<widget name="config" position="%d,%d" size="%d,%d" itemHeight="%d" font="Regular;%d" transparent="0" enableWrapAround="1" scrollbarMode="showNever"/>
		<widget name="output" position="%d,e-%d" size="%d,%d" font="Regular;%d" halign="left" valign="top" transparent="0" zPosition="1"/>
	</screen>""",
		560, 650, # screen
		0, 0, 140, 40, #colors
		0, 0, 140, 40, 20,
		0, 50, 560, 350, 25, 19, # config
		0, 250, 560, 250, 18, # output
	]
	def __init__(self, session):
		self["output"] = ScrollLabel("")
		def notifier(ConfigElement):
			n = ConfigElement.__class__.__name__
			t = datetime.now().strftime("%H:%M:%S.%f")[:13]
			text = "%s %s notifier" % (t, n)
			self["output"].appendText("%s\n" % text)
			print("[NotifierTest] %s" % text)
		self.ConfigSelection = ConfigSelection(["1","2"])
		self.ConfigSelection.addNotifier(notifier, initial_call=False)
		self.ConfigBoolean = ConfigBoolean(graphic=False)
		self.ConfigBoolean.addNotifier(notifier, initial_call=False)
		self.ConfigDateTime = ConfigDateTime(default=mktime(datetime(1970, 1, 1, 7, 0).timetuple()), formatstring=_("%H:%M"), increment=600)
		self.ConfigDateTime.addNotifier(notifier, initial_call=False)
		self.ConfigSequence = ConfigSequence(seperator=',', default=[720, 576], limits=[(352, 720), (480, 576)])
		self.ConfigSequence.addNotifier(notifier, initial_call=False)
		self.ConfigInteger = ConfigInteger(default=5, limits=(1, 10))
		self.ConfigInteger.addNotifier(notifier, initial_call=False)
		self.ConfigIP = ConfigIP(default=[0, 0, 0, 0], auto_jump=True)
		self.ConfigIP.addNotifier(notifier, initial_call=False)
		self.ConfigClock = ConfigClock(default=0)
		self.ConfigClock.addNotifier(notifier, initial_call=False)
		self.ConfigText = ConfigText(default="/tmp")
		self.ConfigText.addNotifier(notifier, initial_call=False)
		self.ConfigSelectionNumber = ConfigSelectionNumber(min=3, max=24, stepwidth=3, default=6, wraparound=True)
		self.ConfigSelectionNumber.addNotifier(notifier, initial_call=False)
		self.ConfigNumber = ConfigNumber()
		self.ConfigNumber.addNotifier(notifier, initial_call=False)
		self.ConfigSlider = ConfigSlider(default=5, limits=(0, 26))
		self.ConfigSlider.addNotifier(notifier, initial_call=False)
		self.ConfigSet = ConfigSet(default=[2, 4, 8, 16, 32, 64, 128], choices=[2, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128])
		self.ConfigSet.addNotifier(notifier, initial_call=False)
		self.ConfigLocations = ConfigLocations(default=[resolveFilename(SCOPE_HDD)])
		self.ConfigLocations.addNotifier(notifier, initial_call=False)
		self.ConfigNothing = ConfigNothing()
		self.ConfigNothing.addNotifier(notifier, initial_call=False)
		Setup.__init__(self, session=session, setup=None)
		self["key_green"].text = ""
		self.skinName = [self.__class__.__name__]
		
	def createSetup(self):
		self.list = []
		self.list.append(getConfigListEntry("ConfigSelection", self.ConfigSelection))
		self.list.append(getConfigListEntry("ConfigBoolean", self.ConfigBoolean))
		self.list.append(getConfigListEntry("ConfigDateTime", self.ConfigDateTime))
		self.list.append(getConfigListEntry("ConfigSequence", self.ConfigSequence))
		self.list.append(getConfigListEntry("ConfigInteger", self.ConfigInteger))
		self.list.append(getConfigListEntry("ConfigIP", self.ConfigIP))
		self.list.append(getConfigListEntry("ConfigClock", self.ConfigClock))
		self.list.append(getConfigListEntry("ConfigText", self.ConfigText))
		self.list.append(getConfigListEntry("ConfigSelectionNumber", self.ConfigSelectionNumber))
		self.list.append(getConfigListEntry("ConfigNumber", self.ConfigNumber))
		self.list.append(getConfigListEntry("ConfigSlider", self.ConfigSlider))
		self.list.append(getConfigListEntry("ConfigSet", self.ConfigSet))
		self.list.append(getConfigListEntry("ConfigLocations", self.ConfigLocations))
		self.list.append(getConfigListEntry("ConfigNothing", self.ConfigNothing))
		currentItem = self["config"].getCurrent()
		self["config"].list = self.list
		self.moveToItem(currentItem)

	def changedEntry(self):
		n = self["config"].getCurrent()[1].__class__.__name__
		t = datetime.now().strftime("%H:%M:%S.%f")[:13]
		text = "%s %s callback" % (t, n)
		self["output"].appendText("%s\n" % text)
		print("[NotifierTest] %s" % text)
			
	def keySave(self):
		pass

	def keyCancel(self):
		self.close()

	
def main(session, **kwargs):
	session.open(NotifierTester)

def Plugins(**kwargs):
	list = []

	list.append(
		PluginDescriptor(name=_("Notifier Tester"),
		description=_("See notifiers in action."),
		where = [PluginDescriptor.WHERE_PLUGINMENU],
		needsRestart = False,
		fnc = main))

	return list
				