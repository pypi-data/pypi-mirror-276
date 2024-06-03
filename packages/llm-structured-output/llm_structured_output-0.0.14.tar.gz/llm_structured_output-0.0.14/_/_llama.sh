cd `dirname $0`/../src

LLM=examples.llm_schema
MODEL=mlx-community/Meta-Llama-3-8B-Instruct-4bit
#MODEL=mlx-community/Meta-Llama-3-8B-Instruct-8bit
#MODEL=mlx-community/Meta-Llama-3-70B-Instruct-4bit
OPTIONS="--max-tokens 1000 --repeat-prompt --temp 0.8"

SCHEMA='{"type": "object", "properties": {"streetNumber": {"type": "number"}, "streetName": {"type": "string"}, "city": {"type": "string"}, "state": {"type": "string"}, "zipCode": {"type": "number"}}, "required": ["city"]}'
PROMPT='<|begin_of_text|>
<|start_header_id|>system<|end_header_id|>

Parse the following address into a JSON object: "27 Barrow St, New York, NY 10014".
Your answer should be only a JSON object according to this schema: '$SCHEMA'
Do not explain the result, just output it. Do not add any additional information.
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
'

if [ "$1" == "--encapsulated" ]; then
  ENCAPSULATED=$1
  shift
  PROMPT='<|begin_of_text|>
<|start_header_id|>system<|end_header_id|>

Parse the following address into a JSON object: "27 Barrow St, New York, NY 10014".
Your answer should be only a JSON object according to this schema: '$SCHEMA'
First, explain how to accomplist the objective step by step, and then output a JSON object wrapped between the lines ```json and ```.
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
'
fi

if [ "$1" == "--no-schema" ]; then
  shift
  python3 -m $LLM --model-path $MODEL $OPTIONS --prompt "$PROMPT" $@
else
  SCHEMA='{"type": "object", "properties": {"streetNumber": {"type": "number"}, "streetName": {"type": "string"}, "city": {"type": "string"}, "state": {"type": "string"}, "zipCode": {"type": "number"}}, "required": ["city"]}'
  python3 -m $LLM --model-path $MODEL $OPTIONS --prompt "$PROMPT" --schema "$SCHEMA" $ENCAPSULATED $@
fi
