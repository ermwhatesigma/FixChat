import pygame
import ollama
import threading
import time
import csv
import re
import random

name_chat_random = ["Homie", "Best Friend", "Girlfriend", "Boyfriend", "Dumb Homie", "Torta", "Huzz", "Buzz", "Chuzz", "Fine Shit", "The Fridge", "Walking Wallet", "The Fine Bro", "Quarter Pounder", "Fat Homie", "**Friend**", "The Home Girl", "Girl Bestfriend", "Guy Bestfriend", "Dominant Mommy", "Femboy twinky", "Tomboy", "Dommy Mommy", "Mommy", "Good Boy", "Good Girl"] #preloaded names i tought out the top of my head
all_genders = ["Female", "Male"] #there are only 2 genders

print("--- FixChat ---")
chat_name = input("Who are you texting?: ")
if not chat_name.strip():
    chat_name = random.choice(name_chat_random)

if chat_name == "":
    print(chat_name)
else:
    print(chat_name)

gender_ai = input("\nGender you wan't the person you are talking to be\nIf not said it will be random: ")
if not gender_ai.strip():
    gender_ai = random.choice(all_genders)

if gender_ai == "":
    print(f"{gender_ai}\n")
else:
    print(f"{gender_ai}\n")

pending_ai_message = None
is_thinking = False
scroll_y = 0  
max_scroll = 0

def clean_text_for_pygame(text):
    text = text.replace('\r', '')
    return re.sub(r'[^\x00-\x7F]+', '', text)

def save_diagnostic_files(text):
    with open("diagnostic_report.txt", "w", encoding="utf-8") as f:
        f.write(text)
    
    with open("chat_stats.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Category", "Feedback"])
        lines = text.split('\n')
        for line in lines:
            if ":" in line:
                writer.writerow(line.split(":", 1))
            else:
                writer.writerow(["Note", line])

def chat_worker(history, model="qwen3-vl:8b"): #AI model you will be talking to. You can change it to what you want.
    global pending_ai_message, is_thinking
    system_personality = (
        "You are a human comunicating with a human. You act and sound like a human. Don't say things that are imposible"
        "Use Gen-Z slang naturally. DON'T SPAM THE SLANG"
        "MAKE NORMAL GOOD ENGLISH SENTENCES"
        "Try Keeping replies short."
        "YOU ARE NOT AN AI SO DON'T ACT LIKE ONE EITHER"
        "Never use emoji's. Thats cringe."
        "Just a normal person on their phone. Talking to a friend"
        "DON'T REPEAT THINGS YOU ALREADY ASKED OR SAID"
        "DON'T MENTION ANYTHING HERE ABOVE"
        f"You are an {gender_ai} so act like a {gender_ai}"
    )

    messages = [{'role': 'system', 'content': system_personality}]
    for msg in history:
        messages.append({'role': msg['role'], 'content': msg['text']})
    try:
        response = ollama.chat(model=model, messages=messages, options={'temperature': 1.0})
        pending_ai_message = response['message']['content']
    except Exception as e:
        pending_ai_message = f"Error: {e}"
    is_thinking = False

def diagnostic_worker(history, model="qwen3-vl:8b"): #Model that will analyze your chat and give you feedback on how to improve. You can change it to what you want but make sure it can do the task well or the feedback will be bad.
    global pending_ai_message, is_thinking
    print("--- Diagnostic started ---")

    try:
        ollama.generate(model=model, prompt='', keep_alive=0)
    except:
        pass

    convo_text = ""
    last_ai_msg = ""

    for msg in history:
        if msg["role"] == "assistant":
            last_ai_msg = msg["text"]
        elif msg["role"] == "user" and last_ai_msg:
            convo_text += f"MESSAGE: {last_ai_msg}\nREPLY: {msg['text']}\n\n"
            last_ai_msg = ""

    diagnostic_system = (
        "You are a texting coach analyzing ONLY the user's replies.\n"
        "Conversation format:\n"
        "MESSAGE: what the other person said\n"
        "REPLY: what the user said\n\n"
        "IMPORTANT RULES:\n"
        "- The user ONLY wrote the REPLY lines\n"
        "- MESSAGE lines are NOT written by the user\n"
        "- NEVER evaluate or judge MESSAGE lines\n"
        "- NEVER say the user wrote a MESSAGE\n"
        "- ONLY judge how the REPLY matches the MESSAGE energy\n"
        "- Focus only on REPLY enthusiasm, effort, engagement, and energy match\n\n"
        "OUTPUT FORMAT (strict):\n"
        "dryness score: <1-10>\n"
        "reason: <short explanation about the REPLY>\n"
        "tips: <how the user can improve future replies>\n\n"
        "Plain text only."
    )

    messages = [
        {"role": "system", "content": diagnostic_system},
        {"role": "user", "content": convo_text}
    ]

    try:
        response = ollama.chat(model=model, messages=messages, options={'temperature': 0.8})
        report = response["message"]["content"]
        save_diagnostic_files(report)
        pending_ai_message = "DIAGNOSTIC RESULT\n" + report
        print(f"{report}")
        print("--- Diagnostic finished ---")
    except Exception as e:
        pending_ai_message = f"Diagnostic Error: {e}"

    is_thinking = False

