import dbus, dbus.mainloop.glib, sys
from gi.repository import GLib

from datetime import datetime
import time
import tkinter as tk
from tkinter.constants import CENTER, LEFT, RIGHT

bgColor = "#111"
bgSecondaryColor = "#222"
musicBgColor = "#443046"
musicBgSecondaryColor = "#443046"
phoneBgColor = "#bd8696"
phoneBgSecondaryColor = "#C06C84"
radioBgColor = "#f7c6b2"
radioBgSecondaryColor = "#F8B195"
darkFgColor = "#333"
lightFgColor = "#fff"
brightnessBg = "#E4EDF2"


def onPropertyChanged(interface, changed, invalidated):
    if interface != 'org.bluez.MediaPlayer1':
        return
    for prop, value in changed.items():
        if prop == 'Status':
            print('Playback Status: {}'.format(value))
        elif prop == 'Track':
            print('Music Info:')
            for key in ('Title', 'Artist', 'Album'):
                print('   {}: {}'.format(key, value.get(key, '')))


def playbackControl(command):
    if command.startswith('play'):
        player_iface.Play()
    elif command.startswith('pause'):
        player_iface.Pause()
    elif command.startswith('next'):
        player_iface.Next()
    elif command.startswith('prev'):
        player_iface.Previous()
    elif command.startswith('vol'):
        vol = int(str.split()[1])
        if vol not in range(0, 128):
            print('Possible Values: 0-127')
            return
        transport_prop_iface.Set(
                'org.bluez.MediaTransport1',
                'Volume',
                dbus.UInt16(vol))


# Init Bluetooth Control
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = dbus.SystemBus()
obj = bus.get_object('org.bluez', "/")
mgr = dbus.Interface(obj, 'org.freedesktop.DBus.ObjectManager')
player_iface = None
transport_prop_iface = None
for path, ifaces in mgr.GetManagedObjects().items():
    if 'org.bluez.MediaPlayer1' in ifaces:
        player_iface = dbus.Interface(
                bus.get_object('org.bluez', path),
                'org.bluez.MediaPlayer1')
    elif 'org.bluez.MediaTransport1' in ifaces:
        transport_prop_iface = dbus.Interface(
                bus.get_object('org.bluez', path),
                'org.freedesktop.DBus.Properties')
if not player_iface:
    sys.exit('Error: Media Player not found.')
if not transport_prop_iface:
    sys.exit('Error: DBus.Properties iface not found.')

print("BT Init done")

# bus.add_signal_receiver(
#         onPropertyChanged,
#         bus_name='org.bluez',
#         signal_name='PropertiesChanged',
#         dbus_interface='org.freedesktop.DBus.Properties')
# GLib.MainLoop().run()


root = tk.Tk()
root.title("Car Radio GUI")
root.geometry("800x480")
root.overrideredirect(1) # remove window border

# UI Functions

def updateTime():
    timeString = time.strftime("%H:%M")
    clockLabel.config(text=timeString)
    clockLabel.after(1000, updateTime)


exitCounter = 0
lastExitCounterPress = time.monotonic()
# User has to press 3 times in 3 seconds to exit the GUI
def exitGUI():
    global exitCounter
    global lastExitCounterPress
    if (time.monotonic() - lastExitCounterPress > 3):
        exitCounter = 0
        lastExitCounterPress = time.monotonic()
        exitCounter += 1
        if exitCounter >= 3:
            exit()

def musicPlay():
    playbackControl("play")
    pauseButton.lift()

def musicPause():
    playbackControl("pause")
    playButton.lift()


canvas = tk.Canvas(root, width=800, height=480, bg="black")
canvas.pack()

## Top Bar
topBarFrame = tk.Frame(root, bg=bgSecondaryColor)
topBarFrame.place(relwidth=1, relheight=0.1)

### SCREENS
## Home Screen
homeFrame = tk.Frame(root, bg=bgColor)
homeFrame.place(relwidth=1, relheight=0.9, rely=0.1)

