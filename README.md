# Pdf-screenshot-automatizer

This Python script is built to automatize screenshot taking on pdf documents.

##Requirements

Please remember to install Python on your pc and add it to your PATH.

You need to install the libraries specified in the requirements file.
```
    pip install -r requirements.txt
```

##How to use it

1. Place your pdf inside the 'documents' folder, replacing the placeholder one. Please note: this script only works if there is one exact pdf file inside the folder!

2. Open the terminal in the same folder of the script and launch it with ```python scr_automatize.py```

3. The script will convert each page of your pdf to an image, then it will open the GUI. Use it to navigate through pages,  zoom in/out and scroll. Drag the region you want to screenshot, and then press the 'Crop Image' button to save the screenshot.
Repeat this as many times as you want.
The script will create a folder named after your pdf file, inside the 'screenshot' folder, containing all your screenshot.
When you are done, close the script. 

4. Inside your folder you'll find a file named 'coordinates.json', in which are stored all the coordinates of your screenshots.

5. Replace the pdf file in the 'documents' folder with another one, and then repeat step 2.
This time, everything will be automatic. You'll find a new folder with the screenshots of the new pdf inside the 'screenshot' folder.


##Troubleshooting

-What if I made a mistake in taking screenshots for the first time/ I want to change coordinates?-

To solve this, just delete the 'coordinates.json' file in the folder, or remove it and store it in another place.









