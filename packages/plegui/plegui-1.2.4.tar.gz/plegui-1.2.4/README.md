

        SimpleGUI Does not work if it is in python's program folder!!
                Please put SimpleGUI's Folder within your project for it to work!!


                If you find any bugs please contact the 
                owner in their discord: itarqosv5 
                And thank you for using our software!


How to use:

# To load a Message Box:
mbox.create("Content of the message box")


# To load a GUI (Graphical User Interface)
GUI.Create("Title Of GUI")

# To create a label in your GUI
GUI.label.create("Title of GUI you wanna put the label in", "Content of Label")




# If you have any suggestions or bug reports to inform us, please contact the owner in their discord:
Discord: itarqosv5
Whatsapp: +212 672393739
Telegram: None

# Example usage:
GUI.create("Test Window")
GUI.label.create("Test Window", "This is a label")
GUI.set_title("Test Window", "New Title")
GUI.set_cmd_hidden(True)  # Hide command window
GUI.set_cmd_hidden(False)  # Show command window
GUI.add_button("Test Window", "Click Me", lambda: print("Button Clicked"))
entry = GUI.add_entry("Test Window")
dropdown = GUI.add_dropdown("Test Window", ["Option 1", "Option 2", "Option 3"])
GUI.close_window("Test Window")
plegui.process_add(True)  # Attempt to rename process to "main.py"
plegui.process_add(False)  # Restore original process name
messagebox.form("This is a message box")
