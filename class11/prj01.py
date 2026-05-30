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
from something.function import WeatherAPI

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

#把WEATHER_API_KEY給WeatherAPI類別使用
weather_api = WeatherAPI(os.getenv("WEATHER_API_KEY"))

def build_weather_embed(weather_summary):
   #把整理好的天氣摘要排成Discord卡片
    embed = discord.Embed(
        title=f"{weather_summary['city_name']}的當前天氣",
        description=f"描述: {weather_summary['description']}",
        color=discord.Colour.from_str("#1E90FF"),  # 使用藍色作為卡片顏色
    )
    #get_icon_url()會把圖示代碼組成圖片網址，再放到卡片裡
    icon_url = weather_api.get_icon_url(weather_summary["icon_code"])
    embed.set_thumbnail(url=icon_url)
    embed.add_field(name="溫度", value=f"{weather_summary['temperature_celsius']}°C", inline=False)
    return embed
#######################事件#######################
# 在此定義Discord機器人事件(如 on_ready, on_message 等)
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
#######################指令#######################
# 在此定義Discord機器人的斜杠指令
@tree.command(name="hello", description="say hello to bot")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hey!")
#######################啟動#######################
# 在此定義機器人啟動邏輯
def main():
    bot.run(os.getenv("DC_BOT_TOKEN")) 
     # 從環境變數中獲取Discord機器人的令牌並啟動機器人
if __name__ == "__main__":
    main()
#/weather 的重點是:
#把[查資料]交給WeatherAPI，把[回應使用者]交給bot主程式處理
@tree.command(name="weather", description="取得當前天氣資訊")
async def weather(interaction: discord.Interaction, city_name: str):
    """輸入/weather 並提供城市名稱 就會回覆天氣"""
    #defer()會先告訴Discord[機器人正在處理中]
    #這樣就不會因為處理資料需要時間而讓使用者以為機器人沒反應
    await interaction.response.defer()

    city=city.strip() 
    if not weather_api.api_key:
        await interaction.followup.send("WEATHER_API_KEY未設定，請先在.env文件中設定")
        return