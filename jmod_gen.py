#!/usr/bin/python
#coding: utf8
# Инструмент для генерации модулей для Joomla3
# Запускать так:
# 
# usage: jmod_gen.py [-h] [-a ALIAS] [-n NAME] [-d DESC] [-l LANG] [-u USER]
#                    [-e EMAIL] [-s SITE] [-m MODDIR]
# 
# Generate blank Joomla3 module. Use quotes for arguments with spaces
# 
# optional arguments:
#   -h, --help            			Show this help message and exit
#   -a ALIAS, --alias ALIAS 		Alias for your module. Default: "Noname"
#   -n NAME, --name NAME  			Name for module. Default: "Noname module"
#   -d DESC, --desc DESC  			Description for module. Default: "Noname module description"
#   -l LANG, --lang LANG  			Set default language. Default: "ru-RU"
#   -u USER, --user USER  			Set default user name for module. Default: "Nikolay Shangin"
#   -e EMAIL, --email EMAIL 		Set default user email. Default: "shanginn@gmail.com"
#   -s SITE, --site SITE  			Set default site. Default: "http://vk.com/shangin74"
#   -m MODDIR, --mod-dir MODDIR 	Set default directory for result modules. Default: none

import sys, shutil, io, time, os, tempfile, sqlite3, tarfile, random, argparse, re

parser = argparse.ArgumentParser(description='Generate blank Joomla3 module. Use quotes for arguments with spaces')

# Настройки для модуля
parser.add_argument('-a', '--alias',	action='store', dest='alias',	help='Alias for your module.  Default: "Noname"')
parser.add_argument('-n', '--name',		action='store', dest='name',	help='Name for module.  Default: "Noname module"')
parser.add_argument('-d', '--desc',		action='store', dest='desc',	help='Description for module  Default: "Noname module description"')

# Настройки по умолчанию
parser.add_argument('-l', '--lang',		action='store', dest='lang',	help='Set default language. Default: "ru-RU"')
parser.add_argument('-u', '--user',		action='store', dest='user',	help='Set default user name for module. Default: "Nikolay Shangin"')
parser.add_argument('-e', '--email',	action='store', dest='email',	help='Set default user email. Default: "shanginn@gmail.com"')
parser.add_argument('-s', '--site',		action='store', dest='site',	help='Set default site. Default: "http://vk.com/shangin74"')
parser.add_argument('-m', '--mod-dir',	action='store', dest='moduleDir',	help='Set default directory for result modules. Default: none')

options = parser.parse_args()
if len(sys.argv) == 1:
	parser.print_help()
	sys.exit()

alias		  = options.alias if options.alias else 'Noname'
ruName		= options.name if options.name else 'Noname module'
ruDesc		= options.desc if options.desc else 'Noname module description'
lowName		= alias.lower()
uppName		= alias.upper()
fcupName	= alias.title().replace('_','')
baseDir		= 'mod_'+lowName+'/'
date		= time.strftime("%d %b %Y")
year		= time.strftime("%Y")

db			= 'settings.db'
conn 		= sqlite3.connect(db)
cursor		= conn.cursor()

def repl(aliases, text):
	rep = dict((re.escape(k), v) for k, v in aliases.iteritems())
	pattern = re.compile("|".join(rep.keys()))
	return pattern.sub(lambda m: rep[re.escape(m.group(0))], text)


#####################################################################################
#-- Написано для оптимизации участка кода, идущего под этим куском, но заброшенно из-за пятницы.

# Если не передали параметр, получаем его из базы
# for option in (name for name in dir(options) if not name.startswith('_')):
# 	currentOption = getattr(options,option)
# 	if(currentOption):
# 		cursor.execute("UPDATE userinfo set " + option + " = '"+currentOption+"'")
# 		exec(option + " = '" + currentOption + "'")
# 	else:
# 		try:
# 			cursor.execute("SELECT " + option + " FROM userinfo")
# 			exec(option + " = '" + cursor.fetchone()[0] + "'")
# 		except Exception, e:
# 			print e
######################################################################################

# Получаем имя пользователя
if(options.user):
	cursor.execute("UPDATE userinfo set name = '"+options.user+"'")
	user = options.user
else:
	cursor.execute("SELECT Name FROM userinfo")
	user = cursor.fetchone()[0]

