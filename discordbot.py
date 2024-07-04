import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import calendar
import datetime

TOKEN = 'TOKEN'
CHANNEL_ID = 1257704819410337842

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

events = []

# 폰트 설정 (Windows의 기본 한글 폰트 경로)
FONT_PATH = "C:/Windows/Fonts/malgunbd.ttf"  # 굵은 글꼴로 변경
FONT_SIZE = 14

# 달력을 이미지로 생성하는 함수
def create_calendar_image(year, month, events):
    print(f"Creating calendar image for {month}/{year} with events: {events}")

    cal = calendar.Calendar(calendar.SUNDAY)
    month_days = cal.monthdayscalendar(year, month)
    event_days = {day: [] for week in month_days for day in week if day != 0}

    for event in events:
        event_date = event['date']
        if event_date.month == month and event_date.year == year:
            event_days[event_date.day].append(event['event'])

    print(f"Event days: {event_days}")

    # 이미지 설정
    width, height = 1000, 750  # 이미지 크기 조정
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    event_font = ImageFont.truetype(FONT_PATH, FONT_SIZE - 2)  # 이벤트 표시용 폰트

    # 제목 그리기
    title = f"{calendar.month_name[month]} {year}"
    title_bbox = draw.textbbox((0, 0), title, font=font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text((width // 2 - title_width // 2, 10), title, fill="black", font=font)

    # 요일 그리기
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    for i, day in enumerate(days):
        draw.text((i * 140 + 20, 50), day, fill="black", font=font)

    # 날짜 그리기
    for week_num, week in enumerate(month_days):
        for day_num, day in enumerate(week):
            x = day_num * 140 + 20
            y = week_num * 100 + 100
            if day != 0:
                draw.text((x, y), str(day), fill="black", font=font)
                if day in event_days:
                    for i, event_text in enumerate(event_days[day]):
                        # 박스 크기 설정
                        box_x1, box_y1 = x, y + 20 + i * 35
                        box_x2, box_y2 = x + 120, y + 20 + (i + 1) * 35 - 5
                        draw.rounded_rectangle([box_x1, box_y1, box_x2, box_y2], radius=10, fill="#FF00FF")
                        draw.text((box_x1 + 10, box_y1 + 5), event_text, fill="white", font=event_font)  # 패딩 추가
                        print(f"Added event '{event_text}' on {month}/{day}/{year}")

    return image

# 임베드를 통해 달력을 보내는 함수
async def send_calendar_image():
    now = datetime.datetime.now()
    image = create_calendar_image(now.year, now.month, events)
    image_path = "calendar.png"
    image.save(image_path)
    print("Calendar image saved.")

    channel = bot.get_channel(CHANNEL_ID)
    
    # 이전에 보낸 메시지를 삭제
    async for message in channel.history(limit=10):
        if message.author == bot.user and message.attachments:
            await message.delete()
            print("Deleted old calendar message.")

    await channel.send(file=discord.File(image_path))
    print("Sent new calendar image.")

# 봇이 준비되었을 때 실행되는 이벤트
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await send_calendar_image()  # 봇이 시작되자마자 달력을 전송

# 일정 추가 명령어
@bot.command(name='일정추가', help='일정을 추가합니다. 예: !일정추가 2024-07-02 14:00 회의')
async def add_event(ctx, date: str, time: str, *, event: str):
    event_date = datetime.datetime.strptime(f'{date} {time}', '%Y-%m-%d %H:%M')
    events.append({'date': event_date, 'event': event})
    print(f'Event added: {event_date} - {event}')
    await ctx.send(f'일정이 추가되었습니다: {event_date} - {event}', delete_after=60)  # 60초 후 삭제
    await ctx.message.delete()
    await send_calendar_image()  # 이벤트 추가 후 달력을 즉시 갱신

# 일정 목록 명령어
@bot.command(name='일정목록', help='저장된 일정을 표시합니다.')
async def show_events(ctx):
    if events:
        event_list = '\n'.join([f"**{event['date'].strftime('%Y-%m-%d %H:%M')}** - {event['event']}" for event in events])
        await ctx.send('저장된 일정 목록:\n' + event_list, delete_after=60)  # 60초 후 삭제
    else:
        await ctx.send('저장된 일정이 없습니다.', delete_after=60)  # 60초 후 삭제
    await ctx.message.delete()

bot.run(TOKEN)
