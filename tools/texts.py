# -*- coding: utf-8 -*-
"""Modun tum Turkce metinleri. build_text.py bu dosyayi okuyarak XML ve SQL uretir."""

CIVS = ["OSMAN", "ORHAN", "FATIH", "YAVUZ", "BATTAL", "ATATURK"]

# ---------------------------------------------------------------- sehirler
CITIES = {
    "OSMAN": ["Söğüt", "Bilecik", "Karacahisar", "Domaniç", "İnegöl", "Yenişehir", "Eskişehir", "Bozüyük",
              "Yarhisar", "Mudurnu", "Göynük", "Taraklı", "Geyve", "Akyazı", "Kütahya", "Ermeni Pazarı",
              "Lefke", "Mekece", "Seyitgazi Yolu", "Gölpazarı"],
    "ORHAN": ["Bursa", "İznik", "İzmit", "Gemlik", "Mudanya", "Bergama", "Balıkesir", "Gelibolu", "Bolayır",
              "Çorlu", "Tekirdağ", "Ulubat", "Kirmasti", "Edremit", "Biga", "Karamürsel", "Kandıra", "Çimpe",
              "Keşan", "Malkara"],
    "FATIH": ["İstanbul", "Edirne", "Galata", "Üsküdar", "Amasra", "Sinop", "Semendire", "Üsküp", "Prizren",
              "Saraybosna", "Mora", "Midilli", "Eğriboz", "İşkodra", "Kefe", "Akkerman", "Otranto", "Konya",
              "Karaman", "Rumeli Hisarı"],
    "YAVUZ": ["Amasya", "Kahire", "Şam", "Halep", "Kudüs", "Mekke", "Medine", "Tebriz", "Diyarbakır", "Mardin",
              "Gazze", "Trablusşam", "İskenderiye", "Antep", "Urfa", "Dımaşk Kalesi", "Ridaniye", "Mercidabık",
              "Hama", "Humus"],
    "BATTAL": ["Malatya", "Seyitgazi", "Amorium", "Tarsus", "Adana", "Maraş", "Antakya", "Sivas", "Tokat", "Niksar",
               "Elbistan", "Darende", "Kemah", "Erzincan", "Harput", "Çorum", "Afyonkarahisar", "Kayseri",
               "Zamantı", "Gürün"],
    "ATATURK": ["Ankara", "İzmir", "Samsun", "Erzurum", "Selanik", "Havza", "Amasya Genelgesi", "Antalya", "Trabzon",
                "Gaziantep", "Kahramanmaraş", "Şanlıurfa", "Sakarya", "Dumlupınar", "İnönü", "Çanakkale",
                "Kocatepe", "Elazığ", "Van", "Hatay"],
}
# Not: "Amasya Genelgesi" ve "Seyitgazi Yolu" gibi adlar cakisma olmasin diye secildi; asagida duzeltildi.
CITIES["ATATURK"][6] = "Kastamonu"
CITIES["OSMAN"][18] = "Osmaneli"

SPIES = {
    "OSMAN": ["Turgut Alp", "Samsa Çavuş", "Konur Alp", "Akça Koca", "Abdurrahman Gazi", "Aykut Alp", "Hasan Alp",
              "Gündüz Alp", "Saltuk Alp", "Bamsı Bey"],
    "ORHAN": ["Hacı İlbey", "Gazi Evrenos", "Lala Şahin", "Çandarlı Kara Halil", "Süleyman Paşa", "Akçakoca",
              "Karamürsel Bey", "Konuralp", "Ece Bey", "Fazıl Bey"],
    "FATIH": ["Zağanos Paşa", "Mahmud Paşa", "Gedik Ahmed", "Akşemseddin", "Ali Kuşçu", "Molla Gürani",
              "Hadım Süleyman", "Turahan Bey", "Baltaoğlu", "Ulubatlı Hasan"],
    "YAVUZ": ["Hadım Sinan", "Piri Mehmed", "İdris-i Bitlisi", "Hayır Bey", "Canberdi Gazali", "Mustafa Paşa",
              "Ferhad Paşa", "Kemalpaşazade", "Hüsrev Paşa", "Pîrî Reis"],
    "BATTAL": ["Seyyid Ahmed", "Abdülvehhab Gazi", "Ömer Hakim", "Cafer Bey", "Danişmend Ahmed", "Şücaeddin",
               "Melik Gazi", "Artuk Bey", "Akkoyunlu Hasan", "Sultan Şuca"],
    "ATATURK": ["Kâzım Karabekir", "İsmet İnönü", "Fevzi Çakmak", "Rauf Orbay", "Halide Edib", "Ali Fuat Cebesoy",
                "Refet Bele", "Nene Hatun", "Fahrettin Altay", "Sakallı Nurettin"],
}

TEXT = {}


def t(tag, text):
    TEXT[tag] = text


# ======================================================================
# OSMAN BEY - KAYI BEYLIGI
# ======================================================================
t("TXT_KEY_CIV_TL_OSMAN_DESC", "Kayı Beyliği")
t("TXT_KEY_CIV_TL_OSMAN_SHORT_DESC", "Kayı")
t("TXT_KEY_CIV_TL_OSMAN_ADJECTIVE", "Kayı")
t("TXT_KEY_LEADER_TL_OSMAN", "Osman Bey")
t("TXT_KEY_TRAIT_TL_OSMAN_SHORT", "Kuruluş Rüyası")
t("TXT_KEY_TRAIT_TL_OSMAN",
  "Sınırlar %33 daha hızlı genişler. Her şehir +1 [ICON_FOOD] Gıda üretir.")
t("TXT_KEY_CIV5_DAWN_TL_OSMAN_TEXT",
  "Selam sana, Osman Bey, Ertuğrul Gazi'nin oğlu ve Kayı boyunun yiğit önderi! Bizans ile Selçuklu "
  "arasındaki o çalkantılı uç bölgesinde, Söğüt'ün yeşil vadilerinde büyüdün. Bir gece Şeyh Edebali'nin "
  "evinde uyurken rüyanda göğsünden bir ağaç çıktığını, dallarının dünyayı gölgelediğini gördün. Bu rüya "
  "senin ve soyunun kaderi oldu: küçük bir uç beyliği, kılıcın, adaletin ve sabrınla bir cihan devletinin "
  "temeline dönüştü.[NEWLINE][NEWLINE]Osman Bey, obanı yeniden toplamanın vakti geldi. Atlıların hazır, "
  "otlakların geniş. Toprağı adaletle yönetecek ve rüyadaki o ağacı göğe yükseltecek bir devlet kurabilecek misin?")
