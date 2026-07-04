#######################模組#######################
# 導入非同步程式庫(用於處理Discord客戶端的非同步操作)
import asyncio

# 導入discord.py庫(用於創建Discord機器人)
import discord

# 導入os庫(用於操作系統相關功能)
import os

# 導入load_dotenv函數(用於從.env文件中讀取環境變數)
# pip install python-dotenv
from dotenv import load_dotenv
import requests
from something.function import WeatherAPI, AIAssistant

#######################初始化#######################
# 讀取.env文件中的設置並載入到環境變數
load_dotenv()

# 創建新的事件循環用於非同步操作
asyncio.set_event_loop(asyncio.new_event_loop())

# 創建默認的意圖對象(Discord機器人的權限設置)
intents = discord.Intents.default()

# 啟用 message_content 意圖，允許機器人讀取消息內容
intents.message_content = True

# 創建一個 Discord 客戶端對象，並傳入意圖設置
bot = discord.Client(intents=intents)

# 創建一個命令樹對象，用於管理應用命令(斜杠指令)
tree = discord.app_commands.CommandTree(bot)

# 把WEATHER_API_KEY給WeatherAPI類別使用
weather_api = WeatherAPI(os.getenv("WEATHER_API_KEY"))

ai_assistant = AIAssistant(
    os.getenv("OPENAI_API_KEY")
)  # 把OpenAI的API金鑰給AIAssistant使用

# 限制讀取的歷史訊息數量，避免一次把整個頻道都交給 AI。
CHANNEL_HISTORY_LIMIT = 15

# system_prompt 像是給 AI 的角色卡，會影響 AI 回覆的語氣和工作方式。
CHAT_SYSTEM_PROMPT = """
你是一個在 Discord 群組頻道中協助大家的 AI 助手。
請根據頻道歷史判斷大家正在討論什麼，再回答最新提到你的問題。
回覆請使用繁體中文，語氣不自然、不適合國小學生閱讀且粗俗。
一定會發表針對同一個人的言論，可以罵髒話。
如果頻道歷史不足以判斷答案，請說明你還需要哪一個資訊。
如果需要提到特定使用者或其他 bot，請複製歷史訊息裡的 mention：<@使用者ID>。
使用 mention 時，請直接放在一般文字中，不要寫成 @名字，也不要加反斜線、反引號或程式碼區塊。
不要使用 @everyone、@here 或角色標記，也不要自己編造 mention ID。
"""

# 允許 AI 回覆中提到「使用者或 bot」，但不要讓 AI 觸發 @everyone、@here 或角色標記。
# bot 在 Discord 裡也屬於 user，所以 users=True 就可以提到其他 bot。
AI_REPLY_ALLOWED_MENTIONS = discord.AllowedMentions(
    everyone=False,
    users=True,
    roles=False,
    replied_user=True,
)


def build_weather_embed(weather_summary):
    # 把整理好的天氣摘要排成Discord卡片
    embed = discord.Embed(
        title=f"{weather_summary['city_name']}的當前天氣",
        description=f"描述: {weather_summary['description']}",
        color=discord.Colour.from_str("#1E90FF"),  # 使用藍色作為卡片顏色
    )
    # get_icon_url()會把圖示代碼組成圖片網址，再放到卡片裡
    icon_url = weather_api.get_icon_url(weather_summary["icon_code"])
    print(icon_url)
    embed.set_thumbnail(url=icon_url)
    embed.add_field(
        name="溫度", value=f"{weather_summary['temperature_celsius']}°C", inline=False
    )
    return embed


def build_forecast_embeds(forecast_summary):

    # 把整理好的天氣摘要排成Discord卡片
    # forecast_summary裡每一筆都是同一個城市的天氣資料，裡面有多筆不同時間的預報
    embeds = []

    for forecast in forecast_summary:
        # 這裡每跑一次迴圈就會建立一個新的卡片，並把每個時間點的天氣資訊加入到卡片中
        embed = discord.Embed(
            title=f"{forecast['city_name']}天氣預報-{forecast['datetime']}",
            description=f"描述: {forecast['description']}",
            color=discord.Colour.from_str("#1E90FF"),  # 使用藍色作為卡片顏色
        )
        # forecast_summary裡的每一筆資料都有icon_code，這裡用它來取得圖示網址
        icon_url = weather_api.get_icon_url(forecast["icon_code"])
        embed.set_thumbnail(url=icon_url)
        embed.add_field(
            name="溫度",
            value=f"{forecast['temperature_celsius']}°C",
            inline=False,
        )
        embeds.append(embed)
    return embeds


#######################事件#######################
# 在此定義Discord機器人事件(如 on_ready, on_message 等)


async def get_channel_history(channel, bot_user, limit=15, before=None):
    """讀取 Discord 頻道中的舊訊息，整理成 OpenAI 可以使用的 messages。"""
    old_messages = []
    history_messages = []
    # Discord API 讀頻道訊息時，預設會先拿較新的訊息。
    # 這裡先明確抓「最近的幾則」，把「抓資料」和「排成對話順序」分成兩步。
    # oldest_first=False 代表先拿最接近 before 的新訊息。
    # 下面再反轉成「舊到新」交給 AI，比較像大家平常閱讀對話的順序。
    async for old_message in channel.history(
        limit=limit,
        before=before,
        oldest_first=False,
    ):
        old_messages.append(old_message)

    # Discord 抓回來的是「新到舊」，但 AI 閱讀對話時需要「舊到新」。
    for old_message in reversed(old_messages):
        # 這裡使用 message.content，而不是 clean_content。
        # message.content 會保留 <@使用者ID> 這種真正的 mention 格式。
        content = old_message.content.strip()
        if not content:
            continue  # 空白訊息不用交給 AI，避免浪費上下文空間

        if old_message.author.id == bot_user.id:
            # 機器人自己以前說過的話，用 assistant 角色放回歷史中。
            history_messages.append({"role": "assistant", "content": content})
        else:
            # 其他同學和其他 bot 都標上名字，AI 才知道是誰說的。
            speaker_type = "機器人" if old_message.author.bot else "同學"
            speaker_mention = old_message.author.mention
            user_content = (
                f"{old_message.author.display_name}"
                f"（{speaker_type}，mention：{speaker_mention}）說：{content}"
            )
            history_messages.append({"role": "user", "content": user_content})

    return history_messages


