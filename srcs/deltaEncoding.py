from difflib import SequenceMatcher

def encode(old: str, new: str) -> list[tuple[int, int, str]]:
	matcher = SequenceMatcher(a = old, b = new)
	delta = []

	for tag, i1, i2, j1, j2 in matcher.get_opcodes():
		if tag != 'equal':
			delta.append((i1, i2 - i1, new[j1:j2]))
	return delta