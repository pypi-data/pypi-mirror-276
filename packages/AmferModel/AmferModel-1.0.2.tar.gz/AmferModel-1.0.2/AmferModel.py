import time
from difflib import SequenceMatcher
import json
import base64
from PIL import Image
import random

class AMFER_Model: # Artificial Mind Forging and Educational Realm (AMFER)
	def __init__(self, system_setups=True):
		self.brain = {"languages": {}, "languagesText": [], "images": {}}
		self.sessions = {"system": []}
		self.setups = {}
		self.include_language("system")
		if system_setups:
			self.include_setup("en-part1", """Hi Hello there! How's your day going?
Hey! I'm doing well, thanks for asking. How about you?
Not too bad, just trying to stay productive. What do you enjoy doing in your free time?
I love reading books and going for long walks. How about you?
I'm a big fan of cooking and trying out new recipes. Any favorite cuisines?
Italian cuisine is my weakness! Pizza and pasta are my go-to comfort foods.
Can't go wrong with Italian! Do you have a favorite pizza topping?
Definitely pepperoni! What about you?
I'm more of a veggie lover myself. Mushroom and spinach are my top picks.
Sounds delicious! Maybe we should swap recipes sometime. That sounds like a plan! I have a fantastic pasta recipe I'd love to share.
I'm all ears! Pasta is always a winner in my book.
Great! It's a creamy garlic parmesan pasta with roasted cherry tomatoes.
Wow, that sounds amazing! I'm getting hungry just thinking about it.
It's really simple to make too, perfect for a cozy night in.
Count me in! I'll have to try it out this weekend.
Let me know how it turns out! I'm sure you'll love it.
Will do! Thanks for the recipe inspiration.
No problem at all. Sharing recipes is one of my favorite things to do.
Likewise! It's always fun to discover new dishes and flavors. Absolutely! I'm always on the lookout for new recipes to try.
Me too! It's like a culinary adventure every time.
Speaking of adventures, do you enjoy traveling?
I love it! Exploring new cultures and cuisines is so enriching.
I couldn't agree more. Any favorite travel destinations?
I'm partial to tropical locations with beautiful beaches. How about you?
I'm more into historical cities with rich architecture and art.
That sounds fascinating! Any particular city you've enjoyed visiting?
I recently visited Rome, and it was absolutely breathtaking.
Rome is on my bucket list! Hopefully, I'll get to visit someday.""", language="en")
			self.include_setup("tr-part1", """Selamlar! Merhaba! Günün nasıl geçiyor?
Hey! İyiyim, sorduğun için teşekkürler. Peki ya sen?
Çok kötü değil, sadece üretken kalmaya çalışıyorum. Boş zamanlarınızda ne yapmaktan hoşlanırsınız?
Kitap okumayı ve uzun yürüyüşlere çıkmayı seviyorum. Peki ya sen?
Yemek pişirmenin ve yeni tarifler denemenin büyük bir hayranıyım. Favori mutfaklarınız var mı?
İtalyan mutfağı benim zayıf noktam! Pizza ve makarna benim en sevdiğim yiyeceklerdir.
İtalyanca ile yanlış gidemem! Favori pizza malzemeniz var mı?
Kesinlikle biberli! Senden ne haber?
Ben daha çok vejetaryen aşığıyım. Mantar ve ıspanak en çok tercih ettiğim ürünlerdir.
Lezzetli geliyor! Belki bir ara tarifleri değiştirmeliyiz. Bu bir plana benziyor! Paylaşmak istediğim harika bir makarna tarifim var.
Can kulağı ile dinliyorum! Benim kitabımda makarna her zaman kazanır.
Harika! Kavrulmuş kiraz domatesli, kremalı sarımsaklı parmesanlı makarnadır.
Vay, bu kulağa harika geliyor! Bunu düşündükçe acıkıyorum.
Yapımı da çok basit, rahat bir gece geçirmek için mükemmel.
Beni de sayın! Bu hafta sonu denemek zorunda kalacağım.
Nasıl olacağını bana bildirin! Eminim bunu seveceksiniz.
Yapacak! Tarif ilhamı için teşekkürler.
Hiç sorun değil. Tarif paylaşmak en sevdiğim şeylerden biri.
Aynı şekilde! Yeni yemekler ve tatlar keşfetmek her zaman eğlencelidir. Kesinlikle! Her zaman deneyecek yeni tarifler arayışındayım.
Ben de! Her seferinde bir mutfak macerası gibi.
Maceralardan bahsetmişken, seyahat etmekten hoşlanıyor musunuz?
Bayıldım! Yeni kültürleri ve mutfakları keşfetmek çok zenginleştirici.
Daha fazla katılamazdım. Favori seyahat destinasyonlarınız var mı?
Güzel plajları olan tropik yerleri tercih ediyorum. Peki ya sen?
Zengin mimarisi ve sanatı olan tarihi şehirlere daha çok ilgi duyuyorum.
Kulağa büyüleyici geliyor! Ziyaret etmekten keyif aldığınız herhangi bir şehir var mı?
Yakın zamanda Roma'yı ziyaret ettim ve kesinlikle nefes kesiciydi.
Roma yapılacaklar listemde! İnşallah bir gün ziyaretine giderim.""", language="tr")
			self.include_setup("de-part1", """Hallo! Wie läuft dein Tag?
Hey! Mir geht es gut, danke der Nachfrage. Und du?
Nicht schlecht, ich versuche nur, produktiv zu bleiben. Was machst Du in Deiner Freizeit gerne?
Ich liebe es, Bücher zu lesen und lange Spaziergänge zu machen. Und du?
Ich bin ein großer Fan des Kochens und des Ausprobierens neuer Rezepte. Irgendwelche Lieblingsküchen?
Italienische Küche ist meine Schwäche! Pizza und Pasta sind meine liebsten Wohlfühlspeisen.
Mit Italienisch kann man nichts falsch machen! Haben Sie einen Lieblingspizzabelag?
Auf jeden Fall Peperoni! Was ist mit dir?
Ich selbst bin eher ein Vegetarier. Pilze und Spinat sind meine Lieblingsgerichte.
Hört sich lecker an! Vielleicht sollten wir irgendwann Rezepte austauschen. Das klingt nach einem Plan! Ich habe ein fantastisches Pastarezept, das ich gerne teilen würde.
Ich bin ganz Ohr! Pasta ist meiner Meinung nach immer ein Gewinner.
Großartig! Es handelt sich um cremige Knoblauch-Parmesan-Nudeln mit gerösteten Kirschtomaten.
Wow, das klingt großartig! Ich werde hungrig, wenn ich nur daran denke.
Es ist auch wirklich einfach zuzubereiten und perfekt für einen gemütlichen Abend zu Hause.
Ich bin dabei! Ich muss es dieses Wochenende ausprobieren.
Lass mich wissen, wie es ausgeht! Ich bin mir sicher, dass es Ihnen gefallen wird.
Wird tun! Danke für die Rezeptinspiration.
Überhaupt kein Problem. Rezepte zu teilen ist eine meiner Lieblingsbeschäftigungen.
Ebenfalls! Es macht immer Spaß, neue Gerichte und Geschmacksrichtungen zu entdecken. Absolut! Ich bin immer auf der Suche nach neuen Rezepten zum Ausprobieren.
Ich auch! Es ist jedes Mal wie ein kulinarisches Abenteuer.
Apropos Abenteuer: Reisen Sie gerne?
Ich liebe es! Das Entdecken neuer Kulturen und Küchen ist so bereichernd.
Ich kann nur zustimmen. Irgendwelche Lieblingsreiseziele?
Ich habe eine Vorliebe für tropische Orte mit wunderschönen Stränden. Und du?
Ich mag mehr historische Städte mit reicher Architektur und Kunst.
Das klingt faszinierend! Gibt es eine bestimmte Stadt, die Sie gerne besucht haben?
Ich war kürzlich in Rom und es war absolut atemberaubend.
Rom steht auf meiner Wunschliste! Hoffentlich komme ich eines Tages zu Besuch.""", language="de")
			self.include_setup("ru-part1", """Привет! Как проходит твой день?
Привет! Всё хорошо, спасибо, что спросил. Как насчёт тебя?
Не плохо, просто стараюсь оставаться продуктивным. Чем ты любишь заниматься в свободное время?
Я люблю читать книги и ходить на длинные прогулки. А у тебя?
Я большой любитель готовить и пробовать новые рецепты. Есть любимые кухни?
Итальянская кухня - моя слабость! Пицца и паста - мои любимые утешительные блюда.
С итальянской кухней не ошибешься! У тебя есть любимая начинка для пиццы?
Определённо, пепперони! А у тебя?
Я больше люблю овощи. Грибы и шпинат - мои самые любимые.
Звучит вкусно! Может быть, нам стоит поменяться рецептами когда-нибудь. Это звучит как план! У меня есть фантастический рецепт пасты, который я хотел бы поделиться.
Я весь внимание! Паста всегда выигрышный вариант для меня.
Отлично! Это кремовая чесночная паста с жареными черри-томатами.
Вау, это звучит потрясающе! Я просто начинаю голодать, только думая об этом.
И его действительно легко приготовить, идеально для уютного вечера.
Я в игре! Мне придётся попробовать это в выходные.
Сообщи мне, как получится! Я уверен, тебе это понравится.
Хорошо! Спасибо за вдохновение на рецепт.
Никаких проблем. Обмен рецептами - одно из моих любимых занятий.
Точно так же! Всегда интересно открывать новые блюда и вкусы. Абсолютно! Я всегда в поиске новых рецептов для пробы.
Я тоже! Это как кулинарное приключение каждый раз.
Говоря о приключениях, тебе нравится путешествовать?
Обожаю! Исследование новых культур и кухонь так обогащает.
Я полностью согласен. Есть любимые места для путешествий?
Я предпочитаю тропические места с красивыми пляжами. А у тебя?
Я больше люблю исторические города с богатой архитектурой и искусством.
Это звучит увлекательно! Есть какой-то конкретный город, который тебе понравился посетить?
Я недавно побывал в Риме, и это было абсолютно захватывающе.
Рим на моем списке желаний! Надеюсь, когда-нибудь я смогу его посетить.""", language="ru")
			self.include_setup("en-part2", """You definitely should! The history and food in Rome are incredible.
I'll make sure to plan a trip there soon. Thanks for the recommendation!
Anytime! Let me know if you need any travel tips or suggestions.
Will do! It's always helpful to get advice from someone who's been there.
Happy to help! Traveling is one of my passions.
It shows! Your enthusiasm for exploring new places is contagious.
Thanks! I believe there's so much beauty and diversity in the world to experience.
Absolutely, traveling opens our minds and hearts to new perspectives.
And it creates memories that last a lifetime. What's your favorite travel memory? One of my favorite memories is hiking to Machu Picchu in Peru.
That sounds incredible! The views must have been breathtaking.
They were! It was a challenging hike but so worth it in the end.
I can imagine. Machu Picchu is on my travel bucket list for sure.
You should definitely go if you get the chance. It's unforgettable.
I'll make sure to prioritize it. Thanks for sharing your experience.
Of course! I love reminiscing about past adventures.
Me too! It keeps the wanderlust alive until the next journey.
Exactly! And there's always something new to discover out there.
Absolutely. The world is full of surprises and wonders waiting to be explored. It's truly remarkable how much there is to see and learn.
Indeed! Traveling broadens our horizons in so many ways.
And it fosters connections with people from different cultures.
That's one of the most beautiful aspects of traveling.
Definitely. The friendships made while traveling are so special.
Agreed. They often lead to unforgettable experiences and adventures.
It's like forming a global network of friends and fellow explorers.
Precisely! It's a testament to the power of human connection.
And it reminds us that, despite our differences, we're all connected.
Absolutely. Traveling brings us closer to understanding and unity.""", language="en")
			self.include_setup("tr-part2", """Kesinlikle yapmalısın! Roma'nın tarihi ve yemekleri inanılmaz.
Yakında oraya bir gezi planlayacağımdan emin olacağım. Tavsiye için teşekkürler!
İstediğin zaman! Seyahat ipuçlarına veya önerilerine ihtiyacınız olursa bana bildirin.
Yapacak! Orada bulunmuş birinden tavsiye almak her zaman faydalıdır.
Memnuniyetle yardım ettim! Seyahat etmek tutkularımdan biri.
Gösteriyor! Yeni yerleri keşfetme hevesiniz bulaşıcıdır.
Teşekkürler! Dünyada deneyimlenecek çok fazla güzellik ve çeşitlilik olduğuna inanıyorum.
Kesinlikle seyahat etmek zihnimizi ve kalbimizi yeni bakış açılarına açar.
Ve ömür boyu sürecek anılar yaratır. En sevdiğiniz seyahat anınız hangisi? En sevdiğim anılarımdan biri Peru'daki Machu Picchu'ya yürüyüş yapmak.
Bu inanılmaz geliyor! Manzaralar nefes kesici olsa gerek.
Onlar! Zorlu bir yürüyüştü ama sonunda buna değdi.
Tahmin edebiliyorum. Machu Picchu kesinlikle seyahat listemde.
Fırsat bulursanız mutlaka gitmelisiniz. Unutulmaz.
Buna öncelik vereceğimden emin olacağım. Deneyiminizi paylaştığınız için teşekkür ederiz.
Elbette! Geçmiş maceraları hatırlamayı seviyorum.
Ben de! Bir sonraki yolculuğa kadar yolculuk tutkusunu canlı tutar.
Kesinlikle! Ve orada her zaman keşfedilecek yeni bir şeyler vardır.
Kesinlikle. Dünya keşfedilmeyi bekleyen sürprizlerle ve harikalarla dolu. Görülecek ve öğrenilecek bu kadar çok şeyin olması gerçekten dikkate değer.
Aslında! Seyahat etmek ufkumuzu pek çok açıdan genişletir.
Ve farklı kültürlerden insanlarla bağları güçlendirir.
Seyahat etmenin en güzel yönlerinden biri de bu.
Kesinlikle. Seyahat ederken edinilen dostluklar çok özeldir.
Kabul. Genellikle unutulmaz deneyimlere ve maceralara yol açarlar.
Bu, arkadaşlar ve kaşiflerden oluşan küresel bir ağ oluşturmak gibidir.
Açık olarak! Bu, insani bağlantının gücünün bir kanıtıdır.
Ve bize, farklılıklarımıza rağmen hepimizin birbirimize bağlı olduğumuzu hatırlatıyor.
Kesinlikle. Seyahat etmek bizi anlayışa ve birliğe yaklaştırır.""", language="tr")
			self.include_setup("de-part2", """Das solltest du auf jeden Fall! Die Geschichte und das Essen in Rom sind unglaublich.
Ich werde auf jeden Fall bald eine Reise dorthin planen. Danke für die Empfehlung!
Jederzeit! Lassen Sie mich wissen, wenn Sie Reisetipps oder Anregungen benötigen.
Wird tun! Es ist immer hilfreich, sich von jemandem Rat zu holen, der schon einmal dabei war.
Es freut mich, dass ich Ihnen helfen konnte! Reisen ist eine meiner Leidenschaften.
Es zeigt! Ihre Begeisterung für die Erkundung neuer Orte ist ansteckend.
Danke! Ich glaube, dass es auf der Welt so viel Schönheit und Vielfalt zu erleben gibt.
Auf jeden Fall öffnet das Reisen unseren Geist und unser Herz für neue Perspektiven.
Und es schafft Erinnerungen, die ein Leben lang halten. Was ist deine schönste Reiseerinnerung? Eine meiner schönsten Erinnerungen ist die Wanderung nach Machu Picchu in Peru.
Das klingt unglaublich! Die Aussicht muss atemberaubend gewesen sein.
Sie waren! Es war eine anspruchsvolle Wanderung, aber am Ende hat sie sich wirklich gelohnt.
Ich kann mir vorstellen. Machu Picchu steht auf jeden Fall auf meiner Reiseliste.
Sie sollten auf jeden Fall hingehen, wenn Sie die Gelegenheit dazu haben. Es ist unvergesslich.
Ich werde darauf achten, es zu priorisieren. Vielen Dank, dass Sie Ihre Erfahrungen geteilt haben.
Natürlich! Ich liebe es, mich an vergangene Abenteuer zu erinnern.
Ich auch! Es hält das Fernweh bis zur nächsten Reise wach.
Genau! Und da draußen gibt es immer etwas Neues zu entdecken.
Absolut. Die Welt ist voller Überraschungen und Wunder, die darauf warten, erkundet zu werden. Es ist wirklich bemerkenswert, wie viel es zu sehen und zu lernen gibt.
In der Tat! Reisen erweitert unseren Horizont in vielerlei Hinsicht.
Und es fördert Verbindungen zu Menschen aus verschiedenen Kulturen.
Das ist einer der schönsten Aspekte des Reisens.
Definitiv. Die auf Reisen geschlossenen Freundschaften sind etwas ganz Besonderes.
Vereinbart. Sie führen oft zu unvergesslichen Erlebnissen und Abenteuern.
Es ist, als würde man ein globales Netzwerk aus Freunden und Entdeckerkollegen aufbauen.
Genau! Es ist ein Beweis für die Kraft der menschlichen Verbindung.
Und es erinnert uns daran, dass wir trotz unserer Unterschiede alle miteinander verbunden sind.
Absolut. Reisen bringt uns dem Verständnis und der Einheit näher.""", language="de")
			self.include_setup("ru-part2", """Обязательно посети! История и еда в Риме невероятны.
Обязательно запланирую поездку туда в ближайшее время. Спасибо за рекомендацию!
В любое время! Дай знать, если нужны какие-то советы по путешествиям или рекомендации.
Обязательно! Всегда полезно получать советы от тех, кто уже там был.
Рад помочь! Путешествия - одна из моих страстей.
Это видно! Твой энтузиазм к исследованию новых мест заразителен.
Спасибо! Я верю, что в мире так много красоты и разнообразия, которые стоит испытать.
Абсолютно, путешествия открывают нам новые перспективы и возможности.
И создают воспоминания, которые остаются с нами на всю жизнь. Какое твоё любимое путешественническое воспоминание? Одно из моих любимых воспоминаний - это поход к Мачу-Пикчу в Перу.
Звучит невероятно! Виды, должно быть, были захватывающими.
Они были! Это был сложный поход, но оно того стоило в конце концов.
Могу представить. Мачу-Пикчу определённо на моём списке желаний.
Тебе обязательно стоит пойти, если у тебя будет возможность. Это незабываемо.
Я обязательно приоритизирую это. Спасибо за то, что поделился своим опытом.
Конечно! Мне нравится вспоминать о прошлых приключениях.
Мне тоже! Это поддерживает внутреннюю жажду приключений до следующей поездки.
Именно! И всегда есть что-то новое для открытия там.
Абсолютно. Мир полон сюрпризов и чудес, которые ждут, чтобы их исследовали. Это действительно замечательно, сколько есть для увидения и изучения.
Именно! Путешествия расширяют наши горизонты во многих отношениях.
И они способствуют установлению связей с людьми из разных культур.
Это один из самых прекрасных аспектов путешествий.
Точно. Дружбы, заключенные во время путешествий, такие особенные.
Согласен. Они часто приводят к незабываемым впечатлениям и приключениям.
Это как формирование глобальной сети друзей и единомышленников-исследователей.
Именно так! Это подтверждает силу человеческих связей.
И это напоминает нам, что, несмотря на наши различия, мы все связаны.
Абсолютно. Путешествия приближают нас к пониманию и единству.""", language="ru")
			self.include_setup("en-part3", """It's like a journey of self-discovery as well.
Very true. Traveling pushes us out of our comfort zones.
And helps us grow as individuals in the process.
Definitely. We become more adaptable and resilient.
And we learn to appreciate the beauty of diversity.
Yes, diversity enriches our lives in countless ways.
It's what makes the world such an interesting place.
Indeed, embracing diversity leads to a more inclusive world.
And fosters mutual respect and understanding.
Absolutely, it's the foundation for a better future for all. I couldn't agree more. It's essential to celebrate our differences.
Exactly, diversity should be embraced and valued.
It makes our communities stronger and more vibrant.
And encourages innovation and creativity.
Precisely, different perspectives lead to new ideas and solutions.
That's why inclusion is crucial in every aspect of society.
Agreed, everyone deserves to feel welcomed and respected.
And to have equal opportunities to thrive.
Creating a more inclusive world is a collective responsibility.
And it starts with each of us fostering understanding and acceptance. Absolutely, small acts of kindness and empathy can make a big difference.
They create ripple effects that spread positivity and harmony.
Even a smile or a kind word can brighten someone's day.
It costs nothing to be kind, yet it's priceless in its impact.
We should strive to be the reason someone believes in the goodness of people.
That's beautifully said. Compassion has the power to heal and unite.
And it transcends cultural and linguistic barriers.
Indeed, it's a universal language that connects us all.
Imagine a world where kindness is the norm rather than the exception.
It's a world worth working towards, one small act of kindness at a time.""", language="en")
			self.include_setup("tr-part3", """Aynı zamanda bir kendini keşfetme yolculuğu gibi.
Çok doğru. Seyahat etmek bizi konfor bölgelerimizin dışına iter.
Ve bu süreçte birey olarak büyümemize yardımcı olur.
Kesinlikle. Daha uyumlu ve dayanıklı oluruz.
Ve çeşitliliğin güzelliğini takdir etmeyi öğreniyoruz.
Evet, çeşitlilik hayatımızı sayısız şekilde zenginleştirir.
Dünyayı bu kadar ilginç bir yer yapan şey de bu.
Aslında çeşitliliği benimsemek daha kapsayıcı bir dünyaya yol açar.
Ve karşılıklı saygı ve anlayışı teşvik eder.
Kesinlikle, bu herkes için daha iyi bir geleceğin temelidir. Daha fazla katılamazdım. Farklılıklarımızı kutlamak çok önemli.
Aynen öyle, çeşitlilik kucaklanmalı ve değer verilmeli.
Topluluklarımızı daha güçlü ve daha canlı hale getirir.
Ve yenilikçiliği ve yaratıcılığı teşvik eder.
Kesinlikle farklı bakış açıları yeni fikirlere ve çözümlere yol açar.
Bu nedenle kapsayıcılık toplumun her alanında hayati öneme sahiptir.
Kabul ediyorum, herkes hoş karşılanmayı ve saygı duyulmayı hak eder.
Ve gelişmek için eşit fırsatlara sahip olmak.
Daha kapsayıcı bir dünya yaratmak kolektif bir sorumluluktur.
Ve bu her birimizin anlayışı ve kabulü geliştirmesiyle başlar. Kesinlikle, küçük nezaket ve empati eylemleri büyük bir fark yaratabilir.
Pozitifliği ve uyumu yayan dalgalanma etkileri yaratırlar.
Bir gülümseme ya da nazik bir söz bile birinin gününü aydınlatabilir.
Nazik olmanın hiçbir maliyeti yoktur, ancak etkisi paha biçilemezdir.
Birinin insanların iyiliğine inanmasının nedeni olmaya çalışmalıyız.
Bu çok güzel söylendi. Merhametin iyileştirme ve birleştirme gücü vardır.
Ve kültürel ve dilsel engelleri aşar.
Aslında bu hepimizi birbirine bağlayan evrensel bir dildir.
Nezaketin istisnadan ziyade norm olduğu bir dünya hayal edin.
Uğrunda çalışmaya değer bir dünya, her seferinde küçük bir nezaket eylemi.""", language="tr")
			self.include_setup("de-part3", """Es ist auch wie eine Reise der Selbstfindung.
Sehr richtig. Reisen treibt uns aus unserer Komfortzone.
Und hilft uns dabei, als Individuen zu wachsen.
Definitiv. Wir werden anpassungsfähiger und resilienter.
Und wir lernen die Schönheit der Vielfalt zu schätzen.
Ja, Vielfalt bereichert unser Leben auf unzählige Arten.
Das macht die Welt zu einem so interessanten Ort.
Tatsächlich führt die Akzeptanz von Vielfalt zu einer integrativeren Welt.
Und fördert gegenseitigen Respekt und Verständnis.
Auf jeden Fall ist es die Grundlage für eine bessere Zukunft für alle. Ich kann nur zustimmen. Es ist wichtig, unsere Unterschiede zu feiern.
Genau, Vielfalt sollte angenommen und wertgeschätzt werden.
Es macht unsere Gemeinschaften stärker und lebendiger.
Und fördert Innovation und Kreativität.
Denn unterschiedliche Perspektiven führen zu neuen Ideen und Lösungen.
Deshalb ist Inklusion in allen Bereichen der Gesellschaft von entscheidender Bedeutung.
Einverstanden ist, dass jeder es verdient, sich willkommen und respektiert zu fühlen.
Und gleiche Chancen zu haben, sich zu entfalten.
Die Schaffung einer integrativeren Welt ist eine kollektive Verantwortung.
Und es beginnt damit, dass jeder von uns Verständnis und Akzeptanz fördert. Auf jeden Fall können kleine Taten der Freundlichkeit und des Einfühlungsvermögens einen großen Unterschied machen.
Sie erzeugen Welleneffekte, die Positivität und Harmonie verbreiten.
Sogar ein Lächeln oder ein freundliches Wort können den Tag eines Menschen erhellen.
Es kostet nichts, freundlich zu sein, aber seine Wirkung ist unbezahlbar.
Wir sollten danach streben, der Grund dafür zu sein, dass jemand an die Güte der Menschen glaubt.
Das ist schön gesagt. Mitgefühl hat die Kraft zu heilen und zu vereinen.
Und es überwindet kulturelle und sprachliche Barrieren.
Tatsächlich ist es eine universelle Sprache, die uns alle verbindet.
Stellen Sie sich eine Welt vor, in der Freundlichkeit eher die Norm als die Ausnahme ist.
Es ist eine Welt, an der es sich zu arbeiten lohnt, ein kleiner Akt der Freundlichkeit nach dem anderen.""", language="de")
			
			self.include_setup("ru-part3", """Это как путешествие самопознания тоже.
Очень верно. Путешествие выбрасывает нас из нашей зоны комфорта.
И помогает нам развиваться как личности в процессе.
Определённо. Мы становимся более адаптивными и устойчивыми.
И мы учимся ценить красоту разнообразия.
Да, разнообразие обогащает нашу жизнь бесчисленными способами.
Это то, что делает мир таким интересным местом.
Действительно, принятие разнообразия ведёт к более инклюзивному миру.
И способствует взаимному уважению и пониманию.
Абсолютно, это основа для лучшего будущего для всех. Я полностью согласен. Важно отмечать наши различия.
Именно так, разнообразие следует принимать и ценить.
Оно делает наши сообщества сильнее и более яркими.
И поощряет инновации и креативность.
Именно так, разные точки зрения приводят к новым идеям и решениям.
Поэтому инклюзия важна в каждом аспекте общества.
Согласен, каждый заслуживает чувствовать себя приветствованным и уважаемым.
И иметь равные возможности для процветания.
Создание более инклюзивного мира - это коллективная ответственность.
И начинается с того, чтобы каждый из нас способствовал пониманию и принятию. Абсолютно, маленькие акты доброты и эмпатии могут иметь большое значение.
Они создают волны позитива, распространяющие добро и гармонию.
Даже улыбка или доброе слово может возвеселить чей-то день.
Это не стоит ничего быть добрым, но его влияние бесценно.
Мы должны стремиться быть причиной того, что кто-то верит в доброту людей.
Это красиво сказано. Сострадание имеет силу исцелять и объединять.
И оно преодолевает культурные и языковые барьеры.
Действительно, это универсальный язык, который связывает нас всех.
Представьте мир, где доброта является нормой, а не исключением.
Это мир, ради которого стоит работать, один маленький акт доброты за раз.""", language="ru")
		self.presave()
	def include_language(self, name):
		if name in self.brain["languages"]:
			return "Alredy found."
		else:
			self.brain["languages"][name] = {"vocab": [], "data": []}
			self.brain["languagesText"].append(name)
			return "Language included."
	def similarity(self, text1, text2):
		return SequenceMatcher(None, text1, text2).ratio()*100
	def language_detector(self, data):
		most1 = {}
		data = self.tokenizer(data.lower().strip())
		for language in self.brain["languagesText"]:
			for word in data:
				if word in self.brain["languages"][language]["vocab"]:
					if language in most1:
						most1[language] += 1
					else:
						most1[language] = 1
		most = ("system", 0)
		for name, value in most1.items():
			if value > most[1]:
				most = (name, value)
		return most[0]
	def tokenizer(self, data):
		words = []
		deletethe = '''.,!?()<>{}[]:;'"'''
		for h in deletethe:
			data = data.replace(h, "")
		for word in data.split():
			words.append(word)
		return words
	def train(self, data, language="system", controlled=True, temperature=0.2):
		qq = time.time()
		datasets = 0
		words = 0
		ww = 0
		ee = 0
		if controlled:
			self.include_language(language)
		data = data.lower().strip()
		if controlled:
			required = (1-temperature)*100
			newdata = []
			vocab = self.brain["languages"][language]["vocab"]
			for word in self.tokenizer(data):
				if word in vocab:
					newdata.append(word)
				else:
					q = True
					for word2 in vocab:
						if self.similarity(word, word2) >= required:
							newdata.append(word2)
							q = False
							break
					if q:
						newdata.append(word)
			vocab = None
			data = " ".join(newdata)
		if data in self.brain["languages"][language]["data"]:
			pass
		else:
			self.brain["languages"][language]["data"] = [data]+self.brain["languages"][language]["data"]
			datasets += 1
			ww += 1
		ee += 1
		for word in self.tokenizer(data):
			if word in self.brain["languages"][language]["vocab"]:
				pass
			else:
				self.brain["languages"][language]["vocab"] = [word]+self.brain["languages"][language]["vocab"]
				words += 1
				ww += 1
			ee += 1
		if ww == 0:
			ww = 1
		if ee == 0:
			ee = 1
		r = time.time()-qq
		return f"Learned Words: {words}\nLearned Datasets: {datasets}\nTime Spent: {r} seconds.\nChanged/Loss: {(ww/ee)}"
	def learnimage(self, file, means):
		self.brain["images"][file] = str(means).lower().strip()
	def completion(self, data, temperature=0.2, max_tokens=150, count=1, session="system", recall=False, keepinmind=False, wordreply=True, wordreplycount=5, transformdata=False):
		qq = time.time()
		if session in self.sessions:
			pass
		else:
			self.sessions[session] = []
		data = data.lower().strip()
		olddata = data
		if recall:
			for word in self.tokenizer(data):
				for data2 in self.sessions[session]:
					if word in data2:
						data = data2+" "+data
		language = self.language_detector(data)
		response = []
		for text in self.brain["languages"][language]["data"]:
			if len(" ".join(response)) >= max_tokens:
				break
			if data in text:
				if transformdata:
					data = text[text.find(data)+len(data):]
					response.append(data)
				else:
					response.append(text[text.find(data)+len(data):])
				if len(response) >= count:
					break
			else:
				if wordreply:
					if wordreplycount >= 1:
						for word in self.tokenizer(data):
							if word in text:
								if transformdata:
									data = text[text.find(word)+len(word):]
									response.append(data)
								else:
									response.append(text[text.find(word)+len(word):])
								if len(response) >= count:
									break
							wordreplycount -= 1
		response = " ".join(response)
		response = self.deviate(response, temperature=temperature, language=language)[:max_tokens]
		if keepinmind:
			self.sessions[session].append(data)
			self.sessions[session].append(response)
		return [response, time.time()-qq]
	def observation_detector(self, data, language="system"):
		obs = []
		for word in self.tokenizer(data):
			if word in self.brain["languages"][language]["vocab"]:
				obs.append(self.brain["languages"][language]["vocab"].index(word))
			else:
				tt = True
				for word2 in self.brain["languages"][language]["vocab"]:
					if self.similarity(word, word2) >= 70:
						obs.append(self.brain["languages"][language]["vocab"].index(word))
						tt = False
						break
				if tt:
					obs.append(0)
		return obs
	def hhmm(self, data, temperature=0.5, max_tokens=150, count=1, session="system", recall=False, keepinmind=False): # Hierarchical Hidden Markov Model
		qq = time.time()
		if session in self.sessions:
			pass
		else:
			self.sessions[session] = []
		data = data.lower().strip()
		olddata = data
		if recall:
			for word in self.tokenizer(data):
				for data2 in self.sessions[session]:
					if word in data2:
						data = data2+" "+data
		language = self.language_detector(data)
		obs = self.observation_detector(data, language=language)
		response = []
		required = (1-temperature)*100
		for text in self.brain["languages"][language]["data"]:
			obs2 = self.observation_detector(text, language=language)
			true = 0
			maxtrue = 0
			for ob in obs:
				if ob in obs2:
					true += 1
				maxtrue += 1
			w = (true/maxtrue)*100
			if w >= required:
				response.append(text)
				if len(response) >= count:
					break
		response = " ".join(response)
		newresponse = []
		for word in self.tokenizer(response):
			q = True
			for word2 in self.brain["languages"][language]["vocab"]:
				if self.similarity(word, word2) >= required:
					newresponse.append(word2)
					q = False
					break
			if q:
				newresponse.append(word)
		response = " ".join(newresponse)[:max_tokens]
		if keepinmind:
			self.sessions[session].append(data)
			self.sessions[session].append(response)
		return [response, time.time()-qq]
	def text_to_image(self, data, file="result.jpg", create_temp=0.1, guess_temp=0.5):
		qq = time.time()
		data = data.lower().strip()
		required = (1-guess_temp)*100
		targets = []
		endd = ""
		for image, mean in self.brain["images"].items():
			endd = image
			if self.similarity(mean, data) >= required:
				targets.append(image)
		pixels = {}
		for target in targets:
			image = Image.open(target)
			width, height = image.size
			for y in range(width):
				for x in range(height):
					name = (x, y)
					if name in pixels:
						try:
							colorold = pixels[name]
							newcolors = image.getpixel((x, y))
							color = []
							for hex1, hex2 in zip(colorold, newcolors):
								newhex = int((hex1+hex2)/2)
								newhex = int(random.uniform(newhex-(create_temp*255), newhex+(create_temp*255)))
								if newhex >= 255:
									newhex = 255
								if newhex <= 0:
									newhex = 0
								color.append(newhex)
							pixels[name] = (color[0], color[1], color[2])
						except Exception as e:
							print(e)
					else:
						try:
							color = image.getpixel((x, y))
							pixels[name] = (color[0], color[1], color[2])
						except:
							pass
		image = Image.new("RGB", (width, height))
		for pixel, color in pixels.items():
			image.putpixel(pixel, color)
		image.save(file)
		return time.time()-qq
	def deviate(self, data, temperature=0.5, language="system"):
		required = (1-temperature)*100
		if required != 100:
			response = []
			for word in self.tokenizer(data):
				q = True
				for word2 in self.brain["languages"][language]["vocab"]:
					if self.similarity(word, word2) >= required:
						response.append(word2)
						q = False
						break
				if q:
					response.append(word)
			response = " ".join(response)
		return response
	def amfer_setup(self, setupname, controlled=True, temperature=0.2):
		output = []
		if setupname in self.setups:
			for setupdata in self.setups[setupname]:
				language = setupdata["lang"]
				data = setupdata["data"]
				output.append(self.train(data, controlled=controlled, temperature=temperature, language=language))
			return "\n\n".join(output)
		else:
			return "Setup not found."
	def include_setup(self, setupname, data, language="system"):
		if setupname in self.setups:
			self.setups[setupname].append({"lang": language, "data": data})
		else:
			self.setups[setupname] = [{"lang": language, "data": data}]
	def delete_setup(self, setupname):
		del self.setups[setupname]
	def presave(self):
		self.last = self.brain
	def preload(self):
		self.brain = self.last
	def savebrain(self, target, safe=True):
		data = json.dumps(self.brain)
		if safe:
			data = base64.b64encode(data.encode()).decode()
		with open(target, "w") as f:
			f.write(data)
	def loadbrain(self, target, safe=True):
		with open(target, "r") as f:
			data = f.read()
		if safe:
			data = base64.b64decode(data.encode()).decode()
		self.brain = json.loads(data)
	def savesession(self, target, safe=True, session="system"):
		data = json.dumps(self.sessions[session])
		if safe:
			data = base64.b64encode(data.encode()).decode()
		with open(target, "w") as f:
			f.write(data)
	def loadsession(self, target, safe=True, session="system"):
		with open(target, "r") as f:
			data = f.read()
		if safe:
			data = base64.b64decode(data.encode()).decode()
		self.sessions[session] = json.loads(data)