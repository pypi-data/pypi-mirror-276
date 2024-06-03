cd `dirname $0`/../src
API_URL=https://alice.sungrazing-iguana.ts.net/llm
API_KEY=none
MODEL_NAME=none
NO_PROMPT_STEERING=--disable-prompt-steering
if [ "$1" == "--openai" ]; then
  shift
  API_URL=https://api.openai.com
  API_KEY=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
  MODEL_NAME=gpt-4o
  NO_PROMPT_STEERING=
fi
EVAL_FILE=../../eval/fireworks-ai_function-calling-eval-dataset-v0/multi_turn-00000-of-00001.json
python3 -m tests.eval_api --api-url $API_URL --api-key $API_KEY --model-name $MODEL_NAME $NO_PROMPT_STEERING --dataset $EVAL_FILE $@