## BT Music Screen
musicFrame = tk.Frame(root, bg=musicBgColor)
musicFrame.place(relwidth=1, relheight=0.9, rely=0.1)

## BT Phone Screen
phoneFrame = tk.Frame(root, bg=phoneBgColor)
phoneFrame.place(relwidth=1, relheight=0.9, rely=0.1)

## Radio Screen
radioFrame = tk.Frame(root, bg=radioBgColor)
radioFrame.place(relwidth=1, relheight=0.9, rely=0.1)

## Settings Screen
settingsFrame = tk.Frame(root, bg=bgColor)
settingsFrame.place(relwidth=1, relheight=0.9, rely=0.1)

# Brightness Screen
brightnessFrame = tk.Frame(root, bg=brightnessBg)
brightnessFrame.place(relwidth=1, relheight=0.9, rely=0.1)


### CONTENTS
## Top Bar Content
homeButtonImage = tk.PhotoImage(file=r"img/home-outline.png")
homeButton = tk.Button(topBarFrame, image=homeButtonImage, bg=bgSecondaryColor, activebackground=bgSecondaryColor, border=0, borderwidth=0, highlightthickness=0, command=homeFrame.lift)
homeButton.pack(side=LEFT, padx=12)

screenoffButtonImage = tk.PhotoImage(file=r"img/brightness.png")
screenoffButton = tk.Button(topBarFrame, image=screenoffButtonImage, bg=bgSecondaryColor, activebackground=bgSecondaryColor, border=0, borderwidth=0, highlightthickness=0)
screenoffButton.pack(side=RIGHT, padx=12)

clockLabel = tk.Label(topBarFrame, bg=bgSecondaryColor, fg="white", font=("Calibri", "20"))
clockLabel.place(relx=0.5, rely=0.5, anchor="c")

## Home Screen Content
homeHeading = tk.Label(homeFrame, text="Willkommen", bg=bgColor, fg="white", font=("Calibri", "28"), pady=8)
homeHeading.grid(row=1, column=1, columnspan=2)

navigateMusicButtonImage = tk.PhotoImage(file=r"img/musicButton.png")
navigateMusicButton = tk.Button(homeFrame, image=navigateMusicButtonImage, text="BT Musik", fg="white", bg="#F67280", command=musicFrame.lift, border=0, borderwidth=0, highlightthickness=0, width=372, height=132, font=("Calibri", "24"))
navigateMusicButton.grid(row=2, column=1, padx=8, pady=8, sticky="NESW")

navigatePhoneButtonImage = tk.PhotoImage(file=r"img/phoneButton.png")
navigatePhoneButton = tk.Button(homeFrame, image=navigatePhoneButtonImage, text="BT Telefon", fg="white", bg="#C06C84", command=phoneFrame.lift, border=0, borderwidth=0, highlightthickness=0, width=372, height=132, font=("Calibri", "24"))
navigatePhoneButton.grid(row=2, column=2, padx=8, pady=8, sticky="NESW")

navigateRadioButtonImage = tk.PhotoImage(file=r"img/radioButton.png")
navigateRadioButton = tk.Button(homeFrame, image=navigateRadioButtonImage, text="Radio", fg="white", bg="#F8B195", command=radioFrame.lift, border=0, borderwidth=0, highlightthickness=0, width=372, height=132, font=("Calibri", "24"))
navigateRadioButton.grid(row=3, column=1, padx=8, pady=8, sticky="NESW")

navigateSettingsButtonImage = tk.PhotoImage(file=r"img/settingsButton.png")
navigateSettingsButton = tk.Button(homeFrame, image=navigateSettingsButtonImage, text="Einstellungen", fg="white", bg="#6C5B7B", command=settingsFrame.lift, border=0, borderwidth=0, highlightthickness=0, width=372, height=132, font=("Calibri", "24"))
navigateSettingsButton.grid(row=3, column=2, padx=8, pady=8, sticky="NESW")

