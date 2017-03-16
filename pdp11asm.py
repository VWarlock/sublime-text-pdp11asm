import sublime, sublime_plugin
import os

# Consts
THIS_PLUGIN_NAME = 'pdp11asm'
THIS_PLUGIN_DEBUG = True
NOT_IMPLEMENTED_MENU_ITEM = ["Not_Implemented_Command_1", "Not_Implemented_Command_2"]

# Initialize plugin
def Pdp11Init():
	global PDP11_DIR, PDP11_SYNTAX_FILE, PDP11_SNIP_DIR, PDP11_HELP_DIR
	PDP11_DIR=os.path.join(sublime.packages_path(), THIS_PLUGIN_NAME)
	PDP11_SYNTAX_FILE='Packages'+'/'+THIS_PLUGIN_NAME+'/'+THIS_PLUGIN_NAME+'.tmLanguage'
	PDP11_SNIP_DIR='Packages'+'/'+THIS_PLUGIN_NAME+'/'+'snippets'
	PDP11_HELP_DIR=PDP11_DIR+'/'+'helps'



# Debug print
def dbgprint(s):
	if THIS_PLUGIN_DEBUG:
		print ("PDP-11 Asm:",s)
		sublime.status_message(s)



# Command handler class
class Pdp11DoCmdCommand(sublime_plugin.WindowCommand):
	# Command handler
	def run(self, cmd):

		if cmd=="NewCode":
			v=self.window.new_file()
			v.set_syntax_file(PDP11_SYNTAX_FILE)
			v.run_command("insert_snippet", {"name": PDP11_SNIP_DIR+'/init.sublime-snippet'})
			dbgprint("New Code created")

		elif cmd=="NewRT11Prog":
			v=self.window.new_file()
			v.set_syntax_file(PDP11_SYNTAX_FILE)
			v.run_command("insert_snippet", {"name": PDP11_SNIP_DIR+'/rt11prog.sublime-snippet'})
			dbgprint("New RT-11 Programm created")

		elif cmd=="Build":
			self.window.run_command("build")
			dbgprint("Build started")

		elif cmd=="Run":
			self.window.run_command("build", {"variant": "Run"})
			dbgprint("Emulator started")

		elif cmd=="Build_Run":
			self.window.run_command("build", {"variant": "Build and Run"})
			dbgprint("Build and Run script started")

		elif cmd=="Not_Implemented_Menu_Item_1":
			self.window.run_command("Not_Implemented_Command_1", "Not Implemented Menu Item 1")
			dbgprint("Not implemented yet")

		elif cmd=="Not_Implemented_Menu_Item_2":
			self.window.run_command("Not_Implemented_Command_2", "Not Implemented Menu Item 2")
			dbgprint("Not implemented yet")

	# Disable not implemented items
	def is_enabled(self, cmd):
		if cmd not in NOT_IMPLEMENTED_MENU_ITEM:
			return True
		return False
	
		# Hide not implemented items
	def is_visible(self, cmd):
		if cmd not in NOT_IMPLEMENTED_MENU_ITEM:
			return True
		return False
		

# Helps
class Pdp11HelpCommand(sublime_plugin.WindowCommand):
	def run(self, indx):
		n=self.help_list()
		self.window.run_command("open_file", {"file": "${packages}/pdp11asm/helps/"+n[indx]})

	# Scan helps folder for files (10 max)
	def help_list(self):
		lst=os.listdir(PDP11_HELP_DIR)
		lst.sort()
		return lst[:10]

	# Show help
	def is_visible(self, indx):
		n=self.help_list()
		if indx<len(n):
			return True
		return False

	# Show help names
	def description(self, indx):
		n=self.help_list()
		if indx<len(n):
			return n[indx]
		return ""



# Quick help - F1
class Pdp11QuickHelpCommand(sublime_plugin.WindowCommand):
	# Init: read items from file
	def __init__(self, *args, **kwargs):
		self.help=[]
		with open(PDP11_DIR+'/'+THIS_PLUGIN_NAME+'.quickhelp','rt') as f:
			self.help = [line.strip() for line in f]

		super(Pdp11QuickHelpCommand,self).__init__(*args, **kwargs)

	# Show help
	def run(self):
		self.window.show_quick_panel(self.help, None, sublime.MONOSPACE_FONT)



# Autocompletion class
class Pdp11Autocomplete(sublime_plugin.EventListener):
	# Generate completion list from all opened tabs
	def on_query_completions(self, view, prefix, locations):
		# Check if option is enabled
		if view.settings().get("use_global_completion") != True:
			return []

		# List of all views (our one is always first)
		views = [view] + [v for v in sublime.active_window().views() if v.id() != view.id()]
		compl=[]
		for v in views:
			if v.id() == view.id():
				# For our view use cursor location
				words = v.extract_completions(prefix,locations[0])
			else:
				words = v.extract_completions(prefix)
			# Add only unique words
			for w in words:
				if w not in compl:
					compl.append(w)

		return [(el, el) for el in compl]



# Define plugin_loaded() function for ST3 because it's have another plugin lifecycle
# (cannot call sublime.packages_path() at importing time). For ST2 fust call PDP11Init().
if int(sublime.version())>=3000:
	def plugin_loaded():
		Pdp11Init()
else:
	Pdp11Init()

dbgprint("PDP-11 Asm plugin started!")
