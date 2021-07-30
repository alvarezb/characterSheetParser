import requests
from bs4 import BeautifulSoup
import re
import pdfrw

####
#   Variables
####

templatePath = "blank.pdf"
blankCharacterSheetURL = "https://media.wizards.com/2021/dnd/downloads/charactersheet_ravenloft.pdf"
numCharacters = 20

onlyPrintFirstPage = True

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
PDF_TEXT_APPEARANCE = pdfrw.objects.pdfstring.PdfString.encode('/Courier 12.00 Tf 0 g')

#weapons

## weapon data here
weapons = {
	'Club': ('1d4 bludgeoning', 'Light'),
	'Dagger': ('1d4 piercing', 'Finesse, light, thrown (range 20/60)'),
	'Greatclub': ('1d8 bludgeoning', 'Two-handed'),
	'Handaxe': ('1d6 slashing', 'Light, thrown (range 20/60)'),
	'Javelin': ('1d6 piercing', 'Thrown (range 30/120)'),
	'Light Hammer': ('1d4 bludgeoning', 'Light, thrown (range 20/60)'),
	'Mace': ('1d6 bludgeoning', '—'),
	'Quarterstaff': ('1d6 bludgeoning', 'Versatile (1d8)'),
	'Sickle': ('1d4 slashing', 'Light'),
	'Spear': ('1d6 piercing', 'Thrown (range 20/60), versatile (1d8)'),
	'Crossbow, light': ('1d8 piercing', 'Ammunition (range 80/320), loading, two-handed'),
	'Dart': ('1d4 piercing', 'Finesse, thrown (range 20/60)'),
	'Shortbow': ('1d6 piercing', 'Ammunition (range 80/320), two-handed'),
	'Sling': ('1d4 bludgeoning	—	Ammunition (range 30/120)'),
	'Battleaxe': ('1d8 slashing', 'Versatile (1d10)'),
	'Flail': ('1d8 bludgeoning', '—'),
	'Glaive': ('1d10 slashing', 'Heavy, reach, two-handed'),
	'Greataxe': ('1d12 slashing', 'Heavy, two-handed'),
	'Greatsword': ('2d6 slashing', 'Heavy, two-handed'),
	'Halberd': ('1d10 slashing', 'Heavy, reach, two-handed'),
	'Lance': ('1d12 piercing', 'Reach, special'),
	'Longsword': ('1d8 slashing', 'Versatile (1d10)'),
	'Maul': ('2d6 bludgeoning', 'Heavy, two-handed'),
	'Morningstar': ('1d8 piercing', '—'),
	'Pike': ('1d10 piercing', 'Heavy, reach, two-handed'),
	'Rapier': ('1d8 piercing', 'Finesse'),
	'Scimitar': ('1d6 slashing', 'Finesse, light'),
	'Shortsword': ('1d6 piercing', 'Finesse, light'),
	'Trident': ('1d6 piercing', 'Thrown (range 20/60), versatile (1d8)'),
	'War pick': ('1d8 piercing', '—'),
	'Warhammer': ('1d8 bludgeoning', 'Versatile (1d10)'),
	'Whip': ('1d4 slashing', 'Finesse, reach'),
	'Blowgun': ('1 piercing', 'Ammunition (range 25/100), loading'),
	'Crossbow, hand': ('1d6 piercing', 'Ammunition (range 30/120), light, loading'),
	'Crossbow, heavy': ('1d10 piercing', 'Ammunition (range 100/400), heavy, loading, two-handed'),
	'Longbow': ('1d8 piercing', 'Ammunition (range 150/600), heavy, two-handed'),
	'Net': ('—', 'Special, thrown (range 5/15)')
}

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

	#alignment = str(soup.find(lambda tag: tag.name=="p" and "Alignment:" in tag.text))
	#alignmentRE = re.compile(r'</strong>.*?<strong>(.*?)strong>')
	#results['Alignment 2'] = alignmentRE.search(alignment).group(1)
	#alignment is taken from the traits field, lower down

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

	results['Equipment 4'] = BeautifulSoup(soup.find(id="equipmentreasure").text, "html.parser").get_text("\n")

	traitsAndMore = BeautifulSoup(soup.find(id="specialabilities").text, "html.parser").get_text()
	results['Alignment 2'] = re.search(r'Alignment: ([\w\s]+)\.', traitsAndMore).group(1)
	results['PersonalityTraits  2'] = re.search(r'Traits: (.*)', traitsAndMore).group(1)
	results['Ideals 2'] = re.search(r'Ideal: (.*)', traitsAndMore).group(1)
	results['Bonds 2'] = re.search(r'Bond: (.*)', traitsAndMore).group(1)
	results['Flaws 2'] = re.search(r'Flaw: (.*)', traitsAndMore).group(1)

	while "\n\n\n" in traitsAndMore:
		traitsAndMore = traitsAndMore.replace("\n\n\n", "\n\n")
	results['Equipment 5'] = traitsAndMore #this is terribly named

	primaryAttack = soup.find(id="attack01").text.strip()
	weapon = re.search(r'(.*?)\.', primaryAttack).group(1)
	bonus = re.search(r'([+-]\d+?)', primaryAttack).group(1)
	damage = re.findall(r'(\dd\d+[+-]\d+)', primaryAttack)
	if len(damage) >= 2:
		damage = damage[0] + " | " + damage[1] #handle the two handed case
	else:
		damage = damage[0]
	results['Wpn Name 6'] = weapon
	results['Wpn1 AtkBonus 2'] = bonus
	results['Wpn1 Damage 2'] = damage

	magicAttacks = soup.find(lambda tag: tag.name=="strong" and "Cantrip" in tag.text)
	if magicAttacks != None:
		magicAttacks = str(magicAttacks.parent)
		name = re.search(r'<em>([\w\s]*?)</em>', magicAttacks).group(1)
		bonus = re.search(r'[+-]\d+?', magicAttacks)
		bonus = (bonus.group() if bonus else "")
		dist = re.search(r'\w+ ft.', magicAttacks)
		dist = (dist.group() if dist else "")
		damage = re.search(r'\dd\d+(?:[+-]\d+)?', magicAttacks)
		damage = (damage.group() if damage else "")


		results['Wpn Name 8'] = name
		results['Wpn3 AtkBonus   2'] = bonus
		results['Wpn3 Damage  2'] = damage + ", " + dist

	allAttacks = soup.find(id="attackactions").text.strip()
	allAttacks = allAttacks.split("EQUIPMENT & TREASURE")[0]
	results['AttacksSpellcasting 2'] = allAttacks


	#Magic:
	if soup.find(id="spellability"):
		spellcasting = soup.find(id="specialabilities").text
		spellcasting = spellcasting.split("Spellcasting [PHB p. 201]")[1]

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
						#annotation.update({'/DA': PDF_TEXT_APPEARANCE})
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
		outputPath = "output%s.pdf"%i
		fill_pdf(templatePath, outputPath, parseSheet(getFastCharacter(URL, requestData)))
		if onlyPrintFirstPage:
			splitPDFs(outputPath, outputPath)

def splitPDFs(input_pdf_path, output_pdf_path, ranges=["1"]): #default to only the first page
	pages = pdfrw.PdfReader(input_pdf_path).pages
	outdata = pdfrw.PdfWriter(output_pdf_path)
	ranges = ([int(y) for y in x.split('-')] for x in ranges)


	for onerange in ranges:
		onerange = (onerange + onerange[-1:])[:2]
		for pagenum in range(onerange[0], onerange[1]+1):
			outdata.addpage(pages[pagenum-1])
	outdata.write()


####
#   Code runs here
####

#download_pdf(blankCharacterSheetURL, templatePath)
generateSheets(numCharacters, templatePath, URL, requestData)

