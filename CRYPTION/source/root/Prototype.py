import dbg
import app
import localeInfo
import wndMgr
import systemSetting
import mouseModule
import networkModule
import constInfo
import musicInfo
import stringCommander
import exception

if constInfo.ENABLE_PASTE_FEATURE:
	from ui import EnablePaste as ui_EnablePaste
	ui_EnablePaste(True)

def RunApp():
	musicInfo.LoadLastPlayFieldMusic()

	app.SetHairColorEnable(constInfo.HAIR_COLOR_ENABLE)
	app.SetArmorSpecularEnable(constInfo.ARMOR_SPECULAR_ENABLE)
	app.SetWeaponSpecularEnable(constInfo.WEAPON_SPECULAR_ENABLE)

	localeInfo.UI_DEF_FONT = "Tahoma:12"
	localeInfo.UI_DEF_FONT_LARGE = "Tahoma:16"
	
	app.SetMouseHandler(mouseModule.mouseController)
	wndMgr.SetMouseHandler(mouseModule.mouseController)
	wndMgr.SetScreenSize(systemSetting.GetWidth(), systemSetting.GetHeight())
	
	#ui_EnablePaste(True)

	try:
		app.Create(localeInfo.APP_TITLE, systemSetting.GetWidth(), systemSetting.GetHeight(), 1)
	except RuntimeError, msg:
		msg = str(msg)
		if "CREATE_DEVICE" == msg:
			dbg.LogBox("Sorry, Your system does not support 3D graphics,\r\nplease check your hardware and system configeration\r\nthen try again.")
			dbg.TraceError("Sorry, Your system does not support 3D graphics,\r\nplease check your hardware and system configeration\r\nthen try again.")
		else:
			dbg.LogBox("Error! %s" % (msg))
			dbg.TraceError(msg)
		return
	except:
		exception.Abort("App create fail!")
		return

	app.SetCamera(1500.0, 30.0, 0.0, 180.0)

	if not mouseModule.mouseController.Create():
		return

	mainStream = networkModule.MainStream()
	mainStream.Create()

	if constInfo.CLIENTLESS_TEST_SERVER:
		mainStream.SetTestGamePhase(921600 + 45400, 204800 + 70900)
	else:
		mainStream.SetLoginPhase()

	#mainStream.SetLogoPhase()
	#mainStream.SetCreateCharacterPhase()
	#mainStream.SetSelectEmpirePhase()
	#mainStream.SetSelectCharacterPhase()
	#mainStream.SetLoadingPhase()
	#mainStream.SetGamePhase()

	app.Loop()

	mainStream.Destroy()

RunApp()

