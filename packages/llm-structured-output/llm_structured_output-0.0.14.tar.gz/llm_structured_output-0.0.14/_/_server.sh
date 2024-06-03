PORT=8001
/Applications/Tailscale.app/Contents/MacOS/Tailscale funnel --bg --set-path llm $PORT
cd `dirname $0`/../src
#MODEL_PATH=mistralai/Mistral-7B-Instruct-v0.2 uvicorn examples.server:app --port $PORT --reload
#MODEL_PATH=mlx-community/Meta-Llama-3-8B-Instruct-8bit uvicorn examples.server:app --port $PORT --reload
MODEL_PATH=mlx-community/Meta-Llama-3-8B-Instruct-4bit uvicorn examples.server:app --port $PORT --reload
