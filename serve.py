from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional, Union
from srcs.SentenceCorrector import SentenceCorrector
from srcs.FormatManager import FORMAT_SENTENCE

corrector = SentenceCorrector()
app = FastAPI(title="SentenceCorrector API")

class CorrectionRequest(BaseModel):
	sentences: Union[str, List[str]]
	language: Optional[str] = "english"
	format: Optional[str] = FORMAT_SENTENCE

class CorrectionResponse(BaseModel):
	corrections: Union[str, List[tuple]]
	language: str
	format: str

@app.post("/correct", response_model=CorrectionResponse)
def correct_sentences(request: CorrectionRequest):
	correction = corrector.correct(request.sentences, request.language, request.format)
	return {
		"corrections": correction, 
		"language": request.language,
		"format": request.format
	}
