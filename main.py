#
# Импорт библиотек
#

# Работа с элементами бота
from telebot.async_telebot import AsyncTeleBot
from telebot import types

# Запуск бота
import asyncio

# Работа с моделью
from transformers import AutoModelForCausalLM, AutoTokenizer
from audiocraft.models import musicgen
from scipy.io.wavfile import write
import torch

#
# Базовые значения
#

qwen_model_name = "Qwen/Qwen2.5-0.5B-Instruct"
qwen_model = AutoModelForCausalLM.from_pretrained(
    qwen_model_name,
    torch_dtype="auto"
).to('cuda')
tokenizer = AutoTokenizer.from_pretrained(qwen_model_name)

model = musicgen.MusicGen.get_pretrained('medium', device='cuda')
model.set_generation_params(duration=10)

#
# Работа с ботом
#

# Определение бота
bot = AsyncTeleBot('7602640476:AAEAGJbWCLA3V6JsKf1bt2yKdM4NKMxpLgY')


# Получение значений для модели
def generate_text_for_MusicGen(user_text):
    messages = [
        {"role": "system", "content": """
        Describe the essence of the text in a few words. Suggest the mood, genre of the song and BPM for the text-to-audio generation model MusicGen.
        Write the answer in the format:
        Scenario: *scenario text*
        Mood: *mood text*
        Genre: *genre text*
        BPM: *bpm text* 
        """},
        {"role": "user", "content": user_text}
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(qwen_model.device)

    generated_ids = qwen_model.generate(
        **model_inputs,
        max_new_tokens=100
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response


# Указание действий при запуске бота
@bot.message_handler(commands=['start'])
async def welcome(message):
    # Сообщение для отображения
    text = "Hi! Write a scenario for which you want to generate music."

    # Отправка действий в бота
    await bot.send_message(message.chat.id, text=text)

# Генерация аудиофайла
async def generate_music(message):
    scenario = message.text

    data = generate_text_for_MusicGen(scenario)
    # Разделяем строку по символам ':' и '\n'
    split_data = data.replace('\n', ':').split(':')

    # Генерация музыки
    query = split_data[1]+"; Mood: "+split_data[3]+"; Genre: "+split_data[5]+"; BPM: "+split_data[7]
    await bot.send_message(message.chat.id, text=f"Generating music for request: {query}")
    
    res = model.generate([query], progress=True)
    
    # Сохранение аудиофайла
    file_path = f"{split_data[1]}.wav"
    audio_array = res[0].cpu().numpy()  # Преобразуем в numpy-массив
    write(file_path, 32000, audio_array.T)  # Сохраняем WAV-файл (частота 32000 Hz)
    
    # Отправка аудиофайла
    with open(file_path, 'rb') as audio:
        await bot.send_audio(message.chat.id, audio, caption="Here is your generated music!")

# Указание действий при получении текстового сообщения
@bot.message_handler(content_types=['text'])
async def handle_text(message):
    await generate_music(message)

# Запуск бота
asyncio.run(bot.polling(none_stop=True, interval=0))