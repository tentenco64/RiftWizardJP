

import mods.API_Universal.APIs.API_OptionsMenu.API_OptionsMenu as API_OptionsMenu
import os
import pygame
import re

NO_TRANSLATION = 'English (default)'

translations = [NO_TRANSLATION]
def initialize():
	global translations
	if not os.path.exists(os.path.join('mods','API_Universal','translations')):
		return

	for f in os.listdir(os.path.join('mods','API_Universal','translations')):
		if os.path.isdir(os.path.join('mods','API_Universal','translations', f)):
			translations.append(f)
		

initialize()



def translation_changed(self, cur_value):
	self.options['translation'] = cur_value
	load_translation(self)


translation = None
translation_font = None

def load_translation(self):

	global translation
	global translation_font
	translation = dict()
	translation_folder = os.path.join('mods','API_Universal','translations',self.options['translation'])
	translation_filename = None
	font_filename = None

	if self.options['translation'] == NO_TRANSLATION or not os.path.exists(translation_folder):
		translation = None
		translation_font = None
		return
	

	for f in os.listdir(translation_folder):
		if os.path.isdir(os.path.join('mods','API_Universal','translations', f)):
			continue
		
		extension = f.split('.')[-1]

		if extension == 'csv':
			translation_filename = f
		elif extension == 'ttf':
			font_filename = f


	if translation_filename == None:
		translation = None
		translation_font = None
		return


	with open(os.path.join('mods','API_Universal','translations', self.options['translation'], translation_filename), 'r', encoding='utf-8') as f:
		for line in f:
			split_line = line.split('\t')
			if len(split_line) <= 1:
				# 警告をコメントアウト
				# print('WARNING: translation file ' + translation_filename + ' - no tab character found on line: ' + line)
				continue
			(english, translated) = split_line
			if r"\n" in translated:
				translated = translated.replace(r"\n", "\n")
			translation[english] = translated[:-1]

	if font_filename != None:
		font_path = os.path.join('mods','API_Universal','translations', self.options['translation'], font_filename)
		translation_font = pygame.font.Font(font_path, 20)
	else:
		translation_font = None

untranslated_strings = set()
def declare_untranslated_string(string):
	# global untranslated_strings
	# if string not in untranslated_strings:
	# 	print(string)
	# 	untranslated_strings.add(string)
	pass

num_p = re.compile(r"\d+")
d_p = re.compile(r"%d")
s_p = re.compile(r"%s")
a_p = re.compile(r"\[%a\]")
item_p = re.compile(r"A%d  ")
spell_p = re.compile(r" %d  ")
damage_p = re.compile(r"^ %d ")
resist_p = re.compile(r"^-?%d% ")
spell_expo_p=re.compile(r"%d - ")
word_p = re.compile(r"\b[a-zA-Z]{2,}\b( \b[a-zA-Z]+\b)*")
gate_p = re.compile(r"(?<=Spawns a )\b[a-zA-Z]{2,}\b( \b[a-zA-Z]+\b)*(?= every)")
learn_p = re.compile(r"(?<=Learn )\b[a-zA-Z]{2,}\b( \b[a-zA-Z]+\b)*(?= for)")
attribute_p = re.compile(r"\[[a-zA-Z]+?\]")
spell_gain_p = re.compile(r"^[\w ]+?(?= gains \[)")

can_be_upgrade_spellname_p = re.compile(r"^[\w ]+?(?= can be upgraded with only )")
can_be_upgrade_type_p = re.compile(r"(?<=with only %d )[\w ]+?(?= upgrade$)")

