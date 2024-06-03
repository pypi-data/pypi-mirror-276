cd `dirname $0`/../src

LLM=examples.llm_schema
#MODEL=mistralai/Mistral-7B-Instruct-v0.2
#MODEL=mlx-community/Mistral-7B-v0.2-4bit
#MODEL=mlx-community/Mixtral-8x22B-4bit
#MODEL=mlx-community/Meta-Llama-3-8B-Instruct-4bit
MODEL=mlx-community/Meta-Llama-3-8B-Instruct-8bit
#MODEL=mlx-community/Phi-3-mini-128k-instruct-8bit
#MODEL=mlx-community/Meta-Llama-3-70B-Instruct-4bit
OPTIONS="--max-tokens 4000 --repeat-prompt --temp 0"

PROMPT=$(cat << EOF
Translate the following node.js code to modern browser ES6 code, using modules, const/let instead of var, etc.

### old node.js code
exports.encode = VariableLengthEncode;
exports.decode = VariableLengthDecode;
exports.encodeArray = VariableLengthEncodeArray;
exports.decodeArray = VariableLengthDecodeArray;
exports.encode7bitArray = VariableLengthEncode7bitArray;
exports.decode7bitArray = VariableLengthDecode7bitArray;
exports.encodeKnownLengthArray = VariableLengthEncodeKnownLengthArray;
exports.decodeKnownLengthArray = VariableLengthDecodeKnownLengthArray;
exports.encodeString = VariableLengthEncodeString;
exports.decodeString = VariableLengthDecodeString;


var assert = require('assert');


function VariableLengthEncode(number) {
  assert(typeof number == 'number' && number >= 0);

  // The MSB of each byte is zero if this is the last byte.
  // Bytes are ordered low to high (big-endian, in a way).

  return new Buffer(VariableLengthEncode_bytes(number));
}


function VariableLengthEncode_bytes(number) {
  var bytes = [];
  for (;;) {
    var byte = number & 0x7F;
    // Note: Javascript performs bitwise operations by converting numbers to
    //       signed 32-bit integers. For positive numbers larger than 31-bits,
    //       masking the low bits seems to work, but shift doesn\'t.
    if (number >= Math.pow(2, 31))
      number = Math.floor(number / (1<<7));
    else
      number >>= 7;
    if (number > 0) {
      bytes.push(byte | 0x80);
    } else {
      bytes.push(byte);
      return bytes;
    }
  }
}


function VariableLengthDecode(buffer, offset) {
  // See encoding note about bitwise ops.
  for (var number = 0, length = 0, shift = 1; ; shift *= 1<<7) {
    var byte = buffer.readUInt8(offset + length++);
    number  += (byte & 0x7f) * shift;
    if (!(byte & 0x80))
      return {
               n:      number,
               length: length,
             }
  }
}

### new ES6 code
EOF)

python3 -m $LLM --model-path $MODEL $MODEL_TYPE $OPTIONS --prompt "$PROMPT" $@
