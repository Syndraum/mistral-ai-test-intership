from vllm import LLM, SamplingParams
from .deltaEncoding import encode

MAX_MODEL_LEN = 8192

class SentenceCorrector:
	"""A sentence correction system using a language model.
		
	This class provides functionality to correct sentences in a target language
	using the Qwen3-0.6B model. It supports batch processing and different
	output formats including delta encoding.
		
	Attributes:
		target_language: The language to correct sentences in.
		format: The output format ("sentence" or "encode").
	"""

	def __init__(self, target_language: str = "english", format: str = "sentence"):
		"""Initialize the SentenceCorrector.
		
		Sets up the language model and sampling parameters for sentence correction.
		
		Args:
			target_language: The target language for corrections. Defaults to "english".
			format: The output format for corrections. Either "sentence" for full
				corrected text or "encode" for delta encoding. Defaults to "sentence".
		"""
		self._llm = LLM(
			model="Qwen/Qwen3-0.6B", 
			max_model_len=MAX_MODEL_LEN, 
			max_num_batched_tokens=MAX_MODEL_LEN
		)
		self._sampling_params = SamplingParams(
			max_tokens=512,
			stop=["<|endoftext|>", "<|im_end|>"]
		)
		self.target_language = target_language
		self.setFormat(format)
	
	def _create_chat(self, sentence: str, target_language: str = None) -> list[dict]:
		"""Create a chat conversation template for correction.
		
		Builds the conversation structure needed by the language model to
		perform sentence correction.
		
		Args:
			sentence: The sentence to be corrected.
			target_language: Optionnel, language to use for this chat.
		
		Returns:
			A list of message dictionaries containing the system prompt,
			assistant greeting, and user's sentence.
		"""
		lang = target_language if target_language is not None else self.target_language
		chat = [
			{
				"role": "system",
				"content": f"You are an expert in correcting {lang} sentences. You will receive sentence from user. Your mission is to respond with a corrected version if needed. if the sentence have no fault, do not modify it. Do not change the meaning of the sentence."
			},
			{
				"role": "assistant",
				"content": "Hello user, please provide me a sentence."
			},
			{
				"role": "user",
				"content": f"{sentence}"
			}
		]
		return chat
	
	def _get_format_func(self, format: str):
		"""Get the formatting function based on the specified format.
		
		Determines the appropriate function to apply to the corrected sentence
		based on the desired output format.
		
		Args:
			format: The output format ("sentence" or "encode").
		Returns:
			The formatting function to apply, or None for no formatting.
		"""
		return encode if format == "encode" else None	

	def apply_format(self, original: str, corrected: str, format: str = None) -> str:
		"""Apply the configured output format to the correction.
		
		Transforms the corrected sentence according to the format setting.
		
		Args:
			original: The original uncorrected sentence.
			corrected: The corrected sentence from the model.
		
		Returns:
			The corrected sentence in the configured format. Returns the
			corrected sentence as-is if format is "sentence", or a delta
			encoding if format is "encode".
		"""
		format_func = self._get_format_func(format) if format is not None else self._format_func
		if format_func == None:
			return corrected
		return format_func(original, corrected)

	def correct(self, sentences: str | list[str], target_language: str = None, format: str = None) -> list[str]:
		"""Correct one or multiple sentences.
		
		Processes sentences through the language model to generate corrections.
		Supports both single sentence strings and batch processing of multiple
		sentences.
		
		Args:
			sentences: A single sentence string or a list of sentences to correct.
			target_language: Optionnel, override the target language for this correction.
			format: Optionnel, override the output format for this correction.

		Returns:
			A list of corrected sentences in the configured output format.
			Even if a single sentence is provided, the return value is a list.
		"""
		lang = target_language if target_language is not None else self.target_language
		fmt = format if format is not None else self.format
		# format_func = self._get_format_func(fmt) if fmt is not None else self._format_func

		if isinstance(sentences, str):
			sentences = [sentences]
		chats = [ self._create_chat(s, lang) for s in sentences ]
		outputs = self._llm.chat(
			chats,
			self._sampling_params,
			use_tqdm=False,
			chat_template_kwargs={"enable_thinking": False},
			continue_final_message=False
		)
		corrected = [ self.apply_format(sentences[idx], output.outputs[0].text, fmt) for idx, output in enumerate(outputs) ]
		# corrected = [ (format_func(sentences[idx], output.outputs[0].text) if format_func else output.outputs[0].text) for idx, output in enumerate(outputs) ]
		return corrected
	
	def setFormat(self, format: str):
		"""Set the output format for corrections.
		
		Changes how correction results are returned.
		
		Args:
			format: The desired output format. Use "sentence" for full
				corrected text or "encode" for delta encoding representation.
		"""
		self.format = format
		self._format_func = self._get_format_func(format)