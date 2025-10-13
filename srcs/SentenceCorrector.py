from vllm import LLM, SamplingParams
from .deltaEncoding import encode

MAX_MODEL_LEN = 8192

class SentenceCorrector:

	def __init__(self, target_language: str = "english", format: str = "sentence"):
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
	
	def _create_chat(self, sentence: str) -> list[dict]:
		chat = [
			{
				"role": "system",
				"content": f"You are an expert in correcting {self.target_language} sentences. You will receive sentence from user. Your mission is to respond with a corrected version if needed. if the sentence have no fault, do not modify it. Do not change the meaning of the sentence."
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
	
	def apply_format(self, orginal: str, corrected: str):
		if self._format_func == None:
			return corrected
		return self._format_func(orginal, corrected)

	def correct(self, sentences: str | list[str]) -> list[str]:
		if isinstance(sentences, str):
			sentences = [sentences]
		chats = [ self._create_chat(s) for s in sentences ]
		outputs = self._llm.chat(
			chats,
			self._sampling_params,
			use_tqdm=False,
			chat_template_kwargs={"enable_thinking": False},
			continue_final_message=False
		)
		corrected = [ self.apply_format(sentences[idx], output.outputs[0].text) for idx, output in enumerate(outputs) ]
		return corrected
	
	def setFormat(self, format: str):
		self.format = format
		self._format_func = encode if format == "encode" else None