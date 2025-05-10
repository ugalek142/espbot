from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A3
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import black, red

# Подключаем шрифт
pdfmetrics.registerFont(TTFont("DejaVuSans", "DejaVuSans.ttf"))

# Настройки страницы
pdf_path = "50_fraz_na_ispanskom_dlya_poezdki.pdf"
c = canvas.Canvas(pdf_path, pagesize=A3)
width, height = A3

# Обложка (вставка изображения на весь лист)
cover_image = ImageReader("frazidlyaputeshestveya.png")
c.drawImage(cover_image, 0, 0, width=width, height=height)
c.showPage()

# Заголовок
c.setFont("DejaVuSans", 16)
c.setFillColor(red)
c.drawCentredString(width / 2, height - 2 * cm, "50 фраз на испанском для поездки")

y = height - 3 * cm
line_height = 14

def draw_section(title, phrases):
    global y
    c.setFont("DejaVuSans", 12)
    c.setFillColor(black)
    c.drawString(2 * cm, y, title)
    y -= 0.7 * cm
    c.setFont("DejaVuSans", 10)
    for phrase in phrases:
        if y < 2 * cm:
            c.showPage()
            y = height - 3 * cm
        c.drawString(2 * cm, y, f"– {phrase}")
        y -= line_height
    y -= 0.5 * cm

sections = {
    "Аэропорт": [
        "¿Dónde está la puerta de embarque? – Где выход на посадку?",
        "¿Dónde recojo mi equipaje? – Где получить багаж?",
        "¿Cuánto dura el vuelo? – Сколько длится полёт?",
        "¿Hay retraso en el vuelo? – Есть ли задержка рейса?",
        "¿Dónde está el control de pasaportes? – Где паспортный контроль?",
        "Tengo una conexión. – У меня пересадка.",
        "¿Dónde se facturan las maletas? – Где сдать багаж?",
        "¿Cuál es la puerta de salida? – Где выход на посадку?",
        "He perdido mi vuelo. – Я пропустил рейс.",
        "Mi equipaje no ha llegado. – Мой багаж не пришёл."
    ],
    "Отель": [
        "Tengo una reserva. – У меня бронь.",
        "¿Dónde está mi habitación? – Где моя комната?",
        "¿Hay desayuno incluido? – Завтрак включён?",
        "Necesito una toalla extra. – Мне нужно дополнительное полотенце.",
        "¿A qué hora es el check-out? – Во сколько выселение?",
        "¿Puedo tener la llave, por favor? – Можно ключ, пожалуйста?",
        "¿El Wi-Fi es gratuito? – Wi-Fi бесплатный?",
        "¿Hay servicio de habitaciones? – Есть обслуживание в номерах?",
        "¿Puedo pagar con tarjeta? – Можно оплатить картой?",
        "¿Dónde está el ascensor? – Где лифт?"
    ],
    "Кафе и рестораны": [
        "¿Tiene menú en inglés? – У вас есть меню на английском?",
        "¿Qué me recomienda? – Что вы посоветуете?",
        "Sin picante, por favor. – Без острого, пожалуйста.",
        "Una mesa para dos. – Столик на двоих.",
        "¿Cuánto cuesta esto? – Сколько это стоит?",
        "¿Está incluido el servicio? – Обслуживание включено?",
        "La cuenta, por favor. – Счёт, пожалуйста.",
        "Estoy alérgico a los frutos secos. – У меня аллергия на орехи.",
        "Solo quiero una bebida. – Я только напиток хочу.",
        "¿Dónde está el baño? – Где туалет?"
    ],
    "Транспорт": [
        "¿Dónde está la parada de autobús? – Где автобусная остановка?",
        "¿Cuánto cuesta un billete? – Сколько стоит билет?",
        "Un billete para el centro, por favor. – Один билет до центра, пожалуйста.",
        "¿Este tren va a Madrid? – Этот поезд идёт в Мадрид?",
        "¿Dónde está la estación? – Где станция?",
        "¿Cuánto tarda el metro? – Сколько едет метро?",
        "Necesito un taxi. – Мне нужно такси.",
        "¿Puede llevarme aquí? – Вы можете отвезти меня сюда?",
        "¿Este asiento está libre? – Это место свободно?",
        "¿Dónde bajo? – Где мне выходить?"
    ],
    "Покупки": [
        "¿Cuánto cuesta esto? – Сколько это стоит?",
        "¿Tiene otro color? – Есть другой цвет?",
        "¿Está en oferta? – Это по скидке?",
        "Solo estoy mirando. – Я просто смотрю.",
        "¿Puedo pagar en efectivo? – Можно оплатить наличными?",
        "¿Aceptan tarjeta? – Принимаете карту?",
        "¿Puedo probarlo? – Можно примерить?",
        "¿Tiene una bolsa? – У вас есть пакет?",
        "¿Dónde está el probador? – Где примерочная?",
        "Me lo llevo. – Я это беру."
    ]
}

for section, phrases in sections.items():
    draw_section(section, phrases)

c.save()
print("PDF с обложкой успешно создан.")
