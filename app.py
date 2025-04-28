
from flask import Flask, render_template, request
from lunar_python import Solar
import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        if 'today' in request.form:
            date = datetime.date.today()
        else:
            year = int(request.form['year'])
            month = int(request.form['month'])
            day = int(request.form['day'])
            date = datetime.date(year, month, day)

        solar = Solar.fromYmd(date.year, date.month, date.day)
        lunar = solar.getLunar()

        # 修正臘月顯示
        month_chinese = lunar.getMonthInChinese()
        if month_chinese == "腊":
            month_chinese = "十二"
        elif month_chinese =="冬":
             month_chinese = "十一"
        lunar_date = f"{month_chinese}月{lunar.getDayInChinese()}"

        zodiac_simple = lunar.getYearShengXiao()

        zodiac_mapping = {
            "鼠": "鼠",
            "牛": "牛",
            "虎": "虎",
            "兔": "兔",
            "龙": "龍",
            "蛇": "蛇",
            "马": "馬",
            "羊": "羊",
            "猴": "猴",
            "鸡": "雞",
            "狗": "狗",
            "猪": "豬"
}

        zodiac = zodiac_mapping.get(zodiac_simple, zodiac_simple)
        year_ganzhi = lunar.getYearInGanZhi()
        is_after_lichun = solar.getLunar().getJieQiTable().get("立春")
        if is_after_lichun and solar.toYmd() >= is_after_lichun.toYmd():
            lichun_info = "已過立春"
        else:
            lichun_info = "未過立春"

        result = {
            'solar_date': date.strftime('%Y-%m-%d'),
            'lunar_date': lunar_date,
            'zodiac': zodiac,
            'year_ganzhi': year_ganzhi,
            'lichun_info': lichun_info
        }

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