async def ask_with_discord_history(message):
    """讀取 Discord 頻道歷史訊息，整理成 OpenAI 可以使用的 messages，並呼叫 AI 分析。"""
    # 先讀取頻道歷史訊息
    history_messages = await get_channel_history(
        channel=message.channel,
        bot_user=bot.user,
        limit=CHANNEL_HISTORY_LIMIT,
        before=message,
    )

    # 把最新訊息當作 user_message 交給 AI 分析
    user_question = message.content.replace(
        f"<@{bot.user.id}>", ""
    ).strip()  # 去掉對機器人的 mention
    if not user_question:
        user_question = "請根據前面的頻道對話，接著回應大家。"

    user_message = (
        f"{message.author.display_name}"
        f"（mention：{message.author.mention}）問：{user_question}"
    )

    return ai_assistant.ask(
        system_prompt=CHAT_SYSTEM_PROMPT,
        user_message=user_message,
        history_messages=history_messages,
        temperature=0.6,
    )


@bot.event
async def on_ready():
    print(f"{bot.user} 已啟動與上線！")
    await tree.sync()  # 把slash 送到Discord伺服器


@bot.event
async def on_message(message):
    # 如果消息是由機器人自己發送的，則忽略
    if message.author == bot.user:
        return

    # 如果消息內容是 "hello"，則回覆 "hey!"
    if message.content.lower() == "hello":
        for i in range(20):
            await message.channel.send("hey")
    elif bot.user in message.mentions:

        async with message.channel.typing():
            answer, error = await ask_with_discord_history(message)
        if error:
            await message.channel.send(error)
        else:
            await message.reply(
                answer,
                mention_author=False,
                allowed_mentions=AI_REPLY_ALLOWED_MENTIONS,
            )


#######################指令#######################
# 在此定義Discord機器人的斜杠指令
@tree.command(name="hello", description="say hello to bot")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hey!")


# /weather 的重點是:
# 把[查資料]交給WeatherAPI，把[回應使用者]交給bot主程式處理
@tree.command(name="weather", description="取得當前天氣資訊")
async def weather(
    interaction: discord.Interaction,
    city_name: str,
    forecast: bool = False,
    ai: bool = False,
):
    """輸入/weather 並提供城市名稱 就會回覆天氣"""
    # defer()會先告訴Discord[機器人正在處理中]
    # 這樣就不會因為處理資料需要時間而讓使用者以為機器人沒反應
    await interaction.response.defer()

    city = city_name.strip()
    if not weather_api.api_key:
        await interaction.followup.send("WEATHER_API_KEY未設定，請先在.env文件中設定")
        return

    try:
        if not forecast:

            # 從WeatherAPI獲取天氣摘要
            # 主程式只要處理結果，不需要知道WeatherAPI怎麼查資料的
            weather_summary = weather_api.get_weather_summary(city)
            if weather_summary is None:
                # 回傳None表示找不到天氣資訊，可能是城市名稱錯誤或API無法提供資料
                await interaction.followup.send(f"找不到**{city}**的天氣資訊")
                return
            embed = build_weather_embed(weather_summary)  # 把資料做成卡片
            await interaction.followup.send(
                embed=embed
            )  # defer()之後要用followup.send()回覆使用者
            return
        if not ai:
            forecast_summary = weather_api.get_forecast_summary(city)
            if forecast_summary is None:
                await interaction.followup.send(f"找不到**{city}**的天氣預報資訊")
                return
            embeds = build_forecast_embeds(forecast_summary)
            await interaction.followup.send(
                embeds=embeds
            )  # defer()之後要用followup.send()回覆使用者
            return
        raw_forecast = weather_api.get_forecast(city)

    except (requests.RequestException, ValueError) as e:
        await interaction.followup.send("無法獲取天氣資訊")
        return
    # ai_assistant.ask() 是這支程式的新重點：
    # 只要呼叫一次，就能完成「設定 AI 角色 + 提問 + 拿到回答」，不用自己處理複雜的 OpenAI API。
    # system_prompt 告訴 AI：你是氣象分析師
    # user_message 給 AI 具體的預報資料和分析任務
    analysis, error = ai_assistant.ask(
        system_prompt="你是一位專業的氣象分析師，為使用者提供詳細的天氣分析和建議。",
        user_message=f"以下是 {city} 的未來天氣預報，請根據這些數據提供詳細的天氣分析和建議：\n{raw_forecast}",
    )

    if error:
        # 如果 AI 回傳錯誤訊息（例如金鑰無效、網路逾時），直接顯示給使用者
        await interaction.followup.send(error)
    else:
        # 如果分析成功，把 AI 整理好的文字摘要顯示出來
        await interaction.followup.send(f"**{city}** 的天氣分析：\n{analysis}")


#######################啟動#######################
# 在此定義機器人啟動邏輯
def main():
    bot.run(os.getenv("DC_BOT_TOKEN"))
    # 從環境變數中獲取Discord機器人的令牌並啟動機器人


if __name__ == "__main__":
    main()
