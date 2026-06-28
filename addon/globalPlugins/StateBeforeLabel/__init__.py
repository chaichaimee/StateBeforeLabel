# __init__.py
# Copyright (C) 2026 Chai Chaimee
# Licensed under GNU General Public License. See COPYING.txt for details.

import core
import speech
import controlTypes
import globalPluginHandler
import addonHandler
import config
import gui
import wx
from gui.settingsDialogs import SettingsPanel

addonHandler.initTranslation()

confspec = {
	"enableCheckRoles": "boolean(default=True)",
	"enableToggleRoles": "boolean(default=True)",
	"enableExpandRoles": "boolean(default=True)",
	"enableUnavailableState": "boolean(default=True)",
	"enableSelectedState": "boolean(default=False)",
	"enableButtonExpand": "boolean(default=True)",
	"enableReadOnlyState": "boolean(default=True)"
}
config.conf.spec["StateBeforeLabel"] = confspec


class StateBeforeLabelSettingsPanel(SettingsPanel):
	title = _("State Before Label")

	def makeSettings(self, settingsSizer):
		sblHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)

		self.checkRolesCheckBox = sblHelper.addItem(
			wx.CheckBox(self, label=_("Enable for Checkboxes, Radio buttons, and Check Menu Items"))
		)
		self.checkRolesCheckBox.SetValue(config.conf["StateBeforeLabel"]["enableCheckRoles"])

		self.toggleRolesCheckBox = sblHelper.addItem(
			wx.CheckBox(self, label=_("Enable for Toggle buttons"))
		)
		self.toggleRolesCheckBox.SetValue(config.conf["StateBeforeLabel"]["enableToggleRoles"])

		self.expandRolesCheckBox = sblHelper.addItem(
			wx.CheckBox(self, label=_("Enable for TreeView items (Expanded/Collapsed)"))
		)
		self.expandRolesCheckBox.SetValue(config.conf["StateBeforeLabel"]["enableExpandRoles"])

		self.unavailableCheckBox = sblHelper.addItem(
			wx.CheckBox(self, label=_("Announce &Unavailable state before name (global)"))
		)
		self.unavailableCheckBox.SetValue(config.conf["StateBeforeLabel"]["enableUnavailableState"])

		self.selectedCheckBox = sblHelper.addItem(
			wx.CheckBox(self, label=_("Announce &Selected state for Tabs and List items"))
		)
		self.selectedCheckBox.SetValue(config.conf["StateBeforeLabel"]["enableSelectedState"])

		self.buttonExpandCheckBox = sblHelper.addItem(
			wx.CheckBox(self, label=_("Include &Buttons for Expanded/Collapsed detection"))
		)
		self.buttonExpandCheckBox.SetValue(config.conf["StateBeforeLabel"]["enableButtonExpand"])

		self.readOnlyCheckBox = sblHelper.addItem(
			wx.CheckBox(self, label=_("Announce &Read-only state for Edit boxes"))
		)
		self.readOnlyCheckBox.SetValue(config.conf["StateBeforeLabel"]["enableReadOnlyState"])

	def onSave(self):
		config.conf["StateBeforeLabel"]["enableCheckRoles"] = self.checkRolesCheckBox.GetValue()
		config.conf["StateBeforeLabel"]["enableToggleRoles"] = self.toggleRolesCheckBox.GetValue()
		config.conf["StateBeforeLabel"]["enableExpandRoles"] = self.expandRolesCheckBox.GetValue()
		config.conf["StateBeforeLabel"]["enableUnavailableState"] = self.unavailableCheckBox.GetValue()
		config.conf["StateBeforeLabel"]["enableSelectedState"] = self.selectedCheckBox.GetValue()
		config.conf["StateBeforeLabel"]["enableButtonExpand"] = self.buttonExpandCheckBox.GetValue()
		config.conf["StateBeforeLabel"]["enableReadOnlyState"] = self.readOnlyCheckBox.GetValue()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(StateBeforeLabelSettingsPanel)

		self.lblChecked = getattr(controlTypes.State.CHECKED, "displayString", "")
		self.lblNotChecked = getattr(controlTypes.State.CHECKED, "negativeDisplayString", "")

		self.lblPressed = getattr(controlTypes.State.PRESSED, "displayString", "")
		self.lblNotPressed = getattr(controlTypes.State.PRESSED, "negativeDisplayString", "")

		self.lblExpanded = getattr(controlTypes.State.EXPANDED, "displayString", "")
		self.lblCollapsed = getattr(controlTypes.State.COLLAPSED, "displayString", "")

		self.lblSelected = getattr(controlTypes.State.SELECTED, "displayString", "")
		self.lblUnavailable = getattr(controlTypes.State.UNAVAILABLE, "displayString", "")
		self.lblReadOnly = getattr(controlTypes.State.READONLY, "displayString", "")

	def terminate(self):
		if StateBeforeLabelSettingsPanel in gui.settingsDialogs.NVDASettingsDialog.categoryClasses:
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(StateBeforeLabelSettingsPanel)
		super().terminate()

	def event_gainFocus(self, obj, nextHandler):
		if not obj:
			return nextHandler()

		role = obj.role
		states = obj.states
		priorityStateStr = ""
		roleSpecificStateStr = ""
		addonConfig = config.conf["StateBeforeLabel"]

		checkRoles = (
			controlTypes.Role.CHECKBOX,
			controlTypes.Role.RADIOBUTTON,
			controlTypes.Role.CHECKMENUITEM,
			controlTypes.Role.RADIOMENUITEM
		)
		toggleRoles = (controlTypes.Role.TOGGLEBUTTON,)
		expandRoles = [controlTypes.Role.TREEVIEWITEM]
		if addonConfig["enableButtonExpand"]:
			expandRoles.append(controlTypes.Role.BUTTON)
		expandRoles = tuple(expandRoles)
		selectedRoles = (controlTypes.Role.TAB, controlTypes.Role.LISTITEM)
		readOnlyRoles = (controlTypes.Role.EDITABLETEXT,)

		# Global Unavailable check
		if addonConfig["enableUnavailableState"] and controlTypes.State.UNAVAILABLE in states:
			priorityStateStr = self.lblUnavailable

		# Role-specific state determination
		if role in checkRoles and addonConfig["enableCheckRoles"]:
			if controlTypes.State.CHECKED in states:
				roleSpecificStateStr = self.lblChecked
			else:
				roleSpecificStateStr = self.lblNotChecked

		elif role in toggleRoles and addonConfig["enableToggleRoles"]:
			if controlTypes.State.PRESSED in states:
				roleSpecificStateStr = self.lblPressed
			else:
				roleSpecificStateStr = self.lblNotPressed

		elif role in expandRoles and addonConfig["enableExpandRoles"]:
			if controlTypes.State.EXPANDED in states:
				roleSpecificStateStr = self.lblExpanded
			elif controlTypes.State.COLLAPSED in states:
				roleSpecificStateStr = self.lblCollapsed

		elif role in selectedRoles and addonConfig["enableSelectedState"]:
			if controlTypes.State.SELECTED in states:
				roleSpecificStateStr = self.lblSelected

		elif role in readOnlyRoles and addonConfig["enableReadOnlyState"]:
			if controlTypes.State.READONLY in states:
				roleSpecificStateStr = self.lblReadOnly

		if not priorityStateStr and not roleSpecificStateStr:
			return nextHandler()

		# Read-only and Unavailable: modify name and remove state temporarily
		if roleSpecificStateStr == self.lblReadOnly or priorityStateStr == self.lblUnavailable:
			prependParts = []
			if priorityStateStr:
				prependParts.append(priorityStateStr)
			if roleSpecificStateStr:
				prependParts.append(roleSpecificStateStr)
			prependText = " ".join(prependParts) + " "

			originalName = obj.name
			statesToRemove = set()
			if priorityStateStr == self.lblUnavailable:
				statesToRemove.add(controlTypes.State.UNAVAILABLE)
			if roleSpecificStateStr == self.lblReadOnly:
				statesToRemove.add(controlTypes.State.READONLY)

			try:
				obj.name = prependText + (originalName if originalName else "")
				obj.states = states - statesToRemove
				return nextHandler()
			finally:
				obj.name = originalName
				obj.states = states

		# All other roles: full custom announcement
		objName = obj.name if obj.name else ""
		shortcut = obj.keyboardShortcut if obj.keyboardShortcut else ""

		components = [priorityStateStr, roleSpecificStateStr, objName, shortcut]
		finalText = " ".join([comp for comp in components if comp]).strip()

		if finalText:
			core.callLater(10, self._speakCustomFocus, finalText)
			return

		return nextHandler()

	def _speakCustomFocus(self, text):
		speech.cancelSpeech()
		speech.speakText(text)