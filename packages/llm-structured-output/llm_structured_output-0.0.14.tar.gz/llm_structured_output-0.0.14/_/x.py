import json
import mlx.core as mx
from mlx_lm.utils import load  # Needs pip import mlx_lm
from src.llm_structured_output import (
    JsonSchemaAcceptorDriver,
    HuggingfaceTokenizerHelper,
    bias_logits,
)
from src.llm_structured_output.util.output import setbg, setfg, clear, bold


# MODEL_PATH = "mistralai/Mistral-7B-Instruct-v0.2"
MODEL_PATH = "mlx-community/Meta-Llama-3-8B-Instruct-4bit"
SCHEMA = {
    "type": "object",
    "properties": {
        "streetNumber": {"type": "number"},
        "streetName": {"type": "string"},
        "city": {"type": "string"},
        "state": {"type": "string"},
        "zipCode": {"type": "number"},
    },
}
PROMPT = f"""
[INST] Parse the following address into a JSON object: "27 Barrow St, New York, NY 10014".
Your answer should be only a JSON object according to this schema: {json.dumps(SCHEMA)}
Do not explain the result, just output it. Do not add any additional information. [/INST]
"""


# Load the model as usual.
model, tokenizer = load(MODEL_PATH)

# Instantiate a token acceptor
tokenizer_helper = HuggingfaceTokenizerHelper(tokenizer)
vocabulary, eos_id = tokenizer_helper.extract_vocabulary()
token_acceptor_factory = JsonSchemaAcceptorDriver.driver_factory_for_model(
    vocabulary, eos_id
)
token_acceptor = token_acceptor_factory(SCHEMA)

cache = None
tokens = tokenizer_helper.encode_prompt(PROMPT)
fragments = [tokenizer_helper.no_strip_decode([token]) for token in tokens]

layer_attention_scores = []
mx_fast_scaled_dot_product_attention = mx.fast.scaled_dot_product_attention


def mock_fast_scaled_dot_product_attention(
    queries, keys, values, *, scale, mask=None, stream=None
):
    """
    O = softmax(Q @ K.T, dim=-1) @ V
    result = mx_fast_scaled_dot_product_attention(queries, keys, values, scale=scale, mask=mask, stream=stream)
    """
    B, n_kv_heads, L, _ = keys.shape
    _, n_heads, _, _ = queries.shape
    repeats = n_heads // n_kv_heads

    def repeat(a):
        a = mx.concatenate([mx.expand_dims(a, 2)] * repeats, axis=2)
        return a.reshape([B, n_heads, L, -1])

    keys, values = map(repeat, (keys, values))

    scores = (queries * scale) @ keys.transpose(0, 1, 3, 2)
    if mask is not None:
        scores += mask
    scores = mx.softmax(scores.astype(mx.float32), axis=-1).astype(scores.dtype)
    result = scores @ values
    # print("< MOCK", "Q", queries.shape, "K", keys.shape, "V", values.shape, "S", scores.shape, "R", result.shape)
    # Q (1, 32, 1, 128) K (1, 32, 184, 128) V (1, 32, 184, 128) S (1, 32, 1, 184) R (1, 32, 1, 128)
    # Q(batch_size, n_heads, 1, head_dim) K,V(batch_size, n_heads, input_token_length, head_dim)
    # S(batch_size, n_heads, 1, input_token_lenth) R(batch_size, n_heads, 1, head_dim)
    # print()
    # for i in range(scores.shape[3]):
    # token_score = scores[0, :, 0, i]
    # all_head_weights = mx.sum(token_score, 0).item()
    # setbg(1, 1-all_head_weights, 1-all_head_weights)
    # print(fragments[i].replace("\n", "\\n"), end="")
    # clear()
    # Sum the attention over all heads
    layer_attention_scores.append(mx.sum(scores[0, :, -1, :], 0))
    return result


mx.fast.scaled_dot_product_attention = mock_fast_scaled_dot_product_attention

while tokens[-1] != eos_id:
    # Evaluate the model as usual.
    layer_attention_scores = []
    logits, cache = model(mx.array(tokens)[None], cache)
    token_scores = [
        sum(layer[token].item() for layer in layer_attention_scores)
        / len(layer_attention_scores)
        for token in range(len(fragments))
    ]
    for score, fragment in zip(token_scores, fragments):
        setbg(1, 1 - score, 1 - score)
        print(fragment.replace("\n", "\\n"), end="")
        clear()

    # Set probability to -inf for invalid tokens.
    accepted_token_bitmap = token_acceptor.select_valid_tokens()
    logits = bias_logits(mx, logits[0, -1, :], accepted_token_bitmap)

    # Sample as usual, e.g.:
    token = mx.argmax(logits, axis=-1).item()

    if token == eos_id:
        break

    # Store or use the generated token.
    tokens = [token]
    fragment = tokenizer_helper.no_strip_decode(tokens)
    fragments.append(fragment)
    bold(fragment)

    # Advance the acceptor to the next state.
    token_acceptor.advance_token(token)