t("TXT_KEY_LEADER_TL_OSMAN_PEDIA", "Osman Bey")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_OSMAN_NAME", "Osman Bey")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_OSMAN_SUBTITLE", "Kayı Beyliği'nin ve Osmanlı Devleti'nin Kurucusu")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_OSMAN_LIVED", "y. 1258 - 1326")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_OSMAN_HEADING_1", "Hayatı")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_OSMAN_TEXT_1",
  "Osman Bey, Oğuzların Kayı boyuna mensup Ertuğrul Gazi'nin oğludur. Babasının ölümünden sonra Söğüt ve "
  "Domaniç çevresindeki aşiretin başına geçti. Bizans tekfurlarıyla mücadele ederek Karacahisar, Bilecik, "
  "Yarhisar ve İnegöl gibi kaleleri ele geçirdi. Geleneksel olarak 1299 yılı, beyliğin bağımsızlığının "
  "başlangıcı kabul edilir.")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_OSMAN_HEADING_2", "Şeyh Edebali ve Rüya")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_OSMAN_TEXT_2",
  "Osmanlı kroniklerine göre Osman Bey, Şeyh Edebali'nin evinde misafirken rüyasında şeyhin göğsünden çıkan "
  "bir ayın kendi göğsüne girdiğini, ardından göğsünden büyük bir ağaç yükselip dallarının dünyayı "
  "kapladığını gördü. Şeyh Edebali bu rüyayı Osman Bey'e ve soyuna verilecek bir hükümranlık müjdesi olarak "
  "yorumladı ve kızı Malhun (veya Rabia) Hatun'u onunla evlendirdi. Osman Bey, Bursa kuşatması sürerken "
  "1326 civarında vefat etti; şehri oğlu Orhan fethetti.")

# ======================================================================
# ORHAN GAZI - OSMANLI BEYLIGI
# ======================================================================
t("TXT_KEY_CIV_TL_ORHAN_DESC", "Osmanlı Beyliği")
t("TXT_KEY_CIV_TL_ORHAN_SHORT_DESC", "Osmanlı Beyliği")
t("TXT_KEY_CIV_TL_ORHAN_ADJECTIVE", "Osmanlı")
t("TXT_KEY_LEADER_TL_ORHAN", "Orhan Gazi")
t("TXT_KEY_TRAIT_TL_ORHAN_SHORT", "İlk Düzenli Ordu")
t("TXT_KEY_TRAIT_TL_ORHAN",
  "Yakın dövüş ve barutlu birimler %25 daha hızlı üretilir ve +10 deneyimle başlar. "
  "Kara birimlerinin bakım masrafı %25 daha azdır.")
t("TXT_KEY_CIV5_DAWN_TL_ORHAN_TEXT",
  "Selam sana, Orhan Gazi, Osman Bey'in oğlu! Babanın yaktığı ocağı bir beylikten devlete dönüştürdün. "
  "Bursa'yı alıp başkent yaptın, İznik'i ve İzmit'i fethettin. İlk Osmanlı akçesini bastırdın, İznik'te ilk "
  "medreseyi açtın ve yaya ile müsellemlerden oluşan ilk düzenli orduyu kurdun. Oğlun Süleyman Paşa ile "
  "Çanakkale'yi geçerek Rumeli'ye ilk adımı attın.[NEWLINE][NEWLINE]Orhan Gazi, halkın düzen, askerin disiplin "
  "bekliyor. Kanunla, ilimle ve kılıçla iki kıtaya uzanan bir devlet kurabilecek misin?")
t("TXT_KEY_LEADER_TL_ORHAN_PEDIA", "Orhan Gazi")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_ORHAN_NAME", "Orhan Gazi")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_ORHAN_SUBTITLE", "Osmanlı Beyliği'nin İkinci Hükümdarı")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_ORHAN_LIVED", "y. 1281 - 1362")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_ORHAN_HEADING_1", "Bursa'dan Rumeli'ye")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_ORHAN_TEXT_1",
  "Orhan Gazi 1326'da Bursa'yı fethederek beyliğin merkezi yaptı. 1329'da Palekanon (Maltepe) Savaşı'nda "
  "Bizans ordusunu yendi, 1331'de İznik'i, 1337'de İzmit'i aldı. Karesi Beyliği'ni topraklarına katarak "
  "donanma geleneğine sahip bir bölgeyi kazandı. 1352'de Çimpe Kalesi'ne, 1354'te Gelibolu'ya yerleşilmesiyle "
  "Osmanlılar Rumeli'ye geçti.")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_ORHAN_HEADING_2", "Devlet Teşkilatı")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_ORHAN_TEXT_2",
  "Orhan Gazi döneminde ilk gümüş akçe basıldı, ilk Osmanlı medresesi 1331'de İznik'te açıldı ve "
  "aşiret kuvvetlerinin yanında yaya ve müsellem adı verilen ilk düzenli askerî birlikler oluşturuldu. "
  "Bu adımlar, beyliğin bir uç teşkilatından kurumsal bir devlete dönüşmesinin temelini attı.")

# ======================================================================
# FATIH SULTAN MEHMET - OSMANLI DEVLETI
# ======================================================================
t("TXT_KEY_CIV_TL_FATIH_DESC", "Osmanlı Devleti")
t("TXT_KEY_CIV_TL_FATIH_SHORT_DESC", "Osmanlı Devleti")
t("TXT_KEY_CIV_TL_FATIH_ADJECTIVE", "Osmanlı")
t("TXT_KEY_LEADER_TL_FATIH", "Fatih Sultan Mehmet")
t("TXT_KEY_TRAIT_TL_FATIH_SHORT", "Kuşatma Ustası")
t("TXT_KEY_TRAIT_TL_FATIH",
  "Kuşatma birimleri şehirlere karşı +%30 savaş gücü kazanır. Fethedilen şehirlerde direniş süresi yarıya iner "
  "ve fetih başına şehir nüfusu x 10 [ICON_GOLD] Altın kazanılır.")
t("TXT_KEY_CIV5_DAWN_TL_FATIH_TEXT",
  "Selam sana, Sultan II. Mehmet, Kayser-i Rûm ve iki denizin hakanı! Henüz yirmi bir yaşındayken, asırlardır "
  "fethedilemeyen Konstantinopolis'in surlarını dev toplarınla dövdün. Gemilerini karadan yürütüp Haliç'e "
  "indirdin ve 29 Mayıs 1453'te şehri fethederek bir çağı kapatıp yenisini açtın. Sırbistan'ı, Mora'yı, "
  "Bosna'yı ve Kırım'ı egemenliğine kattın; Ali Kuşçu gibi âlimleri sarayında ağırladın.[NEWLINE][NEWLINE]"
  "Ey Fatih, dünya yeni bir fetih bekliyor. Bilimin ve topun gücüyle Kızıl Elma'ya ulaşabilecek misin?")
