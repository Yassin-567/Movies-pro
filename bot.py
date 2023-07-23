import os
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InputFile
import ffmpeg

API_TOKEN = "6192009745:AAEmB8TpAnPDYroterQfACHIzGT5r3B7p5E"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['start'])
async def on_start(message: types.Message):
    await message.reply("I am ready for videos!")

@dp.message_handler(content_types=types.ContentType.VIDEO)
async def on_video_received(message: types.Message):
    video_file = await bot.get_file(message.video.file_id)
    video_path = await video_file.download()
    
    # Compress video using ffmpeg
    compressed_video_path = "compressed_" + os.path.basename(video_path)
    ffmpeg.input(video_path).output(compressed_video_path, crf=30).run()
    
    # Send the compressed video back
    with open(compressed_video_path, 'rb') as video:
        await bot.send_video(message.chat.id, InputFile(video))
    
    # Clean up temporary files
    os.remove(video_path)
    os.remove(compressed_video_path)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
