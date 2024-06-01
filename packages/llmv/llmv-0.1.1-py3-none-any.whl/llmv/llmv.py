import argparse
import datetime
import json
import os
import shutil
import llmv.chat as chat
from llmv.llm_template import LlmTemplate
import llmv.prompt as prompt


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-sf",
        "--system_prompt_path",
        help="the path to the system prompt",
    )
    parser.add_argument(
        "-s",
        "--system_prompt",
        help="System prompt to use, overrides --system_prompt_path if set",
    )
    
    parser.add_argument(
        "-pf",
        "--prompt_path",
        help="the path to the prompt template file",
    )
    
    parser.add_argument(
        "-p",
        "--user_prompt",
        help="User prompt to use, overrides --prompt_path if set",
    )
    
    parser.add_argument(
        "-i",
        "--images",
        nargs="*",
        help="path to images to include with the prompt, can be zero or more",
    )
    
    parser.add_argument(
        '-v',
        '--video',
        help='path to video file',    
    )

    # parser.add_argument(
    #     "--prompt_args",
    #     metavar="KEY=VALUE",
    #     nargs="*",
    #     help="""Set a number of key-value pairs (do not put spaces before or after the = sign). 
    #     If a value contains spaces, you should define it with double quotes: 
    #     foo="this is a sentence". Note that values are always treated as strings.""",
    # )

    parser.add_argument(
        "-m",
        "--model",
        help="the model to use, default is gpt-4o",
        default="gpt-4o",
    )
    
    parser.add_argument(
        "-o",
        "--output",
        help="path to output file",
        default = "out/res-" + datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".txt",
    )
    parser.add_argument(
        "-t",
        "--temperature",
        type=float,
        help="the temperature to use, default is 0",
        default=0,
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="enable debug mode",
    )
   
    args = parser.parse_args()
    
    piped_input = ""
    if not args.user_prompt and not args.prompt_path:
        while True:
            try:
                piped_input += input() + "\n"
            except EOFError:
                # no more information
                break
    
    print(piped_input)
    args.user_prompt = piped_input
    # if not args.system_prompt and not args.system_prompt_path and not args.user_prompt and not args.prompt_path:
    #     raise ValueError("No prompt provided, please provide either --system_prompt, --system_prompt_path, --user_prompt or --prompt_path")
    return args

def log_run(result, images, resized_images, label):
    log_folder = os.path.join("logs", label + "_" + datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
    os.makedirs(log_folder, exist_ok=True)
    for image in images:
        shutil.copy(image, log_folder)
    for image in resized_images:
        basename = os.path.basename(image)
        shutil.copy(image, os.path.join(log_folder, "resized_" + basename))
    
    with open(os.path.join(log_folder, "result.txt"), "w") as f:
        f.write(result)
    
    
def main():
    args = parse_args()
    # print(f"prompt_args: {prompt_args}")
    
    # load prompts from files
    system_prompt = None
    if args.system_prompt:
        system_prompt = args.system_prompt
    elif args.system_prompt_path:
        system_prompt, _= LlmTemplate.from_file(args.system_prompt_path).format()
    
    if args.user_prompt:
        user_prompt_base = args.user_prompt
    else:
        user_prompt_base, _ = LlmTemplate.from_file(args.prompt_path).format()
        
    
    # resize images for faster and cheaper inference
    resize = "1024x1024"
    resized_images = prompt.resize_images(args.images, resize)
    user_prompt = prompt.wrap_prompt(user_prompt_base, resized_images)
    
    if args.video: # TODO: ignoring images if video is present, should we try to combine them?
        user_prompt = prompt.video_prompt_messages(user_prompt_base, args.video)
    
    # prepare messages in openai format
    messages = prompt.wrap_system_prompt(system_prompt) + user_prompt
    
    json_response = False
    
    response_stream = chat.stream(
        messages=messages,
        model=args.model,
        temperature=args.temperature,
        verbose=False, # streams to stdout
        output_path=args.output,
        json_response=json_response,
    )
    
    for part, resp, cost in response_stream:
        print(part, end="", flush=True)
    
    if not json_response:
        return
    
    try:
        resp_json = json.loads(resp)
        label = resp_json["label"]
        resp_json["cost"] = cost
        log_run(resp, args.images, resized_images, label)
    except Exception as e:
        print(f"parsing response as json failed: {e}")
        print(f"cost: {cost}")


if __name__ == "__main__":
    main()


