
import telebot
from telebot import types
import json
import os
import time
import datetime
import pytz
TOKEN = "8041528980:AAEcUj-VokTFHnJ1hzvcZeLpgkmn0A2kDos"
bot = telebot.TeleBot(TOKEN)


def get_cambodia_datetime_as_string():
    """Return current date and time in Cambodia as a string 'YYYY-MM-DD HH:MM:SS'."""
    cambodia_tz = pytz.timezone("Asia/Phnom_Penh")
    now = datetime.datetime.now(cambodia_tz)
    return now.strftime("%Y-%m-%d %H:%M:%S")

#admin ids
ADMIN_ID = [7917444837]  # replace with actual
GROUP_ID = -1001443699476
#save all user ids
def save_user_ids_to_file():
    try:
        with open('user_ids.txt', 'r') as f:
            content = f.read()
            if content:
                user_ids = set(content.splitlines())
            else:
                user_ids = set()
    except FileNotFoundError:
        user_ids = set()
    
    with open('user_ids.txt', 'w') as f:
        f.write('\n'.join(sorted(list(user_ids))))


@bot.message_handler(func=lambda message: message.text == '/admin')
def broadcast_message(message):
    if message.from_user.id not in ADMIN_ID:
        bot.reply_to(message, "You don't have permission to do this!")
        return
    #check all user ids
    save_user_ids_to_file()
    total_users = len(open('user_ids.txt', 'r').readlines())
    bot.reply_to(message, f"អ្នកប្រើប្រាស់ សរុប: {total_users}")
    
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_cancel = types.KeyboardButton('បោះបង់')
    markup.add(button_cancel)
    bot.send_message(message.chat.id, "សូមផ្ញើសារ, សំឡេង, វីដេអូ ឬឯកសារដែលអ្នកចង់:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_admin_message)


def handle_admin_message(message):
    if message.from_user.id in ADMIN_ID:
        if message.text == 'បោះបង់':
            bot.send_message(message.chat.id, "បោះបង់", reply_markup=types.ReplyKeyboardRemove())
            return send_welcome(message)
        
        content_type = message.content_type
        caption = message.caption if hasattr(message, 'caption') else None
        
        try:
            with open('user_ids.txt', 'r') as f:
                user_ids = set(f.read().splitlines())
        except FileNotFoundError:
            user_ids = set()
        
        users_received = set()
        users_not_received = set()
        for user_id in list(user_ids):  # Convert set to list to avoid iteration issues
            try:
                if content_type == 'text':
                    bot.send_message(user_id, message.text)
                elif content_type == 'voice':
                    bot.send_voice(user_id, message.voice.file_id, caption=caption)
                elif content_type == 'video':
                    bot.send_video(user_id, message.video.file_id, caption=caption)
                elif content_type == 'photo':
                    bot.send_photo(user_id, message.photo[-1].file_id, caption=caption)
                elif content_type == 'document':
                    bot.send_document(user_id, message.document.file_id, caption=caption)
                users_received.add(user_id)
            except telebot.apihelper.ApiException:
                users_not_received.add(user_id)
        with open('user_ids.txt', 'w') as f:
            f.write('\n'.join(sorted(list(user_ids - users_not_received))))
        
        bot.send_message(
            message.chat.id, f"អ្នកប្រើប្រាស់ សរុប: {len(user_ids)}\n អ្នក ទទួលបាន សារ: {len(users_received)} \nអ្នក មិនទទួលបាន សារ: {len(users_not_received)}.")
        

GROUP_USERNAME = "@TSH_luy"
@bot.message_handler(func=lambda message: message.text == '/photo')
def handle_photo(message):
    bot.reply_to( message, "Please send the photo you want to share with the group.")
    bot.register_next_step_handler(message, process_photo)

# Step 2: Bot processes the photo and sends it to the group with buttons


def process_photo(message):
    # Get the photo file_id (highest resolution)
    photo_id = message.photo[-1].file_id

    # Get the caption from the photo (if admin included one)
    caption_text = message.caption if message.caption else ""

    # Create inline buttons
    keyboard = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton(
        text="🇬🇧 គ្រូ ភាសាអង់គ្លេស", url="https://t.me/Bellyallisa")
    button2 = types.InlineKeyboardButton(
        text="🇨🇳 គ្រូ ភាសាចិន", url="https://t.me/Vansasun")
    button3 = types.InlineKeyboardButton(
        text="🏫 គ្រូ ភាសាថ្នាក់ជាតិ", url="https://t.me/Sreyleabsan")
    button4 = types.InlineKeyboardButton(
        text="🧑‍🏫 ចុះឈ្មោះចូលរៀន គ្រូគរុកោសល្យ", url="https://t.me/ornmengang")
    button5 = types.InlineKeyboardButton(
        text="❓ សាកសួរ ព័ត៌មានផ្សេងៗ", url="https://t.me/ornmengang")

    # Arrange buttons (1 per row + 2 in one row)
    keyboard.add(button4)
    keyboard.add(button3)          # row 1
    keyboard.row(button1, button2)  # row 2
    keyboard.add(button5)          # row 3

    # Send photo to group with caption and buttons
    bot.send_photo(chat_id=GROUP_USERNAME, photo=photo_id,
                   caption=caption_text, reply_markup=keyboard)

    bot.reply_to(message, "Photo sent to the group successfully!")
    
markup = types.InlineKeyboardMarkup(row_width=2)

button1 = types.InlineKeyboardButton("កុំព្យូទ័រ 💻", callback_data="computer")
button2 = types.InlineKeyboardButton("គណិតវិទ្យា ➗", callback_data="math")
button3 = types.InlineKeyboardButton("គីមីវិទ្យា ⚗️", callback_data="chemistry")
button4 = types.InlineKeyboardButton("ជីវៈវិទ្យា 🧬", callback_data="biology")
button5 = types.InlineKeyboardButton("ភាសាកូរ៉េ 🇰🇷", callback_data="korean")
button6 = types.InlineKeyboardButton("ភាសាខ្មែរ 🇰🇭", callback_data="khmer")
button7 = types.InlineKeyboardButton("ភាសាចិន 🇨🇳", callback_data="chinese")
button9 = types.InlineKeyboardButton("ភាសាអង់គ្លេស 🇬🇧", callback_data="english")
button10 = types.InlineKeyboardButton("មត្តេយ្យ 🧸", callback_data="kindergarten")
button11 = types.InlineKeyboardButton("រូបវិទ្យា 🔭", callback_data="physics")

button12 = types.InlineKeyboardButton(
    "ចុះឈ្មោះចូលរៀន 📝", callback_data=" register"
)

button13 = types.InlineKeyboardButton(
    "មើលទីតាំងលើផែនទី 🗺️", callback_data= "map")

# 🆕 New buttons
button14 = types.InlineKeyboardButton(
    "ពិភាក្សាលើបញ្ហាគ្រូបង្រៀន 🗣️", url="https://t.me/TONGPOR001")
button15 = types.InlineKeyboardButton(
    "ជួបជាមួយក្រុមការងារ 👥", url="https://t.me/TONGPORHONG")
button16 = types.InlineKeyboardButton(
    "ប្រមូលសិនរបស់សាលា 🎉", callback_data="collect_items")
button17 = types.InlineKeyboardButton(
    "ចង់ផ្លាស់ប្ដូរគ្រូ 🔄", url="https://t.me/TONGPOR001")
button18 = types.InlineKeyboardButton(
    "ចង់បានគ្រូបន្ថែម ➕", url="https://t.me/TONGPORHONG")

markup.add(button1)
markup.add(button2, button3, button4, button5,
             button6, button7,button9, button10, button11)
markup.add(button14, button15)
markup.add(button17, button18)
markup.add(button16)
markup.add(button13,button12)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = str(message.from_user.id)
    
    # Save user_id to file if not already present
    try:
        with open('user_ids.txt', 'r') as f:
            user_ids = set(f.read().splitlines())
    except FileNotFoundError:
        user_ids = set()
    if user_id not in user_ids:
        user_ids.add(user_id)
        with open('user_ids.txt', 'w') as f:
            f.write('\n'.join(sorted(user_ids)))
        user_name = message.from_user.fast_name or "អតិថិជនថ្មីម្នាក់"
        mention = f"[{user_name}](tg://user?id={user_id})"
        bot_msg = (
                f"🆕 សារជូនដំណឹង៖ អតិថិជនថ្មីមកដល់ហើយ!\n\n"
                f"👋 សូមស្វាគមន៍ {mention} មកកាន់ក្រុមយើង ❤️\n"
                f"សូមអរគុណដែលបានជ្រើសរើសប្រើសេវារបស់យើង។\n\n"
            f"📅 ថ្ងៃចូលរួម៖ {get_cambodia_datetime_as_string()}"
            )

        bot.send_message(GROUP_ID, bot_msg, parse_mode='Markdown')
    # បង្កើត Inline Keyboard
    photo = 'https://t.me/TSH_midea/38'
    bot.send_photo(message.chat.id,photo,caption="សាលាបង្រៀនគួរពិសេស តុងប៉​ សូមស្វាគមន៍!\n\nសូមជ្រើសរើសមុខវិជ្ជាដែលលោក/លោកស្រីចង់រៀនខាងក្រោម៖", reply_markup=markup)



# === Use group ID instead of username ===
# Replace with your actual group ID

# Step 1: When admin sends /photo command

@bot.message_handler(commands=['photo'])
def handle_photo(message):
    bot.reply_to(message, "📸 សូមផ្ញើរូបភាពដែលអ្នកចង់ចែករំលែកទៅក្នុងក្រុម។")
    bot.register_next_step_handler(message, process_photo)

# Step 2: Process the received photo and send it to the group


def process_photo(message):
    if not message.photo:
        bot.reply_to(
            message, "⚠️ សូមផ្ញើជារូបភាពមែនទេ។ សូមព្យាយាមម្តងទៀតដោយប្រើ /photo។")
        return

    # Get highest resolution photo
    photo_id = message.photo[-1].file_id
    caption_text = message.caption if message.caption else ""

    # Inline buttons
    keyboard = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton(
        text="🇬🇧 គ្រូ ភាសាអង់គ្លេស", url="https://t.me/Bellyallisa")
    button2 = types.InlineKeyboardButton(
        text="🇨🇳 គ្រូ ភាសាចិន", url="https://t.me/Vansasun")
    button3 = types.InlineKeyboardButton(
        text="🏫 គ្រូ ភាសាថ្នាក់ជាតិ", url="https://t.me/Sreyleabsan")
    button4 = types.InlineKeyboardButton(
        text="🧑‍🏫 ចុះឈ្មោះចូលរៀន គ្រូគរុកោសល្យ", url="https://t.me/ornmengang")
    button5 = types.InlineKeyboardButton(
        text="❓ សាកសួរ ព័ត៌មានផ្សេងៗ", url="https://t.me/ornmengang")

    keyboard.add(button4)
    keyboard.add(button3)
    keyboard.row(button1, button2)
    keyboard.add(button5)

    try:
        # Send photo + caption + inline buttons to the group via group ID
        bot.send_photo(
            chat_id=GROUP_ID,
            photo=photo_id,
            caption=caption_text,
            reply_markup=keyboard
        )

        bot.reply_to(message, "✅ ផ្ញើររូបភាពទៅក្រុមដោយជោគជ័យ!")
    except Exception as e:
        bot.reply_to(message, f"❌ មានបញ្ហាក្នុងការផ្ញើរទៅក្រុម។\n{e}")
        
        

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    data = call.data

    if data == "computer":
        photo = 'https://t.me/TSH_midea/24'
        bot.send_photo(call.message.chat.id, photo,
                       caption="សូមស្វាគមន៍មកកាន់មុខវិជ្ជា កុំព្យូទ័រ", reply_markup=markup)

    elif data == "math":
        video = 'https://t.me/TSH_midea/35'
        bot.send_video(call.message.chat.id, video,
                       caption="សូមស្វាគមន៍មកកាន់មុខវិជ្ជា គណិតវិទ្យា", reply_markup=markup)

    elif data == "khmer":
        video = 'https://t.me/TSH_midea/30'
        bot.send_video(call.message.chat.id, video,
                       caption="សូមស្វាគមន៍មកកាន់មុខវិជ្ជា ភាសាខ្មែរ", reply_markup=markup)

    elif data == "chinese":
        video = 'https://t.me/TSH_midea/27'
        bot.send_video(call.message.chat.id, video,
                       caption="សូមស្វាគមន៍មកកាន់មុខវិជ្ជា ភាសាចិន", reply_markup=markup)

    elif data == "english":
        video = 'https://t.me/TSH_midea/29'
        bot.send_video(call.message.chat.id, video,
                       caption="សូមស្វាគមន៍មកកាន់មុខវិជ្ជា ភាសាអង់គ្លេស", reply_markup=markup)

    elif data == "kindergarten":
        video = 'https://t.me/TSH_midea/37'
        bot.send_video(call.message.chat.id, video,
                       caption="សូមស្វាគមន៍មកកាន់មុខវិជ្ជា មត្តេយ្យ", reply_markup=markup)

    elif data == "physics":
        video = 'https://t.me/TSH_midea/33'
        bot.send_video(call.message.chat.id, video,
                       caption="សូមស្វាគមន៍មកកាន់មុខវិជ្ជា រូបវិទ្យា", reply_markup=markup)

    elif data == "chemistry":
        video = 'https://t.me/TSH_midea/34'
        bot.send_video(call.message.chat.id, video,
                       caption="សូមស្វាគមន៍មកកាន់មុខវិជ្ជា រូបវិទ្យា", reply_markup=markup)

    elif data == "biology":
        video = 'https://t.me/TSH_midea/27'
        bot.send_video(call.message.chat.id, video,
                       caption="សូមស្វាគមន៍មកកាន់មុខវិជ្ជា រូបវិទ្យា", reply_markup=markup)

    elif data == "korean":
        video = 'https://t.me/TSH_midea/27'
        bot.send_video(call.message.chat.id, video,
                       caption="សូមស្វាគមន៍មកកាន់មុខវិជ្ជា ភាសាកូរ៉េ", reply_markup=markup)

    elif data == "thai":
        video = 'https://t.me/TSH_midea/27'
        bot.send_video(call.message.chat.id, video,
                       caption="សូមស្វាគមន៍មកកាន់មុខវិជ្ជា ភាសាថៃ", reply_markup=markup)

    # Only one 'map' block, cleaned
    elif data == "map":
        return map(call)
        # Alert message (short version)
    elif data == " register":
        return register(call)
        
        
    else:
        bot.answer_callback_query(call.id, "មុខវិជ្ជានេះនឹងមកឆាប់ៗនេះ!")
        
        
# Map on button click go to google map location
def map(call):
    bot.answer_callback_query(
        call.id,
        "📍 សូមជ្រើសរើសទីតាំងសាខា ⬇️",
        show_alert=True
    )

    # Inline buttons for locations
    markup_map = types.InlineKeyboardMarkup(row_width=1)


    btn1 = types.InlineKeyboardButton(
        "🏠 វិមានភ្នំពេញ (ផ្លូវជាសុផារ៉ា)",
        web_app=types.WebAppInfo("https://maps.app.goo.gl/F9FzzdFP31ufKjZs5")
    )

    btn2 = types.InlineKeyboardButton(
        "🏘️ មេគង្គរ៉ូយ៉ា ព្រែកលៀប (ផ្លូវជាតិលេខ6A)",
        web_app=types.WebAppInfo("https://maps.app.goo.gl/GZpevfDwuXAPUtGaA")
    )

    btn3 = types.InlineKeyboardButton(
        "🏢 កម្ពុព្រែកព្នៅ",
        web_app=types.WebAppInfo("https://maps.app.goo.gl/vKZpVh1zKre3ycDx7")
    )

    btn4 = types.InlineKeyboardButton(
        "🏫 វិមានភ្នំពេញ ព្រែកអញ្ជាញ (ផ្លូវជាតិលេខ6A)",
        web_app=types.WebAppInfo("https://maps.app.goo.gl/uE3UAm5xaZPUx4GF6")
    )

    markup_map.add(btn1, btn2, btn3, btn4, )

    bot.send_message(
        call.message.chat.id,
        "🗺️  សូមជ្រើសរើសទីតាំងសាខា Google Maps ⬇️",
        reply_markup=markup_map
    )
def register(call):
    bot.answer_callback_query(
        call.id,
        "📝 សូមចុចលើតំណរខាងក្រោមដើម្បីចុះឈ្មោះ៖",
        show_alert=True
    )
    markup_map = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton(
        "🏠 វិមានភ្នំពេញ (ផ្លូវជាសុផារ៉ា)",
        web_app=types.WebAppInfo(
            "https://docs.google.com/forms/d/e/1FAIpQLSe7HQT0aNWVi-eYqWnnRErM2k16jFo5oAVKEv21EmmOu2yaBw/viewform")
    )

    btn2 = types.InlineKeyboardButton(
        "🏘️ មេគង្គរ៉ូយ៉ា ព្រែកលៀប (ផ្លូវជាតិលេខ6A)",
        web_app=types.WebAppInfo(
            "https://docs.google.com/forms/d/e/1FAIpQLSffaO_Ex4qoKMEaPWZXlzEUERrUo4fPhpxL5weFYTaQBoI82Q/viewform")
    )

    btn3 = types.InlineKeyboardButton(
        "🏢 កម្ពុព្រែកព្នៅ",
        web_app=types.WebAppInfo(
            "https://docs.google.com/forms/d/e/1FAIpQLSdr7bBBSzkC33S-DOBe_n5ohVcZLJnjE93fWiLBQGzR0R6t4g/viewform")
    )

    btn4 = types.InlineKeyboardButton(
        "🏫 វិមានភ្នំពេញ ព្រែកអញ្ជាញ (ផ្លូវជាតិលេខ6A)",
        web_app=types.WebAppInfo(
            "https://docs.google.com/forms/d/e/1FAIpQLScryLQ4wal-i0A5SS1zlxUu-oWCXVDXPX97WLXC97Lufa-A5Q/viewform")
    )

    markup_map.add(btn1, btn2, btn3, btn4 )
    bot.send_message(
        call.message.chat.id,
        "📝 សូមចុចលើតំណរខាងក្រោមដើម្បីចុះឈ្មោះ៖",
        reply_markup=markup_map
    )
    
    





print("🤖 Bot is running...")
bot.infinity_polling()


