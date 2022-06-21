days = [[{"day": 0,
          "time": 1,
          "main": "우동",
          "mainkcal": 2000,
          "sub": "김치",
          "subkcal": 500,
          "img": "https://file.mk.co.kr/meet/neds/2017/09/image_readtop_2017_587233_15042337473013492.jpg"},
         {"day": 0,
          "tme": 0,
          "main": "라면",
          "mainkcal": 1500,
          "sub": "김치",
          "subkcal": 500,
          "img": "https://file.mk.co.kr/meet/neds/2017/09/image_readtop_2017_587233_15042337473013492.jpg"},
         {"day": 0,
          "tme": 2,
          "main": "짜장면",
          "mainkcal": 900,
          "sub": "김치",
          "subkcal": 500,
          "img": "https://file.mk.co.kr/meet/neds/2017/09/image_readtop_2017_587233_15042337473013492.jpg"}
         ],
        [{"day": 1,
          "time": 0,
          "main": "라면",
          "mainkcal": 1500,
          "sub": "김치",
          "subkcal": 500,
          "img": "https://file.mk.co.kr/meet/neds/2017/09/image_readtop_2017_587233_15042337473013492.jpg"},
         {"day": 1,
          "time": 1,
          "main": "우동",
          "mainkcal": 2000,
          "sub": "김치",
          "subkcal": 500,
          "img": "https://file.mk.co.kr/meet/neds/2017/09/image_readtop_2017_587233_15042337473013492.jpg"},
         {"day": 1,
          "time": 2,
          "main": "짜장면",
          "mainkcal": 900,
          "sub": "김치",
          "subkcal": 500,
          "img": "https://file.mk.co.kr/meet/neds/2017/09/image_readtop_2017_587233_15042337473013492.jpg"}
         ]
        ]

big = []
diet = []
total = 0
one = None

for day in days:
    for someday in day:
        someday_kcal = someday['mainkcal'] + someday['subkcal']
        if someday_kcal > total:
            total = someday_kcal
            one = someday
    total = 0
    diet.append(one)
    print(diet)
