import pymysql
import pandas as pd

#def to_db(a,brand,name):
#   car_db = pymysql.connect(
 #       user='root',
  #      passwd='1234',
   #     host='0.0.0.0',
    #    db='data',
     #   charset='utf8'
#    )
 #   cursor = car_db.cursor(pymysql.cursors.DictCursor)
  #  insert_data=[{'id':a,'brand':brand,'name':name}]
  #  insert_sql2 = "INSERT INTO `search` VALUES (%(id)s,%(brand)s,%(name)s);"
  #  cursor.executemany(insert_sql2, insert_data)
  #  car_db.commit()

def get_trim(brand,trim):
    if brand == '기아':
        if trim in [ '럭셔리', '스탠다드', '레이디', '트립', '트렌디', '디럭스', '스마트', '캠핑카', '기본형', 'L', 'LX']:
            trim = 1
        elif trim in ['프레스티지', '스타일 에디션', 'X 에디션', '스페셜 에디션', '리미티드', 'W 스페셜', 'GL', 'GX', '플래티넘', '이그제큐티브', '고급형']:
            trim = 2
        elif trim in ['노블레스', '스포츠', '베스트 셀렉션', '파크', '프레지던트', '스페셜', 'VIP', '마스터즈', 'GLX']:
            trim = 3
        else:
            trim = 4
    elif brand == '현대':
        if trim in ['스타일','벨류 플러스','케어플러스','스마트','모던 베이직','모던']:
            trim = 1
        elif trim in ['프리미엄','프리미엄스페셜']:
            trim = 2
        elif trim in ['익스클루시브','익스클루시브 스페셜','셀러브리티']:
            trim = 3
        else:
            trim = 4
    elif brand == '제네시스':
        if trim in ['2.0', '2.0T', '2.2', '2.5', '2.5T']:
            trim = 1
        elif trim in ['3.0', '3.3', '3.3T', '3.5', '3.5T']:
            trim = 2
        elif trim in ['3.8', '5.0', '3.3 프레스티지', '3.3T 스포츠', '3.3 프리미엄 럭셔리', '3.3T 프리미엄 럭셔리', '3.8 럭셔리', '3.8 프리미엄 럭셔리']:
            trim = 3
        else:
            trim = 4
    elif brand == '르노삼성':
        if trim in ['PE', 'SE', 'SE 플러스', 'D', 'D프리미엄', 'SE 블랙', 'SE 플레져', '클래식']:
            trim = 1
        elif trim in ['인텐스', 'LE', 'LE 플러스', 'LE 익스클루시브']:
            trim = 2
        elif trim in ['RE', 'RE 시그니처']:
            trim = 3
        else:
            trim = 4

    elif brand == '쌍용':
        if trim == '일반형':
            trim = 1
        elif trim == '고급형':
            trim = 2
        else:
            trim = 3
    elif brand == '미니':
        if trim == 'STANDARD':
            trim = 1
        elif trim == "MID":
            trim = 2
        else:
            trim =3
    elif brand == '랜드로버':
        if trim == '스탠다드':
            trim = 1
        elif trim == '다이나믹':
            trim = 2
        else:
            trim = 3
    elif brand == '폭스바겐':
        if trim == '기본':
            trim = 1
        elif trim == '컴포트':
            trim = 2
        elif trim == '프리미엄':
            trim = 3
        else:
            trim =4
    elif brand == '벤츠':
        if trim == '기본':
            trim = 1
        elif trim == '아방가르드':
            trim = 2
        else:
            trim =3
    elif brand == '포드':
        if trim == "스탠다드":
            trim = 1
        else:
            trim =2
    elif brand == '쉐보레':
        if trim in ['코치','SE','팝','LS','LS','디럭스','5.3','SS 3.6 V8','익스트림']:
            trim = 1
        elif trim in ['판넬밴','SX','X','재즈','LT','SLT','밴','패션','6','SS 6.2 V8','다이나믹레드','어드벤처패키지','익스트림-X','익스트림-X스포츠바']:
            trim = 2
        elif trim in ['CDX','그루브','LTZ','RS','다이나믹','Z71-X','LTZ+','ACTIV']:
            trim = 3
        else:
            trim = 4
    elif brand == 'BMW':
        if trim in ['조이 퍼스트 에디션','G20', 'M스포츠 F40','M스포츠 G20']:
            trim = 1
        elif trim in ['스포츠 F40','럭셔리 G20','럭셔리 플러스 G30','M 스포츠 G30','M스포츠 G12','M 스포츠 G02',' M 스포츠 F48','M스포츠 G05','M 스포츠 G06','M 스포츠 G11','M 스포츠 F33','F12 F06','F02','M스포츠 F01','스포츠 라인 F32','솔 플러스', 'M스포츠 F32']:
            trim = 2
        elif trim in ['M 스포츠 G20','M 스포츠 플러스 G30','M 스포츠 G12','인디비주얼 F02','럭셔리 LP F36','럭셔리 플러스 F10']:
            trim = 3
        else:
            trim = 4
    elif brand == '아우디':
        if trim in ['기본형', '엔트리', '스포트라인', '다이나믹']:
            trim = 1
        elif trim in ['프레스티지', '프리미엄', '리미티드']:
            trim = 2
        elif trim in ['S-LINE']:
            trim = 3
        else:
            trim = 4

    return trim

