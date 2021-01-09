import tkinter as tk
import requests
from bs4 import BeautifulSoup
from random import sample

# ----------------------------以下為爬蟲部分----------------------------


def cat(url):  # 有分類的食品
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")
    names_lst = []
    type_lst = []
    kcal_lst = []
    price_lst = []
    commodity = []
    for name in soup.find_all("name"):
        names_lst.append(name.text)
    for ty in soup.find_all("type"):
        type_lst.append(ty.text)
    for kcal in soup.find_all("kcal"):
        kcal_lst.append(kcal.text)
    for price in soup.find_all("price"):
        price_lst.append(price.text)
    for i in range(len(names_lst)):
        commodity.append([])
        commodity[i].append(names_lst[i])
        commodity[i].append(type_lst[i])
        if kcal_lst[i] == '':
            commodity[i].append(-1)  # 沒有標熱量記為-1
        else:
            commodity[i].append(float(kcal_lst[i]))
        try:
            commodity[i].append(float(price_lst[i]))
        except ValueError:
            commodity[i].append(price_lst[i])  # 依重量定價
    return commodity


def no_cat(url):  # 沒分類的食品
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")
    names_lst = []
    kcal_lst = []
    price_lst = []
    commodity = []
    for name in soup.find_all("name"):
        names_lst.append(name.text)
    for kcal in soup.find_all("kcal"):
        kcal_lst.append(kcal.text)
    for price in soup.find_all("price"):
        price_lst.append(price.text)
    for i in range(len(names_lst)):
        commodity.append([])
        commodity[i].append(names_lst[i])
        if kcal_lst[i] == '':
            commodity[i].append(-1)
        else:
            commodity[i].append(float(kcal_lst[i]))
        try:
            commodity[i].append(float(price_lst[i]))
        except ValueError:
            commodity[i].append(price_lst[i])
    return commodity


def slurpee(url):  # 思樂冰
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")
    names_lst = []
    kcal_lst = []
    price_lst = []
    commodity = []
    for name in soup.find_all("name"):
        names_lst.append(name.text)
    for kcal in soup.find_all("kcal"):
        kcal_lst.append(kcal.text)
    for price in soup.find_all("price"):
        price_lst.append(price.text.replace("\u3000", " "))
    for i in range(len(names_lst)):
        commodity.append([])
        commodity[i].append(names_lst[i])
        commodity[i].append(kcal_lst[i])
        commodity[i].append(price_lst[i])
    return commodity


def ice_cream(url):  # 霜淇淋
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")
    names_lst = []
    kcal_lst = []
    nutrition_lst = []
    material_lst = []
    price_lst = []
    commodity = []
    for name in soup.find_all("name"):
        names_lst.append(name.text)
    for nutrition in soup.find_all("nutrition"):
        word = nutrition.text
        kcal_lst.append(word[word.find("熱量") + 3: word.find("大卡")])
        nutrition_lst.append(nutrition.text)
    for material in soup.find_all("material"):
        material_lst.append(material.text)
    for price in soup.find_all("price"):
        price_lst.append(price.text)
    for i in range(len(names_lst)):
        commodity.append([])
        commodity[i].append(names_lst[i])
        commodity[i].append(float(kcal_lst[i]))  # 熱量
        commodity[i].append(nutrition_lst[i])  # 營養標示
        commodity[i].append(material_lst[i])  # 原料
        commodity[i].append(float(price_lst[i]))
    return commodity