t("TXT_KEY_LEADER_TL_FATIH_PEDIA", "Fatih Sultan Mehmet")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_FATIH_NAME", "Fatih Sultan Mehmet")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_FATIH_SUBTITLE", "İstanbul'un Fatihi, Osmanlı Padişahı")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_FATIH_LIVED", "1432 - 1481")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_FATIH_HEADING_1", "İstanbul'un Fethi")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_FATIH_TEXT_1",
  "II. Mehmet, 1451'de ikinci kez tahta çıktı. Boğaz'ın kontrolü için Rumeli Hisarı'nı yalnızca birkaç ayda "
  "inşa ettirdi. 6 Nisan 1453'te başlayan kuşatmada büyük toplar kullanıldı, gemiler karadan Haliç'e "
  "indirildi. Şehir 29 Mayıs 1453'te fethedildi ve Bizans İmparatorluğu sona erdi. Bu fetih, birçok tarihçi "
  "tarafından Orta Çağ'ın sonu olarak kabul edilir.")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_FATIH_HEADING_2", "Devlet Adamı ve Bilim Hamisi")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_FATIH_TEXT_2",
  "Fatih, Kanunname-i Âl-i Osman ile devlet teşkilatını düzenledi. Fatih Külliyesi'ni ve Sahn-ı Seman "
  "medreselerini kurdurdu, Kapalıçarşı'nın çekirdeği olan Cevahir Bedesteni'ni yaptırdı. Rumca, Arapça ve "
  "Farsça kaynaklarla ilgilendi; astronom Ali Kuşçu'yu İstanbul'a davet etti; İtalyan ressam Gentile Bellini "
  "onun portresini yaptı. 1481'de yeni bir sefere çıkarken Gebze yakınlarında vefat etti.")

# ======================================================================
# YAVUZ SULTAN SELIM - OSMANLI HILAFETI
# ======================================================================
t("TXT_KEY_CIV_TL_YAVUZ_DESC", "Osmanlı Hilafeti")
t("TXT_KEY_CIV_TL_YAVUZ_SHORT_DESC", "Osmanlı Hilafeti")
t("TXT_KEY_CIV_TL_YAVUZ_ADJECTIVE", "Osmanlı")
t("TXT_KEY_LEADER_TL_YAVUZ", "Yavuz Sultan Selim")
t("TXT_KEY_TRAIT_TL_YAVUZ_SHORT", "Halifelik")
t("TXT_KEY_TRAIT_TL_YAVUZ",
  "Öldürülen düşman birimlerinin savaş gücünün %50'si kadar [ICON_PEACE] İnanç kazanılır. Fethedilen her şehir, "
  "nüfusu x 15 [ICON_PEACE] İnanç kazandırır.")
t("TXT_KEY_CIV5_DAWN_TL_YAVUZ_TEXT",
  "Selam sana, Yavuz Sultan Selim, Hâdimü'l-Haremeyni'ş-Şerifeyn! Sekiz yıl gibi kısa bir saltanatta "
  "devletinin topraklarını neredeyse iki katına çıkardın. Çaldıran'da toplarınla ve tüfekli yeniçerilerinle "
  "Şah İsmail'in süvarilerini dağıttın. Mercidabık'ta ve Ridaniye'de Memlükleri yenerek Suriye'yi, Mısır'ı ve "
  "Hicaz'ı egemenliğine kattın; Kutsal Emanetler İstanbul'a geldi.[NEWLINE][NEWLINE]Ey Yavuz, gözün doğuyu ve "
  "güneyi görüyor. Halkın senden korku ve saygı bekliyor. İslam dünyasını tek sancak altında toplayabilecek misin?")
t("TXT_KEY_LEADER_TL_YAVUZ_PEDIA", "Yavuz Sultan Selim")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_YAVUZ_NAME", "Yavuz Sultan Selim")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_YAVUZ_SUBTITLE", "Osmanlı Padişahı ve Halife")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_YAVUZ_LIVED", "1470 - 1520")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_YAVUZ_HEADING_1", "Doğu ve Güney Seferleri")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_YAVUZ_TEXT_1",
  "I. Selim, Trabzon sancakbeyliği yaptıktan sonra 1512'de tahta çıktı. 1514'te Çaldıran Savaşı'nda Safevi "
  "hükümdarı Şah İsmail'i yendi ve Tebriz'e girdi. 1516'da Mercidabık'ta, 1517'de Ridaniye'de Memlük "
  "ordularını bozguna uğrattı. Bu seferlerle Suriye, Filistin, Mısır ve Hicaz Osmanlı topraklarına katıldı.")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_YAVUZ_HEADING_2", "Hilafet ve Mirası")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_YAVUZ_TEXT_2",
  "Mısır'ın fethiyle Mekke ve Medine'nin koruyuculuğu Osmanlılara geçti. Geleneksel anlatıya göre Abbasi "
  "halifesi III. Mütevekkil hilafeti Yavuz'a devretti; tarihçiler bu devrin biçimini tartışsa da halifelik "
  "unvanı sonraki yüzyıllarda Osmanlı padişahlarınca kullanıldı. Yavuz aynı zamanda Farsça şiirler yazan bir "
  "şairdi. 1520'de Çorlu yakınlarında, Sırtköy'de vefat etti.")

# ======================================================================
# BATTAL GAZI - UC GAZILERI
# ======================================================================
t("TXT_KEY_CIV_TL_BATTAL_DESC", "Uç Gazileri")
t("TXT_KEY_CIV_TL_BATTAL_SHORT_DESC", "Gaziler")
t("TXT_KEY_CIV_TL_BATTAL_ADJECTIVE", "Gazi")
t("TXT_KEY_LEADER_TL_BATTAL", "Seyyid Battal Gazi")
t("TXT_KEY_TRAIT_TL_BATTAL_SHORT", "Destan Kahramanı")
t("TXT_KEY_TRAIT_TL_BATTAL",
  "Yakın dövüş ve atlı birimler dost topraklar dışında +%15 savaş gücü kazanır. [ICON_GREAT_GENERAL] Büyük "
  "General üretimi +%50, yağmadan elde edilen [ICON_GOLD] Altın +%100.")
t("TXT_KEY_CIV5_DAWN_TL_BATTAL_TEXT",
  "Selam sana, Seyyid Battal Gazi, uçların aslanı ve destanların kahramanı! Malatya'dan çıkıp Bizans "
  "sınırlarında akınlar yaptın. Adın dilden dile, kopuzdan kopuza dolaştı. Battalnâme'de anlatılan "
  "yiğitliklerin, yüzyıllar boyunca Anadolu'nun gazilerine ve dervişlerine ilham verdi. Bugün Seyitgazi'deki "
  "türben hâlâ ziyaretçilerle dolup taşıyor.[NEWLINE][NEWLINE]Ey Gazi, at kişniyor, sınır boyları seni "
  "çağırıyor. Uçlardan bir devlet doğurup adını ebedî kılabilecek misin?")
