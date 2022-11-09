import urllib3
import json

# Сгенерированные субтитры из видео https://www.youtube.com/watch?v=dQw4w9WgXcQ
# Получены путем открытия инструментов разработчика F12 и открытия вкладки "Сеть".
# Необходимо установить в фильтре слово "text" и включить-выключить субтитры у видео.
# Появившийся адрес устанавливается в переменную url
url = "https://www.youtube.com/api/timedtext?v=dQw4w9WgXcQ&caps=asr&xoaf=5&hl=ru&ip=0.0.0.0&ipbits=0&expire=1668038643&sparams=ip,ipbits,expire,v,caps,xoaf&signature=C974CED1EABC1C7B6EBBCE5CAA23A1AF6FE45FC0.B27023FFF8F23CFB436BB85A9B9EABB46FC690A6&key=yt8&kind=asr&lang=en&fmt=json3&xorb=2&xobt=3&xovt=3&cbr=Firefox&cbrver=106.0&c=WEB&cver=2.20221107.06.00&cplayer=UNIPLAYER&cos=Windows&cosver=10.0&cplatform=DESKTOP"

# Выходной файл
outfile = "subtitles as text.txt"

# Функция для получения текста из автоматических субтитров
def get_text(timedtext_url):
    # Используем родные библиотеки для загрузки файла по заданному пути
    http = urllib3.PoolManager()
    r = http.request('GET', timedtext_url)

    # Полученную информацию декодируем из UTF-8
    contents = r.data.decode("utf-8")

    # Объявляем массив букв, который будет заполняться по мере нахождения текста из полученного файла
    chars = []

    # Убеждаемся, что файл найден
    if "Error 404 (Not Found)" in contents:
        print("Недопустимый адрес субтитров")
        return " ".join(chars)

    # Десериализуем полученные данные
    json_obj = json.loads(contents)

    # Из массива events находим объекты, в которых есть текст (segs) и забираем оттуда полученный текст
    for event in json_obj["events"]:
        if 'segs' in event:
            for segment in event["segs"]:
                if '[Music]' not in segment["utf8"]:
                    chars.extend(segment["utf8"])

    # Собираем текст воедино
    result_text = "".join(chars)

    # Очищаем текст от переносов строк, чтобы получилась сплошная строка
    return result_text.strip().replace("\n", " ")

# Вызов получения текста по заданному выше урлу
final_text = get_text(url)

# Сохраняем полученный текст в файл
if len(final_text) > 0:
    with open(outfile, 'w') as f:
        f.write(final_text)

# Показываем в логе, что получилось
print(final_text)