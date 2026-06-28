<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>StateBeforeLabel NVDA Add-on</title>
<style>
body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    padding: 20px;
    background-color: #f4f4f4;
}
.container {
    max-width: 800px;
    margin: auto;
    background: #fff;
    padding: 20px 40px;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
h1, h2, h3 {
    text-align: center;
}
b {
    font-weight: bold;
}
.section {
    margin-bottom: 30px;
}
.nvda-logo {
    display: block;
    margin: 0 auto 20px;
    width: 120px;
    height: auto;
}
.hotkey {
    background: #f8f9fa;
    border-left: 4px solid #3498db;
    padding: 15px;
    margin: 15px 0;
    border-radius: 0 4px 4px 0;
}
.tap-explanation {
    background: #e8f4fc;
    padding: 15px;
    border-radius: 5px;
    margin: 10px 0;
}
.feature-item {
    margin: 15px 0;
    padding-left: 10px;
}
.note {
    background: #fff3cd;
    border-left: 4px solid #ffc107;
    padding: 12px;
    margin: 15px 0;
    border-radius: 0 4px 4px 0;
}
</style>
</head>
<body>

<div class="container">

<div class="section">
    <img src="https://www.nvaccess.org/files/nvda/documentation/userGuide/images/nvda.ico" alt="NVDA Logo" class="nvda-logo">
    <h1>StateBeforeLabel</h1>


<br>

<p style="text-align: center;">Get the status upfront. Skip the ones that don't matter</div>

<br>

<div class="section">
    <p style="text-align: center;"><b>author:</b> chai chaimee</p>
    <p style="text-align: center;"><b>url:</b> https://github.com/chaichaimee/StateBeforeLabel</p>
</div>

<hr>

<div class="section">
           <br>    

<h2>Description</h2>
    <p>
        Have you ever tabbed through a long form, waited to hear the full label of a control, only to find out at the very end that it was disabled or already checked? That split-second delay adds up, forcing your brain to re-evaluate every control after hearing its label rather than before.
    </p>
    <p>
        State Before Label flips the announcement order. It speaks the most important state information first, then the name, so you can decide instantly whether to stop and interact or keep moving. No more listening to a lengthy button label only to hear "Unavailable" tacked on at the end.
    </p>
    <p>
        Every state category comes with its own on/off toggle in NVDA's settings, so you control exactly which states get priority treatment.
    </p>
    <br>
    <h2>Features</h2>

    <h3>Checkboxes, Radio Buttons, and Check Menu Items</h3>
    <p>
        <strong>Pain point:</strong> When a checkbox label is long or descriptive, NVDA traditionally announces the name first, then the checked state. By the time you hear "checked", you've already invested attention in understanding what the control is.
    </p>
    <p><strong>Before:</strong> "I agree to the terms and conditions and privacy policy of this website, including all subsections related to data collection. Checked"</p>
    <p><strong>After:</strong> "Checked. I agree to the terms and conditions and privacy policy of this website, including all subsections related to data collection."</p>
    <p>
        When unchecked, the add-on speaks the negative state instead: "Not checked" before the label. NVDA's default role announcement such as "checkbox" is naturally suppressed so the state stands out cleanly without redundancy.
    </p>
    <p>
        <strong>Real-world example — NVDA Voice Settings:</strong> This is a panel you likely visit often. Here is how the checkboxes appear with State Before Label active:
    </p>
    <p><strong>Before:</strong></p>
    <ul>
        <li>Rate boost. Check box. Not checked. Alt+t</li>
        <li>Use modern audio output system (WASAPI). Check box. Checked</li>
        <li>Automatic language switching (when supported). Check box. Not checked</li>
        <li>Automatic dialect switching (when supported). Check box. Not checked</li>
        <li>Report language changes while reading. Check box. Not checked. Alt+g</li>
        <li>Trust voice's language when processing characters and symbols. Check box. Checked</li>
        <li>Unicode Consortium data (including emoji). Check box. Checked</li>
        <li>Delayed descriptions for characters on cursor movement. Check box. Not checked. Alt+d</li>
        <li>Say cap before capitals. Check box. Not checked. Alt+c</li>
        <li>Beep for capitals. Check box. Not checked. Alt+b</li>
        <li>Use spelling functionality if supported. Check box. Not checked. Alt+s</li>
    </ul>
    <p><strong>After — with State Before Label:</strong></p>
    <ul>
        <li>Not checked. Rate boost. Alt+t</li>
        <li>Checked. Use modern audio output system (WASAPI)</li>
        <li>Not checked. Automatic language switching (when supported)</li>
        <li>Not checked. Automatic dialect switching (when supported)</li>
        <li>Not checked. Report language changes while reading. Alt+g</li>
        <li>Checked. Trust voice's language when processing characters and symbols</li>
        <li>Checked. Unicode Consortium data (including emoji)</li>
        <li>Not checked. Delayed descriptions for characters on cursor movement. Alt+d</li>
        <li>Not checked. Say cap before capitals. Alt+c</li>
        <li>Not checked. Beep for capitals. Alt+b</li>
        <li>Not checked. Use spelling functionality if supported. Alt+s</li>
    </ul>
    <p>
        Notice how the word "Check box" is gone from every line. You hear only the state followed by the label and shortcut. This transforms a cluttered settings page into a clean, instantly scannable list where your brain processes the on/off status first, then the feature name. Tabbing through 11 checkboxes becomes significantly faster when every single one follows the same crisp pattern.
    </p>
    <br>

    <h3>Toggle Buttons</h3>
    <p>
        <strong>Pain point:</strong> Toggle buttons like Bold, Italic, or Mute visually indicate their state through highlighting, but screen reader users must hear the label first before learning whether the feature is on or off.
    </p>
    <p><strong>Before:</strong> "Bold. Toggle button. Pressed"</p>
    <p><strong>After:</strong> "Pressed. Bold"</p>
    <p>
        When the toggle is off, "Not pressed" is spoken before the button name. The role announcement is similarly streamlined so the focus remains on state then identity.
    </p>
    <p>
        <strong>Real-world example — Windows Settings &gt; Accounts &gt; Sign-in options:</strong> This page contains several toggle buttons that control how Windows behaves when you restart or sign back in. Here is how one of them reads:
    </p>
    <p><strong>Before:</strong> "Automatically save my restartable apps and restart them when I sign back in. Toggle button. Not pressed"</p>
    <p><strong>After:</strong> "Not pressed. Automatically save my restartable apps and restart them when I sign back in"</p>
    <p>
        The label is long, but with State Before Label you hear the status first. If the toggle is already on, you hear "Pressed" and move on. If it is off and you want to turn it on, you know immediately and press Space. No waiting through a long sentence to get to the decision point.
    </p>
    <br>

    <h3>TreeView Items (Expanded/Collapsed)</h3>
    <p>
        <strong>Pain point:</strong> Navigating a tree structure in file explorers or settings panels requires knowing whether a branch is open or closed. Hearing the folder name first forces you to remember where you are, then process the expand state after.
    </p>
    <p><strong>Before:</strong> "Documents. Expanded. Level 2"</p>
    <p><strong>After:</strong> "Expanded. Documents"</p>
    <p>
        Collapsed branches announce "Collapsed" first, giving you an immediate cue to press Right Arrow if you want to explore deeper, without waiting through the full name.
    </p>
    <br>

    <h3>Buttons with Expanded/Collapsed State</h3>
    <p>
        <strong>Pain point:</strong> Modern websites and apps often use standard buttons as dropdown triggers or accordion headers with <code>aria-expanded</code>. These buttons look like regular buttons to NVDA, but their expand state is critical for understanding whether a menu or content section is currently open.
    </p>
    <p><strong>Before:</strong> "Settings. Button" (no indication the dropdown is open)</p>
    <p><strong>After:</strong> "Expanded. Settings"</p>
    <p>
        This feature is opt-in via settings. When enabled, any Button role carrying Expanded or Collapsed state will announce the state first, giving you the same tree-view-like awareness for menus, FAQ accordions, and expandable sections.
    </p>
    <br>

    <h3>Selected State for Tabs and List Items</h3>
    <p>
        <strong>Pain point:</strong> When cycling through tabs in a dialog or browsing a long list of files, knowing which item is currently selected requires hearing the name first, then "Selected". In a list of dozens of items, this adds cognitive load.
    </p>
    <p><strong>Before:</strong> "General. Tab. Selected"</p>
    <p><strong>After:</strong> "Selected. General"</p>
    <p>
        This setting is off by default to keep the experience minimal. Turn it on when you work frequently with tabbed interfaces or long selectable lists where current-selection awareness matters.
    </p>
    <br>

    <h3>Unavailable State (Global)</h3>
    <p>
        <strong>Pain point:</strong> Disabled controls appear everywhere: grayed-out buttons, locked edit fields, unavailable menu items. Hearing a long name only to discover the control is unusable wastes keystrokes and mental energy.
    </p>
    <p><strong>Before:</strong> "Submit application. Button. Unavailable"</p>
    <p><strong>After:</strong> "Unavailable. Submit application"</p>
    <p>
        This check runs globally for every control type. Any object carrying the Unavailable state will announce it first, allowing you to skip past it immediately. The control's role and other states are handled cleanly so nothing gets announced twice.
    </p>
    <br>

    <h3>Read-only State for Edit Boxes</h3>
    <p>
        <strong>Pain point:</strong> You land on an edit field ready to type, only to hear "Read-only" at the end of the announcement. This breaks workflow and creates confusion about whether the field is truly editable.
    </p>
    <p><strong>Before:</strong> "Email address. Edit. Read-only"</p>
    <p><strong>After:</strong> "Read-only. Email address"</p>
    <p>
        The add-on prepends "Read-only" before the field name while preserving all standard NVDA behavior: text selection announcement, cursor position, and value reading all work exactly as expected.
    </p>
    <br>

    <h2>Usage</h2>
    <ol>
        <li>Open NVDA Menu &gt; Preferences &gt; Settings &gt; State Before Label.</li>
        <li>Check or uncheck each state category to match your preferences.</li>
        <li>Press OK. Changes take effect immediately without restarting NVDA.</li>
    </ol>
    <p>
        All features work automatically when you move focus with Tab, arrow keys, or mouse navigation. No extra keystrokes to memorize.
    </p>
</main>

<br><br>
<h2>Support Me</h2>
    <p>If this tool has made your life easier, consider fueling the next update with a small donation.</p>

<br>

<p>
  <a href="https://buy.stripe.com/dRm9AU1xQ3Ds22N6VK1VK01">
    <img src="https://img.shields.io/badge/Donate-Support%20Me-blue?style=for-the-badge&logo=stripe" alt="Support me">
  </a>
</p>
<br>


<p>Your support means the world. Let's build something great together</p>

<br>

  <div class="footer-note">
<p>&copy; 2026 Chai Chaimee NVDA Add-on Released under GN
</p>
</div>
</div>
</body>
</html>