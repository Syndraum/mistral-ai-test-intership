from difflib import SequenceMatcher

def encode(old: str, new: str) -> list[tuple[int, int, str]]:
	"""Encode the differences between two strings as a delta.
    
    Compares two strings and generates a compact delta representation containing
    only the operations needed to transform the old string into the new string.
    Equal sections are omitted from the delta.
    
    Args:
        old: The original string to compare from.
        new: The target string to compare to.
    
    Returns:
        A list of tuples representing the delta operations. Each tuple contains:
            - int: Start position in the old string
            - int: Length of the section in the old string
            - str: Replacement text from the new string
    
    Example:
        >>> encode("hello world", "hello python")
        [(6, 5, 'python')]
    """
	matcher = SequenceMatcher(a = old, b = new)
	delta = []

	for tag, i1, i2, j1, j2 in matcher.get_opcodes():
		if tag != 'equal':
			delta.append((i1, i2 - i1, new[j1:j2]))
	return delta