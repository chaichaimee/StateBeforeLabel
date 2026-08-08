# __init__.py
# Copyright (C) 2026 Chai Chaimee
# Licensed under GNU General Public License. See COPYING.txt for details.

# (Import Order: Standard libraries -> Overlay/External -> Internal modules)
import os
import sys
import threading
import addonHandler
import core
import logHandler

from comtypes import COMError
import speech
import controlTypes
import globalPluginHandler
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
		addonConfig = config.conf["StateBeforeLabel"]
		addonConfig["enableCheckRoles"] = self.checkRolesCheckBox.GetValue()
		addonConfig["enableToggleRoles"] = self.toggleRolesCheckBox.GetValue()
		addonConfig["enableExpandRoles"] = self.expandRolesCheckBox.GetValue()
		addonConfig["enableUnavailableState"] = self.unavailableCheckBox.GetValue()
		addonConfig["enableSelectedState"] = self.selectedCheckBox.GetValue()
		addonConfig["enableButtonExpand"] = self.buttonExpandCheckBox.GetValue()
		addonConfig["enableReadOnlyState"] = self.readOnlyCheckBox.GetValue()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self._isTargetActive = False

		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(StateBeforeLabelSettingsPanel)

		self.lblChecked = controlTypes.stateLabels.get(controlTypes.State.CHECKED, "")
		self.lblNotChecked = controlTypes.negativeStateLabels.get(controlTypes.State.CHECKED, "")
		self.lblPressed = controlTypes.stateLabels.get(controlTypes.State.PRESSED, "")
		self.lblNotPressed = controlTypes.negativeStateLabels.get(controlTypes.State.PRESSED, "")
		self.lblExpanded = controlTypes.stateLabels.get(controlTypes.State.EXPANDED, "")
		self.lblCollapsed = controlTypes.stateLabels.get(controlTypes.State.COLLAPSED, "")
		self.lblSelected = controlTypes.stateLabels.get(controlTypes.State.SELECTED, "")
		self.lblUnavailable = controlTypes.stateLabels.get(controlTypes.State.UNAVAILABLE, "")
		self.lblReadOnly = controlTypes.stateLabels.get(controlTypes.State.READONLY, "")

	def terminate(self):
		self._isTargetActive = False
		if StateBeforeLabelSettingsPanel in gui.settingsDialogs.NVDASettingsDialog.categoryClasses:
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(StateBeforeLabelSettingsPanel)
		super().terminate()

	def event_foreground(self, foregroundObj, nextHandler):
		try:
			if not foregroundObj:
				self._isTargetActive = False
				return nextHandler()

			targetAppModule = getattr(foregroundObj, "appModule", None)
			if not targetAppModule:
				self._isTargetActive = False
				return nextHandler()

			appName = getattr(targetAppModule, "appName", "")
			if appName:
				self._isTargetActive = True
			else:
				self._isTargetActive = False

		except (RuntimeError, COMError, AttributeError) as err:
			logHandler.log.debug(f"StateBeforeLabel: Error evaluating foreground watchdog state: {err}")
			self._isTargetActive = False

		return nextHandler()

	def event_gainFocus(self, focusedObj, nextHandler):
		if not self._isTargetActive:
			return nextHandler()

		if not focusedObj:
			return nextHandler()

		currentRole = focusedObj.role
		currentStates = focusedObj.states
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
		expandRolesTuple = tuple(expandRoles)
		
		selectedRoles = (controlTypes.Role.TAB, controlTypes.Role.LISTITEM)
		readOnlyRoles = (controlTypes.Role.EDITABLETEXT,)

		if addonConfig["enableUnavailableState"] and controlTypes.State.UNAVAILABLE in currentStates:
			priorityStateStr = self.lblUnavailable

		if currentRole in checkRoles and addonConfig["enableCheckRoles"]:
			if controlTypes.State.CHECKED in currentStates:
				roleSpecificStateStr = self.lblChecked
			else:
				roleSpecificStateStr = self.lblNotChecked
		elif currentRole in toggleRoles and addonConfig["enableToggleRoles"]:
			if controlTypes.State.PRESSED in currentStates:
				roleSpecificStateStr = self.lblPressed
			else:
				roleSpecificStateStr = self.lblNotPressed
		elif currentRole in expandRolesTuple and addonConfig["enableExpandRoles"]:
			if controlTypes.State.EXPANDED in currentStates:
				roleSpecificStateStr = self.lblExpanded
			elif controlTypes.State.COLLAPSED in currentStates:
				roleSpecificStateStr = self.lblCollapsed
		elif currentRole in selectedRoles and addonConfig["enableSelectedState"]:
			if controlTypes.State.SELECTED in currentStates:
				roleSpecificStateStr = self.lblSelected
		elif currentRole in readOnlyRoles and addonConfig["enableReadOnlyState"]:
			if controlTypes.State.READONLY in currentStates:
				roleSpecificStateStr = self.lblReadOnly

		if not priorityStateStr and not roleSpecificStateStr:
			return nextHandler()

		if roleSpecificStateStr == self.lblReadOnly or priorityStateStr == self.lblUnavailable:
			prependParts = []
			if priorityStateStr:
				prependParts.append(priorityStateStr)
			if roleSpecificStateStr:
				prependParts.append(roleSpecificStateStr)
			prependText = " ".join(prependParts) + " "

			originalName = ""
			try:
				originalName = focusedObj.name
			except (RuntimeError, COMError, AttributeError) as err:
				logHandler.log.debug(f"StateBeforeLabel: Cannot read object name: {err}")

			statesToRemove = set()
			if priorityStateStr == self.lblUnavailable:
				statesToRemove.add(controlTypes.State.UNAVAILABLE)
			if roleSpecificStateStr == self.lblReadOnly:
				statesToRemove.add(controlTypes.State.READONLY)

			try:
				focusedObj.name = prependText + (originalName if originalName else "")
				focusedObj.states = currentStates - statesToRemove
				return nextHandler()
			except (RuntimeError, COMError, AttributeError) as err:
				logHandler.log.debug(f"StateBeforeLabel: Object mutation failed: {err}")
			finally:
				try:
					focusedObj.name = originalName
					focusedObj.states = currentStates
				except (RuntimeError, COMError, AttributeError) as err:
					logHandler.log.debug(f"StateBeforeLabel: Object restoration failed: {err}")

		objName = ""
		shortcut = ""
		try:
			objName = focusedObj.name if focusedObj.name else ""
			shortcut = focusedObj.keyboardShortcut if focusedObj.keyboardShortcut else ""
		except (RuntimeError, COMError, AttributeError) as err:
			logHandler.log.debug(f"StateBeforeLabel: Error reading properties for fallback: {err}")

		components = [priorityStateStr, roleSpecificStateStr, objName, shortcut]
		finalText = " ".join([comp for comp in components if comp]).strip()

		if finalText:
			core.callLater(10, self._speakCustomFocus, finalText)
			return

		return nextHandler()

	def _speakCustomFocus(self, textToSpeak):
		speech.cancelSpeech()
		speech.speakText(textToSpeak)