# This is to center the grid
homeFrame.grid_rowconfigure(0, weight=1)
homeFrame.grid_rowconfigure(4, weight=1)
homeFrame.grid_columnconfigure(0, weight=1)
homeFrame.grid_columnconfigure(3, weight=1)

## Music Screen Content
musicHeadingImage = tk.PhotoImage(file=r"img/music-note-bluetooth-small.png")
musicHeading = tk.Label(musicFrame, image=musicHeadingImage, bg=musicBgColor)
musicHeading.pack(pady=20)

musicTitle = tk.Label(musicFrame, text="Back To You", font=("Calibri", "36"), bg=musicBgColor, fg=lightFgColor)
musicTitle.pack()

musicArtist = tk.Label(musicFrame, text="Our Last Night", font=("Calibri", "18"), bg=musicBgColor, fg=lightFgColor)
musicArtist.pack()

musicControlsFrame = tk.Frame(musicFrame, bg=musicBgSecondaryColor)
musicControlsFrame.place(x=0, rely=0.6, relwidth=1, relheight=0.4)

prevButtonImage = tk.PhotoImage(file=r"img/skip-backward.png")
prevButton = tk.Button(musicControlsFrame, image=prevButtonImage, bg=musicBgSecondaryColor, activebackground=musicBgSecondaryColor, fg=lightFgColor, border=0, borderwidth=0, highlightthickness=0)
prevButton.grid(row=1, column=1, padx=28)

playButtonImage = tk.PhotoImage(file=r"img/play-circle.png")
playButton = tk.Button(musicControlsFrame, image=playButtonImage, bg=musicBgSecondaryColor, activebackground=musicBgSecondaryColor, fg=lightFgColor, border=0, borderwidth=0, highlightthickness=0, command=musicPlay)
playButton.grid(row=1, column=2, padx=28)

pauseButtonImage = tk.PhotoImage(file=r"img/pause-circle.png")
pauseButton = tk.Button(musicControlsFrame, image=pauseButtonImage, bg=musicBgSecondaryColor, activebackground=musicBgSecondaryColor, fg=lightFgColor, border=0, borderwidth=0, highlightthickness=0, command=musicPause)
pauseButton.grid(row=1, column=2, padx=28)

nextButtonImage = tk.PhotoImage(file=r"img/skip-forward.png")
nextButton = tk.Button(musicControlsFrame, image=nextButtonImage, bg=musicBgSecondaryColor, activebackground=musicBgSecondaryColor, fg=lightFgColor, border=0, borderwidth=0, highlightthickness=0)
nextButton.grid(row=1, column=3, padx=28)

# This is to center the grid
musicControlsFrame.grid_rowconfigure(0, weight=1)
musicControlsFrame.grid_rowconfigure(2, weight=1)
musicControlsFrame.grid_columnconfigure(0, weight=1)
musicControlsFrame.grid_columnconfigure(4, weight=1)

## Phone Screen Content

## Radio Screen Content
radioHeadingImage = tk.PhotoImage(file=r"img/radio-small.png")
radioHeading = tk.Label(radioFrame, image=radioHeadingImage, bg=radioBgColor)
radioHeading.pack(pady=20)

radioFrequency = tk.Label(radioFrame, text="104.7", font=("Calibri", "48"), bg=radioBgColor, fg=darkFgColor)
radioFrequency.pack()

radioStation = tk.Label(radioFrame, text="Hitradio FFH", font=("Calibri", "28"), bg=radioBgColor, fg=darkFgColor)
radioStation.pack()

radioText = tk.Label(radioFrame, text="Ed Sheeran - Shape Of You", font=("Calibri", "14"), bg=radioBgColor, fg=darkFgColor)
radioText.pack()

