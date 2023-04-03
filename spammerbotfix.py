import os, json, asyncio
from logging import basicConfig, getLogger, WARNING
from telethon import TelegramClient, events, Button
from telethon.sync import TelegramClient as TMPTelegramClient
from telethon.errors import PhoneNumberFloodError, SessionPasswordNeededError, FloodWaitError
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import GetAllChatsRequest
from telethon.sessions import StringSession

basicConfig(format="%(asctime)s - [Bot] %(message)s", level=WARNING)
LOGS = getLogger(__name__)

ADMIN = 1062204008

API_KEY = "12239970"

API_HASH = "f935d589592a183f212250574d4ec3e7"

bot_token = "6225248171:AAGEGiFK59nLSL5uPt32cNyNm02b1pUigyY"

Getter = None
Number = None
TempClient = None
SpamEnabled = False
Time = None
Message = None

if os.path.exists("SSs.json"):
	with open("SSs.json", "r+") as f:
		SSs = json.load(f)
else:
	SSs = {}
	with open("SSs.json", "w+") as f:
		json.dump(SSs, f)


if os.path.exists("ArchSSs.json"):
	with open("ArchSSs.json", "r+") as f:
		ArchSSs = json.load(f)
else:
	ArchSSs = {}
	with open("ArchSSs.json", "w+") as f:
		json.dump(ArchSSs, f)


def saveSS():
	global SSs
	with open("SSs.json", "w+") as f:
		json.dump(SSs, f)


def saveArchSS():
	global ArchSSs
	with open("ArchSSs.json", "w+") as f:
		json.dump(ArchSSs, f)


async def getAllChats(chats):
	global VARS
	groups = []
	for i in chats.chats:
		if type(i).__name__ == "Channel":
			if i.megagroup and not i.left:
				groups.append(i.id)
		elif type(i).__name__ == "Chat":
			if not i.left and not i.kicked and not i.deactivated:
				groups.append(i.id)
	return groups

async def doSpam(bot, msg):
	global ADMIN, SSs, API_KEY, API_HASH
	banned = []
	for SS in SSs:
		isAlive = False
		CClient = TMPTelegramClient(StringSession(SSs[SS]), API_KEY, API_HASH)
		await CClient.connect()
		try:
			me = await CClient.get_me()
			if me == None:
				isAlive = False
			else:
				isAlive = True
		except:
			isAlive = False
		if isAlive:
			async with CClient as client:
				try:
					groups = await getAllChats(await client(GetAllChatsRequest([])))
					for group in groups:
						try:
							await client.send_message(group, msg[0], file=msg[1], link_preview=msg[2])
							await asyncio.sleep(0.2)
						except:
							pass
				except:
					pass
		else:
			banned.append(SS)
			await bot.send_message(ADMIN, f"**⚠️ »** __Il VoIP__ `{SS}` __potrebbe essere stato bannato da Telegram! Se l'hai solo disconnesso riaggiungilo.__")
	if banned.__len__() > 0:
		for n in banned:
			if n in SSs:
				del(SSs[n])
		saveSS()


async def joinGroups(SS, groups):
	global ADMIN, SSs, API_KEY, API_HASH
	isAlive = False
	CClient = TMPTelegramClient(StringSession(SSs[SS]), API_KEY, API_HASH)
	await CClient.connect()
	try:
		me = await CClient.get_me()
		if me == None:
			isAlive = False
		else:
			isAlive = True
	except:
		isAlive = False
	if isAlive:
		async with CClient as client:
			for group in groups:
				try:
					await client(JoinChannelRequest(group))
				except FloodWaitError as err:
					await asyncio.sleep(err.seconds + 2)
					try:
						await client(JoinChannelRequest(group))
					except:
						pass
				except:
					pass
	else:
		await bot.send_message(ADMIN, f"**⚠️ »** __Il VoIP__ `{SS}` __potrebbe essere stato bannato da Telegram! Se l'hai solo disconnesso riaggiungilo.__")
		del(SSs[SS])
		saveSS()


bot = TelegramClient('bot', API_KEY, API_HASH).start(bot_token=bot_token)

