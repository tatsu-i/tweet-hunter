import os
import json
import tweepy
from datetime import timedelta
from elasticsearch import Elasticsearch
from elasticsearch_dsl import UpdateByQuery

API_KEY = os.environ.get("TWITTER_API_KEY", "")
API_SECRET_KEY = os.environ.get("TWITTER_API_SECRET_KEY", "")
ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN", "")
ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET", "")

es = Elasticsearch(hosts=[{"host": "elasticsearch", "port": 9200}])
with open("/scripts/template.json", "r") as f:
    print("update template")
    es.indices.put_template(name="tweet", body=json.load(f))

# StreamListenerを継承するクラスListener作成
class Listener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            body = status._json
            body["@timestamp"] = status.created_at
            es.index("tweet", body=body)
        except Exception as e:
            print(e)
        return True

    def on_delete(self, status_id, user_id):
        ubq = UpdateByQuery(using=es, index="tweet*")
        query = (
            ubq.query("match", id_str__keyword=str(status_id))
            .query("match", user__id_str__keyword=str(user_id))
            .script(source="ctx._source.delete = true")
        )
        resp = query.execute()
        print(f"deleted {status_id} {user_id} {resp.to_dict()}")
        return

    def on_error(self, status_code):
        print("エラー発生: " + str(status_code))
        return True

    def on_timeout(self):
        print("Timeout...")
        return True


