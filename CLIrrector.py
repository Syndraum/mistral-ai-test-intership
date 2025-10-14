from srcs.SentenceCorrector import SentenceCorrector
from argparse import ArgumentParser, Namespace

parser = ArgumentParser(
	prog="CLIrrector",
	description="Correct sentences in any language using AI-powered language models.",
	epilog="Example: uv run CLIrrector.py 'Bonjours le monde' --language french --format sentence"
)

parser.add_argument(
	"sentence",
	help="The sentence to correct. Can contain grammatical errors, spelling mistakes, or other language issues."
)

parser.add_argument(
	"-f", "--format", 
	choices=['sentence', 'encode'],
	default='sentence',
	help="Output format for the correction. 'sentence' returns the full corrected text (default), 'encode' returns delta encoding showing only the differences."
)

parser.add_argument(
	"-l", "--language",
	default="french",
	help="Target language for correction (default: french). Examples: english, french, spanish, german, etc."
)

def main(args: Namespace):
	corrector = SentenceCorrector(
		target_language=args.language,
		format=args.format
	)

	corrections = corrector.correct(args.sentence)
	print(f"{corrections[0]}")

if __name__ == "__main__":
	args = parser.parse_args()
	main(args)