t("TXT_KEY_LEADER_TL_BATTAL_PEDIA", "Seyyid Battal Gazi")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_BATTAL_NAME", "Seyyid Battal Gazi")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_BATTAL_SUBTITLE", "Anadolu Destanlarının Kahramanı")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_BATTAL_LIVED", "? - y. 740")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_BATTAL_HEADING_1", "Tarihteki Battal")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_BATTAL_TEXT_1",
  "Battal Gazi'nin tarihî kişiliği, Emevîler döneminde Bizans'a karşı akınlar düzenleyen ve Malatya ile "
  "ilişkilendirilen komutan Abdullah el-Battal'a dayanır. Arap kaynaklarına göre el-Battal, 740 yılında "
  "Akroinon (bugünkü Afyonkarahisar yakınları) Savaşı'nda hayatını kaybetmiştir. Tarihî bilgiler sınırlıdır; "
  "bu nedenle bu modda Battal Gazi tarihî bir hükümdardan çok bir destan kahramanı olarak canlandırılmıştır.")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_BATTAL_HEADING_2", "Destandaki Battal")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_BATTAL_TEXT_2",
  "Anadolu'nun Türkleşme sürecinde Battal Gazi, Türk halk edebiyatının en sevilen kahramanlarından biri oldu. "
  "Battalnâme adlı destanda doğaüstü yiğitlikleriyle anlatıldı ve Danişmendnâme gibi sonraki gazavatnâmelere "
  "örnek teşkil etti. Eskişehir'in Seyitgazi ilçesindeki türbesi ve külliyesi, Selçuklu döneminden beri önemli "
  "bir ziyaret yeridir.")

# ======================================================================
# ATATURK - TURKIYE CUMHURIYETI
# ======================================================================
t("TXT_KEY_CIV_TL_ATATURK_DESC", "Türkiye Cumhuriyeti")
t("TXT_KEY_CIV_TL_ATATURK_SHORT_DESC", "Türkiye")
t("TXT_KEY_CIV_TL_ATATURK_ADJECTIVE", "Türk")
t("TXT_KEY_LEADER_TL_ATATURK", "Mustafa Kemal Atatürk")
t("TXT_KEY_TRAIT_TL_ATATURK_SHORT", "Cumhuriyet İnkılapları")
t("TXT_KEY_TRAIT_TL_ATATURK",
  "Tüm şehirlerde [ICON_RESEARCH] Bilim ve [ICON_CULTURE] Kültür +%10. Kara birimleri dost topraklarda "
  "+%15 savaş gücü kazanır.")
t("TXT_KEY_CIV5_DAWN_TL_ATATURK_TEXT",
  "Selam sana, Mustafa Kemal Atatürk, Türkiye Cumhuriyeti'nin kurucusu! Çanakkale'de Conkbayırı'nda "
  "askerlerine \"Ben size taarruzu emretmiyorum, ölmeyi emrediyorum!\" diyerek cepheyi tuttun. 19 Mayıs "
  "1919'da Samsun'a çıkıp milletini Kurtuluş Savaşı'na yönelttin; Sakarya'da ve Büyük Taarruz'da işgalcileri "
  "yurttan çıkardın. 29 Ekim 1923'te Cumhuriyeti ilan ettin; harften hukuka, eğitimden kadın haklarına kadar "
  "köklü inkılaplar yaptın.[NEWLINE][NEWLINE]Ey Atatürk, \"Hayatta en hakiki mürşit ilimdir.\" Milletini "
  "muasır medeniyetler seviyesinin üstüne çıkarabilecek misin? Yurtta sulh, cihanda sulh!")
t("TXT_KEY_LEADER_TL_ATATURK_PEDIA", "Mustafa Kemal Atatürk")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_ATATURK_NAME", "Mustafa Kemal Atatürk")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_ATATURK_SUBTITLE", "Türkiye Cumhuriyeti'nin Kurucusu ve İlk Cumhurbaşkanı")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_ATATURK_LIVED", "1881 - 1938")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_ATATURK_HEADING_1", "Çanakkale'den Kurtuluş Savaşı'na")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_ATATURK_TEXT_1",
  "Mustafa Kemal 1881'de Selanik'te doğdu. Harbiye'yi kurmay yüzbaşı olarak bitirdi. 1915'te Çanakkale "
  "Cephesi'nde Arıburnu ve Anafartalar'da gösterdiği başarılarla öne çıktı. 19 Mayıs 1919'da Samsun'a çıkarak "
  "Milli Mücadele'yi başlattı. Erzurum ve Sivas kongrelerinin ardından 23 Nisan 1920'de Türkiye Büyük Millet "
  "Meclisi açıldı. Sakarya Meydan Muharebesi (1921) ve Büyük Taarruz (1922) ile Kurtuluş Savaşı kazanıldı; "
  "1923'te Lozan Antlaşması imzalandı.")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_ATATURK_HEADING_2", "Cumhuriyet ve İnkılaplar")
t("TXT_KEY_CIVILOPEDIA_LEADERS_TL_ATATURK_TEXT_2",
  "29 Ekim 1923'te Cumhuriyet ilan edildi ve Mustafa Kemal ilk cumhurbaşkanı seçildi. Saltanat (1922) ve "
  "hilafet (1924) kaldırıldı; Tevhid-i Tedrisat Kanunu, Medeni Kanun (1926), Harf İnkılabı (1928) ve kadınlara "
  "seçme-seçilme hakkı (1930-1934) gibi köklü reformlar yapıldı. 1934'te TBMM kendisine Atatürk soyadını "
  "verdi. 10 Kasım 1938'de İstanbul'da, Dolmabahçe Sarayı'nda vefat etti.")

