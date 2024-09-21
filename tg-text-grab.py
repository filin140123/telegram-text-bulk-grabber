import requests
import re

channel = input("Ссылка на канал: ")
start = input("Диапазон, с какого поста начать?: ")
count = input("Диапазон, до какого поста ищем?: ")


def get_post(link, num):
	url = f"{link}/{num}"
	r = requests.get(url).text

	start_phrase = '<meta property="og:description" content='
	end_phrase = '>'

	pattern = re.compile(rf'{re.escape(start_phrase)}(.|\n)*?{re.escape(end_phrase)}')
	match = pattern.search(r)

	return match.group()[len(start_phrase)+1:-2]

print("Формируем список...")

lines = []
for i in range(int(start), int(count)+1):
	strnum = str(i)
	post = get_post(channel, strnum)

	if post and (post not in lines):
		lines.append(post)
		print(f"Пост №{strnum} получен.")
	else:
		print(f"Пост №{strnum} пропущен: пост удален или дубликат")

filename = channel[13:]
print(f'Список готов, идет запись в файл "{filename}_{start}-{count}.txt"...')

with open(f'{filename}_{start}-{count}.txt', 'w', encoding="utf-8") as f:
    for line in lines:
        f.write(f"{line}\n\n---\n\n")

print("Готово.")
