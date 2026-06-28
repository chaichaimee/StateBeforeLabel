![NVDA Logo](https://www.nvaccess.org/files/nvda/documentation/userGuide/images/nvda.ico)

# StateBeforeLabel

Get the status upfront. Skip the ones that don't matter.

**author:** chai chaimee  
**url:** https://github.com/chaichaimee/StateBeforeLabel

---

## Description

Have you ever tabbed through a long form, waited to hear the full label of a control, only to find out at the very end that it was disabled or already checked? That split-second delay adds up, forcing your brain to re-evaluate every control after hearing its label rather than before.

State Before Label flips the announcement order. It speaks the most important state information first, then the name, so you can decide instantly whether to stop and interact or keep moving. No more listening to a lengthy button label only to hear "Unavailable" tacked on at the end.

Every state category comes with its own on/off toggle in NVDA's settings, so you control exactly which states get priority treatment.

## Features

### Checkboxes, Radio Buttons, and Check Menu Items

**Pain point:** When a checkbox label is long or descriptive, NVDA traditionally announces the name first, then the checked state. By the time you hear "checked", you've already invested attention in understanding what the control is.

**Before:** "I agree to the terms and conditions and privacy policy of this website, including all subsections related to data collection. Checked"

**After:** "Checked. I agree to the terms and conditions and privacy policy of this website, including all subsections related to data collection."

When unchecked, the add-on speaks the negative state instead: "Not checked" before the label. NVDA's default role announcement such as "checkbox" is naturally suppressed so the state stands out cleanly without redundancy.

**Real-world example — NVDA Voice Settings:** This is a panel you likely visit often. Here is how the checkboxes appear with State Before Label active:

**Before:**

- Rate boost. Check box. Not checked. Alt+t
- Use modern audio output system (WASAPI). Check box. Checked
- Automatic language switching (when supported). Check box. Not checked
- Automatic dialect switching (when supported). Check box. Not checked
- Report language changes while reading. Check box. Not checked. Alt+g
- Trust voice's language when processing characters and symbols. Check box. Checked
- Unicode Consortium data (including emoji). Check box. Checked
- Delayed descriptions for characters on cursor movement. Check box. Not checked. Alt+d
- Say cap before capitals. Check box. Not checked. Alt+c
- Beep for capitals. Check box. Not checked. Alt+b
- Use spelling functionality if supported. Check box. Not checked. Alt+s

**After — with State Before Label:**

- Not checked. Rate boost. Alt+t
- Checked. Use modern audio output system (WASAPI)
- Not checked. Automatic language switching (when supported)
- Not checked. Automatic dialect switching (when supported)
- Not checked. Report language changes while reading. Alt+g
- Checked. Trust voice's language when processing characters and symbols
- Checked. Unicode Consortium data (including emoji)
- Not checked. Delayed descriptions for characters on cursor movement. Alt+d
- Not checked. Say cap before capitals. Alt+c
- Not checked. Beep for capitals. Alt+b
- Not checked. Use spelling functionality if supported. Alt+s

Notice how the word "Check box" is gone from every line. You hear only the state followed by the label and shortcut. This transforms a cluttered settings page into a clean, instantly scannable list where your brain processes the on/off status first, then the feature name. Tabbing through 11 checkboxes becomes significantly faster when every single one follows the same crisp pattern.

### Toggle Buttons

**Pain point:** Toggle buttons like Bold, Italic, or Mute visually indicate their state through highlighting, but screen reader users must hear the label first before learning whether the feature is on or off.

**Before:** "Bold. Toggle button. Pressed"

**After:** "Pressed. Bold"

When the toggle is off, "Not pressed" is spoken before the button name. The role announcement is similarly streamlined so the focus remains on state then identity.

**Real-world example — Windows Settings > Accounts > Sign-in options:** This page contains several toggle buttons that control how Windows behaves when you restart or sign back in. Here is how one of them reads:

**Before:** "Automatically save my restartable apps and restart them when I sign back in. Toggle button. Not pressed"

**After:** "Not pressed. Automatically save my restartable apps and restart them when I sign back in"

The label is long, but with State Before Label you hear the status first. If the toggle is already on, you hear "Pressed" and move on. If it is off and you want to turn it on, you know immediately and press Space. No waiting through a long sentence to get to the decision point.

### TreeView Items (Expanded/Collapsed)

**Pain point:** Navigating a tree structure in file explorers or settings panels requires knowing whether a branch is open or closed. Hearing the folder name first forces you to remember where you are, then process the expand state after.

**Before:** "Documents. Expanded. Level 2"

**After:** "Expanded. Documents"

Collapsed branches announce "Collapsed" first, giving you an immediate cue to press Right Arrow if you want to explore deeper, without waiting through the full name.

### Buttons with Expanded/Collapsed State

**Pain point:** Modern websites and apps often use standard buttons as dropdown triggers or accordion headers with `aria-expanded`. These buttons look like regular buttons to NVDA, but their expand state is critical for understanding whether a menu or content section is currently open.

**Before:** "Settings. Button" (no indication the dropdown is open)

**After:** "Expanded. Settings"

This feature is opt-in via settings. When enabled, any Button role carrying Expanded or Collapsed state will announce the state first, giving you the same tree-view-like awareness for menus, FAQ accordions, and expandable sections.

### Selected State for Tabs and List Items

**Pain point:** When cycling through tabs in a dialog or browsing a long list of files, knowing which item is currently selected requires hearing the name first, then "Selected". In a list of dozens of items, this adds cognitive load.

**Before:** "General. Tab. Selected"

**After:** "Selected. General"

This setting is off by default to keep the experience minimal. Turn it on when you work frequently with tabbed interfaces or long selectable lists where current-selection awareness matters.

### Unavailable State (Global)

**Pain point:** Disabled controls appear everywhere: grayed-out buttons, locked edit fields, unavailable menu items. Hearing a long name only to discover the control is unusable wastes keystrokes and mental energy.

**Before:** "Submit application. Button. Unavailable"

**After:** "Unavailable. Submit application"

This check runs globally for every control type. Any object carrying the Unavailable state will announce it first, allowing you to skip past it immediately. The control's role and other states are handled cleanly so nothing gets announced twice.

### Read-only State for Edit Boxes

**Pain point:** You land on an edit field ready to type, only to hear "Read-only" at the end of the announcement. This breaks workflow and creates confusion about whether the field is truly editable.

**Before:** "Email address. Edit. Read-only"

**After:** "Read-only. Email address"

The add-on prepends "Read-only" before the field name while preserving all standard NVDA behavior: text selection announcement, cursor position, and value reading all work exactly as expected.

## Usage

1. Open NVDA Menu > Preferences > Settings > State Before Label.
2. Check or uncheck each state category to match your preferences.
3. Press OK. Changes take effect immediately without restarting NVDA.

All features work automatically when you move focus with Tab, arrow keys, or mouse navigation. No extra keystrokes to memorize.

## Support Me

If this tool has made your life easier, consider fueling the next update with a small donation.

[![Support me](https://img.shields.io/badge/Donate-Support%20Me-blue?style=for-the-badge&logo=stripe)](https://buy.stripe.com/dRm9AU1xQ3Ds22N6VK1VK01)

Your support means the world. Let's build something great together.

---

© 2026 Chai Chaimee NVDA Add-on Released under GNU General Public License.