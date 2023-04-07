#
#   IMPORTS
#

import os
from os import listdir
from os.path import isfile, join

#
#   MAIN STUFF
#

class main():
    def start(self):
        os.system('cls')
        name = input("\nEnter the name of your DSPreset here: ")
        samplesDir = input("\nEnter your folder with samples here: ")

        try:                                                                                        
            allSamples = [f for f in listdir(samplesDir) if isfile(join(samplesDir, f))]     #Searches the directory for files and copys them to allSamples.
        except:                                                                              #If the directory doesn't exist this fires.
            input("\nCouldn't find the directory you typed in (" + samplesDir + "), press enter to try again.\n")
            self.start()

        os.system('cls')
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

    def samplesDir(self, dir, files, name):
        os.system('cls')
        print("You have continued in the local directory: '/" + dir + "/'\nWith the name: " + name + "\n")

        

        dsp = open(name + ".dspreset", "w+")                                                  #Creates the decent sampler file
        dsp.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<!--Decent Sampler pack created using 'DSH' made by SO_Snake-->\n<DecentSampler pluginVersion=\"1\">\n  <groups name=\"" + name + "\" ampVelTrack=\"1\" volume=\"5.0dB\">\n    <group>")

        for file in files:          #Writes all the files in the pack.
            rfe = file[:-4]
            dsp.write("\n      <sample path=\"" + dir + "/" + file + "\" volume=\"5dB\" rootNote=\"" + rfe + "\" loNote=\"" + rfe + "\" hiNote=\"" + rfe + "\"/>")
        dsp.write("\n    </group>\n  </groups>")
        bgn = input("What is your background-image called? (For example: bg.png)\n")
        dsp.writelines("\n  <ui bgImage=\"" + bgn + "\" width=\"812\" height=\"375\" layoutMode=\"relative\" bgColor=\"FF000000\"\n      bgMode=\"top_left\">\n    <tab name=\"main\">\n    ")

        loc = -1

        inp = input("Do you want a volume knob? [y/n]\n")
        if inp == "y":
            loc = loc + 1
            self.volume(dsp, loc)

        inp = input("Do you want a tone knob? [y/n]\n")
        if inp == "y":
            loc = loc + 1
            self.tone(dsp, loc)

        inp = input("Do you want a reverb knob? [y/n]\n")
        if inp == "y":
            loc = loc + 1
            self.reverb(dsp, loc)

        inp = input("Do you want an attack knob? [y/n]\n")
        if inp == "y":   
            loc = loc + 1
            self.attack(dsp, loc)
            
        inp = input("Do you want a release knob? [y/n]\n")
        if inp == "y":   
            loc = loc + 1
            self.release(dsp, loc)
        
        dsp.write("\n    </tab>\n  </ui>")
        dsp.write("\n  <effects>\n    <effect type=\"lowpass\" frequency=\"22000.0\"/>\n    <effect type=\"reverb\" wetLevel=\"0\" roomSize=\"0.85\" damping=\"O.2\"/>\n  </effects>")
        dsp.write("\n</DecentSampler>")
        dsp.close()                 #Exits the writing
        input("\nDone writing to file! You can close this tab now.")

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

input("Before you start please read this:\nName your files in your samples folder to the according notes.\nFor example: 'C4' as name will be played back on the note 'C4'.\nNOTE: Right now there is support for audio-files with a 3-long extension, .wav and .mp3 work this way.\nThe width and height of the background picture should be around width=\"812\" and height=\"375\"\nType anything and press enter to continue.\n")
main().start()