def to_csv(bra,na,trim,fuel,year,acci,color,wd,km):

    df = pd.DataFrame()
    empty = pd.DataFrame(columns=['km', 'year', 'accident', 'wd', 'trim', 'brand_BMW', 'brand_기아', 'brand_랜드로버',
                                  'brand_르노삼성', 'brand_미니', 'brand_벤츠', 'brand_쉐보레', 'brand_쌍용', 'brand_아우디',
                                  'brand_제네시스',
                                  'brand_포드', 'brand_폭스바겐', 'brand_현대', 'name_118', 'name_200', 'name_320', 'name_330',
                                  'name_420   쿠페', 'name_420  그란쿠페',
                                  'name_428   컨버터블', 'name_428   쿠페', 'name_520', 'name_528', 'name_530',
                                  'name_640    그란쿠페', 'name_730',
                                  'name_730Ld', 'name_740', 'name_740Li', 'name_750Ld', 'name_750Li', 'name_A200',
                                  'name_A220', 'name_A3', 'name_A4',
                                  'name_A45', 'name_A5', 'name_A6', 'name_A7', 'name_A8', 'name_B200', 'name_C200',
                                  'name_C220', 'name_C220 블루텍', 'name_C63',
                                  'name_CC', 'name_CC 블루모션', 'name_CLA220', 'name_CLA250', 'name_CLA45', 'name_CLS250',
                                  'name_CLS350', 'name_CLS4.0',
                                  'name_CLS450', 'name_CLS63', 'name_E200', 'name_E220', 'name_E220 블루텍', 'name_E250',
                                  'name_E250 블루텍', 'name_E300',
                                  'name_E350', 'name_E400', 'name_EQ900', 'name_F150', 'name_G63', 'name_G70',
                                  'name_G80', 'name_G90', 'name_GLA220',
                                  'name_GLA45', 'name_GLC220', 'name_GLC250', 'name_GLC300', 'name_GLC350e',
                                  'name_GLC43', 'name_GLE350', 'name_GLK220',
                                  'name_GT', 'name_GV70', 'name_GV80', 'name_K3', 'name_K5', 'name_K7', 'name_K8',
                                  'name_K9', 'name_ML350 블루텍', 'name_Q3',
                                  'name_Q5', 'name_Q7', 'name_Q8', 'name_QM5', 'name_QM6', 'name_R8', 'name_S3',
                                  'name_S350', 'name_S350 블루텍', 'name_S350L',
                                  'name_S350L 블루텍', 'name_S4', 'name_S4.0', 'name_S5', 'name_S500', 'name_S500L',
                                  'name_S550', 'name_S560', 'name_S6',
                                  'name_S600', 'name_S63', 'name_S7', 'name_S8', 'name_SM3', 'name_SM5', 'name_SM6',
                                  'name_SM7', 'name_TT', 'name_X1  20',
                                  'name_X4 20', 'name_X5  30', 'name_X6 30', 'name_X6 40', 'name_e-트론', 'name_i3',
                                  'name_i30', 'name_i40', 'name_골프',
                                  'name_골프 블루모션', 'name_그랜드스타렉스', 'name_그랜저', 'name_뉴 CC', 'name_뉴 CC 블루모션', 'name_니로',
                                  'name_다마스',
                                  'name_디스커버리 SE', 'name_라세티', 'name_레이', 'name_레인지로버', 'name_레인지로버 AB',
                                  'name_레인지로버 SE', 'name_레인지로버 Vogue',
                                  'name_렉스턴', 'name_렉스턴 RX4', 'name_렉스턴 RX6', 'name_렉스턴 RX7', 'name_로드스터', 'name_로디우스',
                                  'name_로체',
                                  'name_마티즈', 'name_말리부', 'name_맥스크루즈', 'name_머스탱 컨버터블', 'name_머스탱 쿠페', 'name_모닝',
                                  'name_모하비',
                                  'name_몬데오 2.0 트렌드', 'name_몬데오 2.0 티타늄', 'name_베뉴', 'name_벨로스터', 'name_볼트', 'name_봉고3',
                                  'name_비틀', 'name_셀토스', 'name_스타렉스', 'name_스타리아', 'name_스토닉', 'name_스팅어', 'name_스파크',
                                  'name_스포티지', 'name_시로코', 'name_싼타페', 'name_쎄라토', 'name_쏘나타', 'name_쏘렌토', 'name_쏘울',
                                  'name_쏠라티',
                                  'name_아반떼', 'name_아베오', 'name_아슬란', 'name_아테온', 'name_알페온', 'name_액티언', 'name_에쿠스',
                                  'name_엑센트',
                                  'name_엑센트(신형)', 'name_오피러스', 'name_올란도', 'name_옵티마', 'name_윈스톰', 'name_익스프레스밴',
                                  'name_익스플로러',
                                  'name_임팔라', 'name_제네시스', 'name_제타', 'name_제타 블루모션', 'name_조에', 'name_체어맨', 'name_카니발',
                                  'name_카렌스',
                                  'name_카마로', 'name_카이런', 'name_캡처', 'name_캡티바', 'name_코나', 'name_코란도',
                                  'name_코란도 어드벤처 60th 에디션',
                                  'name_코란도 익스트림', 'name_콜로라도', 'name_쿠퍼', 'name_쿠퍼 5도어', 'name_쿠퍼 JCW', 'name_쿠퍼 SE',
                                  'name_쿠퍼 컨트리맨',
                                  'name_쿠퍼 컨트리맨 파크래인', 'name_크루즈', 'name_클리오', 'name_토러스', 'name_토러스 2.0 에코부스트',
                                  'name_투싼', 'name_투아렉',
                                  'name_투아렉 블루모션', 'name_트래버스', 'name_트랙스', 'name_트레일블레이저', 'name_트위지', 'name_티구안',
                                  'name_티록',
                                  'name_티볼리', 'name_파사트', 'name_팰리세이드', 'name_페이톤', 'name_펠리세이드', 'name_포르테',
                                  'name_포터2', 'name_폴로',
                                  'name_프라이드', 'name_프리랜더 SE', 'type_LPG', 'type_가솔린', 'type_디젤', 'type_바이퓨얼',
                                  'type_전기', 'type_하이브리드',
                                  'color_검정색', 'color_기타', 'color_회색', 'color_흰색'])
    df2 = pd.DataFrame({'km':km,
                        'year': 2022-int(year),
                        'accident': acci,
                        'wd': wd,
                        'trim':trim,
                        f'brand_{bra}':bra,
                        f'name_{na}':na,
                        f'type_{fuel}':fuel,
                        f'color_{color}':color},
                       index=[0])
    df=pd.concat([empty,df2])
    df.fillna(0,inplace=True)
    df.iloc[0:, 5:] = df.iloc[0:, 5:][df.iloc[0:, 5:] == 0].fillna(1)
    # df.to_csv("test_data.csv",sep=',',na_rep='NaN',index=False)
    return df
