install:
	uv venv --python 3.12 --seed
	uv pip install vllm --torch-backend=auto

serve:
	fastapi run serve.py