# ======================================================================
# MEDENIYET CIVILOPEDIA SAYFALARI
# ======================================================================
CIV_PEDIA = {
    "OSMAN": ("Kayı Boyu",
              "Kayılar, Oğuz Kağan'ın torunlarından sayılan 24 Oğuz boyundan biridir. Moğol istilası sırasında "
              "Anadolu'ya gelen bir Kayı obası, Selçuklu sultanı tarafından Bizans sınırındaki Söğüt ve Domaniç "
              "çevresine yerleştirildi. Ertuğrul Gazi ve oğlu Osman Bey önderliğinde bu oba, kısa sürede bölgenin "
              "en dinamik uç beyliğine dönüştü.",
              "Kayı boyunun damgası, Osmanlı hanedanının da sembollerinden biri olarak bugün hâlâ kullanılır."),
    "ORHAN": ("Beylikten Devlete",
              "Orhan Gazi döneminde Osmanlı Beyliği; Bursa, İznik ve İzmit gibi büyük Bizans şehirlerini alarak "
              "Marmara havzasına hâkim oldu. Karesi Beyliği'nin katılmasıyla deniz kıyısına ulaşan beylik, 1354'te "
              "Gelibolu'ya yerleşerek Avrupa'ya geçti. İlk sikke, ilk medrese ve ilk düzenli ordu bu döneme aittir.",
              "Bursa, Osmanlıların ilk büyük başkenti olarak bugün de Orhan Gazi Camii ve Külliyesi'ne ev sahipliği yapar."),
    "FATIH": ("Cihan Devleti",
              "İstanbul'un fethiyle Osmanlı Devleti, Roma'nın mirasına sahip çıkan bir imparatorluğa dönüştü. "
              "İstanbul yeniden imar edildi; Anadolu'dan ve Balkanlar'dan getirilen halkla şehir kısa sürede "
              "dünyanın en kalabalık şehirlerinden biri oldu. Fatih döneminde kurulan merkezî teşkilat, "
              "imparatorluğun yüzyıllarca ayakta kalmasını sağladı.",
              "Fatih, İstanbul'u fethettikten sonra kendisine Kayser-i Rûm (Roma Kayseri) unvanını da aldı."),
    "YAVUZ": ("Haremeyn'in Hizmetkârı",
              "Yavuz Sultan Selim'in seferleriyle Osmanlı Devleti, Mısır'dan Hicaz'a uzanan geniş toprakları "
              "egemenliğine aldı. Kahire'den İstanbul'a getirilen Kutsal Emanetler ve Mekke ile Medine'nin "
              "koruyuculuğu, Osmanlı padişahlarına İslam dünyasında eşsiz bir manevi otorite kazandırdı.",
              "Yavuz Sultan Selim'in saltanatı yalnızca sekiz yıl sürmesine rağmen devletin toprakları yaklaşık iki katına çıktı."),
    "BATTAL": ("Uçların Ruhu",
               "Orta Çağ Anadolu'sunda 'uç' adı verilen sınır bölgeleri, gazilerin, akıncıların ve dervişlerin "
               "dünyasıydı. Bu bölgelerde yaşayanlar için Battal Gazi, Melik Danişmend ve Sarı Saltuk gibi "
               "destan kahramanları birer örnekti. Bu medeniyet, tek bir devleti değil, uç kültürünün bu "
               "kahramanlık geleneğini temsil eder.",
               "Battal Gazi'nin adı Eskişehir'in Seyitgazi ilçesinde yaşamaya devam eder."),
    "ATATURK": ("Türkiye Cumhuriyeti",
                "Türkiye Cumhuriyeti, Kurtuluş Savaşı'nın ardından 29 Ekim 1923'te Ankara'da ilan edildi. "
                "Laiklik, cumhuriyetçilik ve milliyetçilik gibi ilkeler doğrultusunda eğitimden hukuka, "
                "ekonomiden kültüre kadar geniş kapsamlı bir modernleşme süreci başlatıldı. Ankara, "
                "Cumhuriyet'in başkenti oldu.",
                "Türkiye'de 23 Nisan, Atatürk tarafından çocuklara armağan edilen bir bayram olarak kutlanır."),
}
for civ, (head, body, fact) in CIV_PEDIA.items():
    t("TXT_KEY_CIV5_TL_%s_TEXT_1" % civ, body)
    t("TXT_KEY_CIVILOPEDIA_CIVS_TL_%s_HEADING_1" % civ, head)
    t("TXT_KEY_CIVILOPEDIA_CIVS_TL_%s_TEXT_1" % civ, body)
    t("TXT_KEY_CIVILOPEDIA_CIVS_TL_%s_FACTOID_HEADING" % civ, "Biliyor muydunuz?")
    t("TXT_KEY_CIVILOPEDIA_CIVS_TL_%s_FACTOID_TEXT" % civ, fact)

# ======================================================================
# BENZERSIZ BIRIMLER
# ======================================================================
UNITS = {
    "AKINCI": ("Akıncı",
               "Şövalye (Knight) yerine geçer. +1 hareket puanına sahiptir.",
               "Akıncılar hızlı keşif ve baskın birimleridir. Fazladan hareket puanı sayesinde düşman topraklarına "
               "derin akınlar yapabilir, savunmasız işçileri ve yerleşimcileri yakalayabilirsiniz.",
               "Akıncılar, Osmanlı'nın erken döneminden itibaren düşman topraklarına hızlı baskınlar yapan hafif "
               "süvarilerdi. Ücret yerine ganimet payı alırlar, düşmanın direncini kırmak ve keşif yapmak için kullanılırlardı."),
    "YAYA": ("Yaya",
             "Mızrakçı yerine geçer. Daha güçlüdür ve ücretsiz Talim I terfisiyle başlar.",
             "Yayalar, erken dönemin en sağlam savunma birimidir. Talim terfisi sayesinde engebeli arazide üstünlük "
             "kurarlar; atlı saldırılara karşı hattınızı tutmak için idealdirler.",
             "Orhan Gazi döneminde kurulan yayalar, Osmanlı'nın ilk düzenli piyade birlikleriydi. Savaş zamanında "
             "maaş alır, barışta kendilerine verilen toprakları işlerlerdi."),
    "SAHI_TOPU": ("Şahi Topu",
                  "Mancınık yerine geçer. Daha yüksek menzilli saldırı ve savaş gücüne sahiptir.",
                  "Şahi topları, ortaçağ surlarını yıkmak için tasarlanmıştır. Fatih'in kuşatma yeteneğiyle "
                  "birleştiğinde düşman şehirlerini kısa sürede düşürebilirsiniz. Mutlaka yakın dövüş birimleriyle koruyun.",
                  "1453 kuşatmasında kullanılan dev toplar, döneminin en büyük ateşli silahlarıydı. Kaynaklara göre bu "
                  "toplardan bazıları yüzlerce kilogramlık taş gülleler atabiliyordu. Bu topların Theodosius surlarında "
                  "açtığı gedikler, fethin en önemli etkenlerinden biri oldu."),
    "TUFEKENDAZ": ("Tüfekendaz",
                   "Tüfekçi yerine geçer. Daha güçlüdür ve atlı birimlere karşı +%33 savaş gücü kazanır.",
                   "Tüfekendazlar, süvari ağırlıklı ordulara karşı mükemmel bir savunma hattı oluşturur. Hızlı "
                   "düşman atlılarının bulunduğu cephelerde kullanın.",
                   "Tüfekendaz, Osmanlı ordusunda tüfek kullanan piyadeye verilen addır. 1514 Çaldıran Savaşı'nda "
                   "yeniçerilerin tüfekleri ve sahra topları, Safevi süvarilerine karşı zaferin kazanılmasında belirleyici oldu."),
    "GAZI": ("Gazi",
             "Kılıçlı yerine geçer. Daha güçlüdür ve ücretsiz Şok I terfisiyle başlar.",
             "Gaziler açık arazide çok etkilidir. Battal Gazi'nin yeteneğiyle düşman topraklarında daha da güçlenirler; "
             "erken saldırı savaşları için idealdirler.",
             "Gazi unvanı, Orta Çağ Anadolu'sunda sınır boylarında savaşan savaşçılara verilirdi. Gaziler; ahi ve "
             "derviş gelenekleriyle iç içe, uç beyliklerinin askerî omurgasını oluşturuyordu."),
    "MEHMETCIK": ("Mehmetçik",
                  "Büyük Savaş Piyadesi yerine geçer. Daha güçlüdür ve dost topraklarda +%25 savaş gücü kazanır.",
                  "Mehmetçikler, vatan topraklarını savunmada eşsizdir. Atatürk'ün yeteneğiyle birlikte dost "
                  "topraklarda düşmana ağır kayıplar verdirirler.",
                  "Mehmetçik, Türk askerine halk arasında verilen sevgi dolu addır. Çanakkale Cephesi'nde ve Kurtuluş "
                  "Savaşı'nda gösterdikleri fedakârlık, Türk tarihinin unutulmaz destanları arasında yer alır."),
}
for tag, (name, helptext, strat, pedia) in UNITS.items():
    t("TXT_KEY_UNIT_TL_%s" % tag, name)
    t("TXT_KEY_UNIT_HELP_TL_%s" % tag, helptext)
    t("TXT_KEY_UNIT_TL_%s_STRATEGY" % tag, strat)
    t("TXT_KEY_CIV5_UNIT_TL_%s_TEXT" % tag, pedia)