@bot.on(events.NewMessage(incoming=True))
async def MessagesManager(e):
	global ADMIN, Getter, Number, TempClient, API_KEY, API_HASH, ArchSSs, SSs, SpamEnabled, Time, Message
	if e.chat_id == ADMIN:
		if e.text == "/start":
			if SpamEnabled:
				await e.respond("**🤖 Spammer Bot v1.3 🤖**\n\n__ℹ️ Stato Spam »__ **Attivo ✅**", buttons=[[Button.inline("❌ Stoppa", "stop"), Button.inline("Spammer 📞", "voip")], [Button.inline("⏱ Tempo", "timer"), Button.inline("Messaggio 💬", "messaggio")], [Button.inline("👥 Entra nei Gruppi 👥", "join")], [Button.url("⚙️Developer⚙️", "https://t.me/+pTUE15M4XU43NDVk")]])
			else:
				await e.respond("**🤖 Spammer Bot v1.3 🤖**\n\n__ℹ️ Stato Spam »__ **Non Attivo ❌**", buttons=[[Button.inline("✅ Avvia", "avvia"), Button.inline("Spammer 📞", "voip")], [Button.inline("⏱ Tempo", "timer"), Button.inline("Messaggio 💬", "messaggio")], [Button.inline("👥 Entra nei Gruppi 👥", "join")], [Button.url("⚙️Developer⚙️", "https://t.me/+pTUE15M4XU43NDVk")]])
		elif Getter != None:
			if Getter == 0:
				Getter = None
				if not e.text in SSs:
					if not e.text in ArchSSs:
						TempClient = TMPTelegramClient(StringSession(), API_KEY, API_HASH)
						await TempClient.connect()
						try:
							await TempClient.send_code_request(phone=e.text, force_sms=False)
							Number = e.text
							Getter = 1
							await e.respond("**📩 Inserisci il Codice 📩**", buttons=[Button.inline("❌ Annulla ❌", "voip")])
						except PhoneNumberFloodError:
							await e.respond("**❌ Troppi tentativi! Prova con un altro numero. ❌**", buttons=[Button.inline("🔄 Riprova 🔄", "addvoip")])
						except:
							await e.respond("**❌ Numero non Valido ❌**", buttons=[Button.inline("🔄 Riprova 🔄", "addvoip")])
					else:
						await e.respond("**❌ VoIP Archiviato! Riaggiungilo. ❌**", buttons=[[Button.inline("📁 VoIP Archiviati 📁", "arch")], [Button.inline("🔄 Riprova 🔄", "addvoip")]])
				else:
					await e.respond("**❌ VoIP già aggiunto ❌**", buttons=[Button.inline("🔄 Riprova 🔄", "addvoip")])
			elif Getter == 1:
				try:
					await TempClient.sign_in(phone=Number, code=e.text)
					SSs[Number] = TempClient.session.save()
					Getter, Number = None, None
					saveSS()
					await e.respond("**✅ VoIP Aggiunto Correttamente ✅**", buttons=[Button.inline("🔙 Indietro 🔙", "voip")])
				except SessionPasswordNeededError:
					Getter = 2
					await e.respond("**🔑 Inserisci la Password (2FA) 🔑**", buttons=[Button.inline("❌ Annulla ❌", "voip")])
				except:
					Getter, Number = None, None
					await e.respond("**❌ Codice Errato ❌**", buttons=[Button.inline("🔄 Riprova 🔄", "addvoip")])
			elif Getter == 2:
				try:
					await TempClient.sign_in(phone=Number, password=e.text)
					SSs[Number] = TempClient.session.save()
					Getter, Number = None, None
					saveSS()
					await e.respond("**✅ VoIP Aggiunto Correttamente ✅**", buttons=[Button.inline("🔙 Indietro 🔙", "voip")])
				except:
					Getter, Number = None, None
					await e.respond("**❌ Password Errata ❌**", buttons=[Button.inline("🔄 Riprova 🔄", "addvoip")])
			elif Getter == 3:
				Getter = None
				if e.text in SSs:
					await e.respond(f"**🔧 Gestione »** `{e.text}`", buttons=[[Button.inline("📁 Archivia", "arch;" + e.text), Button.inline("Rimuovi ➖", "del;" + e.text)], [Button.inline("🔙 Indietro 🔙", "voip")]])
				else:
					await e.respond("**❌ VoIP non Trovato ❌**", buttons=[Button.inline("🔄 Riprova 🔄", "voips")])
			elif Getter == 4:
				Getter = None
				if e.text in ArchSSs:
					await e.respond(f"**🔧 Gestione »** `{e.text}`", buttons=[[Button.inline("➕ Riaggiungi", "add;" + e.text), Button.inline("Rimuovi ➖", "delarch;" + e.text)], [Button.inline("🔙 Indietro 🔙", "voip")]])
				else:
					await e.respond("**❌ VoIP non Trovato ❌**", buttons=[Button.inline("🔄 Riprova 🔄", "voips")])
			elif Getter == 5:
				if e.text.isnumeric():
					num = int(e.text)
					if num > 4 and num < 501:
						Getter = None
						Time = num
						await e.respond("**✅ Tempo impostato correttamente ✅**", buttons=[Button.inline("🔙 Indietro 🔙", "timer")])
					else:
						await e.respond("**❌ Tempo non valido! (minimo 5 minuti e massimo 500) ❌\n\n🔄 Riprovare 🔄**", buttons=[Button.inline("❌ Annulla ❌", "back")])
				else:
					await e.respond("**❌ Formato tempo non valido! (usare la sintassi a numeri: es. 5) ❌\n\n🔄 Riprovare 🔄**", buttons=[Button.inline("❌ Annulla ❌", "back")])
			elif Getter == 6:
				Getter = None
				if e.media != None and type(e.media).__name__ != "MessageMediaWebPage" and type(e.media).__name__ != "MessageMediaUnsupported":
					media = e.media
				else:
					media = None
				if e.web_preview != None:
					lp = True
				else:
					lp = False
				Message = [e.text, media, lp]
				await e.respond("**✅ Messaggio Impostato Correttamente ✅**", buttons=[Button.inline("🔙 Indietro 🔙", "messaggio")])
			elif Getter == 7:
				if e.text != None and e.text != "":
					Getter = None
					groups = e.text.split("\n")
					tasks = []
					for SS in SSs:
						tasks.append(joinGroups(SS, groups))
					msg = await e.respond("__⛈ » Accesso ai Gruppi in corso...__\n\n**⚠️ » Questa operazione è pesante e lunga, potrebbero richiedere ore (o giorni)**")
					await asyncio.gather(*tasks)
					await msg.edit("**✅ Accesso ai Gruppi completato ✅**", buttons=[Button.inline("🔙 Indietro 🔙", "back")])
				else:
					await e.respond("**❌ Formato gruppi non valido! (usare la sintassi con l'username (ps: puoi dare una lista al bot e entrerà in automatico)) ❌\n\n🔄 Riprovare 🔄**", buttons=[Button.inline("❌ Annulla ❌", "back")])





