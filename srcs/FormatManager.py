from .deltaEncoding import encode

FORMAT_SENTENCE = "sentence"
FORMAT_ENCODE = "encode"

class FormatManager:
	"""Manages different output formats for sentence corrections.
	Provides formatter functions for various formats including full sentences
	and delta encoding.
	"""

	def __init__(self):
		"""Initialize the FormatManager with available formatters.
		"""
		self.formatters = {
			FORMAT_SENTENCE: self._sentence,
			FORMAT_ENCODE: encode
		}

	def get_formatter(self, format_name: str):
		"""Get the formatter function for the given format name.

		Args:
			format_name: The name of the format.

		Returns:
			The formatter function for the specified format. If the format
			is not recognized, returns the sentence formatter by default.
		"""
		return self.formatters.get(format_name, self._sentence)

	def _sentence(self, original: str, corrected: str):
		"""Return the corrected sentence as-is.
		"""
		return corrected