# Получаем email пользователя
if(options.email):
	cursor.execute("UPDATE userinfo set email = '"+options.email+"'")
	email = options.email
else:
	cursor.execute("SELECT Email FROM userinfo")
	email = cursor.fetchone()[0]

# Получаем сайт пользователя
if(options.site):
	cursor.execute("UPDATE userinfo set site = '"+options.site+"'")
	site = options.site
else:
	cursor.execute("SELECT Site FROM userinfo")
	site = cursor.fetchone()[0]

# Получаем язык по умолчанию
if(options.lang):
	cursor.execute("UPDATE userinfo set lang = '"+options.lang+"'")
	lang = options.lang
else:
	cursor.execute("SELECT lang FROM userinfo")
	lang = cursor.fetchone()[0]

# Получаем папку для копирования
if(options.moduleDir):
	cursor.execute("UPDATE userinfo set moduleDir = '"+options.moduleDir+"'")
	moduleDir = options.moduleDir
else:
	cursor.execute("SELECT moduleDir FROM userinfo")
	moduleDir = cursor.fetchone()[0]

conn.commit()
# Словарь с подстановками
replaceList = {	'$LOW_NAME$'	: lowName,
				'$UPP_NAME$'	: uppName,
				'$CREAT_DATE$'	: date,
				'$FCUP_NAME$'	: fcupName,
				'$NAME$'		: ruName,
				'$DESC$'		: ruDesc,
				'$CREATE_YEAR$'	: year,
				'$USER_NAME$'	: user,
				'$USER_EMAIL$'	: email,
				'$USER_URL$'	: site,
				'$LANG$'		: lang
			}
print 'Aliases: '
print replaceList
#sys.exit()
# Читаем архив из базы данных
print 'Read options from database'
tmpGzipH, tmpGzipPath = tempfile.mkstemp()
with open(tmpGzipPath, 'w') as tgzFile:
	cursor.execute("SELECT file FROM data WHERE type = 'module'")
	ablob = cursor.fetchone() 
	tgzFile.write(ablob[0]) 
	cursor.close()
	conn.close()
# Распаковываем архив во временную папку
tmpDir = tempfile.gettempdir()
print 'Unpack folder in temp directory: ' + tmpDir
tgzFile = tarfile.open(tmpGzipPath)
tgzFile.extractall(tmpDir)

# Генерируем уникальное название папки
i, tmpCheckDir = 0, baseDir
while os.path.isdir(tmpCheckDir):
	print tmpCheckDir+' exists! '
	tmpCheckDir = baseDir[:-1] + ' (' + str(i) + ')/'
	i += 1

baseDir = tmpCheckDir
# Копируем папку
print 'Copy in ' + baseDir
shutil.copytree(tmpDir+'/mod_$LOW_NAME$', baseDir)

# Список файлов, которые нужно переименовать
fileList = [baseDir+'mod_$LOW_NAME$.xml',
			baseDir+'mod_$LOW_NAME$.php',
			baseDir+'language/$LANG$.mod_$LOW_NAME$.sys.ini',
			baseDir+'language/$LANG$.mod_$LOW_NAME$.ini',
			baseDir+'helper.php']

print fileList

# Поочереди переименовываем файлы и производим замену переменных
for filePath in fileList:
	with open(filePath, 'r+') as oneFile:
		print '	Now open file ' + filePath
		# Создаем временный файл, в который будет записан результат подстановок
		tempFileHandler, tempFilePath = tempfile.mkstemp()
		print '	Create temp file at ' + tempFilePath
		tempFile = open(tempFilePath, 'w')
		# Лютая магия для замены переменных
		text = repl(replaceList, oneFile.read())
		
		tempFile.write(text)
		tempFile.close()
		os.close(tempFileHandler)
	os.remove(filePath)
	# Используем новый словарь, чтобы избежать проблем в кодировкой
	for replaceFrom, replaceTo in { '$LOW_NAME$' : lowName, '$UPP_NAME$': uppName, '$LANG$': lang }.iteritems():
		filePath = filePath.replace(replaceFrom, replaceTo)
	shutil.move(tempFilePath, filePath)

if(moduleDir):
	shutil.move(baseDir, moduleDir+baseDir)
	print "Done! "+alias+" module at "+moduleDir+baseDir
else:
	print "Done! "+alias+" module at "+baseDir