radioControlsFrame = tk.Frame(radioFrame, bg=radioBgSecondaryColor)
radioControlsFrame.place(x=0, rely=0.6, relwidth=1, relheight=0.4)

radioPresetButtons = []
radioPresetImages = []
for p in range(6):
    radioPresetImages.append(tk.PhotoImage(file=r"img/numeric-"+str(p+1)+".png"))
    radioPresetButtons.append(tk.Button(radioControlsFrame, bg=radioBgSecondaryColor, fg=darkFgColor, border=0, borderwidth=0, highlightthickness=0, text=str(p+1), font=("Calibri", "16"), image=radioPresetImages[p], padx=10))
    radioPresetButtons[p].grid(row=1, column=p+1, padx=12)


freqDownButtonImage = tk.PhotoImage(file=r"img/skip-previous.png")
freqDownButton = tk.Button(radioControlsFrame, image=freqDownButtonImage, bg=radioBgSecondaryColor, fg=darkFgColor, border=0, borderwidth=0, highlightthickness=0)
freqDownButton.grid(row=2, column=1, columnspan=2, pady=20)

scanButtonImage = tk.PhotoImage(file=r"img/magnify-scan.png")
scanButton = tk.Button(radioControlsFrame, image=scanButtonImage, bg=radioBgSecondaryColor, fg=darkFgColor, border=0, borderwidth=0, highlightthickness=0)
scanButton.grid(row=2, column=3, columnspan=2, pady=20)

freqUpButtonImage = tk.PhotoImage(file=r"img/skip-next.png")
freqUpButton = tk.Button(radioControlsFrame, image=freqUpButtonImage, bg=radioBgSecondaryColor, fg=darkFgColor, border=0, borderwidth=0, highlightthickness=0)
freqUpButton.grid(row=2, column=5, columnspan=2, pady=20)

# This is to center the grid
radioControlsFrame.grid_rowconfigure(0, weight=1)
radioControlsFrame.grid_rowconfigure(3, weight=1)
radioControlsFrame.grid_columnconfigure(0, weight=1)
radioControlsFrame.grid_columnconfigure(7, weight=1)

## Settings Screen Content
settingsHeadingImage = tk.PhotoImage(file=r"img/cogs-small.png")
settingsHeading = tk.Label(settingsFrame, image=settingsHeadingImage, bg=bgColor)
settingsHeading.pack(pady=20)

settingsButton1 = tk.Button(settingsFrame, bg=bgColor, fg="white", border=0, borderwidth=0, highlightthickness=0, text="Bildschirmhelligkeit", font=("Calibri", "16"), command=brightnessFrame.lift)
settingsButton1.place(x=16, y=0*(56)+80, width=768, height=56)

settingsButton2 = tk.Button(settingsFrame, bg=bgColor, fg="#888", border=0, borderwidth=0, highlightthickness=0, text="Python GUI verlassen", font=("Calibri", "16"), command=exitGUI)
settingsButton2.place(x=16, y=1*(56)+80, width=768, height=56)

# Brightness Screen Content
brightnessHeading = tk.Label(brightnessFrame, text="Bildschirmhelligkeit", bg=brightnessBg, fg=darkFgColor, font=("Calibri", "28"), pady=16)
brightnessHeading.pack()

brightnessDownImage = tk.PhotoImage(file=r"img/brightness-down.png")
brightnessDown = tk.Button(brightnessFrame, text="-", font=("Calibri", "16"), image=brightnessDownImage, bg=brightnessBg, border=0, borderwidth=0, highlightthickness=0)
brightnessDown.pack()

brightnessUpImage = tk.PhotoImage(file=r"img/brightness-up.png")
brightnessUp = tk.Button(brightnessFrame, text="-", font=("Calibri", "16"), image=brightnessUpImage, bg=brightnessBg, border=0, borderwidth=0, highlightthickness=0)
brightnessUp.pack()

###

homeFrame.lift()

updateTime()

root.mainloop()
