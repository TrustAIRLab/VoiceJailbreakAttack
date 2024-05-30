# Voice Jailbreak Attacks Against GPT-4o

[![arXiv: paper](https://img.shields.io/badge/arXiv-paper-red.svg)](https://arxiv.org/abs/2405.19103)
[![license: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is the official repository for [Voice Jailbreak Attacks Against GPT-4o](https://arxiv.org/abs/2405.19103). In this paper, we present the first study on how to jailbreak GPT-4o with voice.

**Disclaimer. This repo contains examples of harmful language. Reader discretion is recommended.**

## Code

1. Set your OpenAI key

```bash
echo "export OPENAI_API_KEY='YOURKEY'" >> ~/.zshrc
source ~/.zshrc
echo $OPENAI_API_KEY # check your key
```

2. Convert forbidden questions to audio files

```bash
python tts/prompt2audio.py --dataset baseline --voice fable
```

3. Convert text jailbreak prompts to audio files

```bash
python tts/prompt2audio.py --dataset textjailbreak --voice fable
```

Then, manually play each audio on GPT-4o to test its performance.

## Data

**Forbidden Questions**
* English: `data/question_set/questions_tiny.csv`
* Chinese: `data/question_set/questions_tiny_zh.csv`

**Prompts**

* Text jailbreak prompts: `data/jailbreak_prompts/text_jailbreak_prompts.csv`
* VoiceJailbreak prompts: `data/jailbreak_prompts/voicejailbreak.csv`
  * Plot format of the forbidden questions: `data/question_set/questions_tiny_plot.csv`

**Success Cases**
```
data/screenshot/
```

## Ethics
We take utmost care of the ethics of our study. Specifically, all experiments are conducted using two registered accounts and manually labeled by the authors, thus eliminating the exposure risks to third parties, such as crowdsourcing workers. Therefore, our work is not considered human subjects research by our Institutional Review Boards (IRB). We acknowledge that evaluating GPT-4o's capabilities in answering forbidden questions can reveal how the model can be induced to generate inappropriate content. This can raise concerns about potential misuse. We believe it is important to disclose this research fully. The methods presented are straightforward to implement and are likely to be discovered by potential adversaries. We have responsibly disclosed our findings to related LLM vendors.

## Citation
If you find this useful in your research, please consider citing:

```
@article{SWBZ24,
  author = {Xinyue Shen and Yixin Wu and Michael Backes and Yang Zhang},
  title = {{Voice Jailbreak Attacks Against GPT-4o}},
  journal = {{CoRR abs/2405.19103}},
  year = {2024}
}
```

## License
`VoiceJailbreak` is licensed under the terms of the MIT license. See LICENSE for more details.

