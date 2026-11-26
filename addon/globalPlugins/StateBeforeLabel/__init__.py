# __init__.py
# Copyright (C) 2026 Chai Chaimee
# Licensed under GNU General Public License. See COPYING.txt for details.

import os
import sys
import threading
import weakref
import addonHandler
import api
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

		# Cache state labels for performance (they change only on language switch)
		self._lblChecked = controlTypes.stateLabels.get(controlTypes.State.CHECKED, "")
		self._lblNotChecked = controlTypes.negativeStateLabels.get(controlTypes.State.CHECKED, "")
		self._lblPressed = controlTypes.stateLabels.get(controlTypes.State.PRESSED, "")
		self._lblNotPressed = controlTypes.negativeStateLabels.get(controlTypes.State.PRESSED, "")
		self._lblExpanded = controlTypes.stateLabels.get(controlTypes.State.EXPANDED, "")
		self._lblCollapsed = controlTypes.stateLabels.get(controlTypes.State.COLLAPSED, "")
		self._lblSelected = controlTypes.stateLabels.get(controlTypes.State.SELECTED, "")
		self._lblUnavailable = controlTypes.stateLabels.get(controlTypes.State.UNAVAILABLE, "")
		self._lblReadOnly = controlTypes.stateLabels.get(controlTypes.State.READONLY, "")

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
			self._isTargetActive = bool(appName)
		except (RuntimeError, COMError, AttributeError) as err:
			logHandler.log.debug(f"StateBeforeLabel: Error in foreground watchdog: {err}")
			self._isTargetActive = False
		return nextHandler()

	def event_gainFocus(self, focusedObj, nextHandler):
		if not self._isTargetActive:
			return nextHandler()
		if not focusedObj:
			return nextHandler()

		# Snapshot config to avoid repeated dict lookups
		addonConfig = config.conf["StateBeforeLabel"]
		try:
			currentRole = focusedObj.role
			currentStates = focusedObj.states
		except (RuntimeError, COMError, AttributeError) as err:
			logHandler.log.debug(f"StateBeforeLabel: Cannot read role/states: {err}")
			return nextHandler()

		priorityStateStr = ""
		roleSpecificStateStr = ""

		checkRoles = (
			controlTypes.Role.CHECKBOX, controlTypes.Role.RADIOBUTTON,
			controlTypes.Role.CHECKMENUITEM, controlTypes.Role.RADIOMENUITEM
		)
		toggleRoles = (controlTypes.Role.TOGGLEBUTTON,)
		expandRoles = [controlTypes.Role.TREEVIEWITEM]
		if addonConfig["enableButtonExpand"]:
			expandRoles.append(controlTypes.Role.BUTTON)
		expandRolesTuple = tuple(expandRoles)
		selectedRoles = (controlTypes.Role.TAB, controlTypes.Role.LISTITEM)
		readOnlyRoles = (controlTypes.Role.EDITABLETEXT,)

		if addonConfig["enableUnavailableState"] and controlTypes.State.UNAVAILABLE in currentStates:
			priorityStateStr = self._lblUnavailable

		if currentRole in checkRoles and addonConfig["enableCheckRoles"]:
			if controlTypes.State.CHECKED in currentStates:
				roleSpecificStateStr = self._lblChecked
			else:
				roleSpecificStateStr = self._lblNotChecked
		elif currentRole in toggleRoles and addonConfig["enableToggleRoles"]:
			if controlTypes.State.PRESSED in currentStates:
				roleSpecificStateStr = self._lblPressed
			else:
				roleSpecificStateStr = self._lblNotPressed
		elif currentRole in expandRolesTuple and addonConfig["enableExpandRoles"]:
			if controlTypes.State.EXPANDED in currentStates:
				roleSpecificStateStr = self._lblExpanded
			elif controlTypes.State.COLLAPSED in currentStates:
				roleSpecificStateStr = self._lblCollapsed
		elif currentRole in selectedRoles and addonConfig["enableSelectedState"]:
			if controlTypes.State.SELECTED in currentStates:
				roleSpecificStateStr = self._lblSelected
		elif currentRole in readOnlyRoles and addonConfig["enableReadOnlyState"]:
			if controlTypes.State.READONLY in currentStates:
				roleSpecificStateStr = self._lblReadOnly

		if not priorityStateStr and not roleSpecificStateStr:
			return nextHandler()

		# For unavailable/readonly we mutate object and let NVDA speak naturally
		if roleSpecificStateStr == self._lblReadOnly or priorityStateStr == self._lblUnavailable:
			prependParts = []
			if priorityStateStr:
				prependParts.append(priorityStateStr)
			if roleSpecificStateStr:
				prependParts.append(roleSpecificStateStr)
			prependText = " ".join(prependParts) + " "

			try:
				originalName = focusedObj.name
			except (RuntimeError, COMError, AttributeError) as err:
				logHandler.log.debug(f"StateBeforeLabel: Cannot read name: {err}")
				return nextHandler()

			statesToRemove = set()
			if priorityStateStr == self._lblUnavailable:
				statesToRemove.add(controlTypes.State.UNAVAILABLE)
			if roleSpecificStateStr == self._lblReadOnly:
				statesToRemove.add(controlTypes.State.READONLY)

			try:
				focusedObj.name = prependText + (originalName if originalName else "")
				focusedObj.states = currentStates - statesToRemove
				return nextHandler()
			except (RuntimeError, COMError, AttributeError) as err:
				logHandler.log.debug(f"StateBeforeLabel: Object mutation failed: {err}")
				return nextHandler()
			finally:
				# Restore original object state regardless of success
				try:
					focusedObj.name = originalName
					focusedObj.states = currentStates
				except (RuntimeError, COMError, AttributeError) as err:
					logHandler.log.debug(f"StateBeforeLabel: Object restoration failed: {err}")

		# Other states: gather text and speak via deferred call to avoid blocking
		try:
			objName = focusedObj.name if focusedObj.name else ""
			shortcut = focusedObj.keyboardShortcut if focusedObj.keyboardShortcut else ""
		except (RuntimeError, COMError, AttributeError) as err:
			logHandler.log.debug(f"StateBeforeLabel: Error reading properties for custom speech: {err}")
			objName = ""
			shortcut = ""

		components = [priorityStateStr, roleSpecificStateStr, objName, shortcut]
		finalText = " ".join([comp for comp in components if comp]).strip()

		if not finalText:
			return nextHandler()

		# The state-first text takes the place of the object's own announcement and nothing is cancelled, so the
		# announcements made just before it (a dialog title, a group name) are still heard.
		wasReported = []

		def reportFocusStateFirst():
			wasReported.append(True)
			speech.speakText(finalText)

		isReplaced = False
		try:
			focusedObj.reportFocus = reportFocusStateFirst
			isReplaced = True
		except (AttributeError, TypeError) as err:
			logHandler.log.debug("StateBeforeLabel: Cannot take over reportFocus: %s", err)

		try:
			nextHandler()
		finally:
			if isReplaced:
				try:
					del focusedObj.reportFocus
				except AttributeError as err:
					logHandler.log.debug("StateBeforeLabel: reportFocus already restored: %s", err)

		# Some objects (for example in browse mode) never call reportFocus; speak for them after NVDA's own speech.
		if not wasReported:
			core.callLater(10, self._speakCustomFocus, finalText, focusedObj)

	def _speakCustomFocus(self, textToSpeak, focusedObj):
		# Focus may have moved on during the short delay; an old announcement must not replace the new one.
		try:
			if api.getFocusObject() != focusedObj:
				return
		except (RuntimeError, COMError, AttributeError) as err:
			logHandler.log.debug("StateBeforeLabel: Cannot compare focus: %s", err)
		speech.cancelSpeech()
		speech.speakText(textToSpeak)