@bot.on(events.CallbackQuery())
async def callbackAIAQuery(e):
	global ADMIN, Getter, Number, TempClient, API_KEY, API_HASH, ArchSSs, SSs, SpamEnabled, Time, Message
	if e.sender_id == ADMIN:
		if e.data == b"back":
			Getter = None
			if SpamEnabled:
				await e.edit("**🤖 Spammer Bot v1.3 🤖**\n\n__ℹ️ Stato Spam »__ **Attivo ✅**", buttons=[[Button.inline("❌ Stoppa", "stop"), Button.inline("Spammer 📞", "voip")], [Button.inline("⏱ Tempo", "timer"), Button.inline("Messaggio 💬", "messaggio")], [Button.inline("👥 Entra nei Gruppi 👥", "join")], [Button.url("⚙️Developer⚙️", "https://t.me/Ciro_Ruba_Rolex_x")]])
			else:
				await e.edit("**🤖 Spammer Bot v1.3 🤖**\n\n__ℹ️ Stato Spam »__ **Non Attivo ❌**", buttons=[[Button.inline("✅ Avvia", "avvia"), Button.inline("Spammer 📞", "voip")], [Button.inline("⏱ Tempo", "timer"), Button.inline("Messaggio 💬", "messaggio")], [Button.inline("👥 Entra nei Gruppi 👥", "join")], [Button.url("⚙️Developer⚙️", "https://t.me/Ciro_Ruba_Rolex_x")]])
		elif e.data == b"voip":
			Getter, Number, TempClient = None, None, None
			await e.edit(f"__📞 VoIP Aggiunti »__ **{SSs.__len__()}**", buttons=[[Button.inline("➕ Aggiungi", "addvoip"), Button.inline("Gestisci 🔧", "voips")], [Button.inline("📁 Archiviati 📁", "arch")], [Button.inline("🔙 Indietro 🔙", "back")]])
		elif e.data == b"addvoip":
			Getter = 0
			await e.edit("**☎️ Inserisci il numero del VoIP che desideri aggiungere ☎️**", buttons=[Button.inline("❌ Annulla ❌", "voip")])
		elif e.data == b"voips":
			if SSs.__len__() > 0:
				Getter = 3
				msg = "__☎️ Invia il numero del VoIP che vuoi gestire__\n\n**LISTA VOIP**"
				for n in SSs:
					msg += f"\n`{n}`"
				await e.edit(msg, buttons=[Button.inline("❌ Annulla ❌", "voip")])
			else:
				await e.edit("**❌ Non hai aggiunto nessun VoIP ❌**", buttons=[[Button.inline("➕ Aggiungi ➕", "addvoip")], [Button.inline("🔙 Indietro 🔙", "voip")]])
		elif e.data == b"arch":
			if ArchSSs.__len__() > 0:
				Getter = 4
				msg = f"__📁 Voip Archiviati »__ **{ArchSSs.__len__()}**\n\n__☎️ Invia il numero del VoIP archiviato che vuoi gestire__\n\n**LISTA VOIP ARCHIVIATI**"
				for n in ArchSSs:
					msg += f"\n`{n}`"
				await e.edit(msg, buttons=[Button.inline("❌ Annulla ❌", "voip")])
			else:
				await e.edit("**❌ Non hai archiviato nessun VoIP ❌**", buttons=[Button.inline("🔙 Indietro 🔙", "voip")])
		elif e.data == b"avvia":
			if not SpamEnabled:
				if SSs.__len__() > 0:
					if Time != None:
						if Message != None:
							SpamEnabled = True
							await e.edit("**✅ Spam Avviato Correttamente ✅**", buttons=[Button.inline("🔙 Indietro 🔙", "back")])
							while SpamEnabled:
								await asyncio.wait([doSpam(e.client, Message)])
								for i in range(Time * 60):
									if SpamEnabled:
										await asyncio.sleep(1)
									else:
										break
						else:
							await e.edit("**❌ Messaggio non Impostato ❌**", buttons=[[Button.inline("✍🏻 Imposta ✍🏻", "getmsg")], [Button.inline("🔙 Indietro 🔙", "back")]])
					else:
						await e.edit("**❌ Tempo non Impostato ❌**", buttons=[[Button.inline("✍🏻 Imposta ✍🏻", "gettime")], [Button.inline("🔙 Indietro 🔙", "back")]])
				else:
					await e.edit("**❌ Non hai aggiunto nessun VoIP ❌**", buttons=[[Button.inline("➕ Aggiungi ➕", "addvoip")], [Button.inline("🔙 Indietro 🔙", "voip")]])
			else:
				await e.answer("❌ Lo Spam è già attivo!", alert=True)
		elif e.data == b"stop":
			if SpamEnabled:
				SpamEnabled = False
				await e.edit("**❌ Spam Stoppato Correttamente ❌**", buttons=[Button.inline("🔙 Indietro 🔙", "back")])
			else:
				await e.answer("❌ Lo Spam non è attivo!", alert=True)
		elif e.data == b"timer":
			if Time == None:
				await e.edit("**❌ Tempo non impostato ❌\n\nℹ️ Puoi impostarlo con il tasto qui sotto!**", buttons=[[Button.inline("✍🏻 Imposta ✍🏻", "gettime")], [Button.inline("🔙 Indietro 🔙", "back")]])
			else:
				await e.edit(f"__⏱ Tempo »__ **{Time} Minuti**", buttons=[[Button.inline("✍🏻 Modifica ✍🏻", "gettime")], [Button.inline("🔙 Indietro 🔙", "back")]])
		elif e.data == b"messaggio":
			if Message == None:
				await e.edit("**❌ Messaggio non impostato ❌\n\nℹ️ Puoi impostarlo con il tasto qui sotto!**", buttons=[[Button.inline("✍🏻 Imposta ✍🏻", "getmsg")], [Button.inline("🔙 Indietro 🔙", "back")]])
			else:
				await e.edit(f"**✅ Il messaggio è impostato ✅**", buttons=[[Button.inline("✍🏻 Modifica ✍🏻", "getmsg")], [Button.inline("🔙 Indietro 🔙", "back")]])
		elif e.data == b"gettime":
			Getter = 5
			await e.edit("__⏱ Inviare il tempo in minuti da impostare!__", buttons=[Button.inline("❌ Annulla ❌", "back")])
		elif e.data == b"getmsg":
			Getter = 6
			await e.edit("__💬 Inviare il messaggio da impostare!__", buttons=[Button.inline("❌ Annulla ❌", "back")])
		elif e.data == b"join":
			Getter = 7
			await e.edit("__👥 Inviare la lista di gruppi in cui entrare!__", buttons=[Button.inline("❌ Annulla ❌", "back")])
		else:
			st = e.data.decode().split(";")
			if st[0] == "arch":
				if st[1] in SSs:
					if not st[1] in ArchSSs:
						ArchSSs[st[1]] = SSs[st[1]]
						saveArchSS()
					del(SSs[st[1]])
					saveSS()
					await e.edit("**✅ VoIP Archiviato Correttamente ✅**", buttons=[Button.inline("🔙 Indietro 🔙", "voip")])
				else:
					await e.edit("**❌ VoIP non Trovato ❌**", buttons=[Button.inline("🔙 Indietro 🔙", "voip")])
			elif st[0] == "add":
				if st[1] in ArchSSs:
					SSs[st[1]] = ArchSSs[st[1]]
					saveSS()
					del(ArchSSs[st[1]])
					saveArchSS()
					await e.edit("**✅ VoIP Riaggiunto Correttamente ✅**", buttons=[Button.inline("🔙 Indietro 🔙", "voip")])
				else:
					await e.edit("**❌ VoIP non Trovato ❌**", buttons=[Button.inline("🔙 Indietro 🔙", "voip")])
			elif st[0] == "del":
				if st[1] in SSs:
					CClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH)
					await CClient.connect()
					try:
						me = await CClient.get_me()
						if me != None:
							async with CClient as client:
								await client.log_out()
					except:
						pass
					del(SSs[st[1]])
					saveSS()
					await e.edit("**✅ VoIP Rimosso Correttamente ✅**", buttons=[Button.inline("🔙 Indietro 🔙", "voip")])
				else:
					await e.edit("**❌ VoIP già Rimosso ❌**", buttons=[Button.inline("🔙 Indietro 🔙", "voip")])
			elif st[0] == "delarch":
				if st[1] in ArchSSs:
					CClient = TMPTelegramClient(StringSession(SSs[st[1]]), API_KEY, API_HASH)
					await CClient.connect()
					try:
						me = await CClient.get_me()
						if me != None:
							async with CClient as client:
								await client.log_out()
					except:
						pass
					del(ArchSSs[st[1]])
					saveArchSS()
					await e.edit("**✅ VoIP Rimosso Correttamente ✅**", buttons=[Button.inline("🔙 Indietro 🔙", "voip")])
				else:
					await e.edit("**❌ Voip già Rimosso ❌**", buttons=[Button.inline("🔙 Indietro 🔙", "voip")])





LOGS.warning("Avvio Bot In Corso...")

bot.start()

LOGS.warning("Bot Avviato Correttamente!")

bot.run_until_disconnected()
