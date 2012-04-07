"""


"""

class FirstError(Exception):
	pass

class Reporter:
	"""
	Simple output collector from plug-ins-
	"""

	def __init__(self, suicidal):

		#: List of output lines or line blocks
		self.raw_output = []

		
		#: List of hints to fix errors - outputted as last
		self.hints = []

		self.suicidal = suicidal

	def check_seppuku(self):
		"""
		Check if we die on the first error.
		"""
		if self.suicidal:
			raise FirstError("First error reached - aborting")

	def report_detailed(self, plugin_id, severity, path, line, pos, id, msg, excerpt=None, details=None):
		"""

		:param plugin_id: Which validator failed - later used to display hint message to the user

		:param path: File path relative to the repo root as string

		:param severity: One of Python logging.* constants

		:param id: Error message id if any or None

		:param line: Line number as integer

		:param pos: Text column position as integer, or None

		:param msg: One line error message 

		:param excerpt: One line excerpt where the error occurs

		:param details: Multi-line error messags like a traceback (usually hidden in details view) or None
		"""
		if id is None:
			id = "validation error"

		self.raw_output.append("%s %d: [%s] %s" % (path, line, id, msg))

		if excerpt:
			self.raw_output.append(excerpt)

		self.check_seppuku()
		
	def report_unstructured(self, plugin_id, output):
		"""
		Dump text output as is from the validator
		"""
		self.raw_output.append(output)
		
		self.check_seppuku()

	def report_internal_error(self, plugin_id, msg):
		"""
		Report exception fired from a plug-in.

		Internal error message does not trigger user hint message.
		"""

		msg = "Internal error occured when running validator %s\n" % plugin_id
		msg += msg

		self.report_unstructured(plugin_id, msg)

	def hint_user(self, hint_message):
		"""
		Give user a hint how to proceed to fix the errors.

		:param hint_message: Hinting info as multi-line string
		"""
		if not (hint_message in self.hints):
			self.hints.append(hint_message)

	def get_output_as_text(self):
		out = "\n".join(self.raw_output) 

		if len(self.hints) > 0:			
			out += "\nTo fix validation errors:\n-----------------------------\n"
			out += "\n\n".join(self.hints)

		return out