import os
import argparse
from tqdm import tqdm
from datasets import load_dataset
from openai import OpenAI
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser(description="Standard Voice Generator")
    parser.add_argument("--voice", type=str, default='alloy',help="standard voices from openai tts",)
    parser.add_argument("--dataset", type=str, default='test')
    args = parser.parse_args()
    return args
   
def construct_advanced_prompt(prompt, question):
    if prompt is not None:
        try:
            format_prompt = prompt.format(question=question) if "{question}" in prompt else prompt + "\n" + question
        except:
            format_prompt = prompt.replace("{question}", question)
        assert question in format_prompt # double check, in case the prompt is not correctly formatted
    else:
        format_prompt = question
    return format_prompt

def create_standard_audio(args, audio_root, meta_filename, prompt_dataset,  meta_df):
    client = OpenAI()
    for item in tqdm(prompt_dataset):
        idx, question = item['id'], item['question']
        audio_path = os.path.join(audio_root, f'{idx}_{question}.wav')
        prompt = construct_advanced_prompt(None, question)
        response = client.audio.speech.create(model="tts-1", voice=args.voice, input=prompt, response_format='wav')
        
        response.write_to_file(audio_path)
        item.update({'dataset': args.dataset, 'voice': args.voice, 'question': question, 'prompt': prompt, 'jailbreak_id': -1, 'voice_category': 'standard', 'audio_path': audio_path})
        meta_df = pd.concat([meta_df, pd.DataFrame(item, index=[0])], ignore_index=True)
        meta_df.to_csv(meta_filename, index=False)
        print("Audio file save to ", audio_path)


def write_audio_files(audio_path, response):
    mode = "ab" if os.path.exists(audio_path) else "wb"
    with open(audio_path, mode=mode) as f:
        for data in response.response.iter_bytes():
            f.write(data)


def create_jailbreak_standard_audio(args, audio_root, meta_filename, prompt_dataset,  meta_df, jailbreak_dataset):
    client = OpenAI()
    for jailbreak_item in jailbreak_dataset:
        jid, jailbreak_prompt = jailbreak_item['id'], jailbreak_item['prompt']
        print(f"------------ Jailbreak Prompt: {jid} ------------")
        for item in tqdm(prompt_dataset):
            idx, question = item['id'], item['question']
            audio_path = os.path.join(audio_root, f'{jid}_{idx}_{question}.wav')
            if os.path.exists(audio_path):
                continue
            prompt = construct_advanced_prompt(jailbreak_prompt, question)
            # split the prompt into chunks of 4000 characters
            for chunks in range(0, len(prompt), 4000):
                response = client.audio.speech.create(model="tts-1", voice=args.voice, input=prompt[chunks:chunks+4000], response_format='wav')
                write_audio_files(audio_path, response)

            item.update({'jailbreak_id': jid , 'prompt': prompt, 'question': question, 'dataset': args.dataset, 'voice_category': 'standard', 'voice': args.voice, 'audio_path':audio_path,})
            meta_df = pd.concat([meta_df, pd.DataFrame(item, index=[0])], ignore_index=True)
            meta_df.to_csv(meta_filename, index=False)
            print("Audio file save to ", audio_path)


if __name__ == "__main__":
    args = parse_args()
    # args.voice = "fable"
    # args.dataset = "textjailbreak"

    prompt_dataset_path = 'data/question_set/questions_tiny.csv'
    meta_filename = f'data/meta/standard_voice_{args.dataset}_{args.voice}.csv'
    audio_root = f'data/audio/standard_voice/{args.dataset}_{args.voice}/'
    
    os.makedirs(audio_root, exist_ok=True)
    
    if os.path.exists(meta_filename):
        meta_df = pd.read_csv(meta_filename, header=0)
        print(meta_df.head(1))
    else:
        os.makedirs('data/meta/', exist_ok=True)
        meta_df = pd.DataFrame(columns=['id', 'jailbreak_id', 'prompt', 'content_policy_id', 'content_policy_name', 'q_id', 'question', 'dataset', 'voice_category', 'voice', 'audio_path', 'characteristics', 'quality', 'response', 'label'])
    
    prompt_dataset = load_dataset('csv', data_files={'train': prompt_dataset_path})['train']
    
    if args.dataset == 'textjailbreak':
        jailbreak_dataset = load_dataset('csv', data_files={'train': 'data/jailbreak_prompts/text_jailbreak_prompts.csv'})['train']
        create_jailbreak_standard_audio(args, audio_root, meta_filename, prompt_dataset, meta_df, jailbreak_dataset)
    elif args.dataset == 'baseline':
        create_standard_audio(args, audio_root, meta_filename, prompt_dataset, meta_df)
    else:
        raise ValueError("Invalid dataset")
    