# Twitterオブジェクトの生成
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Listenerクラスのインスタンス
listener = Listener()
# 受信開始
stream = tweepy.Stream(auth, listener)
botter = [
    "1289846552068988933", # bit_moriyama
    "1251325503291588608", # cryptrader2020
    "1248265722217639936", # mockFlyer
    "1235241796789088256", # btcsatoapp
    "1234813279446323200", # fsstreetpiano
    "1233409724814462977", # r1xxal
    "1232288955418021889", # SiGat6cFS4zMWqO
    "1227633193718665217", # Moook1228fx
    "1224578069836521472", # BOTTER74001587
    "1219062567399641088", # tsu_crypt
    "1214890848497782785", # StormBtc
    "1214406811844931584", # bitbotter99
    "1214209769948344320", # CryptoBotKenny
    "1198022938743599105", # aY7OL8RAll64Cvh
    "1191256068589883393", # botter_naminami
    "1189399830851805184", # TraderLust
    "1186672034664697857", # Yunon_botter
    "1186091665364148224", # qutarobot
    "1183226105265680384", # sLKXYOxZLCExwEu
    "1182091014854496256", # mizuiro_ru
    "1176858034653368321", # EwanBotter
    "1174316712444887040", # trade_taroh
    "1172195931023740930", # pinchosssss
    "1169809786864431104", # slime_trader
    "1167113596351811585", # will_create06
    "1163030664607719424", # nocci__
    "1161289315344932866", # kaisei_btc
    "1160713421983084544", # crptkm
    "1160177017540632576", # btcfxpotato
    "1159244094561910784", # btc53301306
    "1155080588581208064", # hogepython
    "1151026742087127040", # crypto__kaiji
    "1149322223636770816", # PpabTrader
    "1147011718138101761", # BSa2alqwPSS3tA4
    "1146645065143476224", # nekoBottter
    "1144557793774432262", # deardeer2020
    "1144376817488285696", # cino_bh
    "1144180424417017857", # crypto_arashi
    "1143418900920459264", # ecteal_comeson
    "1142369562538602496", # Salute19880008
    "1136639734581645312", # dahhhhyama
    "1133695564439146497", # ereonnmaru
    "1133299571805773824", # VdHR7mjeV5lFtx7
    "1131827046852620288", # jp_set
    "1131098516153962496", # matcha_btc
    "1129906510027415552", # bot_araki
    "1128882967055495168", # kokorono_nakakn
    "1128478133303177218", # zar1o
    "1126426088115015680", # mukigorira_san
    "1121599742054506496", # tbachin1
    "1121261583651336192", # kasoutsuker
    "1121219736858025984", # maasa_LL
    "1115970207254630407", # jp011100
    "1114829406780788736", # derivacrypto
    "1113828617316851712", # okinawa_hito
    "1111947470576050180", # BfBotter
    "1110289164824510464", # Vj5hXNEQdp1Mz0j
    "1105416982860423168", # otter_botter
    "1104645076850884608", # pugoog
    "1100387475497701376", # nantona92656718
    "1096063963899387904", # warship_
    "1095878512982933505", # tori_pon_zoo
    "1094786164471455744", # sol_style
    "1094157774982791169", # honehone81
    "1091707697475379200", # slo93769418
    "1089822837664169984", # CryptYasu
    "1089771705675857920", # horumonR_fx
    "1087591853833121793", # BradBotTrader
    "1086917905982271489", # katumikasou
    "1086856136861478912", # yt_bfmaster
    "1085849370245754880", # bittrader2019
    "1083556344521617408", # QuantsMan
    "1081637674849492992", # lvuplife
    "1079377586449457153", # Zawakura3
    "1078183078193901568", # diacompass
    "1078100776499572736", # Python2P
    "1077901273309995008", # Z46463994
    "1076244189493350400", # kijitora_2018
    "1075951615801098240", # Botter33644870
    "1075583889689591809", # BotterCrypto
    "1071983091781005312", # mmbotXXX
    "1071608915811430400", # kawa_program
    "1070354513880539136", # Peach_child_fx
    "1070272656581132294", # kurosutech
    "1069773831919661056", # CryptoAji
    "1069285566611566592", # c0intr8de
    "1066086014630821888", # HeikinP
    "1062079576912719873", # joetheace107
    "1058309042936770562", # erizosanta
    "1056521623879086080", # MattaroSo
    "1055683890847735808", # kokokoyoyoyo121
    "1051830381136080896", # ryjdoge
    "1049574789671673856", # zaihack_com
    "1048569973029842945", # x2a0q
    "1048126479521873922", # One619hebotter
    "1047163419936227328", # poyothon
    "1046970813092642816", # I3RQdTjFidqRhP1
    "1046002448979058688", # akha07638762
    "1045945160704548869", # ayanamirei144
    "1041525488005439488", # rui_crypto8
    "1040148651908067328", # blog_trader_K
    "1040046302824783872", # ea_driver
    "1037589859613851648", # patten_san
    "1036833762493923330", # kagglerkanisawa
    "1036173698422595585", # chibanianyan
    "1033393391654981633", # siro_mmbot
    "1032243278446387200", # arrowhead2018
    "1031103961829269505", # riserice1
    "1028412533781098496", # SakadaruJ
    "1028000231684636672", # arinko_btc
    "1027146763734409217", # crypto_alanjp
    "1027015941928902656", # anoire_fx
    "1026319910438203392", # crypto__moon
    "1026272291238207488", # haruo_bt
    "1026067857392558080", # python_btc_bot
    "1023770273491771393", # nobielu
    "1021174990731804673", # elpheBTCBOT1
    "1020310496027631616", # mpdpdpwq
    "1018860826088726529", # panchan_po
    "1017384271432970241", # hmyk12
    "1014365815661981701", # aluminumkk
    "1014224353980903424", # chikuwa__umai
    "1012576005096009728", # p_faru
    "1011035533835792384", # hogehogehoihoi
    "1010719008012693504", # hoza03565522
    "1010120714790158336", # MAGISYSTEMs
    "1009479039730380800", # 0620Kanno
    "1008351255142387715", # 023incHYqwm2NT6
    "1007811947776040961", # yagirobeibot
    "1007275506268377089", # satan_bitcoin
    "1007205238246289408", # viviff2
    "1006650354962874370", # Freeza_BtcBot
    "1006570658057187328", # CcYuza
    "1006322141976031232", # kazushi_trd
    "1005672974068768768", # trading_algo_Q
    "1005316107597635584", # azuma_bitcoin
    "1003465084046225409", # kf47526970
    "1002511715953623040", # kamayan22345
    "1002509571779248128", # ChikumaroP
    "1002507818119790592", # project_bbb
    "1001066635027886080", # dx_susi
    "1000967297509474305", # hihihihi1986
    "1000406263690285056", # EzIiji
    "1000387817074188288", # KiCrypto
    "1000113852468551680", # klwjrwek
    "999266786192183296", # KoiSo19035148
    "998885285160042497", # MtkN1XBt
    "995632780045250560", # KlSEKATl
    "994812745638916097", # yogabtc
    "994222207273349120", # yaki175
    "993446851729752070", # CryptoYosi
    "992789745552973824", # _elevenpm
    "991318957712789505", # aonori62
    "991024622941364224", # Crpt4Gm
    "989398858378592256", # crypto_gaw
    "988709842574495744", # AAAAisBraver
    "988534550119698432", # mana_community
    "987769246875762688", # btctekunorojii
    "986660838130860032", # low_IQ_penguin
    "984710517263482880", # 836td
    "984337433436160000", # f_dev_o
    "983975513210474498", # taromanabc
    "983581062507839488", # jitensya_btc
    "983082190006177792", # monarier
    "982830335883800576", # NeeTraders
    "982253851905409024", # kunmosky1
    "982194835103756289", # crypto_mori
    "982065005251051520", # qpbitme
    "982039796934561792", # oandalion
    "981892186269626373", # uni_co_bitcoin
    "981165488934809600", # pbUelU9SKZaIkqS
    "980976565306601473", # peanutssking
    "980758913720004608", # crypto_tetsu
    "980640820373041152", # matsu_bitmex
    "980464330100555776", # autorader01
    "980255139612131328", # hig0x
    "980251969175437312", # maasa753
    "979451034933215232", # akagami_lounge
    "978917745587716096", # cryptopippi_dev
    "978187538690072577", # ycrypthon
    "977025692582920192", # ka2kama_bot
    "976771126616457218", # pop_p_ping
    "976416715130028032", # cryptchudoku
    "976300726799319040", # trydiff
    "976067079139807232", # CryptoNinjaX
    "974903712622641152", # ultra_light_up
    "974423416747917312", # postman2829
    "973298261808242689", # ccSurfer2
    "973219710845140992", # regolith1223
    "972874950024441856", # rc_uni0907
    "972722672214802432", # daryl6262
    "972673439017312256", # _P_E_N_T_A
    "972620888095866881", # shimajiro070
    "972383414958477312", # square_of_9
    "971917610622230529", # tibita78
    "970999216351805440", # jassie0406
    "970859328373604353", # _numbP
    "969072225100771328", # hagurinBTC
    "968403982145089536", # mazmex7
    "968300567255658496", # budsrobot
    "967719114050424834", # kinggulf_taco
    "967702498298310656", # tradenist
    "967274437165723650", # sakuraricebird
    "966876408457846784", # wasabi0x00
    "966714225212076034", # istaaaaaaaaa
    "966713048982417408", # piyopiyotch
    "966622484505112577", # Hapix3
    "966211617292718080", # gentokufx
    "966152831185993728", # mnt_coins
    "966131831023153152", # HIROGRAND5252
    "965712511780597761", # dosaken_btc
    "965163270054191105", # fblFveivDJOUBRr
    "964118901863809024", # syasyasyasyathx
    "962953077081784323", # naoto33228429
    "962519068648468481", # Veffidas26
    "962021008013107201", # GRRtestbot
    "961880800051396608", # sato0000xxxx
    "961286551983435776", # yu_btctrader
    "961089805831626752", # tradetomato
    "960085789513105413", # mika1031mika
    "960051784587735040", # ikkiFX1
    "959664130624925696", # algon_fx
    "959262181773594627", # 55_tarou
    "959253285197639680", # flying_medaka
    "958726734047670273", # coin1613
    "958697505872519168", # CKadumin
    "957548784996696065", # koshiitaiyou
    "957379567563370496", # DANCE41956099
    "957187205901967361", # take_btc
    "957181357498679296", # pelo2coin
    "956545439817334784", # yoshino_coin
    "956511435164606464", # yuzoh1125
    "956372937044459520", # kasoutsukayaro1
    "955076748143505408", # cc_infocheck
    "955070187182505986", # bit225
    "955067616434925568", # hami__cc
    "954897069872852992", # aileron_crypto
    "954521273459081216", # pug_crypto
    "954392858571624448", # will_botter
    "953434830506622977", # wizecrpt
    "953414845973450752", # sona_crypto
    "953145190713237504", # mmkey_slil
    "952759442163908608", # ryuden121
    "952073962745286656", # spmonster_coin
    "951805276612628482", # moondancecrypto
    "951368287610224640", # rocka_v
    "950670288533909505", # Crypto_pis
    "950308976264077312", # mojage4
    "950298854674513921", # akane_crypto
    "950281117789143040", # tansokuoji
    "950174697085288450", # anieca_
    "949946529158057984", # tonacoin
    "949648518167257089", # nobu_kasou
    "949493221708582912", # PrDpn5
    "949342278958465024", # bot_btc
    "949295459759153153", # crypto_py0528
    "949210288015884288", # 711lil117
    "949132069380046858", # pen1076
    "948984169148792832", # hasebit1
    "948914678784126977", # halfling_crypto
    "948881895290318849", # ak_ggcjnbcx
    "948877899876061185", # daybreak_trade
    "948828497606197249", # pitI_ax
    "948594259459899392", # hiro_crypto
    "947472773533745157", # kuroshiba_vc
    "947378867517382656", # mukiebi_inv
    "947020820890640384", # kasoyusakapon
    "946980293092638720", # kasousekai2
    "946826509725003776", # nenashi_crypto
    "946613772608618497", # cryptgoat
    "945871220838301701", # sygel_vc
    "945625807602434048", # 6G_bitflyer
    "945615784369254401", # CFOCEOInvestor
    "945596652584304640", # Crypto__Germany
    "945253873698029576", # LilPuun
    "945070186595364864", # hey_fx20170407
    "944963529496444928", # md5_botter
    "944865186481020928", # haranoboyaki
    "943702238622445569", # USER9999999_
    "943690748997881862", # nuunuucrypto
    "943650668660776960", # asayan1026
    "943470383499317248", # boocham_bot
    "943259552442490880", # kasou365
    "942065697395425280", # SAPI_tokyo
    "941528988765241344", # orso_coffee
    "941171509858516992", # coibot127
    "941150195814875136", # Eslice3
    "940897882474889216", # Ros_1224
    "940881620168577024", # yuddill
    "940634952806178816", # otemae_
    "939839494110380032", # yui_bitcoin
    "939837576755666945", # AquaBitMen
    "939796376069619712", # chorocoin
    "939718651913027586", # _moro_hey_yeah
    "939599666466787329", # vx_vix
    "939432220619448320", # yukicryptoo
    "939185990052167680", # mizuguchi_neet
    "938755416439140352", # 2929ojisan
    "938488423584710656", # suama_mbt
    "938182260246720512", # 46bNT3p7XlbWYAV
    "937886630886588416", # weidenthal_llc
    "936939958467674112", # iNaGoBotTrader
    "935525592476172288", # Gaku_cc
    "935448856652685312", # coincoin228
    "935354266348265474", # DeepBlu23167471
    "934939218329026561", # botcat1127
    "934782172564566018", # codepimpone
    "934769123074113538", # unique_ptr_void
    "933871790916485120", # de_no_hito
    "933562753821786112", # bot_Kingdom_
    "932270650575675393", # b_b_sum
    "931907507445891073", # GIRO_air_trader
    "931533348366778368", # takapicoin
    "931172509277339648", # koutya_crypto
    "930565590166659072", # i_love_profit
    "930458771347816448", # CRYPTANNEWS
    "929915855575572481", # ShibaInu9984
    "929740346275196928", # prince_fintech
    "929185095256174592", # cryptomegane
    "927975918043201536", # qpawosk
    "926674249841917953", # mocako55
    "926281122098454532", # K_dia_myt
    "925916586048815105", # Shura_Coin
    "925733909542854657", # pocotin_dragon
    "925599792310321152", # momo_cryptoc
    "925341814772527104", # condoy_jp
    "925039589554757632", # gyun0228
    "922887725065179136", # YOPP_bit
    "922491724328349696", # zephel01_vc
    "921735723501338625", # masao_FX
    "920598613008441344", # k_dull_ge
    "919950091183579136", # Ceron47188479
    "919924906858496000", # akifukaki8
    "915123745324359681", # moycoin
    "915011860700700672", # code_3333
    "914812018024165376", # panbtc
    "913760112581292032", # ClamGBP
    "913707288371675136", # kitkatbtc
    "913694321198604288", # BtcOniku
    "913201584695156741", # btc_bollinger
    "912585133571448832", # zenmodo4
    "912422569919225856", # yuu_kun00
    "912157452941983745", # poke12
    "911781758714052608", # Redmeteor_777
    "911561201057808384", # naokenhappy
    "909983937895718913", # AlphaBit6
    "908706167924260864", # bbbit3
    "908211844925464576", # shinjiro_tigers
    "907937621833261059", # On_Dreamy
    "907637186245169155", # SiroNegio
    "907244736590704640", # secretroadsan
    "906487805429260288", # minitoma_too
    "904785826831155201", # megane_benzou
    "903904173032275968", # x133704
    "903641532435013633", # nakanoponte
    "903179324370575360", # tiger_losscat
    "902832695956221952", # Gorillazee3
    "902736572751069184", # hyouhikaku
    "902563786896191488", # RyuKitchan
    "901328068739870720", # xxxElxxx
    "899907325691019264", # bitco_samurai
    "899582828773429248", # Warashibe2020
    "897660481577426944", # webmoneylife
    "897547523048574976", # _nayotake
    "897012823330390016", # Crypto_Nyanko
    "896422102873497600", # bitmex_fun
    "895925058715111425", # Lara_Bell_com
    "895531483795832832", # ballsan8
    "894845371465121792", # Akao_KunKun
    "894444290432155648", # okinawa_villa
    "893985024508215296", # takeuchi_fx
    "893641170957377536", # crypto_child
    "893604317604618241", # Naop_cc
    "893155277926670336", # DeepCafelate
    "892847954402304001", # arakuma3tw
    "892745086869491712", # yoshinakkuru
    "892003556164648960", # gankochan1000
    "891994408916144128", # Maruo666Maruo
    "890417165760741376", # Inok_04
    "890367543596142592", # taka_tore_a
    "889689085857550337", # CstToken
    "889620845039157249", # npp_crypto
    "887887775072043008", # JhonConnorBoom
    "887083560577970177", # tsuyoshh72
    "886744069715574784", # buch_buch_
    "885036358884098049", # junk_x_jp
    "882498801675534336", # ryuta461
    "880134331355742208", # okachan_nem
    "879644069118353408", # kuromachart
    "878615505522671618", # VBAExcel
    "878218217109331968", # bit_taroh
    "878090159094341632", # DD55884641
    "875430112614768640", # crypto_M_esi
    "875247861511864320", # timutimusan
    "874121710773035008", # huuka_u_u
    "873686825444941824", # trademu
    "870085516074418176", # Poitan_unyo
    "869156984427171841", # fujimonkabu
    "868805461503389696", # LoveCypt0528
    "868129592099328000", # NiceCurrencyX
    "865589576772927488", # kws_fx
    "864926544178761728", # misanfx
    "862548106654515200", # alcoint
    "861946612569972736", # mari4mgo
    "861797543285411840", # ETHxCC
    "858663216821395456", # moca_virt
    "856507781536374786", # wakamennb
    "856396597734678528", # souma5553
    "855687879850209280", # yasu42810
    "854038733363884032", # chacchi0013
    "853208890401366023", # cryptoJUN
    "852117956653961216", # VvEzYTKcVG45OxP
    "852085058911338496", # FitnessMasa
    "851956965270048769", # GANTUPPA_jyoshi
    "850565251783303168", # yamabiko_fx
    "850181849326403585", # 1000crypto
    "847038891819347968", # jigsaw0875
    "846549326608285696", # asapura_crypto
    "843845396782759936", # t_fal04
    "842000330426470400", # btc_bot_player
    "841657912330145792", # yu_gorina
    "840991086629683200", # bitter_jr2
    "840239541768208384", # btc_FX
    "840155668149493761", # inagoflyer
    "840006382657069056", # bitcoin_orrrrr
    "837918338781097984", # bitcoinseeker
    "835838710876782594", # maslogo837
    "835662703888781312", # hirocrypto5
    "831837264225263616", # __main__2525
    "830220611574079488", # ishi_kaeru
    "829697912066093057", # asset_zz
    "829338555897884672", # bF_TASK
    "829143240519536641", # zHXILhARlbQMvjm
    "825733049346248704", # kisabu68
    "825703058122240001", # sukiyakifin
    "822721565456334849", # geboneko
    "819687263684567040", # nomushiki1
    "819096647745486848", # 369_nagisa
    "818699533324460034", # 10hu_mental
    "816553184306962433", # sig_246
    "813845536939773952", # Twoer_alt
    "813728314657361920", # Hitoma555
    "811520460986793984", # kanikama_bit
    "810497876648456192", # blog_uki
    "810129735841783808", # nmtng_net
    "807590094446039041", # dan5_daifuku
    "807054716018376705", # fx_ichizo
    "805052448117125120", # trawi_chaaan
    "800665141876432899", # dosu0217
    "798701963659472896", # Organic80249724
    "798524185001672705", # llIllIlllllllII
    "796356226292457473", # kentyinvester
    "794834741291716608", # xiction1
    "793497999364063232", # Shiqquit
    "791228037513617409", # snowmak13
    "788897827875385344", # sakechi_btc
    "785988721191428096", # tokyowl03
    "785666331332927488", # usigma_
    "785513668381282305", # jdgthjdg
    "784797412615262209", # amdapsi
    "780413999217115136", # miso930
    "777432002806984704", # ryu_botter
    "776745175393579008", # cafeore621
    "772662689864617984", # tanaka_bot_1
    "772355836572164096", # Seville1985
    "769144685826707456", # __WannaBeFree
    "765751028897550340", # autotrademt4
    "754412944285282304", # tadajam
    "753985430681296896", # kanadanotcanada
    "753025401383903232", # tyakoske
    "752173785445306368", # ebch_fx
    "747062396397621249", # tacotokyo
    "747046722791038976", # lightdogs6
    "743303837692235776", # R_Bit_coin
    "738928201162838016", # sen_axis
    "737450784720224256", # _hi_ro_no
    "732195521612259332", # phasespacegate
    "731467924154634241", # kannapoix_jp
    "731332100108881920", # Calcaly73
    "726324706144481280", # telfolio
    "711846798587863040", # xinxin_crypto
    "711481173147422721", # meguru_jp
    "707776397620568066", # ckaapnsa
    "704676698680209409", # taro_shi_310
    "704267541204447232", # Samoyeed
    "4887990166", # kumicho5515
    "4844938058", # namuyan_mine
    "4844304582", # oshaberidepas
    "4709782813", # asupega
    "4567472173", # kinoko1100
    "4453658952", # Nagi7692
    "4437776112", # uhohoiarale
    "4300391714", # rintam_jp
    "4299400711", # snufkin0866
    "3945898334", # francesan5
    "3870673514", # ir0nant_2nd
    "3515736624", # SatyMale
    "3499169774", # forDogs0728
    "3393267914", # kamezou1990
    "3332956154", # qunyoel
    "3323233886", # pgnishi
    "3321562472", # fuyuton
    "3305723606", # pythagorastock
    "3282150948", # sgkabu
    "3279416004", # crptoresearcher
    "3269386356", # Ubermenschkind
    "3248676294", # comusou3
    "3244470595", # procman01
    "3238339590", # privdai
    "3234642703", # satosiportfolio
    "3215104205", # junfoxy
    "3188591906", # hagesensei
    "3168518592", # qq_ack
    "3130332204", # Nickel_Mekki
    "3116614377", # moh_ssk
    "3098213941", # kuuuminnn898
    "3081288350", # dokanyasan
    "3068066791", # kuttsunx
    "3067564688", # kineFX
    "3028623018", # battle_no1
    "3026465162", # hanbe_fx
    "3021186030", # kapipara180
    "2993756635", # jitekineko
    "2976632035", # y_nWozillion
    "2976341532", # johnny_mnz
    "2969235390", # eds110721
    "2959730910", # NL_ENGR_LAB
    "2922727938", # eiken7kyuu
    "2915996250", # torimeshi_wot
    "2909190199", # NL_ENGR
    "2880617515", # deknight440
    "2870827981", # daisukipython
    "2800923745", # foxfoxdev
    "2790922904", # riugurumi
    "2790152815", # Natun_10th
    "2725882494", # hajimechan17
    "2685510524", # fopen_s
    "2584981116", # take5685788
    "2486484307", # nonbirisuruzo
    "2477536692", # lifeez218
    "2423870731", # zyunzyunx
    "2395306045", # gigasawasan
    "2349485090", # Whiskey_bonbon_
    "2336147096", # longshort111
    "2321892516", # him0net
    "2280387523", # catalan_fx
    "2278664010", # rara_st70
    "2259676664", # earlycross007
    "2251618063", # ysuifa
    "2239131776", # yamato_zz
    "2237351016", # satonaka_jp
    "2200751418", # tenten1091
    "2199620604", # nihnuf
    "2198929027", # kokoro_sf
    "2196013645", # brokenthemoon
    "2180160960", # haradadaijiroa
    "2177963378", # GUINEESS
    "2174134688", # _Erisnoel
    "1928991481", # keita_startup
    "1908835784", # yoshiso44
    "1906668986", # yopo777
    "1863221946", # ranranDenki
    "1731982248", # alunbot
    "1707655442", # captain_fuckpos
    "1700679781", # ucchi_macha
    "1682613648", # nakaneiroiro
    "1677298866", # Luk2424
    "1656630708", # pokerlogs
    "1649745049", # xxgreedx
    "1544904660", # trotrogame
    "1465192298", # furatocoin
    "1404458588", # MJ24_trader
    "1401843780", # ihrimi2115
    "1319874686", # nickworks_net
    "1316029926", # Coo_nine2
    "1309779266", # undertheedge2
    "1179541446", # takotako_sun
    "1076848296", # sys_tradingtech
    "1050393517", # takiyamamama
    "1042008901", # rav_wol
    "893084268", # free1967cool
    "769517911", # dddatacrazy
    "761692747", # hoshitter1
    "733957470", # gaco_botter
    "636121957", # dgunji1
    "633116912", # snowfox_botter
    "612182870", # _tsubuo
    "610709672", # echos1121
    "599825946", # ritsuL_coin
    "592704993", # akihirot1
    "581871304", # tkm2261
    "576225186", # dev02081
    "575138428", # CKDryD
    "529471955", # sawara_fx
    "521248085", # J4Np_12
    "519674291", # taku_nyanco
    "514533425", # kiki0625k
    "498524336", # hat_fx
    "491787753", # kkk23232356
    "490275592", # wista_10
    "466120292", # tayappi
    "464394488", # djt_trader
    "443756474", # poso_crypto
    "440955862", # nikaidou49
    "435418011", # asahinoboru_jp
    "424960823", # asaasa21
    "413808270", # jogo_Hi
    "411066741", # CCRising_Dragon
    "406676327", # CANNABIS_ZET
    "398486804", # vs_ino
    "396466885", # d2ftaxi
    "382568334", # yasuFX
    "378692715", # kobin0
    "376523714", # ymgcsm
    "369040158", # yuzjpon
    "363609094", # akoedayo
    "350976740", # milkTornado
    "330998778", # reiru57
    "322677545", # sjpuu
    "320569566", # azul_1221
    "307247014", # Rascal_Sekaikan
    "306802376", # a_gu_ni
    "296154749", # v0w0vv0w0v
    "283778892", # reo3313
    "275043445", # ravitk7
    "265223061", # javeleeer
    "264694839", # kieli0605
    "262755484", # ni_ch
    "258277058", # o_matsuo
    "249014013", # Aloe_A_
    "243683151", # funnist_jp
    "242250432", # _tshink
    "231474223", # ra1zou
    "223072860", # ASIM_IKASIK
    "220375671", # simuya01
    "217329652", # jigooooo
    "210810323", # gloomy_btc
    "196080121", # dakuruto
    "195614547", # EATis
    "191452463", # ea_ika_
    "186654494", # wmatch
    "183437210", # kuchanFX
    "179562677", # muzikun
    "155926323", # KonsanSankon
    "150657896", # caster2none
    "146057625", # Zeni_Navi
    "144327185", # pitopitomm
    "144026985", # ItaGreQ
    "143764225", # tk____42
    "138037217", # nemo_n
    "137996935", # akkagi0416
    "134066098", # yasu_smaholi
    "133683521", # FXjaguar
    "128189848", # furureba
    "127228963", # mokkyu9
    "124698529", # Star_Platina_
    "123171888", # otominet
    "122639011", # ahaha_fxtrader
    "121334842", # tacosMars
    "118687303", # NegiNippon
    "117985262", # yutilil
    "115644398", # mamu_miko
    "114920971", # investmemo
    "113305090", # code_x98000
    "108979900", # teresan256
    "107277457", # toyolab
    "106417915", # sir_siro
    "103298085", # sou01a
    "77695849", # SoftgateJa
    "69485652", # devision00
    "69000993", # egu_chan
    "63784245", # haru_86
    "38843150", # pirowiki
    "37229267", # fukata
    "33877867", # taiga1002
    "23715221", # bui_ningyou
    "22381222", # liquidfunc
    "18946332", # sekitosa
    "14941736", # supermomonga
    "14770638", # 0g
    "14450328", # kojingharang
    "14438068", # ultraistter
    "13580172", # gusutabo
    "7680122", # arms22
    "7217102", # imos
    "4053901", # smly
    "4003701", # meetaco_
    "2444181", # bartomo
]
mirror_trade = [
    "1257488025845592064", # neoneet_jiro
    "1211190353379745792", # av_sachi
    "1204182826540601344", # demokouzasuki
    "987847525058072576", # 26n_BTC
    "964369833625141248", # Light_Yagami_a
    "862199038283661312", # jaggaimoman
]
follow = botter + mirror_trade
print("start collect stream")
stream.filter(follow=follow)