headers = {"cookie": "_ga=GA1.3.838641886.1589788278; _gcl_au=1.1.301249334.1600693829; _gid=GA1.3.511170688.1608138116; ApplicationGatewayAffinityCORS=f8275e479131a9de50a78454cec80a71; ApplicationGatewayAffinity=f8275e479131a9de50a78454cec80a71; ASP.NET_SessionId=ssmvl1fms3t5ga45uaalx0fc; _gat=1",
           "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}

dic_cat = {"riceball": "https://www.7-11.com.tw/freshfoods/read_food_xml.aspx?=0", "freshfood": "https://www.7-11.com.tw/freshfoods/read_food_xml.aspx?=1", "soup_snack": "https://www.7-11.com.tw/freshfoods/read_food_xml.aspx?=3",
           "kanto_cooking": "https://www.7-11.com.tw/freshfoods/read_food_xml.aspx?=6", "hot_dog": "https://www.7-11.com.tw/freshfoods/read_food_xml.aspx?=7"}  # 御飯糰、光合、風味小食、關東煮、大亨堡

dic_nocat = {"t_dish": "https://www.7-11.com.tw/freshfoods/read_food_xml.aspx?=2", "f_dish": "https://www.7-11.com.tw/freshfoods/read_food_xml.aspx?=4",
             "cold_noodles": "https://www.7-11.com.tw/freshfoods/read_food_xml.aspx?=5", "bread": "https://www.7-11.com.tw/freshfoods/read_food_xml.aspx?=10"}  # 台式料理、異國料理、涼麵、麵包甜點

dic_slurpee = {
    "slurpee": "https://www.7-11.com.tw/freshfoods/read_food_xml.aspx?=9"}  # 思樂冰

dic_ice_cream = {
    "ice_cream": "https://www.7-11.com.tw/freshfoods/read_food_xml.aspx?=8"}  # 霜淇淋
# ---------------------------------------------------------
t_dish_all = no_cat(dic_nocat['t_dish'])  # 台式料理
f_dish_all = no_cat(dic_nocat['f_dish'])

# 主視窗
root = tk.Tk()
root.title("7-11 Chef")
root.geometry('800x600')
root.configure(background='medium sea green')

TDEE = float()


class Info(object):   # infopage
    def __init__(self, master=None):
        self.root = master
        self.page = tk.Frame(self.root)
        self.page.pack()
        self.getInfo()

    def getInfo(self):
        self.head_label = tk.Label(self.page, text='請輸入您的資料')
        self.head_label.pack()

        self.height = tk.StringVar()
        self.height_frame = tk.Frame(self.page)
        self.height_frame.pack()
        self.height_label = tk.Label(
            self.height_frame, text='身高（公分）')
        self.height_label.pack(side=tk.LEFT)
        self.height_entry = tk.Entry(
            self.height_frame, textvariable=self.height)
        self.height_entry.pack(side=tk.RIGHT)

        self.weight = tk.StringVar()
        self.weight_frame = tk.Frame(self.page)
        self.weight_frame.pack()
        self.weight_label = tk.Label(
            self.weight_frame, text='體重（公斤）')
        self.weight_label.pack(side=tk.LEFT)
        self.weight_entry = tk.Entry(
            self.weight_frame, textvariable=self.weight)
        self.weight_entry.pack(side=tk.RIGHT)

        self.age = tk.StringVar()
        self.age_frame = tk.Frame(self.page)
        self.age_frame.pack()
        self.age_label = tk.Label(
            self.age_frame, text='年齡')
        self.age_label.pack(side=tk.LEFT)
        self.age_entry = tk.Entry(self.age_frame, textvariable=self.age)
        self.age_entry.pack(side=tk.RIGHT)

        self.gender_frame = tk.Frame(self.page)
        self.gender_frame.pack()
        self.gender_label = tk.Label(
            self.gender_frame, text='性別')
        self.gender_label.pack(side=tk.LEFT)
        self.g = tk.IntVar()
        self.gender_r1 = tk.Radiobutton(
            self.gender_frame, text='男', variable=self.g, value=1)
        self.gender_r1.pack(side=tk.RIGHT)
        self.gender_r2 = tk.Radiobutton(
            self.gender_frame, text='女', variable=self.g, value=0)
        self.gender_r2.pack(side=tk.RIGHT)

        self.exercise = tk.StringVar()
        self.exercise_frame = tk.Frame(self.page)
        self.exercise_frame.pack()
        self.exercise_label = tk.Label(
            self.exercise_frame, text='近期每周運動次數')
        self.exercise_label.pack(side=tk.LEFT)
        self.exercise_entry = tk.Entry(
            self.exercise_frame, textvariable=self.exercise)
        self.exercise_entry.pack(side=tk.RIGHT)

        self.ondiet_frame = tk.Frame(self.page)
        self.ondiet_frame.pack()
        self.ondiet_label = tk.Label(
            self.ondiet_frame, text='目前有無減重需求')
        self.ondiet_label.pack(side=tk.LEFT)
        self.od = tk.IntVar()
        self.ondiet_r1 = tk.Radiobutton(
            self.ondiet_frame, text='有', variable=self.od, value=1)
        self.ondiet_r1.pack(side=tk.RIGHT)
        self.ondiet_r2 = tk.Radiobutton(
            self.ondiet_frame, text='無', variable=self.od, value=0)
        self.ondiet_r2.pack(side=tk.RIGHT)

        self.calculate_btn = tk.Button(
            self.page, text='確認', command=lambda: [self.calculate_kcal(), self.nextpage()])
        self.calculate_btn.pack(pady=10)

    def calculate_kcal(self):
        userheight = float(self.height.get())
        userweight = float(self.weight.get())
        age = int(self.age.get())
        gender = int(self.g.get())
        excersize_per_week = int(self.exercise.get())
        reducefat = int(self.od.get())

        # 計算基礎代謝率
        global TDEE
        if gender == 1:
            userbmr = (10 * userweight) + (6.25 * userheight) - (5 * age) + 5
        else:
            userbmr = (10 * userweight) + (6.25 * userheight) - (5 * age) - 161
        # 計算每日消耗熱量
        if excersize_per_week == 0:
            TDEE = userbmr * 1.2
        elif excersize_per_week == 1:
            TDEE = userbmr * 1.4
        elif 2 <= excersize_per_week <= 3:
            TDEE = userbmr * 1.5
        elif 4 <= excersize_per_week <= 5:
            TDEE = userbmr * 1.6
        elif 6 <= excersize_per_week <= 7:
            TDEE = userbmr * 1.7
        else:
            TDEE = userbmr * 1.8
        # 如有減重需求者，基礎代謝率再乘以0.8
        if reducefat == 1:
            TDEE *= 0.8
        TDEE = float('{:.1f}'.format(TDEE))

    def nextpage(self):
        self.page.destroy()
        Main_option(self.root)


final_main_choice = []
side_choice = []
snack_choice = []
meat_ans = []
spicy_ans = int()


class Main_option(object):  # 選擇主食餐點類別
    def __init__(self, master=None):
        self.root = master
        self.page = tk.Frame(self.root)
        self.page.pack()
        self.print_kcal()

        self.base_item = ['飯類', '麵類', '其他（飯麵以外）', '都可以']
        self.base_value = []
        self.meat_item = ['不吃牛', '不吃豬', '不吃雞', '不吃羊', '不吃鴨', '不吃海鮮']
        self.meat_value = []
        self.spicy = tk.IntVar()
        self.main_item = ['台式料理', '異國料理', '握便當', '無特別偏好']
        self.main_value = []

        self.food_preference()

    def print_kcal(self):
        global TDEE
        self.kcalResult = '您的一日建議攝取熱量為：' + str(TDEE) + '大卡'
        self.kcal_frame = tk.Frame(self.page)
        self.kcal_frame.pack()
        # 顯示計算結果
        self.kcalResult_label = tk.Label(
            self.kcal_frame, text=self.kcalResult, fg='red')
        self.kcalResult_label.pack()

    def food_preference(self):
        # 讓使用者輸入熱量上限
        self.kcal_frame = tk.Frame(self.page)
        self.kcal_frame.pack()
        self.kcal_label = tk.Label(self.kcal_frame, text='請輸入您這一餐的熱量上限（大卡）：')
        self.kcal_label.pack(side=tk.LEFT)
        self.kcal_entry = tk.Entry(self.kcal_frame)
        self.kcal_entry.pack(side=tk.LEFT)

        # 讓使用者輸入預算
        self.budget_frame = tk.Frame(self.page)
        self.budget_frame.pack(pady=10)
        self.budget_label = tk.Label(
            self.budget_frame, text='請輸入您這一餐的預算（元）：')
        self.budget_label.pack(side=tk.LEFT)
        self.budget_entry = tk.Entry(self.budget_frame)
        self.budget_entry.pack(side=tk.LEFT)

        # 問飯麵其他
        self.base_frame = tk.Frame(self.page)
        self.base_frame.pack()
        self.base_label = tk.Label(self.base_frame, text='您今天想吃的主食（可複選）：')
        self.base_label.pack(side=tk.LEFT)
        for i in range(len(self.base_item)):
            self.b = tk.IntVar()
            self.base_value.append(self.b)
            self.c = tk.Checkbutton(
                self.base_frame, text=self.base_item[i], variable=self.base_value[i])
            self.c.pack(side=tk.LEFT)

        # 問不吃什麼肉
        self.meat_frame = tk.Frame(self.page)
        self.meat_frame.pack(pady=10)
        self.meat_label = tk.Label(self.meat_frame, text='您不吃的肉類（可複選）：')
        self.meat_label.pack(side=tk.LEFT)
        for i in range(len(self.meat_item)):
            self.me = tk.IntVar()
            self.meat_value.append(self.me)
            self.c = tk.Checkbutton(
                self.meat_frame, text=self.meat_item[i], variable=self.meat_value[i])
            self.c.pack(side=tk.LEFT)
        global me_var
        me_var = tk.IntVar()
        self.alleat = tk.Checkbutton(
            self.meat_frame, text='都吃', variable=me_var)
        self.alleat.pack()

        # 問吃不吃辣
        self.spicy_frame = tk.Frame(self.page)
        self.spicy_frame.pack()
        self.spicy_label = tk.Label(self.spicy_frame, text='您吃辣嗎？')
        self.spicy_label.pack(side=tk.LEFT)
        self.spicy_r1 = tk.Radiobutton(
            self.spicy_frame, text='吃辣', variable=self.spicy, value=1)
        self.spicy_r1.pack(side=tk.LEFT)
        self.spicy_r2 = tk.Radiobutton(
            self.spicy_frame, text='不吃辣', variable=self.spicy, value=0)
        self.spicy_r2.pack(side=tk.LEFT)

        # 問主食類型偏好
        self.main_frame = tk.Frame(self.page)
        self.main_frame.pack(pady=10)
        self.main_label = tk.Label(self.main_frame, text='您對主食的偏好（可複選）：')
        self.main_label.pack(side=tk.LEFT)
        for i in range(len(self.main_item)):
            self.ma = tk.IntVar()
            self.main_value.append(self.ma)
            self.c = tk.Checkbutton(
                self.main_frame, text=self.main_item[i], variable=self.main_value[i])
            self.c.pack(side=tk.LEFT)

        self.choice_finish_btn = tk.Button(
            self.page, text='確認送出', command=lambda: [self.choice_ans(), self.nextpage()])
        self.choice_finish_btn.pack(pady=10)

    def choice_ans(self):
        rice_ans = []  # 取(飯麵其他)的回答
        for i in range(len(self.base_item)):
            rice = self.base_value[i].get()
            rice_ans.append(int(rice))

        global meat_ans  # 取(不吃肉類)的回答
        for i in range(len(self.meat_item)):
            meat = self.meat_value[i].get()
            meat_ans.append(meat)

        global spicy_ans
        spicy_ans = int(self.spicy.get())  # 取(吃不吃辣)的回答

        genre_ans = []  # 取(主食偏好)的回答
        for i in range(len(self.main_item)):
            main = self.main_value[i].get()
            genre_ans.append(int(main))

            # 處理主食類型
            t_dish_all = no_cat(dic_nocat['t_dish'])  # 台式料理
            f_dish_all = no_cat(dic_nocat['f_dish'])  # 異國料理
            riceball_all = cat(dic_cat['riceball'])  # 御飯糰
            hand_boxed = []  # 握便當該有哪些<list>
            global side_riceball  # 為了副食先順便分出來
            side_riceball = []   
            for rb in riceball_all:
                # 名稱裡面有發現"握便當"關鍵詞
                if rb[0].find('握便當') != -1:
                    hand_boxed.append(rb)
                else:
                    side_riceball.append(rb)

        main_step1 = []  # 第一步：主食類型偏好
        if genre_ans[3] == 1 or genre_ans == [0] * 4:  # 都可以或沒勾選任何選項
            main_step1 += (t_dish_all + f_dish_all + hand_boxed)
        else:
            if genre_ans[0] == 1:
                main_step1 += t_dish_all
            if genre_ans[1] == 1:
                main_step1 += f_dish_all
            if genre_ans[2] == 1:
                main_step1 += hand_boxed

        main_step2 = []  # 第二步：飯/麵/其他
        if rice_ans[3] == 1 or rice_ans == [0] * 4:  # 都可以或沒勾選任何選項
            main_step2 = main_step1
        else:
            if rice_ans[0] == 1:
                # 把含有米飯商品加入step2
                for ms1_r in main_step1:
                    if ms1_r[0].find('飯') != -1 \
                            or ms1_r[0].find('粥') != -1 \
                            or ms1_r[0].find('丼') != -1 \
                            or ms1_r[0].find('便當') != -1:
                        main_step2.append(ms1_r)
            if rice_ans[1] == 1:
                # 把含有麵商品加入step2
                for ms1_n in main_step1:
                    if ms1_n[0].find('麵') != -1 \
                            or ms1_n[0].find('麻辣鍋') != -1:
                        main_step2.append(ms1_n)
            if rice_ans[2] == 1:
                # 把除了飯麵以外(冬粉之類)加入step2
                for ms1_o in main_step1:
                    if ms1_r[0].find('飯') == -1 \
                            and ms1_r[0].find('粥') == -1 \
                            and ms1_r[0].find('丼') == -1 \
                            and ms1_r[0].find('便當') == -1 \
                            and ms1_n[0].find('麵') == -1 \
                            and ms1_n[0].find('麻辣鍋') == -1:
                        main_step2.append(ms1_o)

        main_step3 = []  # 第三步：牛/豬/雞/羊/鴨/海鮮
        global me_var
        if int(me_var.get()) == 1 or meat_ans == [0] * 6:  # 都吃或沒勾選任何選項
            main_step3 = main_step2
        else:
            if meat_ans[0] == 1:  # 不吃牛
                for ms2_b in main_step2:
                    if ms2_b[0].find('牛') != -1:
                        ms2_b[0] = "na"
            if meat_ans[1] == 1:  # 不吃豬
                for ms2_p in main_step2:
                    if ms2_p[0].find('豬') != -1 \
                            or ms2_p[0].find('豚') != -1 \
                            or ms2_p[0].find('排骨') != -1 \
                            or ms2_p[0].find('瘦肉') != -1:
                        ms2_p[0] = "na"
            if meat_ans[2] == 1:  # 不吃雞
                for ms2_c in main_step2:
                    if ms2_c[0].find('雞') != -1:
                        ms2_c[0] = "na"
            if meat_ans[3] == 1:  # 不吃羊
                for ms2_s in main_step2:
                    if ms2_s[0].find('羊') != -1:
                        ms2_s[0] = "na"
            if meat_ans[4] == 1:  # 不吃鴨
                for ms2_d in main_step2:
                    if ms2_d[0].find('鴨') != -1:
                        ms2_d[0] = "na"
            if meat_ans[5] == 1:  # 不吃海鮮
                for ms2_f in main_step2:
                    if ms2_f[0].find('海鮮') != -1 \
                            or ms2_f[0].find('蛤蠣') != -1 \
                            or ms2_f[0].find('魚') != -1 \
                            or ms2_f[0].find('蝦') != -1:
                        ms2_f[0] = "na"
            # 最後把符合的餐點(沒有變成na的)加進step3
            for ms2 in main_step2:
                if ms2[0] != 'na':
                    main_step3.append(ms2)

        main_step4 = []  # 第四步：吃辣/不吃辣
        if spicy_ans == 0:
            for ms3_s in main_step3:
                if ms3_s[0].find('辣') == -1 \
                        and ms3_s[0].find('麻婆') == -1 \
                        and ms3_s[0].find('紅燒') == -1 \
                        and ms3_s[0].find('泡菜') == -1:
                    main_step4.append(ms3_s)
        elif spicy_ans == 1:
            main_step4 = main_step3
        main_choice = main_step4

        # 用預算篩選
        global TDEE_meal
        TDEE_meal = float(self.kcal_entry.get())
        global budget
        budget = float(self.budget_entry.get())
        main_choice.append(["我是分隔", 9999.0, budget])
        # x[-1]：價格(小到大排)；x[-2]：熱量(小到大排)
        sort_main_budget = sorted(main_choice, key=lambda x: (x[-1], x[-2]))
        index_mainbud = sort_main_budget.index(["我是分隔", 9999.0, budget])
        main_choice = sort_main_budget[:index_mainbud]

        # 用熱量篩選
        main_choice.append(["我是分隔", TDEE_meal, 9999.0])
        # x[-2]：熱量(小到大排)；x[-1]：價格(小到大排)
        sort_main_choice = sorted(main_choice, key=lambda x: (x[-2], x[-1]))
        index_split = sort_main_choice.index(["我是分隔", TDEE_meal, 9999.0])
        global final_main_choice
        final_main_choice = sort_main_choice[:index_split]

    def nextpage(self):
        self.page.destroy()
        Main_outcome(self.root)


class Main_outcome(object):  # 選擇主食
    def __init__(self, master=None):
        self.root = master
        self.page = tk.Frame(self.root)
        self.page.pack()
        self.main_outcome()

    def main_outcome(self):
        self.main_result_label = tk.Label(
            self.page, text='以下為推薦的主食品項：（請點選一個您想要的主食）')
        self.main_result_label.pack()
        global final_main_choice
        if len(final_main_choice) < 10:
            main_random = final_main_choice
        else:
            main_random = sample(final_main_choice, 10)
        
      
        for i in (main_random):
            text_content = i[0] + '：' + \
                str(int(i[-2])) + '大卡' + '，' + str(int(i[-1])) + '元'
            self.mainfood_btn = tk.Button(self.page, text=text_content, command=lambda i=i: [
                                          self.calculate_remain(i), self.nextpage()])
            self.mainfood_btn.pack(padx=5, pady=5)

    def calculate_remain(self, main_result):
        # 計算剩餘熱量及預算
        main_meal = main_result
        global main_meal_name
        main_meal_name = main_meal[0]
        global remain_kcal
        remain_kcal = TDEE_meal - main_meal[-2]
        global remain_budget
        remain_budget = budget - main_meal[-1]

    def nextpage(self):
        self.page.destroy()
        Side_check(self.root)


class Side_check(object):  # 呈現主食結果並選擇是否要副食
    def __init__(self, master=None):
        self.root = master
        self.page = tk.Frame(self.root)
        self.page.pack()
        self.willing_side()

    def willing_side(self):
        # 呈現剩餘熱量及預算
        global main_meal_name
        global remain_kcal
        global remain_budget
        buy_cart_text = '您目前預計購買的有：' + main_meal_name
        self.buy_cart_label = tk.Label(self.page, text=buy_cart_text)
        self.buy_cart_label.pack()
        remain_kcal_text = '距離您這餐的熱量上限還有 ' + str(remain_kcal) + ' 大卡'
        self.remain__kcal_label = tk.Label(self.page, text=remain_kcal_text)
        self.remain__kcal_label.pack()
        remain_budget_text = '您的預算還剩下 ' + str(int(remain_budget)) + ' 元'
        self.remain_budget_label = tk.Label(self.page, text=remain_budget_text)
        self.remain_budget_label.pack()

        # 確認使用者需不需要副食
        self.willing = tk.IntVar()
        self.willing_frame = tk.Frame(self.page)
        self.willing_frame.pack()
        self.willing_label = tk.Label(
            self.willing_frame, text='請問您需要副食嗎？')
        self.willing_label.pack(side=tk.LEFT)
        self.willing1 = tk.Radiobutton(
            self.willing_frame, text='需要', variable = self.willing, value = 0)
        self.willing1.pack(side=tk.LEFT)
        self.willing2 = tk.Radiobutton(
            self.willing_frame, text='不需要', variable = self.willing, value = 1)
        self.willing2.pack(side=tk.LEFT)
        self.willing_btn = tk.Button(self.page, text = '確認', command=lambda: self.nextpage())
        self.willing_btn.pack()

    def nextpage(self):
        if self.willing.get() == 0:
            self.page.destroy()
            Side_option(self.root)
        elif self.willing.get() == 1:
            self.page.destroy()
            Snack_check(self.root)



class Side_option(object):  # 選擇副食餐點類別
    def __init__(self, master=None):
        self.root = master
        self.page = tk.Frame(self.root)
        self.page.pack()
        self.preference()

    def preference(self):
        # 副食類型的偏好
        self.side_item = ['御飯糰', '關東煮', '光合', '風味小食', '大亨堡', '無特別偏好']
        self.side_value = []
        self.side_frame = tk.Frame(self.page)
        self.side_frame.pack(pady=10)
        self.side_label = tk.Label(self.side_frame, text='您對副食的偏好（可複選）：')
        self.side_label.pack(side=tk.LEFT)
        for i in range(len(self.side_item)):
            self.si = tk.IntVar()
            self.side_value.append(self.si)
            self.c = tk.Checkbutton(
                self.side_frame, text=self.side_item[i], variable=self.side_value[i])
            self.c.pack(side=tk.LEFT)

        self.choice_finish_btn = tk.Button(
            self.page, text='確認送出', command=lambda: [self.side_choice_ans(), self.nextpage()])
        self.choice_finish_btn.pack(pady=10)

    def side_choice_ans(self):
        global meat_ans
        global spicy_ans

        # 副食類有五類型：御飯糰、關東煮、光合、風味、大亨堡
        kanto_all = cat(dic_cat['kanto_cooking'])  # 關東煮
        fresh_all = cat(dic_cat['freshfood'])  # 光合
        soup_all = cat(dic_cat['soup_snack'])  # 風味
        hotdog_all = cat(dic_cat['hot_dog'])  # 大亨堡
        # 將光合中沒有熱量資訊的剔除(有機生蔬菜、好菇、香蕉)
        fresh_edible = []
        for fr in fresh_all:
            if fr[2] != -1:
                fresh_edible.append(fr)
        # 將風味中沒有熱量資訊的剔除(地瓜、味噌關東煮)
        soup_edible = []
        for so in soup_all:
            if fr[2] != -1:
                soup_edible.append(so)

        side_genre_ans = []  # 取(副食類型偏好)的回答
        for i in range(len(self.side_item)):
            side = self.side_value[i].get()
            side_genre_ans.append(int(side))

        side_step1 = []  # 先決定要哪些類型
        if side_genre_ans[5] == 1 or side_genre_ans == [0] * 6:  # 都可以或沒勾選任何選項
            side_step1 += (
                side_riceball + kanto_all + fresh_edible + soup_edible + hotdog_all)
        else:
            if side_genre_ans[0] == 1:
                side_step1 += side_riceball
            if side_genre_ans[1] == 1:
                side_step1 += kanto_all
            if side_genre_ans[2] == 1:
                side_step1 += fresh_edible
            if side_genre_ans[3] == 1:
                side_step1 += soup_edible
            if side_genre_ans[4] == 1:
                side_step1 += hotdog_all

        side_step2 = []  # 第二步做"牛豬雞羊鴨海鮮"
        # "有不吃的
        global me_var
        if int(me_var.get()) == 1 or meat_ans == [0] * 6:
            side_step2 = side_step1
        else:
            # 代表他不吃牛肉
            if meat_ans[0] == 1:
                for ss1_b in side_step1:
                    if ss1_b[0].find('牛') != -1:
                        ss1_b[0] = "na"
            # 代表他不吃豬肉
            if meat_ans[1] == 1:
                for ss1_p in side_step1:
                    if ss1_p[0].find('豬') != -1 \
                            or ss1_p[0].find('豚') != -1 \
                            or ss1_p[0].find('排骨') != -1 \
                            or ss1_p[0].find('瘦肉') != -1 \
                            or ss1_p[0].find('燒肉') != -1:
                        ss1_p[0] = "na"
            if meat_ans[2] == 1:
                for ss1_c in side_step1:
                    if ss1_c[0].find('雞') != -1:
                        ss1_c[0] = "na"
            if meat_ans[3] == 1:
                for ss1_s in side_step1:
                    if ss1_s[0].find('羊') != -1:
                        ss1_s[0] = "na"
            if meat_ans[4] == 1:
                for ss1_d in side_step1:
                    if ss1_d[0].find('鴨') != -1:
                        ss1_d[0] = "na"
            if meat_ans[5] == 1:
                for ss1_f in side_step1:
                    if ss1_f[0].find('海鮮') != -1 \
                            or ss1_f[0].find('蛤蠣') != -1 \
                            or ss1_f[0].find('魚') != -1 \
                            or ss1_f[0].find('蝦') != -1:
                        ss1_f[0] = "na"
            # 最後要把符合的餐點(沒有變成na的)加進step2
            for ss1 in side_step1:
                if ss1[0] != 'na':
                    side_step2.append(ss1)

        side_step3 = []  # 第三步做"吃不吃辣"
        if spicy_ans == 0:  # 不吃辣
            for ss2_s in side_step2:
                if ss2_s[0].find('辣') == -1 \
                        and ss2_s[0].find('麻婆') == -1 \
                        and ss2_s[0].find('紅燒') == -1 \
                        and ss2_s[0].find('泡菜') == -1:
                    side_step3.append(ss2_s)
        elif spicy_ans == 1:  # 吃辣
            side_step3 = side_step2
        
        global side_choice
        side_choice = side_step3
        # 用剩餘預算篩選
        global remain_kcal
        global remain_budget
        side_choice.append(["我是分隔", 9999.0, remain_budget])
        sort_side_budget = sorted(side_choice, key=lambda x: (x[-1], x[-2]))
        index_sidebud = sort_side_budget.index(["我是分隔", 9999.0, remain_budget])
        side_choice = sort_side_budget[:index_sidebud]

        # 用剩餘熱量篩選
        side_choice.append(["我是分隔", remain_kcal, 9999.0])
        sort_side_choice = sorted(side_choice, key=lambda x: (x[-2], x[-1]))
        index_split = sort_side_choice.index(["我是分隔", remain_kcal, 9999.0])
        global final_side_choice
        final_side_choice = sort_side_choice[:index_split]

    def nextpage(self):
        self.page.destroy()
        Side_outcome(self.root)

side_meal_name = str()
class Side_outcome(object):  # 呈現副食結果並選擇副食
    def __init__(self, master=None):
        self.root = master
        self.page = tk.Frame(self.root)
        self.page.pack()
        self.side_outcome()

    def calculate_remain(self, side_result):
        # 計算剩餘熱量及預算
        side_meal = side_result
        global side_meal_name
        side_meal_name = side_meal[0]
        global remain_kcal
        remain_kcal -= side_meal[-2]
        global remain_budget
        remain_budget -= side_meal[-1]

    def side_outcome(self):
        global final_side_choice
        if final_side_choice == []:
            self.side_result_label = tk.Label(self.page, text='不好意思~沒有符合您剩餘熱量及預算需求的品項！')
            self.side_result_label.pack(pady = 10)
            self.side_result_btn = tk.Button(self.page, text = '下一頁', command = lambda: self.nextpage())
            self.side_result_btn.pack(pady = 10)
        else:
            self.side_result_label = tk.Label(self.page, text='以下為推薦的副食品項：（請點選一個您想要的副食）')
            self.side_result_label.pack()
            if len(final_side_choice) < 10:
                side_random = final_side_choice
            else:
                side_random = sample(final_side_choice, 10)
            for i in side_random:
                text_content = i[0] + '：' + \
                    str(int(i[-2])) + '大卡' + '，' + str(int(i[-1])) + '元'
                self.sidefood_btn = tk.Button(self.page, text=text_content, command=lambda i=i: [
                                              self.calculate_remain(i), self.nextpage()])
                self.sidefood_btn.pack(padx=5, pady=5)

    def nextpage(self):
        self.page.destroy()
        Snack_check(self.root)


class Snack_check(object):  # 呈現主副食結果並確認是否要甜點
    def __init__(self, master=None):
        self.root = master
        self.page = tk.Frame(self.root)
        self.page.pack()
        self.willing_snack()

    def willing_snack(self):
        global side_meal_name
        # 呈現剩餘熱量及預算
        buy_cart_text = '您目前預計購買的有：' + main_meal_name + '、' + side_meal_name
        self.buy_cart_label = tk.Label(self.page, text=buy_cart_text)
        self.buy_cart_label.pack()
        remain_kcal_text = '距離您這餐的熱量上限還有 ' + str(remain_kcal) + ' 大卡'
        self.remain__kcal_label = tk.Label(self.page, text=remain_kcal_text)
        self.remain__kcal_label.pack()
        remain_budget_text = '您的預算還剩下 ' + str(int(remain_budget)) + ' 元'
        self.remain_budget_label = tk.Label(self.page, text=remain_budget_text)
        self.remain_budget_label.pack()

        # 確認使用者需不需要甜點
        self.willing = tk.IntVar()
        self.willing_frame = tk.Frame(self.page)
        self.willing_frame.pack()
        self.willing_label = tk.Label(
            self.willing_frame, text='請問您需要甜點嗎？', fg = 'blue')
        self.willing_label.pack(side=tk.LEFT)
        
        self.willing1 = tk.Radiobutton(
            self.willing_frame, text='需要', variable = self.willing, value = 0)
        self.willing1.pack(side=tk.LEFT)
        self.willing2 = tk.Radiobutton(
            self.willing_frame, text='不需要', variable = self.willing, value = 1)
        self.willing2.pack(side=tk.LEFT)
        self.willing_btn = tk.Button(self.page, text = '確認', command=lambda: self.nextpage())
        self.willing_btn.pack()

    def nextpage(self):
        if self.willing.get() == 0:
            self.page.destroy()
            Snack_option(self.root)
        elif self.willing.get() == 1:
            self.page.destroy()
            Final(self.root)



class Snack_option(object):  # 選擇甜點餐點類別
    def __init__(self, master=None):
        self.root = master
        self.page = tk.Frame(self.root)
        self.page.pack()
        self.preference()

    def preference(self):
        # 甜點類型的偏好
        self.snack_item = ['霜淇淋', '思樂冰', '麵包']
        self.snack_value = []
        self.snack_frame = tk.Frame(self.page)
        self.snack_frame.pack(pady=10)
        self.snack_label = tk.Label(self.snack_frame, text='您對甜點的偏好（可複選）：')
        self.snack_label.pack(side=tk.LEFT)
        for i in range(len(self.snack_item)):
            self.si = tk.IntVar()
            self.snack_value.append(self.si)
            self.c = tk.Checkbutton(
                self.snack_frame, text=self.snack_item[i], variable=self.snack_value[i])
            self.c.pack(side=tk.LEFT)

        self.choice_finish_btn = tk.Button(
            self.page, text='確認送出', command=lambda: [self.choice_ans(), self.nextpage()])
        self.choice_finish_btn.pack(pady=10)

    def choice_ans(self):
        # 點心類有三類型：霜淇淋、思樂冰、麵包
        icecream_all = ice_cream(dic_ice_cream['ice_cream'])  # 霜淇淋
        slurpee_all = slurpee(dic_slurpee['slurpee'])  # 思樂冰
        bread_all = no_cat(dic_nocat['bread'])  # 麵包

        snack_genre_ans = []  # 取(甜點偏好)的回答
        for i in range(len(self.snack_item)):
            snack = self.snack_value[i].get()
            snack_genre_ans.append(int(snack))

        item_price_carlo = []   # 品名、價格、熱量 的list
        if snack_genre_ans[0] == 1:
            icecream_all = ice_cream(dic_ice_cream["ice_cream"])
            softserves_product = []
            for snacks in icecream_all:
                price_carlo = []
                softserves_product.append(snacks[0])
                price_carlo.append(snacks[1])  # 熱量
                price_carlo.append(snacks[-1])  # 價格(價格都出現在最後一個)
                info = [snacks[0]]
                info += price_carlo
                item_price_carlo.append(info)

        if snack_genre_ans[1] == 1:
            slurpee_all = slurpee(dic_slurpee["slurpee"])
            for snacks in slurpee_all:
                # 爬蟲只會依口味分類，每個口味的基礎熱量不同；容量的價格是固定的
                snacks[1] = snacks[1].replace('熱量:', '')
                snacks[1] = snacks[1].replace('kcal/100毫升', '')
                snacks[1] = float(snacks[1])        # 抓出熱量
                # 接著處理大杯中杯小杯
                sizelist = [['(大杯)', 30, 6.6], [
                    '(中杯)', 25, 4.8], ['(小杯)', 20, 3.6]]
                for size in sizelist:
                    info = []
                    name = snacks[0] + size[0]
                    saleprice = size[1]
                    calorieforsize = size[2] * snacks[1]
                    info.append(name)
                    info.append(calorieforsize)
                    info.append(saleprice)
                    item_price_carlo.append(info)

        if snack_genre_ans[2] == 1:
            # 所有麵包，做成字典，字典call出來的是包含價格、熱量的list
            bread_all = no_cat(dic_nocat['bread'])
            for snacks in bread_all:
                price_carlo = []
                price_carlo.append(snacks[1])      # 熱量
                price_carlo.append(snacks[-1])     # 價格(價格都出現在最後一個)
                info = [snacks[0]]
                info += price_carlo
                item_price_carlo.append(info)
        # 自此，依照使用者初步篩選的結果，都放在一個list了
        
        # 篩掉熱量超標、價格超標的產品
        global remain_kcal
        global remain_budget
        item_price_carlo2 = []      
        for lists in item_price_carlo:
            # 先把單一產品價格就超過的商品刪除
            if lists[2] > remain_budget:
                lists.append('超過')
            if lists[1] > remain_kcal:
                lists.append('超過')
                
        for lists in item_price_carlo:
            if len(lists) == 3:
                lists[1] = float(round(lists[1]))
                lists[2] = float(round(lists[2]))
                item_price_carlo2.append(lists)
        sort_snacks = sorted(item_price_carlo2, key=lambda x: (x[1], x[2]))
        global final_snack_choice
        final_snack_choice = sort_snacks        

    def nextpage(self):
        self.page.destroy()
        Snack_outcome(self.root)

snack_meal_name = str()
class Snack_outcome(object):  # 呈現甜點結果並選擇甜點
    def __init__(self, master=None):
        self.root = master
        self.page = tk.Frame(self.root)
        self.page.pack()
        self.snack_outcome()

    def calculate_remain(self, snack_result):
        # 計算剩餘熱量及預算
        snack_meal = snack_result
        global snack_meal_name
        snack_meal_name = snack_meal[0]
        global remain_kcal
        remain_kcal -= snack_meal[-2]
        global remain_budget
        remain_budget -= snack_meal[-1]

    def snack_outcome(self):
        global final_snack_choice
        if final_snack_choice == []:
            self.snack_result_label = tk.Label(self.page, text='不好意思~沒有符合您剩餘熱量及預算需求的品項！')
            self.snack_result_label.pack(pady = 10)
            self.snack_result_btn = tk.Button(self.page, text = '下一頁', command = lambda: self.nextpage())
            self.snack_result_btn.pack(pady = 10)
        else:
            self.snack_result_label = tk.Label(self.page, text='以下為推薦的甜點品項：（請點選一個您想要的甜點）')
            self.snack_result_label.pack()
            
            if len(final_snack_choice) < 10:
                snack_random = final_snack_choice
            else:
                snack_random = sample(final_snack_choice, 10)
            for i in snack_random:
                text_content = i[0] + '：' + \
                    str(int(i[-2])) + '大卡' + '，' + str(int(i[-1])) + '元'
                self.snackfood_btn = tk.Button(self.page, text=text_content, command=lambda i=i: [
                                              self.calculate_remain(i), self.nextpage()])
                self.snackfood_btn.pack(padx=5, pady=5)

    def nextpage(self):
        self.page.destroy()
        Final(self.root)


class Final(object):    # 呈現最終結果
    def __init__(self, master=None):
        self.root = master
        self.page = tk.Frame(self.root)
        self.page.pack()
        self.final()

    def final(self):
        global main_meal_name
        global side_meal_name
        global snack_meal_name
        global TDEE_meal
        global budget
        global remain_kcal
        global remain_budget
        total_kcal = TDEE_meal - remain_kcal
        total_money = budget - remain_budget

        # 呈現最終選擇、大卡及金額
        buy_cart_text = '您最終購買的是：' + main_meal_name + '  ' + side_meal_name + '  ' + snack_meal_name
        self.buy_cart_label = tk.Label(self.page, text=buy_cart_text)
        self.buy_cart_label.pack(pady = 10)
        kcal_text = '總熱量為：' + str(total_kcal) + ' 大卡'
        self.kcal_label = tk.Label(self.page, text=kcal_text)
        self.kcal_label.pack(pady = 10)
        payment_text = '總金額為：' + str(int(total_money)) + ' 元'
        self.payment_label = tk.Label(self.page, text=payment_text)
        self.payment_label.pack(pady = 10)
        self.final_label = tk.Label(self.page, text='祝您用餐愉快！')
        self.final_label.pack(pady = 10)


Info(root)
root.mainloop()