# ======================================================================
# BENZERSIZ BINALAR
# ======================================================================
BUILDINGS = {
    "ZAVIYE": ("Zaviye",
               "Tapınak (Shrine) yerine geçer. Fazladan +1 [ICON_FOOD] Gıda üretir.",
               "Zaviyeler, erken dönemde hem inanç hem de büyüme sağlar. Yeni kurulan şehirlerde ilk yapılacak binalardan biri olmalıdır.",
               "Zaviyeler, Osmanlı'nın kuruluş döneminde dervişlerin yolculara yemek ve barınak sağladığı küçük "
               "tekkelerdi. Fethedilen bölgelerin şenlendirilmesinde ve yerleşime açılmasında önemli rol oynadılar."),
    "MEDRESE": ("Medrese",
                "Kütüphane yerine geçer. Fazladan +1 [ICON_RESEARCH] Bilim ve +1 [ICON_CULTURE] Kültür üretir.",
                "Medreseler bilim ile kültürü bir arada sağlar. Orhan Gazi'nin genişleyen şehirlerinde erkenden inşa edin.",
                "İlk Osmanlı medresesi, Orhan Gazi tarafından 1331'de İznik'te kuruldu ve ilk müderrisi Davud-i "
                "Kayserî oldu. Medreseler; din bilimlerinin yanı sıra matematik, astronomi ve tıp öğretilen kurumlardı."),
    "KAPALICARSI": ("Kapalıçarşı",
                    "Pazar yerine geçer. Fazladan +2 [ICON_GOLD] Altın ve +1 [ICON_HAPPINESS_1] Mutluluk sağlar.",
                    "Kapalıçarşı hem hazineyi hem de halkın mutluluğunu destekler; büyük fetih orduları için gereken altını sağlar.",
                    "Kapalıçarşı'nın çekirdeği olan Cevahir Bedesteni, Fatih Sultan Mehmet tarafından 1455-1461 yılları "
                    "arasında yaptırıldı. Zamanla çevresine eklenen çarşılarla dünyanın en büyük ve en eski kapalı "
                    "çarşılarından biri ortaya çıktı."),
    "KULLIYE": ("Külliye",
                "Mabet (Temple) yerine geçer. Fazladan +1 [ICON_CULTURE] Kültür ve +1 [ICON_FOOD] Gıda üretir.",
                "Külliyeler, fethedilen şehirleri hızla toparlamak için idealdir; inanç, kültür ve gıdayı bir arada sağlar.",
                "Külliye; cami, medrese, imaret, darüşşifa, hamam ve çeşme gibi yapılardan oluşan bir yapı "
                "topluluğudur. Osmanlı şehirlerinde külliyeler, mahallelerin dinî, sosyal ve ekonomik merkeziydi."),
    "RIBAT": ("Ribat",
              "Sur yerine geçer. Şehre daha fazla savunma ve can puanı verir; burada eğitilen birimler +15 deneyim kazanır.",
              "Ribatlar sınır şehirlerinizi düşman akınlarına karşı korur ve deneyimli askerler yetiştirir.",
              "Ribatlar, İslam dünyasında sınır boylarında inşa edilen, hem kale hem de gönüllü savaşçıların "
              "barınağı olarak kullanılan yapılardı. Anadolu uçlarında da gazilerin üssü olarak hizmet ettiler."),
    "HALKEVI": ("Halkevi",
                "Halk Okulu yerine geçer. Fazladan +2 [ICON_CULTURE] Kültür üretir.",
                "Halkevleri bilim ve kültürü birlikte artırır. Atatürk'ün inkılap yeteneğiyle birlikte güçlü bir kültür zaferine katkı sağlar.",
                "Halkevleri, 1932'de Atatürk'ün desteğiyle kuruldu. Dil ve edebiyattan güzel sanatlara, spordan halk "
                "eğitimine kadar pek çok alanda çalışarak Cumhuriyet'in kültür hamlesinin taşıyıcısı oldu."),
}
for tag, (name, helptext, strat, pedia) in BUILDINGS.items():
    t("TXT_KEY_BUILDING_TL_%s" % tag, name)
    t("TXT_KEY_BUILDING_TL_%s_HELP" % tag, helptext)
    t("TXT_KEY_BUILDING_TL_%s_STRATEGY" % tag, strat)
    t("TXT_KEY_BUILDING_TL_%s_PEDIA" % tag, pedia)

# Gorunmez binalar
t("TXT_KEY_BUILDING_TL_DUMMY_OSMAN", "Kuruluş Rüyası")
t("TXT_KEY_BUILDING_TL_DUMMY_OSMAN_HELP", "Osman Bey'in yeteneği: +1 [ICON_FOOD] Gıda.")
t("TXT_KEY_BUILDING_TL_DUMMY_ORHAN", "İlk Düzenli Ordu")
t("TXT_KEY_BUILDING_TL_DUMMY_ORHAN_HELP", "Orhan Gazi'nin yeteneği: yakın dövüş ve barutlu birimlere üretim ve deneyim bonusu.")
t("TXT_KEY_BUILDING_TL_DUMMY_ATATURK", "Cumhuriyet İnkılapları")
t("TXT_KEY_BUILDING_TL_DUMMY_ATATURK_HELP", "Atatürk'ün yeteneği: [ICON_RESEARCH] Bilim ve [ICON_CULTURE] Kültür +%10.")

