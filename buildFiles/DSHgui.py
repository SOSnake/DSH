#
#   IMPORTS
#

import PySimpleGUI as sg
import os
import os.path
from os import listdir
from os.path import isfile, join

#
#   MAIN STUFF
#

class main():
    def start(self, window, name):
        allSamples = []
        sg.theme('DarkAmber')
        layout = [
            [sg.Text(key='error')],
            [sg.Text("Please enter your folder with samples here:   (Found these samples in your folder: " + str(allSamples) + ")", key='allSamples')],
            [sg.InputText('', size=(30, 1), key='samplesDir'), sg.pin(sg.Button("Confirm", key='dirconf'))],
            [sg.Text("Please enter the name of your background picture here: (For example: background.png)")],
            [sg.InputText('', size=(30, 1), key='bgn')],
            [sg.Text("Toggle effects: (green is on, red is off)")],
            [sg.Button("Volume (Off)", button_color=('white', 'red'), key='vol')],
            [sg.Button("Tone (Off)", button_color=('white', 'red'), key='ton')],
            [sg.Button("Reverb (Off)", button_color=('white', 'red'), key='rev')],
            [sg.Button("Attack (Off)", button_color=('white', 'red'), key='att')],
            [sg.Button("Release (Off)", button_color=('white', 'red'), key='rel')],
            [sg.Button("Submit")]
        ]
        window = sg.Window("DSH", layout, margins=(500, 300))
        downVol = False
        downTon = False
        downRev = False
        downAtt = False
        downRel = False
        
        loc = -1
        
        while True:
            event, values = window.read()

            samplesDir = values['samplesDir']
            try:                                                                                        
                allSamples = [f for f in listdir(samplesDir) if isfile(join(samplesDir, f))]     #Searches the directory for files and copys them to allSamples.
                window['allSamples'].update("Please enter your folder with samples here:   (Found these samples in your folder: " + str(allSamples) + ")")   
                window['error'].update("")
            except:                                                                              #If the directory doesn't exist this fires.
                window['error'].update("Could not find the sampels directory, did you type it in correct?")                                                                 
                    

            if event == "Exit" or event == sg.WIN_CLOSED:
                break

            if event == "Submit":
                
                bgn = values['bgn']
                print(name + ", " + samplesDir)
                print(allSamples)

                self.dspWrite(samplesDir, allSamples, bgn, name, loc, downVol, downTon, downRev, downAtt, downRel)
            if event == 'vol':
                downVol = not downVol
                window.Element('vol').Update(('Volume (Off)','Volume (On)')[downVol], button_color=(('white', ('red', 'green')[downVol])))
            if event == 'ton':
                downTon = not downTon
                window.Element('ton').Update(('Tone (Off)','Tone (On)')[downTon], button_color=(('white', ('red', 'green')[downTon])))
            if event == 'rev':
                downRev = not downRev
                window.Element('rev').Update(('Reverb (Off)','Reverb (On)')[downRev], button_color=(('white', ('red', 'green')[downRev])))
            if event == 'att':
                downAtt = not downAtt
                window.Element('att').Update(('Attack (Off)','Attack (On)')[downAtt], button_color=(('white', ('red', 'green')[downAtt])))
            if event == 'rel':
                downRel = not downRel
                window.Element('rel').Update(('Release (Off)','Release (On)')[downRel], button_color=(('white', ('red', 'green')[downRel])))

        

        name = input("\nEnter the name of your DSPreset here: ")
        samplesDir = input("\nEnter your folder with samples here: ")

        try:                                                                                        
            allSamples = [f for f in listdir(samplesDir) if isfile(join(samplesDir, f))]     #Searches the directory for files and copys them to allSamples.
        except:                                                                              #If the directory doesn't exist this fires.
            input("\nCouldn't find the directory you typed in (" + samplesDir + "), press enter to try again.\n")
            self.start()

        
        print("\nDoes this seem correct? \n")
        print("The name of your preset: " + name)
        print("The files in the directory you've chosen (" + samplesDir + "):")
        print(allSamples)
        samplesDirConf = input("\nAnswer: 'y' (yes) to continue or anything else to retry:\n")

        if samplesDirConf == "y" or samplesDirConf == "yes":
            self.samplesDir(samplesDir, allSamples, name)
        else:
            print("You can try again now.")
            self.start()


    def dspWrite(self, dir, files, bgn, name, loc, vol, ton, rev, att, rel):
        dsp = open(name + ".dspreset", "w+")                                                  #Creates the decent sampler file
        dsp.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<!--Decent Sampler pack created using 'DSH' made by SO_Snake-->\n<DecentSampler pluginVersion=\"1\">\n  <groups name=\"" + name + "\" ampVelTrack=\"1\" volume=\"5.0dB\">\n    <group>")

        for file in files:          #Writes all the files in the pack.
            rfe = file[:-4]
            dsp.write("\n      <sample path=\"" + dir + "/" + file + "\" volume=\"5dB\" rootNote=\"" + rfe + "\" loNote=\"" + rfe + "\" hiNote=\"" + rfe + "\"/>")
        dsp.write("\n    </group>\n  </groups>")
        dsp.writelines("\n  <ui bgImage=\"" + bgn + "\" width=\"812\" height=\"375\" layoutMode=\"relative\" bgColor=\"FF000000\"\n      bgMode=\"top_left\">\n    <tab name=\"main\">\n    ")

        if(vol):
            loc = loc + 1
            self.volume(dsp, loc)
        if(ton):
            loc = loc + 1
            self.tone(dsp, loc)
        if(rev):
            loc = loc + 1
            self.reverb(dsp, loc)
        if(att):
            loc = loc + 1
            self.attack(dsp, loc)
        if(rel):
            loc = loc + 1
            self.release(dsp, loc)

        dsp.write("\n    </tab>\n  </ui>")
        dsp.write("\n  <effects>\n    <effect type=\"lowpass\" frequency=\"22000.0\"/>\n    <effect type=\"reverb\" wetLevel=\"0\" roomSize=\"0.85\" damping=\"O.2\"/>\n  </effects>")
        dsp.write("\n</DecentSampler>")
        dsp.close()                 #Exits the writing

    def volume(self, dsp, loc):
        dsp.write("\n      	<labeled-knob x=\"" + self.loc(loc) + "\" y=\"80\" label=\"volume\" type=\"float\" minValue=\"0.0\" maxValue=\"1\" value=\"1\" textColor=\"FFFFFFFF\"\n      	textSize=\"16\" width=\"120\" height=\"120\" trackForegroundColor=\"E63D99F4\" trackBackgroundColor=\"80808080\">\n        <binding type=\"amp\" level=\"instrument\" position=\"0\" parameter=\"AMP_VOLUME\"/>\n		        </labeled-knob>\n    ")

    def tone(self, dsp, loc):
        dsp.write("\n      	<labeled-knob x=\"" + self.loc(loc) + "\" y=\"80\" label=\"tone\" type=\"float\" minValue=\"60\" maxValue=\"22000\" value=\"22000\" textColor=\"FFFFFFFF\"\n      	textSize=\"16\" width=\"120\" height=\"120\" trackForegroundColor=\"E63D99F4\" trackBackgroundColor=\"80808080\">\n        <binding type=\"effect\" level=\"instrument\" position=\"0\" parameter=\"FX_FILTER_FREQUENCY\"/>\n		        </labeled-knob>\n      ")

    def reverb(self, dsp, loc):
        dsp.write("\n      	<labeled-knob x=\"" + self.loc(loc) + "\" y=\"80\" label=\"reverb\" type=\"float\" minValue=\"0.0\" maxValue=\"1\" value=\"0.0\" textColor=\"FFFFFFFF\"\n		    textSize=\"16\" width=\"120\" height=\"120\" trackForegroundColor=\"E63D99F4\" trackBackgroundColor=\"80808080\">\n        <binding type=\"effect\" level=\"instrument\" position=\"1\" parameter=\"FX_REVERB_WET_LEVEL\"/>\n		        </labeled-knob>\n      ")

    def attack(self, dsp, loc):
        dsp.write("\n      	<labeled-knob x=\"" + self.loc(loc) + "\" y=\"80\" label=\"attack\" type=\"float\" minValue=\"0.0\" maxValue=\"2.0\" value=\"0.000\" textColor=\"FFFFFFFF\"\n		    textSize=\"16\" width=\"120\" height=\"120\" trackForegroundColor=\"E63D99F4\" trackBackgroundColor=\"80808080\">\n        <binding type=\"amp\" level=\"instrument\" position=\"2\" parameter=\"ENV_ATTACK\" />\n		        </labeled-knob>\n		")

    def release(self, dsp, loc):
        dsp.write("\n      	<labeled-knob x=\"" + self.loc(loc) + "\" y=\"80\" label=\"release\" type=\"float\" minValue=\"0.0\" maxValue=\"8.0\" value=\"5.35\" textColor=\"FFFFFFFF\"\n		    textSize=\"16\" width=\"120\" height=\"120\" trackForegroundColor=\"E63D99F4\" trackBackgroundColor=\"80808080\">\n        <binding type=\"amp\" level=\"instrument\" position=\"2\" parameter=\"ENV_RELEASE\" />\n		        </labeled-knob>\n      ")

    def loc(self, loc):
        if loc <= 5:
            locX = loc * 162
            return str(locX)

layout = [
    [sg.Text("Before you start please read this:\nName your files in your samples folder to the according notes.\nFor example: 'C4' as name will be played back on the note 'C4'.\nNOTE: Right now there is support for audio-files with a 3-long extension, .wav and .mp3 work this way.\nThe width and height of the background picture should be around width=\"812\" and height=\"375\"\nClick \"OK\" to continue.\n")],
    [sg.Text("\nPlease enter the name of your DSPreset here: ", key='t1')],
    [sg.InputText('mypreset', size=(30, 1), key='name')],
    [sg.Button("OK")]
]

window = sg.Window("DSH", layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    if event == "OK":
        name = values['name']
        window.close()
        main().start(window, name)

window.close()