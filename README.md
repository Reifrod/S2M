# S2M
This project is a Telegram bot that generates music from a text script using the MusicGen model and the Qwen language model. The presentation of this project can be viewed [here](https://docs.google.com/presentation/d/1I49EQbilwWPcnc3723yLJTPR3WqFVosJ8ViBYPTXq-0/edit)

Link to telegram bot: [@project_s2m_bot](https://t.me/project_s2m_bot)

## Team members

- [Artem Sebalo](https://github.com/artemcd)
- [Maxim Hohryakov](https://github.com/standal0n3max)
- [Evgenii Kushakov](https://github.com/Reifrod)
- [Timofey Chernobrovkin](https://github.com/LesostepnoyGnom)

## Main features

- Generate music based on a text script.
- Automatically detect the mood, genre and tempo of the music.
- Send the generated audio file to the user in Telegram.

## Installation and launch

### Requirements

- Python 3.10.11
- CUDA (if using GPU)
- FFmpeg (for working with audio files)

### Installing dependencies

1. Clone the repository:
   ```bash
   git clone https://github.com/Reifrod/S2M.git
   cd S2M
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Make sure you have FFmpeg installed. To install on different platforms:
   - Windows: Download from the [official website](https://ffmpeg.org/download.html) and add to PATH.
   - Linux:
     ```bash
     sudo apt install ffmpeg
     ```
   - macOS:
     ```bash
     brew install ffmpeg
     ```

### Launching the bot

Run the bot with the command:

```bash
python bot.py
```

## Usage

- Start a conversation with the bot by sending the `/start` command.
- Write a scenario for which you want to generate music.
- The bot will automatically generate music and send you an audio file.

## Model training (SFT.ipynb)

The `SFT.ipynb` file contains code for fine-tuning the MusicGen model on your dataset. This notebook allows you to tailor the model to specific tasks, such as generating music in a specific genre or style.

### How to use SFT.ipynb

1. Open a notebook in Jupyter Notebook or Google Colab.
2. Make sure you have all the required dependencies installed:
   ```bash
   pip install torch audiocraft transformers
   ```
3. Upload your training dataset. The data must be in a format supported by MusicGen (e.g. WAV files).
4. Run the notebook cells in order:
   - Loading data.
   - Preparing the model.
   - Configuring training parameters.
   - Starting training.
5. Once training is complete, save the model and use it in your bot.

## Project structure
```
S2M/
├── bot.py # Main bot script
├── SFT.ipynb # Notebook for training the model
├── requirements.txt # List of dependencies
└── README.md # Documentation
```
