
##################
#  Command to load XTM files into local database
#
#  python manage.py parse_xtm --dryrun --customlib
#

#  note: this extracts functions from local_settings.py XTM_LOCAL_FILES

##################


from django.conf import settings
from django.db import connection, models
from django.utils.http import urlquote
from time import strftime

from settings import XTM_VERSION, XTM_LOCAL_FILES, XTM_GITHUB_URL, XTM_EXCLUDE, CUSTOM_GITHUB_URL, CUSTOM_LOCAL_FILES, CUSTOM_EXCLUDE
from extempore.models import *
from extempore.management.commands.helper_parser import walk_xtm_files
from myutils.myutils import *



import djclick as click


#  helper for django models
def get_or_new(model, somename):
	"""helper method"""
	try:
		# if there's an object with same name, we keep that one!
		obj = model.objects.get(name=somename)
		print("++++++++++++++++++++++++++ found existing obj:	%s"	 % (obj))
	except:
		obj = model(name=somename)
		obj.save()
		print("======= created new obj:	  %s"  % (obj))
	return obj





@click.command()
@click.option('--reset', default=False, is_flag=True, help='The _reset_ option removes all previously saved values in the DB')
@click.option('--customlib', default=False, is_flag=True, help='The _customlib_ option allows you to specify a custom directory')
@click.option('--corelib', default=False, is_flag=True, help='The _corelib_ option defines whether to parse the default Extempore library or not')
@click.option('--test_mode', default=False, is_flag=True, help='The test_mode option runs the command on a selected folder hardcoded in the script. Used for testing the parser on a single file.')
@click.option('--dryrun', default=False, is_flag=True, help='The _dryrun_ option allows you to test the script without saving anything')
@click.pass_context
def command(ctx, reset, customlib, corelib, test_mode, dryrun):

	if not reset and not customlib and not corelib:
		print(ctx.get_help())
		return
	
	click.secho(f'Hello - dryrun is {dryrun}', fg='red')

	# feedback:
	click.secho("\n\n++ = ++ = ++ \n%s\nSTARTING:"  % strftime("%Y-%m-%d %H:%M:%S"))
	click.secho("++ = ++ = ++ \n")


	if reset:
		print("++ = ++ = ++ = ++ Cleaning all previously saved contents ....")

		if click.confirm('Do you want to continue?'):
			if not dryrun:
				XTMFundocEntry.objects.all().delete()
			print('.........successfully erased all previously saved contents!\n')
		# pass # nothing to delete



	if corelib:

		SOURCE_DIR = XTM_LOCAL_FILES
		URL = XTM_GITHUB_URL
		IS_CUSTOM = False
		EXCLUDE = XTM_EXCLUDE

		_do_parse_and_save(SOURCE_DIR, URL, IS_CUSTOM, EXCLUDE, dryrun)

	

	if customlib:

		SOURCE_DIR = CUSTOM_LOCAL_FILES
		URL = CUSTOM_GITHUB_URL
		IS_CUSTOM = True
		EXCLUDE = CUSTOM_EXCLUDE

		_do_parse_and_save(SOURCE_DIR, URL, IS_CUSTOM, EXCLUDE, dryrun)


	if test_mode:
		# Hard coded for testing
		SOURCE_DIR = ["/Users/michele.pasin/dev2/extempore-docs/xtm-docs/src/apps/zavrel/management/commands/tests"] 
		URL = "https://github.com/lambdamusic/xtm-hacking/blob/master/init-extempore"
		IS_CUSTOM = True
		EXCLUDE = []

		_do_parse_and_save(SOURCE_DIR, URL, IS_CUSTOM, EXCLUDE, dryrun)




	if (corelib or customlib) and not dryrun:
		click.secho("\nCleaning up permalinks ...)", fg='green')
		XTMFundocEntry.cleanup_permalinks()


	print("\n\n++ = ++ = ++ \nCOMPLETED\n++ = ++ = ++ ")





def _do_parse_and_save(source_dir, url, is_custom, exclude, dryrun):
	"""Walk through XTM files in a specific location (or list of). Extract 
	  function definitions and try to save."""

	functions_index = walk_xtm_files(source_dir, exclude_patterns=exclude, githubUrl=url)

	click.secho(f"""\n****\nResults\n****""", fg='green')

	if not functions_index:
		click.secho(f"""No functions found in {source_dir}""")
		return
	
	for fun in functions_index:

		f1 = XTMFundocEntry()
		f1.name = fun['name']
		f1.url = fun['url']
		f1.source = fun['codepygments'] #note: css needs manually added to page
		f1.fungroup = fun['group']
		f1.funtype = fun['functiontype']
		f1.is_custom = is_custom
		
		if dryrun:
			click.secho("[dryrun] Processed: {f1.name} -- id: {f1.id}""")
		else:
			f1.save()
			click.secho(f"""Saved: {f1.name} -- id: {f1.id} -- permalink: {f1.permalink}""")