# ======================================================================
# TERFILER
# ======================================================================
t("TXT_KEY_PROMOTION_TL_FATIH_SIEGE", "Kuşatma Ustalığı")
t("TXT_KEY_PROMOTION_TL_FATIH_SIEGE_HELP", "Şehirlere karşı +%30 savaş gücü.")
t("TXT_KEY_PROMOTION_TL_BATTAL_RAIDER", "Akıncı Ruhu")
t("TXT_KEY_PROMOTION_TL_BATTAL_RAIDER_HELP", "Dost topraklar dışında +%15 savaş gücü.")
t("TXT_KEY_PROMOTION_TL_ATATURK_HOMELAND", "Vatan Savunması")
t("TXT_KEY_PROMOTION_TL_ATATURK_HOMELAND_HELP", "Dost topraklarda +%15 savaş gücü.")
t("TXT_KEY_PROMOTION_TL_AKINCI", "Akın")
t("TXT_KEY_PROMOTION_TL_AKINCI_HELP", "+1 hareket puanı.")
t("TXT_KEY_PROMOTION_TL_CALDIRAN", "Çaldıran")
t("TXT_KEY_PROMOTION_TL_CALDIRAN_HELP", "Atlı birimlere karşı +%33 savaş gücü.")
t("TXT_KEY_PROMOTION_TL_CANAKKALE", "Çanakkale Ruhu")
t("TXT_KEY_PROMOTION_TL_CANAKKALE_HELP", "Dost topraklarda +%25 savaş gücü.")

# ======================================================================
# LUA BILDIRIMLERI
# ======================================================================
t("TXT_KEY_TL_FATIH_CONQUEST", "Kuşatma Ustası: {1_City} fethedildi! Direniş süresi yarıya indi ve {2_Num} [ICON_GOLD] Altın kazanıldı.")
t("TXT_KEY_TL_FATIH_CONQUEST_SHORT", "Fetih")
t("TXT_KEY_TL_YAVUZ_CONQUEST", "Halifelik: {1_City} fethedildi! {2_Num} [ICON_PEACE] İnanç kazanıldı.")
t("TXT_KEY_TL_YAVUZ_CONQUEST_SHORT", "Halifelik")

# ======================================================================
# HARITA
# ======================================================================
t("TXT_KEY_TL_MAP_EMEA", "Türk Dünyası: Avrupa, Orta Doğu ve Afrika")
t("TXT_KEY_TL_MAP_EMEA_HELP",
  "Natural Earth verisinden üretilmiş gerçekçi Avrupa, Anadolu, Orta Doğu, Arabistan ve Afrika haritası "
  "(100x90). Tarihî başlangıç noktaları seçeneğiyle Türk liderleri gerçek başkentlerinin yakınında başlar. "
  "Önerilen harita boyutu: Devasa (Huge).")
t("TXT_KEY_TL_MAP_OPTION_START", "Başlangıç Noktaları")
t("TXT_KEY_TL_MAP_OPTION_START_HISTORIC", "Tarihî (gerçek konumlar)")
t("TXT_KEY_TL_MAP_OPTION_START_RANDOM", "Dengeli (rastgele)")