def translate(string):
	print(string)
	if translation is None:
		return string
	translated_string = ""
	menu_flag = False
	damage_flag = False
	num_list=[]
	name_list=[]
	attribute_list=[]
	name = ""

	raw_string = repr(string)[1:-1]

	string_list = raw_string.split(r"\n")


	for string in string_list:
		org_str = string

		if num_p.search(string): # 数字を持つ場合%dに変換
			num_list = [m.group() for m in num_p.finditer(string)]
			string = num_p.sub(r"%d", string)

		gate_m = gate_p.search(string)
		if gate_m is not None: # ゲートから出現するモンスター名を%sに変換
			name_list = [gate_m.group()]
			string = gate_p.sub(r"%s", string)
		learn_m = learn_p.search(string)
		if learn_m is not None: # 習得するスキル名を%sに変換
			name_list = [learn_m.group()]
			string = learn_p.sub(r"%s", string)
		spell_gain_m = spell_gain_p.match(string)
		if spell_gain_m is not None:
			end = spell_gain_m.end()
			name_list = [string[:end].upper()]
			string = spell_gain_p.sub(r"%s", string)
		cbus_m = can_be_upgrade_spellname_p.match(string)
		cbut_m = can_be_upgrade_type_p.search(string)
		if (cbus_m and cbut_m) is not None:
			name_list = [cbus_m.group().upper(), cbut_m.group()]
			string = can_be_upgrade_spellname_p.sub(r"%s", string)
			string = can_be_upgrade_type_p.sub(r"%s", string)

		if attribute_p.search(string): # shrineで使用される属性名を%aに変換
			attribute_list = [m.group() for m in attribute_p.finditer(string)]
			string = attribute_p.sub(r"[%a]", string)

		if item_p.search(string) or spell_p.search(string): # インベントリ表示からアイテム名や呪文名を抽出
			menu_flag = True
			string = word_p.search(string).group()

		if damage_p.search(string) or resist_p.search(string): # モンスターの攻撃力表記や抵抗の表記から属性を抽出
			damage_flag = True
			string = word_p.search(string).group()

		print(string)
		if string in translation: # 対応する翻訳がある場合の処理
			if menu_flag: # インベントリ表示用の処理
				name=translation[string]
				space = 10 - len(name)
				string = word_p.sub("   "+name+" "*space, org_str)
			elif damage_flag: # モンスターステータス表示用の処理
				name=translation[string]
				string = word_p.sub(name, org_str)
			else:
				string = translation[string]
			for num in num_list: # %dを元の表記に戻す
				string = d_p.sub(num, string, 1)
			for attribute in attribute_list: # %aを元の表記に戻す
				if attribute in translation:
					attribute = translation[attribute]
				string = a_p.sub(attribute, string, 1)
			for name in name_list:
				string = s_p.sub(name, string, 1) # %sを元の表記に戻す
		else: # 対応する翻訳が無い場合、元の状態に戻す
			string = org_str

		translated_string += string
	print(translated_string)
	return translated_string




"""
	if string in translation:
		print(string)
		if d_p.search(string):
			print("%d finded")
			string = translation[string]
			for num in num_list:
				string = d_p.sub(num, string, 1)
			return string
		elif menu_flag:
			item_name = translation[string]
			space = 10 - len(item_name)
			string = word_p.sub("   "+item_name+" "*space, org_str)
		else:
			return translation[string]
	for num in num_list:
		string = d_p.sub(num, string, 1)
	return string

"""


"""
	# attempt to translate word by word
	#exp = '[\[\]:|\w\|\'|%|-]+|.| |,'
	exp = '[\[\]:|\w\'%-]+|.| |,'
	words = re.findall(exp, string)
	print("wordsnum:" +str(len(words)))
	print(words)
	words.reverse()

	translated_string = ''
	for word in words:
		if word in translation:
			translated_string += translation[word]
		elif word and word[0] == '[' and word[-1] == ']':
			translated_string += '['

			tokens = word[1:-1].split(':')
			if len(tokens) == 1:
				# ex [fire] -> [fuego:fire]
				word = tokens[0]

				if word in translation:
					translated_string += '['+translation[word]+':'+word+']'
				else:
					translated_string += '['+word+']'
					declare_untranslated_string(word)

				translated_string += word
				
			elif len(tokens) == 2:
				# ex [2_fire_damage:fire] -> [2_daños_por_fuego:fire]
				word = tokens[0].replace('_', ' ')

				if word in translation:
					translated_string += translation[w]
				else:
					word = word.split(' ')
					for (w, i) in zip(word, range(len(word))):
						
						if w in translation:
							translated_string += translation[w]
						else:
							translated_string += w
							declare_untranslated_string(w)

						if i < len(word)-1:
							translated_string += '_'

				translated_string += ":"+tokens[1]+"]" # reconstruct the original tag (the tooltip_colors dict is in english regardless of the translation loaded)
		else:
			translated_string += word
			declare_untranslated_string(word)
	return string
"""
	


def get_language_font(self):
	return translation_font




def initialize_translation_option(self):
	if not 'translation' in self.options:
		self.options['translation'] = NO_TRANSLATION
	load_translation(self)

API_OptionsMenu.add_option(
	lambda self, cur_value: "Language: " + cur_value, 
	lambda self: self.options['translation'], 
	translations, 
	'translation_option', 
	trigger_on_select=translation_changed, 
	option_wraps=True, 
	initialize_option=initialize_translation_option
)
API_OptionsMenu.add_blank_option_line()
