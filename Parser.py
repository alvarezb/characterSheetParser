import requests
from bs4 import BeautifulSoup
import re
import pdfrw

####
#   Variables
####

templatePath = "blank.pdf"
blankCharacterSheetURL = "https://media.wizards.com/2021/dnd/downloads/charactersheet_ravenloft.pdf"
numCharacters = 5

URL = "https://fastcharacter.com/results.php"

# parameters for the character
requestData = {
'playername': '',
'randomname': 'yes',
'playercode': '',
'pcrace': 'goblin',
'pcclass': '0',
'pclevel': '1',
'pcgender': '0',
'pcbkgrd': '0',
'pcalignment': 'no',
'pointsBuy': 'random',
'custTrait02': '',
'custTrait01': '',
'custIdeal': '',
'custBond': '',
'custFlaw': '',
'pcformat': 'standard',
}

#parameters for filling PDFs
ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'


####
#   functions
####

def getFastCharacter(URL, requestData):
	page = requests.post(URL, data=requestData)
	soup = BeautifulSoup(page.content, "html.parser")
	return soup


def parseSheet(soup):
	modifiers = re.compile(r'[+-]\d+?')


	results = {}
	results['CharacterName 3'] = soup.find(id="charactername").text.strip()
	results['ClassLevel 2'] = soup.find(id="classlevel").text.strip()
	results['Background 2'] = soup.find(id="background").text.strip()
	results['PlayerName 2'] = soup.find(id="playername").text.strip()
	results['Race  2'] = soup.find(id="race").text.strip()

	alignment = str(soup.find(lambda tag: tag.name=="p" and "Alignment:" in tag.text))
	alignmentRE = re.compile(r'</strong>.*?<strong>(.*?)strong>')
	results['Alignment 2'] = alignmentRE.search(alignment).group(1)
	#TODO: Alignment only gets the first part

	results['XP 2'] = soup.find(id="experiencepoints").text.strip()
	results['STR 2'] = soup.find(id="STRscore").text.strip()
	results['DEX 2'] = soup.find(id="DEXscore").text.strip()
	results['CON 2'] = soup.find(id="CONscore").text.strip()
	results['INT 2'] = soup.find(id="INTscore").text.strip()
	results['WIS 2'] = soup.find(id="WISscore").text.strip()
	results['CHA 2'] = soup.find(id="CHAscore").text.strip()
	results['STRmod 2'] = soup.find(id="STRmodf").text.strip()
	results['DEXmod  2'] = soup.find(id="DEXmodf").text.strip()
	results['CONmod 2'] = soup.find(id="CONmodf").text.strip()
	results['INTmod 2'] = soup.find(id="INTmodf").text.strip()
	results['WISmod 2'] = soup.find(id="WISmodf").text.strip()
	results['CHamod 2'] = soup.find(id="CHAmodf").text.strip()
	results['Inspiration 2'] = '' #no inspiration
	results['Passive 2'] = soup.find(id="passiveperception").text.strip()
	results['AC 2'] = soup.find(id="armorclass").text.strip()
	results['Initiative 2'] = soup.find(id="initiative").text.strip()
	results['Speed 2'] = soup.find(id="speed").text.strip()

	results['HPMax 2'] = soup.find(id="hitpoints").text.strip()
	results['HPCurrent 2'] = "" #current hit points, leave blank
	results['HPTemp 2'] = "" #temp hit points, leave blank
	results['HDTotal 2'] = soup.find(id="hitdice").text.strip()
	results['HD 2'] = "" #hit dice used, leave blank
	
	savingThrows = soup.find(id="savingthrows").text.strip()
	savingThrows = modifiers.findall(savingThrows)
	results['ST Strength 2'] = savingThrows[0]
	results['ST Dexterity 2'] = savingThrows[1]
	results['ST Constitution 2'] = savingThrows[2]
	results['ST Intelligence 2'] = savingThrows[3]
	results['ST Wisdom 2'] = savingThrows[4]
	results['ST Charisma 2'] = savingThrows[5]

	skills = soup.find(id="skills").text.strip()
	skills = modifiers.findall(skills)
	results['Acrobatics 2'] = skills[0]
	results['Animal 2'] = skills[1]
	results['Arcana 2'] = skills[2]
	results['Athletics 2'] = skills[3]
	results['Deception  2'] = skills[4]
	results['History  2'] = skills[5]
	results['Insight 2'] = skills[6]
	results['Intimidation 2'] = skills[7]
	results['Investigation  2'] = skills[8]
	results['Medicine 2'] = skills[9]
	results['Nature 2'] = skills[10]
	results['Perception  2'] = skills[11]
	results['Performance 2'] = skills[12]
	results['Persuasion 2'] = skills[13]
	results['Religion 2'] = skills[14]
	results['SleightofHand 2'] = skills[15]
	results['Stealth  2'] = skills[16]
	results['Survival 2'] = skills[17]

	results['ProfBonus'] = soup.find(id="profmodf").text.strip()

	proficiencies = BeautifulSoup(soup.find(id="proficiencies").text, "html.parser").get_text("\n")
	results['ProficienciesLang 2'] = proficiencies

	traitsAndMore = BeautifulSoup(soup.find(id="specialabilities").text, "html.parser").get_text("\n")
	results['PersonalityTraits  2'] = traitsAndMore


	return results

def download_pdf(url, output_path):
	r = requests.get(url, stream=True)

	with open(output_path, 'wb') as fd:
	    for chunk in r.iter_content(2000):
	        fd.write(chunk)


#taken from https://akdux.com/python/2020/10/31/python-fill-pdf-files.html
def fill_pdf(input_pdf_path, output_pdf_path, data_dict):
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    for page in template_pdf.pages:
        annotations = page[ANNOT_KEY]
        for annotation in annotations:
            if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                if annotation[ANNOT_FIELD_KEY]:
                    key = annotation[ANNOT_FIELD_KEY][1:-1]
                    if key in data_dict.keys():
                        if type(data_dict[key]) == bool:
                            if data_dict[key] == True:
                                annotation.update(pdfrw.PdfDict(
                                    AS=pdfrw.PdfName('Yes')))
                        else:
                            annotation.update(
                                pdfrw.PdfDict(V='{}'.format(data_dict[key]))
                            )
                            annotation.update(pdfrw.PdfDict(AP=''))
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)


def generateSheets(number, templatePath, URL, requestData):
	for i in range(number):
		fill_pdf(templatePath, "output%s.pdf"%i, parseSheet(getFastCharacter(URL, requestData)))

####
#   Code runs here
####

download_pdf(blankCharacterSheetURL, templatePath)
generateSheets(5, templatePath, URL, requestData)




