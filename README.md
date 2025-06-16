FTM2EBB is a script that converts songs from a .txt file exported from FamiTracker into the music format of the video game EarthBound Beginnings (also known as Mother) into output .asm files for assembly with ASM6.

## **Requirements** ##

The **pandas** library is required to run the script. It can be installed using the `Install.bat` file.

## **Usage Methods** ##

### **1. Standard Method:** ###

Execute the script and enter the song data as prompted by the script.

### **2. Redirected Input (stdin) from a .txt file:** ###

Write the song data requested by the script in a separate .txt file (e.g., test.txt) and execute it via CMD as follows:

`python ftm2ebb.py < test.txt`

You can use the `TestTemplateStdin.txt` file as a template to load the required data.

## **Important Notes** ##

- There is currently no support for FamiTracker effect conversion.

- The "instruments" data used by the song must be configured within the script.

- The `TestTemplateStdin.txt` template is valid only when `SongLoopPointOption` and `TimbreSettingsOption` are set to 0. Otherwise, the template must be modified according to the data requested by the script.

This script was created based on the music format documentation by [Quantam](https://github.com/TheRealQuantam/RetroDocs).
