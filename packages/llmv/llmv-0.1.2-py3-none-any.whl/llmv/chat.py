import base64
import os
import random
import time
from io import BytesIO

from litellm import completion, cost_per_token, token_counter, ContentPolicyViolationError, RateLimitError # can take 3-5 secs on rpi
from PIL import Image
import litellm



## set model alias map
model_alias_map = {
    "openai": "gpt-4-vision-preview",
}

litellm.model_alias_map = model_alias_map

## set env variables for logging tools
# os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-d2da0386-2d18-4ec8-8fca-cd16b5e41ece"
# os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-6c5aafda-18b8-4a3c-b9a3-d3d3240149c0"


# # litellm caching
# litellm.cache = litellm.Cache()

# litellm callbacks
# litellm.success_callback = ["langfuse"]
# litellm.failure_callback = ["langfuse"]


# tell litellm to drop unsupported params
litellm.drop_params = True


# set TOKENIZERS_PARALLELISM=false, for hugging face embedding generator
os.environ["TOKENIZERS_PARALLELISM"] = "false"


#from sentence_transformers import SentenceTransformer # takes 10 secs on rpi
# def create_embeddings(data, query_instruction=None):
#     # create 768 dimensional embeddings
#     model = SentenceTransformer("BAAI/bge-base-en-v1.5")
#     return model.encode(data, normalize_embeddings=True)


# define a retry decorator
def retry_with_exponential_backoff(
    func,
    initial_delay: float = 1,
    exponential_base: float = 2,
    jitter: bool = True,
    max_retries: int = 10,
    errors: tuple = (RateLimitError, ContentPolicyViolationError),
):
    """Retry a function with exponential backoff."""

    def wrapper(*args, **kwargs):
        # Initialize variables
        num_retries = 0
        delay = initial_delay

        # Loop until a successful response or max_retries is hit or an exception is raised
        while True:
            try:
                return func(*args, **kwargs)

            # Retry on specific errors
            except errors as e:
                # Increment retries
                num_retries += 1

                # Check if max retries has been reached
                if num_retries > max_retries:
                    raise Exception(
                        f"Maximum number of retries ({max_retries}) exceeded."
                    )

                # Increment the delay
                delay *= exponential_base * (1 + jitter * random.random())

                print(f"Encountered openai rate limit, retry in: {delay}")
                # Sleep for the delay
                time.sleep(delay)

            # Raise exceptions for any errors not specified
            except Exception as e:
                raise e

    return wrapper


def prompt_from_file(file_path, input_text):
    """read the file and return the prompt"""
    with open(file_path, "r") as f:
        prompt = f.read()
    return prompt + "\n" + input_text  # return the prompt with input text appended


def image_tokens(base64_image):
    tile_size = 512  # Tile size (width and height)
    base_tokens = 85
    tile_tokens = 170
    max_width = 1536
    max_height = 768

    # Decode the base64 image
    image_data = base64.b64decode(base64_image.replace("data:image/jpeg;base64", ""))

    # Open the image using a BytesIO stream
    with Image.open(BytesIO(image_data)) as img:
        width, height = img.size
        if width > max_width:
            width = max_width
        if height > max_height:
            height = max_height

    # Calculate the number of tiles
    tiles_across = (width + tile_size - 1) // tile_size
    tiles_down = (height + tile_size - 1) // tile_size
    total_tiles = tiles_across * tiles_down

    # Calculate total tokens
    total_tokens = base_tokens + tile_tokens * total_tiles

    return total_tokens


def parse_messages(messages):
    images = []
    text = []
    for message in messages:
        content = message["content"]
        if not content:
            continue

        # if content is str
        if not isinstance(content, list):
            text.append(content)
            continue
        for content_item in content:
            if content_item.get("type") == "image_url":
                images.append(content_item["image_url"])
            if content_item.get("type") == "text":
                text.append(content_item["text"])
    return images, "".join(text)


def cost(messages, response, model):
    # TODO only works for simple messages
    images, text = parse_messages(messages)
    promt_image_tokens = sum([image_tokens(image) for image in images])
    text_tokens = token_counter(model=model, text=text)
    prompt_tokens = text_tokens + promt_image_tokens
    completion_tokens = token_counter(model=model, text=response)
    prompt_tokens_cost_usd_dollar, completion_tokens_cost_usd_dollar = (
        cost_per_token(
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
        )
    )

    return prompt_tokens_cost_usd_dollar + completion_tokens_cost_usd_dollar

def complete(**kwargs):
    """complete the prompt with an llm"""
    text_stream = stream(**kwargs)
    try:
        for _, resp, cost in text_stream:
            continue
    except Exception as e:
        print(e)
        return None, None

    return resp, cost


@retry_with_exponential_backoff
def stream(
    messages=None,
    prompt=None,
    model="gpt-3.5-turbo-1106",
    temperature=0,
    max_tokens=4096,
    json_response=False,
    verbose=True,
    local_llm=None,
    output_path=None,
):
    """complete the prompt with an llm and log response to file"""
    response_format = {"type": "json_object"} if json_response and model != "gpt-4-vision-preview" else None

    if not messages:
        if not prompt:
            raise ValueError("messages or prompt must be provided")
        messages = [
            {
                "role": "user",
                "content": prompt,
            },
        ]

    if local_llm:
        model = local_llm

    if verbose:
        print("using model: " + model)

    stream = completion(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=messages,
        timeout=13,
        stream=True,
        response_format=response_format,
    )

    response_text = ""

    f = None
    if output_path:
        out_dir = os.path.dirname(output_path)
        if out_dir != '': # if no out_dir don't try to create it
            os.makedirs(out_dir, exist_ok=True)
        f = open(output_path, "w")

    for part in stream:
        ## check if res.choices[0].delta contains content field
        text_part = part.choices[0].delta.content or ""
        if len(text_part) > 0:
            if verbose:
                print(text_part, end="", flush=True)
            
            # append the new text to the file
            if f:
                f.write(text_part)
                f.flush()
                
            response_text += text_part
            yield text_part, response_text, 0

            
    if f:
        f.close()

    # params = {"model": model, "temperature": temperature, "max_tokens": max_tokens}

    prompt_cost = cost(messages, response_text, model)
    if json_response:
        # if using a model that doesn't support json_response, we need to cleanup the response
        response_text = cleanup_response_json(response_text)
        yield "", response_text, prompt_cost

    yield "", response_text, prompt_cost

    # print("\n")
    return  # response_text


def cleanup_response_json(response_text):
    """sometimes the response is not valid json, so we need to cleanup some markup"""
    # if startwith ```json
    if response_text.startswith("```json"):
        response_text = response_text[7:]
    if response_text.startswith("```"):
        response_text = response_text[3:]
    # if endswith ```
    if response_text.endswith("```"):
        response_text = response_text[:-3]
    return response_text