# ======================================================================
# DIPLOMASI SOZLERI
# ======================================================================
DIPLO = {
    "OSMAN": {
        "FIRSTGREETING": "Hoş geldin yolcu! Ben Kayı boyunun beyi, Ertuğrul Gazi'nin oğlu Osman. Obamızda adalet vardır; dost gelene kapımız açık, kötü niyetle gelene kılıcımız hazırdır.",
        "DEFEATED": "Rüyadaki ağaç devrildi... Ama unutma, kökleri toprağın derinlerindedir.",
        "DOW_GENERIC": "Sınırlarıma göz diktin. Şimdi Kayı atlılarının toz bulutunu göreceksin!",
        "ATTACKED_HOSTILE": "Demek savaş istiyorsun? Öyle olsun. Söğüt'ün yiğitleri geri adım atmaz.",
        "GREETING_HOSTILE_HELLO": "Yine mi sen? Söyle ne istiyorsun, vaktim az.",
        "GREETING_NEUTRAL_HELLO": "Selam sana. Konuşmak istediğin bir mesele var mı?",
        "GREETING_POLITE_HELLO": "Ah, dostum! Obamızın ateşi senin için hep yanıyor. Buyur, otur.",
        "LETS_HEAR_IT": "Dinliyorum. Sözünü dolandırmadan söyle.",
        "REQUEST": "Dostluğumuzun hatırına senden küçük bir yardım istiyorum.",
        "WINWAR": "Uç beyi olarak çok savaş gördüm. Bu da onlardan biriydi ve galip gelen biziz.",
        "WORK_WITH_US": "Birlikte hareket edersek bu topraklarda kimse önümüzde duramaz.",
        "WORK_AGAINST_SOMEONE": "Ortak düşmanımıza karşı birleşmenin zamanı geldi.",
    },
    "ORHAN": {
        "FIRSTGREETING": "Selam olsun! Ben Orhan, Osman Bey'in oğlu ve Bursa'nın sahibi. Ticaret de yaparız, savaş da; hangisini seçeceğin sana kalmış.",
        "DEFEATED": "Bursa düştü... Babamın mirasını koruyamadım. Allah'ın takdiri böyleymiş.",
        "DOW_GENERIC": "Düzenli ordumun gücünü sınamak istiyorsan, sahada görüşürüz!",
        "ATTACKED_HOSTILE": "Barışı bozan sen oldun. Yayalarım ve müsellemlerim hazır.",
        "GREETING_HOSTILE_HELLO": "Hayırdır? Bu sefer ne yüzle geldin?",
        "GREETING_NEUTRAL_HELLO": "Selam. İşlerin yolunda mı?",
        "GREETING_POLITE_HELLO": "Hoş geldin dostum! Bursa'nın ipekleri ve İznik'in çinileri senin için.",
        "LETS_HEAR_IT": "Söyle bakalım, teklifin nedir?",
        "REQUEST": "Bir dost olarak senden bir isteğim var.",
        "WINWAR": "Disiplin her zaman kalabalığı yener. Bunu bir kez daha gördük.",
        "WORK_WITH_US": "Kanun ve düzen üzerine kurulu bir ittifak ikimize de fayda sağlar.",
        "WORK_AGAINST_SOMEONE": "Bu düşmana karşı bize katılır mısın?",
    },
    "FATIH": {
        "FIRSTGREETING": "Ben Sultan Mehmet, İstanbul'un Fatihi ve iki denizin hakanı. Ya şehirlerin fethedilir ya da bir dost olarak soframa oturursun.",
        "DEFEATED": "Kızıl Elma'ya ulaşamadım... Ama İstanbul'u alan el, tarihin sayfalarında hep var olacak.",
        "DOW_GENERIC": "Ya ben İstanbul'u alırım, ya İstanbul beni! Şimdi sıra senin şehirlerinde.",
        "ATTACKED_HOSTILE": "Demek surlarına güveniyorsun? Toplarımın sesini duyduğunda pişman olacaksın.",
        "GREETING_HOSTILE_HELLO": "Sabrımı sınama. Ne istiyorsun?",
        "GREETING_NEUTRAL_HELLO": "Selam. Sözünü dinliyorum.",
        "GREETING_POLITE_HELLO": "Hoş geldin. Sarayımda âlimler, şairler ve dostlar her zaman ağırlanır.",
        "LETS_HEAR_IT": "Söyle. Ama bil ki vaktim fetihlere ayrılmıştır.",
        "REQUEST": "Bir hükümdardan diğerine küçük bir ricam var.",
        "WINWAR": "Hiçbir sur, iradeli bir ordunun önünde sonsuza dek duramaz.",
        "WORK_WITH_US": "Benimle birlikte yürü; yeni bir çağ açalım.",
        "WORK_AGAINST_SOMEONE": "Bu hükümdarın surlarını birlikte yıkalım mı?",
    },
    "YAVUZ": {
        "FIRSTGREETING": "Ben Selim Han, Mekke ve Medine'nin hizmetkârı. Bana dost olan, kardeşimdir; bana düşman olan, Çaldıran'ı hatırlasın.",
        "DEFEATED": "Bu dünya iki hükümdara dar gelirdi... Demek ki bu sefer dar gelen ben oldum.",
        "DOW_GENERIC": "Sabrım tükendi. Ordularım ve toplarım senin kapına dayanacak!",
        "ATTACKED_HOSTILE": "Bana kılıç çeken, kılıçla karşılık bulur.",
        "GREETING_HOSTILE_HELLO": "Kısa kes. Ne istiyorsun?",
        "GREETING_NEUTRAL_HELLO": "Selam. Ne için geldin?",
        "GREETING_POLITE_HELLO": "Hoş geldin. Dostlarıma karşı cömert olmayı bilirim.",
        "LETS_HEAR_IT": "Söyle, dinliyorum.",
        "REQUEST": "Senden bir isteğim var. Umarım beni kırmazsın.",
        "WINWAR": "Mısır'ı da, Şam'ı da böyle aldım. Sen de onlar gibi boyun eğdin.",
        "WORK_WITH_US": "Benimle birlikte olursan düşmanlarımız titreyecek.",
        "WORK_AGAINST_SOMEONE": "Bu sapkın hükümdara karşı yanımda olacak mısın?",
    },
    "BATTAL": {
        "FIRSTGREETING": "Ben Seyyid Battal Gazi, uçların gazisi! Adımı kopuzlardan duymuşsundur. Dost musun, yoksa yeni bir destanın kötü adamı mı?",
        "DEFEATED": "Gazi düşer ama destanı düşmez. Adım, Seyitgazi'de yaşamaya devam edecek.",
        "DOW_GENERIC": "Atımı eğerledim, kılıcımı kuşandım. Akın zamanı!",
        "ATTACKED_HOSTILE": "Benimle savaşmak mı? Ozanlar senin yenilgini de anlatacak!",
        "GREETING_HOSTILE_HELLO": "Hâlâ ayakta mısın? Ne istiyorsun?",
        "GREETING_NEUTRAL_HELLO": "Selam, yolcu. Uçlardan haber mi getirdin?",
        "GREETING_POLITE_HELLO": "Hoş geldin, kardeşim! Ateşin başına geç; sana yeni bir destan anlatayım.",
        "LETS_HEAR_IT": "Söyle bakalım, ne teklif ediyorsun?",
        "REQUEST": "Bir gazinin dostuna küçük bir ricası var.",
        "WINWAR": "Bir destan daha yazıldı ve kahramanı yine benim!",
        "WORK_WITH_US": "Birlikte akına çıkalım; ganimet ikimize de yeter.",
        "WORK_AGAINST_SOMEONE": "Bu düşmana karşı benimle at sürer misin?",
    },
    "ATATURK": {
        "FIRSTGREETING": "Ben Mustafa Kemal, Türkiye Cumhuriyeti'nin Cumhurbaşkanı. Yurtta sulh, cihanda sulh ilkesine inanırım; barış içinde yaşamak istiyorsanız elimiz size uzanmıştır.",
        "DEFEATED": "Beni yenmiş olabilirsiniz; ama Türk milletinin istiklal ve hürriyet aşkını asla yenemezsiniz.",
        "DOW_GENERIC": "Milletimizin bağımsızlığına göz diktiniz. Hatlar yoktur, satıh vardır; o satıh bütün vatandır!",
        "ATTACKED_HOSTILE": "Vatanımıza saldıranlar, Sakarya'yı ve Dumlupınar'ı hatırlasın.",
        "GREETING_HOSTILE_HELLO": "Buyurun. Ne konuşmak istiyorsunuz?",
        "GREETING_NEUTRAL_HELLO": "Hoş geldiniz. Sizi dinliyorum.",
        "GREETING_POLITE_HELLO": "Dostum, hoş geldiniz! Medeniyet yolunda birlikte yürümek bizi mutlu eder.",
        "LETS_HEAR_IT": "Teklifinizi dinliyorum.",
        "REQUEST": "Dostluğumuz adına sizden bir ricam var.",
        "WINWAR": "Bu zafer, milletin azim ve iradesinin bir eseridir.",
        "WORK_WITH_US": "Barış ve ilerleme için birlikte çalışmaya ne dersiniz?",
        "WORK_AGAINST_SOMEONE": "Barışı tehdit eden bu güce karşı ortak hareket etmeliyiz.",
    },
}

RESPONSE_TYPES = {
    "FIRSTGREETING": "RESPONSE_FIRST_GREETING",
    "DEFEATED": "RESPONSE_DEFEATED",
    "DOW_GENERIC": "RESPONSE_DOW_GENERIC",
    "ATTACKED_HOSTILE": "RESPONSE_ATTACKED_HOSTILE",
    "GREETING_HOSTILE_HELLO": "RESPONSE_GREETING_HOSTILE_HELLO",
    "GREETING_NEUTRAL_HELLO": "RESPONSE_GREETING_NEUTRAL_HELLO",
    "GREETING_POLITE_HELLO": "RESPONSE_GREETING_POLITE_HELLO",
    "LETS_HEAR_IT": "RESPONSE_LETS_HEAR_IT",
    "REQUEST": "RESPONSE_REQUEST",
    "WINWAR": "RESPONSE_WINWAR",
    "WORK_WITH_US": "RESPONSE_WORK_WITH_US",
    "WORK_AGAINST_SOMEONE": "RESPONSE_WORK_AGAINST_SOMEONE",
}
for civ, lines in DIPLO.items():
    for key, line in lines.items():
        t("TXT_KEY_LEADER_TL_%s_%s_1" % (civ, key), line)