def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        if font.size(word)[0] > max_width:
            for char in word:
                test_line = current_line + char
                if font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = char
            current_line += " "
            continue

        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "

    if current_line:
        lines.append(current_line.strip())

    return lines


def draw_bubble(surface, text, font, x, y, max_width, is_user):
    TEXT_COLOR = (255, 255, 255)
    USER_BG = (10, 132, 255)
    AI_BG = (60, 60, 60)

    bg_color = USER_BG if is_user else AI_BG
    text = clean_text_for_pygame(text)

    lines = wrap_text(text, font, max_width - 30)

    line_height = font.get_linesize()
    bubble_height = (len(lines) * line_height) + 20
    bubble_width = max_width

    if is_user:
        x = surface.get_width() - bubble_width - 15

    if y + bubble_height > 60 and y < 680:
        pygame.draw.rect(surface, bg_color, (x, y, bubble_width, bubble_height), border_radius=15)
        for i, line in enumerate(lines):
            text_surf = font.render(line, True, TEXT_COLOR)
            surface.blit(text_surf, (x + 15, y + 10 + (i * line_height)))

    return bubble_height


pygame.init()

WIDTH, HEIGHT = 400, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f"Chat with {chat_name}")
font = pygame.font.SysFont("Helvetica", 18)
clock = pygame.time.Clock()

chat_history = []
user_text = ""
cursor_timer = time.time()
cursor_visible = True

is_thinking = True
starter_thread = threading.Thread(target=chat_worker, args=([{"role": "user", "text": "yo say hi and start a convo with me"}],))
starter_thread.start()

running = True
while running:
    screen.fill((20, 20, 20))

    if pending_ai_message is not None:
        chat_history.append({"role": "assistant", "text": pending_ai_message})
        pending_ai_message = None
        scroll_y = max_scroll

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if event.button == 4:
                scroll_y = min(0, scroll_y + 30)
            if event.button == 5:
                scroll_y -= 30

            if 10 <= mx <= 110 and 10 <= my <= 40 and not is_thinking:
                is_thinking = True
                threading.Thread(target=diagnostic_worker, args=(chat_history,)).start()

        if event.type == pygame.KEYDOWN and not is_thinking:
            if event.key == pygame.K_RETURN and user_text.strip() != "":
                chat_history.append({"role": "user", "text": user_text})
                user_text = ""
                is_thinking = True
                threading.Thread(target=chat_worker, args=(chat_history,)).start()
            elif event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += event.unicode

    if time.time() - cursor_timer > 0.5:
        cursor_visible = not cursor_visible
        cursor_timer = time.time()

    total_chat_height = 0
    current_draw_y = 70 + scroll_y

    for message in chat_history:
        text = message.get("text")
        if not text or str(text).strip() == "" or text == []:
            continue

        is_user = (message["role"] == "user")
        h = draw_bubble(screen, text, font, 15, current_draw_y, 250, is_user)
        current_draw_y += h + 10
        total_chat_height += h + 10


    if is_thinking:
        draw_bubble(screen, "...", font, 15, current_draw_y, 100, False)
        total_chat_height += 50

    input_area_width = WIDTH - 60
    placeholder = "Message..."
    text_to_wrap = user_text if user_text else placeholder
    input_lines = wrap_text(clean_text_for_pygame(text_to_wrap), font, input_area_width)

    if cursor_visible:
        if user_text:
            input_lines[-1] += "|"
        else:
            input_lines[0] = placeholder + "|"

    line_height = font.get_linesize()
    input_height = 70 + max(0, (len(input_lines)-1)*line_height)

    max_scroll = min(0, (HEIGHT - input_height - 80) - total_chat_height)
    if scroll_y < max_scroll:
        scroll_y = max_scroll

    pygame.draw.rect(screen, (30, 30, 30), (0, 0, WIDTH, 60))
    header_text = font.render(chat_name, True, (255, 255, 255))
    screen.blit(header_text, (WIDTH//2 - header_text.get_width()//2, 18))

    btn_rect = pygame.Rect(10, 10, 100, 30)
    pygame.draw.rect(screen, (70, 70, 70), btn_rect, border_radius=8)
    btn_text = font.render("Analyze", True, (255, 255, 255))
    screen.blit(btn_text, (btn_rect.centerx - btn_text.get_width()//2,
                           btn_rect.centery - btn_text.get_height()//2))

    pygame.draw.rect(screen, (30, 30, 30), (0, HEIGHT - input_height, WIDTH, input_height))
    pygame.draw.rect(screen, (40, 40, 40),
                     (15, HEIGHT - input_height + 15, WIDTH - 30, input_height - 30),
                     border_radius=20)

    start_y = HEIGHT - input_height + 25
    for i, line in enumerate(input_lines):
        color = (255,255,255) if user_text else (150,150,150)
        surf = font.render(line, True, color)
        screen.blit(surf, (30, start_y + i*line_height))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()