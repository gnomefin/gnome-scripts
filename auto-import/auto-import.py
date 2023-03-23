import pyautogui
import os
import time
import xml.etree.ElementTree as ET

# os.startfile("C:\\Users\\User\\Documents\\GitHub\\gnome-scripts\\auto-import\\UABE\\64bit\\AssetBundleExtractor.exe")
# time.sleep(2)

def click_file(clickType="single", file_path="", center=False, duration=0.5, add_left=0, add_top=0):
    time.sleep(duration)
    left, top = find_file_position(file_path, center=center)
    pyautogui.moveTo(left+add_left, top+add_top, duration=0, tween=pyautogui.easeInOutQuad)
    if clickType == "single":
        pyautogui.click()
    elif clickType == "double":
        pyautogui.doubleClick()

    return left, top

def find_file_position(file_path,center=False):
    if os.path.exists(file_path):
        # The file exists
        pass
    else:
        # The file does not exist
        print("File not found.")

    # Get the coordinates of the file on the screen
    file_location = pyautogui.locateOnScreen(file_path, grayscale=True)
    if center == True:
        file_location = pyautogui.center(file_location)

    # Click the file if it is found
    if file_location is not None:
        # print(file_location)

        # Extract the left and top values from the location tuple
        if center == True:
            left, top = file_location.x, file_location.y
        else:
            left, top = file_location.left, file_location.top

        # Print the results
        print(f"[FIND POSITION], position found at: left={left}, top={top}")

    else:
        print("File not found on the screen.")

    return left, top

# list asset_files
folder = "asset_files"
asset_xml = "assetslocation/apk/textassets.xml"

#loop over the files in the directory
for filename in os.listdir(folder):
    time.sleep(1)
    file_path = "imagelocate/UABE.png"
    left, top = find_file_position(file_path)
    pyautogui.moveTo(left-10, top+35, duration=0, tween=pyautogui.easeInOutQuad)
    pyautogui.click()
    pyautogui.moveTo(left-10, top+55, duration=0, tween=pyautogui.easeInOutQuad)
    pyautogui.click()

    # get assetbundle from filename location mapping xml
    tree = ET.parse(asset_xml)
    # Get the root element
    root = tree.getroot()

    # Find the Asset element with the specified Name
    name_input = os.path.splitext(filename)[0]
    asset = None
    for a in root.findall('Asset'):
        if a.find('Name').text == name_input:
            asset = a
            break

    # Extract the Source element and print its text
    if asset is not None:
        source = asset.find('Source').text
    else:
        print(f"No asset found with Name '{name_input}'")

    source_filename = os.path.basename(source)

    print("[GET ASSET BUNDLE]\\n")
    click_file(clickType="single", file_path="imagelocate/APK_AB_DATA.png", duration=1)

    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    print(f'[PROCESS] Assetbundle Name: {source_filename}\\n')
    pyautogui.typewrite(f'{source_filename}')
    pyautogui.press('enter')

    click_file(clickType="double", file_path="imagelocate/TEXTAS.png", duration=1.5,add_left=-290, add_top=10)
    click_file(clickType="single", file_path="imagelocate/PLUGIN.png", center=True)
    click_file(clickType="double", file_path="imagelocate/IMPORT_TXT.png", center=True)
    click_file(clickType="double", file_path="imagelocate/ASSET_FILES.png", duration=1.5)

    print("[IMPORT] Importing asset file\\n")
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    print(filename)
    pyautogui.typewrite(f'{filename}')
    pyautogui.press('enter')

    time.sleep(0.5)
    click_file(clickType="single", file_path="imagelocate/OK.png", center=True)
    pyautogui.press('enter')

    time.sleep(0.5)
    print("[SAVE] Saving new assetbundle {filename}")
    click_file(clickType="single", file_path="imagelocate/RESULTS.png", center=True)
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')



