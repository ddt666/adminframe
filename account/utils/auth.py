import random
from io import BytesIO

from django.core.mail import send_mail
from django.conf import settings

from PIL import Image, ImageDraw, ImageFont



def get_valid(length=6, width=200, height=40):
    def get_random_color():
        """
        随机颜色
        :return:
        """
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    img = Image.new(mode="RGB", size=(width, height), color=get_random_color())
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font="static/font/kumo.ttf", size=32)

    random_str = ""
    for i in range(length):
        random_num = str(random.randint(0, 9))
        random_lower = chr(random.randint(97, 122))
        random_upper = chr(random.randint(65, 90))
        random_char = random.choice([random_num, random_lower, random_upper])
        draw.text(xy=(i * 25 + 15, 0), text=random_char, fill=get_random_color(), font=font)
        random_str += random_char

    # 干扰线，点
    # width=350
    # height=38
    # for i in range(5):
    #     x1 = random.randint(0, width)
    #     x2 = random.randint(0, width)
    #     y1 = random.randint(0, height)
    #     y2 = random.randint(0, height)
    #     draw.line((x1, y1, x2, y2), fill=get_random_color())
    #
    # for i in range(5):
    #     draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
    #     x = random.randint(0, width)
    #     y = random.randint(0, height)
    #     draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())

    f = BytesIO()
    img.save(f, "png")
    img_data = f.getvalue()
    return img_data, random_str.lower()




def send_email_code(email_code, to_email_list):
    res = send_mail("xxx-验证邮件", f"以下6位数字是邮箱验证码:{email_code}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=to_email_list)

    print("res", res)
