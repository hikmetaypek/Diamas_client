import ui
import admin
import chat
import localeInfo
import miniMap
import uiMiniMap
import wndMgr
import background
import app
import playerSettingModule
import player
import uiTaskBar
import net
import uiToolTip
import chr
import skill
import uiCommon
import grp

class AdminManagerWindow(ui.ScriptWindow):

	class MapViewer_AtlasRenderer(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)
			self.AddFlag("not_pick")

		def OnUpdate(self):
			miniMap.UpdateAdminManagerAtlas()

		def OnRender(self):
			(x, y) = self.GetGlobalPosition()
			miniMap.RenderAdminManagerAtlas(float(x), float(y), float(self.GetWidth()), float(self.GetHeight()))

		def HideAtlas(self):
			miniMap.HideAdminManagerAtlas()

		def ShowAtlas(self):
			miniMap.ShowAdminManagerAtlas()

	DISABLE_COLOR = grp.GenerateColor(0.33, 0.33, 0.33, 0.3)

	PAGE_GENERAL = 0
	PAGE_MAPVIEWER = 1
	PAGE_OBSERVER = 2
	PAGE_MAX_NUM = 3

	OBSERVER_NAVI_GENERAL = 0
	OBSERVER_NAVI_ITEM = 1
	OBSERVER_NAVI_WHISPER = 2
	OBSERVER_NAVI_MAX_NUM = 3

	OBSERVER_FACE_IMAGE_DICT = {
		playerSettingModule.RACE_WARRIOR_M	: "icon/face/warrior_m.tga",
		playerSettingModule.RACE_WARRIOR_W	: "icon/face/warrior_w.tga",
		playerSettingModule.RACE_ASSASSIN_M	: "icon/face/assassin_m.tga",
		playerSettingModule.RACE_ASSASSIN_W	: "icon/face/assassin_w.tga",
		playerSettingModule.RACE_SURA_M		: "icon/face/sura_m.tga",
		playerSettingModule.RACE_SURA_W		: "icon/face/sura_w.tga",
		playerSettingModule.RACE_SHAMAN_M	: "icon/face/shaman_m.tga",
		playerSettingModule.RACE_SHAMAN_W	: "icon/face/shaman_w.tga",
	}

	OBSERVER_EMPIRE_IMAGE_DICT = {
		net.EMPIRE_A : "d:/ymir work/ui/intro/empire/empireflag_a.sub",
		net.EMPIRE_B : "d:/ymir work/ui/intro/empire/empireflag_b.sub",
		net.EMPIRE_C : "d:/ymir work/ui/intro/empire/empireflag_c.sub",
	}

	#################################################
	## MAIN FUNCTIONS
	#################################################

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.currentPageIndex = -1

		self.pageNeedRefresh = []
		self.pageData = []
		for i in xrange(self.PAGE_MAX_NUM):
			self.pageNeedRefresh.append(TRUE)
			self.pageData.append({})

		self.LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/AdminManagerWindow.py")
		except:
			import exception
			exception.Abort("AdminManagerWindow.LoadDialog.LoadScript")

		try:
			GetObject=self.GetChild
			self.titleBar = GetObject("TitleBar")

			self.pages = {
				# page general
				self.PAGE_GENERAL : {
					"wnd" : GetObject("page_general"),
					"online_list" : GetObject("general_online_player_table"),
					"online_scroll" : GetObject("general_online_player_scrollbar"),
					"dividing_line" : GetObject("general_online_player_dividing_line"),
					"online_search_edit" : GetObject("general_online_player_search_edit"),
					"online_search_btn" : GetObject("general_online_player_search_button"),
					"user_count" : GetObject("general_current_user_count"),
				},
				# page mapviewer
				self.PAGE_MAPVIEWER : {
					"wnd" : GetObject("page_mapviewer"),
					"atlas" : GetObject("mapviewer_atlas"),
					"no_select_wnd" : GetObject("mapviewer_no_map_selected"),
					"select_list" : GetObject("mapviewer_select_list"),
					"select_scroll" : GetObject("mapviewer_select_scrollbar"),
					"select_btn" : GetObject("mapviewer_select_button"),
					"select_line" : GetObject("mapviewer_dividing_line2"),
					"option_%d" % miniMap.ADMIN_SHOW_PC : GetObject("mapviewer_option_player"),
					"option_%d" % miniMap.ADMIN_SHOW_MOB : GetObject("mapviewer_option_mob"),
					"option_%d" % miniMap.ADMIN_SHOW_STONE : GetObject("mapviewer_option_stone"),
					"option_%d" % miniMap.ADMIN_SHOW_NPC : GetObject("mapviewer_option_npc"),
					"stop_btn" : GetObject("mapviewer_stop_button"),
				},
				# page observer
				self.PAGE_OBSERVER : {
					"wnd" : GetObject("page_observer"),
					"stopped_wnd" : GetObject("observer_stopped_wnd"),
					"stopped_edit" : GetObject("observer_stopped_name_edit"),
					"stopped_btn" : GetObject("observer_stopped_button"),
					"running_wnd" : GetObject("observer_running_wnd"),
					"navi_buttons" : [GetObject("observer_navi_button_%d" % (i + 1)) for i in xrange(self.OBSERVER_NAVI_MAX_NUM)],
					"stop_button" : GetObject("observer_stop_button"),
					"subpage_%d" % self.OBSERVER_NAVI_GENERAL : {
						"wnd" : GetObject("observer_subpage_general"),
						"face" : GetObject("observer_general_face"),
						"pid" : GetObject("observer_general_pid"),
						"name" : GetObject("observer_general_name"),
						"level" : GetObject("observer_general_level"),
						"hpbar" : GetObject("observer_general_hpgauge"),
						"hptext" : GetObject("observer_general_hptext"),
						"spbar" : GetObject("observer_general_spgauge"),
						"sptext" : GetObject("observer_general_sptext"),
						"exp_point_bg" : GetObject("observer_general_exp_bg"),
						"exp_points" : [GetObject("observer_general_exp_%d" % (i + 1)) for i in xrange(4)],
						"empire" : GetObject("observer_general_empire"),
						"channel" : GetObject("observer_general_channel"),
						"map_info" : GetObject("observer_general_map_info"),
						"gold" : GetObject("observer_general_gold"),
						"skillgroup" : GetObject("observer_general_skillgroup"),
						"skill_wnd" : GetObject("observer_general_skill_bg"),
						"skill" : GetObject("observer_general_skill_slot"),
					},
					"subpage_%d" % self.OBSERVER_NAVI_ITEM : {
						"wnd" : GetObject("observer_subpage_item"),
						"equipment" : GetObject("observer_item_equipment_slot"),
						"inventory" : GetObject("observer_item_inventory_slot"),
						"inventory_page_1" : GetObject("observer_item_inventory_tab_01"),
						"inventory_page_2" : GetObject("observer_item_inventory_tab_02"),
						"money" : GetObject("observer_item_money_text"),
					},
					"subpage_%d" % self.OBSERVER_NAVI_WHISPER : {
						"wnd" : GetObject("observer_subpage_whisper"),
						"name_list" : GetObject("observer_whisper_name_list"),
						"name_scroll" : GetObject("observer_whisper_name_scroll"),
						"text" : GetObject("observer_whisper_text"),
						"text_scroll" : GetObject("observer_whisper_text_scroll"),
					},
				},
			}

			self.naviBtnList = [GetObject("navi_button_%d" % (i + 1)) for i in xrange(self.PAGE_MAX_NUM)]

		except:
			import exception
			exception.Abort("AdminManagerWindow.LoadDialog.BindObject")

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

		# PAGE_GENERAL
		self.GENERAL_BuildPage()
		page = self.pages[self.PAGE_GENERAL]
		page["online_list"].SetHeaderClickEvent(ui.__mem_func__(self.GENERAL_OnListHeaderClick))
		page["online_list"].SetDoubleClickEvent(ui.__mem_func__(self.GENERAL_OnListDoubleClick))
		page["online_scroll"].SetScrollEvent(ui.__mem_func__(self.GENERAL_OnOnlineScroll))
		page["online_search_edit"].SetEscapeEvent(ui.__mem_func__(self.OnPressEscapeKey))
		page["online_search_edit"].SetReturnEvent(ui.__mem_func__(self.GENERAL_OnlineSearchPlayer))
		page["online_search_btn"].SAFE_SetEvent(self.GENERAL_OnlineSearchPlayer)

		# PAGE_MAPVIEWER
		self.MAPVIEWER_Build()
		page = self.pages[self.PAGE_MAPVIEWER]
		page["select_scroll"].SetScrollEvent(ui.__mem_func__(self.MAPVIEWER_OnSelectScroll))
		page["select_btn"].SAFE_SetEvent(self.MAPVIEWER_SelectMap)
		page["option_%d" % miniMap.ADMIN_SHOW_PC].SAFE_SetEvent(self.MAPVIEWER_OnClickOptionButton, miniMap.ADMIN_SHOW_PC)
		page["option_%d" % miniMap.ADMIN_SHOW_MOB].SAFE_SetEvent(self.MAPVIEWER_OnClickOptionButton, miniMap.ADMIN_SHOW_MOB)
		page["option_%d" % miniMap.ADMIN_SHOW_STONE].SAFE_SetEvent(self.MAPVIEWER_OnClickOptionButton, miniMap.ADMIN_SHOW_STONE)
		page["option_%d" % miniMap.ADMIN_SHOW_NPC].SAFE_SetEvent(self.MAPVIEWER_OnClickOptionButton, miniMap.ADMIN_SHOW_NPC)
		page["stop_btn"].SAFE_SetEvent(self.MAPVIEWER_Stop)

		# PAGE_OBSERVER
		self.OBSERVER_Build()
		page = self.pages[self.PAGE_OBSERVER]
		page["stopped_edit"].SetEscapeEvent(ui.__mem_func__(self.OnPressEscapeKey))
		page["stopped_edit"].SetReturnEvent(ui.__mem_func__(self.OBSERVER_StartObservation))
		page["stopped_btn"].SAFE_SetEvent(self.OBSERVER_StartObservation)
		for i in xrange(self.OBSERVER_NAVI_MAX_NUM):
			btn = page["navi_buttons"][i]
			btn.SAFE_SetEvent(self.OBSERVER_OnClickNaviButton, i)
		page["stop_button"].SAFE_SetEvent(self.OBSERVER_StopObservation)
		# SUB_PAGE_ITEM
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_ITEM]
		subPage["equipment"].SetOverInItemEvent(ui.__mem_func__(self.OBSERVER_OnOverInItemSlot))
		subPage["equipment"].SetOverOutItemEvent(ui.__mem_func__(self.OBSERVER_OnOverOutItemSlot))
		subPage["inventory"].SetOverInItemEvent(ui.__mem_func__(self.OBSERVER_OnOverInItemSlot))
		subPage["inventory"].SetOverOutItemEvent(ui.__mem_func__(self.OBSERVER_OnOverOutItemSlot))
		for i in xrange(player.INVENTORY_PAGE_COUNT):
			subPage["inventory_page_%d" % (i + 1)].SAFE_SetEvent(self.OBSERVER_OnClickInventoryPageButton, i)
		# SUB_PAGE_WHISPER
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_WHISPER]
		subPage["name_list"].SetEvent(ui.__mem_func__(self.OBSERVER_OnSelectWhisperName))
		subPage["name_scroll"].SetScrollEvent(ui.__mem_func__(self.OBSERVER_OnWhisperNameScroll))
		subPage["text_scroll"].SetScrollEvent(ui.__mem_func__(self.OBSERVER_OnWhisperTextScroll))

		# Navi
		for i in xrange(self.PAGE_MAX_NUM):
			btn = self.naviBtnList[i]
			btn.SAFE_SetEvent(self.OnClickNaviButton, i)
		self.OnClickNaviButton(self.PAGE_GENERAL)

		# refresh rect
		self.UpdateRect()

	def Destroy(self):
		self.Close()

	def Open(self):
		self.OnOpenPage()
		self.Show()

	def Close(self):
		self.OnClosePage()
		self.Hide()

	def OnUpdate(self):
		self.MAPVIEWER_OnUpdate()
		self.OBSERVER_OnUpdate()

	def OnAfterRender(self):
		if self.currentPageIndex == self.PAGE_OBSERVER:
			self.OBSERVER_OnAfterRender()

	def OnPressEscapeKey(self):
		self.Close()
		return TRUE

	#################################################
	## PAGE FUNCTIONS
	#################################################

	def LoadPage(self, pageIndex):
		if self.currentPageIndex == pageIndex:
			return

		self.OnClosePage()

		self.currentPageIndex = pageIndex

		# refresh if needed
		if self.pageNeedRefresh[pageIndex] == TRUE:
			if pageIndex == self.PAGE_GENERAL:
				self.GENERAL_RefreshPage()
			elif pageIndex == self.PAGE_MAPVIEWER:
				self.MAPVIEWER_RefreshPage()
			elif pageIndex == self.PAGE_OBSERVER:
				self.OBSERVER_RefreshPage()

		self.OnOpenPage()

		# show selected pages
		for i in xrange(self.PAGE_MAX_NUM):
			page = self.pages[i]["wnd"]
			if i == pageIndex:
				page.Show()
			else:
				page.Hide()

	def OnClosePage(self):
		if self.currentPageIndex == self.PAGE_GENERAL:
			self.GENERAL_OnClosePage()
		elif self.currentPageIndex == self.PAGE_MAPVIEWER:
			self.MAPVIEWER_OnClosePage()
		elif self.currentPageIndex == self.PAGE_OBSERVER:
			self.OBSERVER_OnClosePage()

	def OnOpenPage(self):
		if self.currentPageIndex == self.PAGE_MAPVIEWER:
			self.MAPVIEWER_OnOpenPage()
		elif self.currentPageIndex == self.PAGE_OBSERVER:
			self.OBSERVER_OnOpenPage()

	#################################################
	## PAGE: GENERAL FUNCTIONS
	#################################################

	def GENERAL_BuildPage(self):
		page = self.pages[self.PAGE_GENERAL]
		pageData = self.pageData[self.PAGE_GENERAL]

		pageData["question_wnd"] = uiCommon.QuestionDialog()
		pageData["question_wnd"].SAFE_SetCancelEvent(pageData["question_wnd"].Close)
		pageData["question_wnd"].Close()

	def GENERAL_RefreshPage(self):
		self.GENERAL_RefreshOnlineList()
		self.GENERAL_RefreshOnlineScrollBar()
		self.GENERAL_RefreshUserCount()

		self.pageNeedRefresh[self.PAGE_GENERAL] = FALSE

	def GENERAL_OnClosePage(self):
		page = self.pages[self.PAGE_GENERAL]
		pageData = self.pageData[self.PAGE_GENERAL]

		page["online_search_edit"].KillFocus()
		pageData["question_wnd"].Close()

	def GENERAL_RefreshOnlineList(self):
		page = self.pages[self.PAGE_GENERAL]

		basePos = page["online_list"].GetBasePos()
		page["online_list"].Clear()

		for i in xrange(admin.GetOnlinePlayerCount()):
			if admin.IsOnlinePlayerSorted():
				(pid, name, map_index, channel, empire) = admin.GetSortOnlinePlayerByIndex(i)
			else:
				(pid, name, map_index, channel, empire) = admin.GetOnlinePlayerByIndex(i)
			page["online_list"].Append(pid, [pid, name, map_index, channel, empire], FALSE)
		page["online_list"].SetBasePos(basePos)

	def GENERAL_RefreshOnlineScrollBar(self):
		page = self.pages[self.PAGE_GENERAL]

		if page["online_list"].GetMaxLineCount() > page["online_list"].GetViewLineCount():
			page["online_scroll"].Hide()
			page["dividing_line"].Show()
		else:
			page["online_scroll"].SetMiddleBarSize(float(page["online_list"].GetMaxLineCount()) / float(page["online_list"].GetLineCount()))
			page["online_scroll"].Show()
			page["dividing_line"].Hide()

	def GENERAL_RefreshUserCount(self):
		page = self.pages[self.PAGE_GENERAL]

		page["user_count"].SetText(localeInfo.ADMIN_MANAGER_GENERAL_USER_COUNT % localeInfo.NumberToString(admin.GetOnlinePlayerCount()))

	def GENERAL_AddOnlinePlayer(self, pid):
		page = self.pages[self.PAGE_GENERAL]

		if admin.IsOnlinePlayerSorted():
			self.GENERAL_RefreshPage()

		else:
			(pid, name, map_index, channel, empire) = admin.GetOnlinePlayerByPID(pid)
			page["online_list"].Append(pid, [pid, name, map_index, channel, empire])

			self.GENERAL_RefreshUserCount()

	def GENERAL_EraseOnlinePlayer(self, pid):
		page = self.pages[self.PAGE_GENERAL]

		page["online_list"].Erase(pid)

		self.GENERAL_RefreshUserCount()

	def GENERAL_OnOnlineScroll(self):
		page = self.pages[self.PAGE_GENERAL]

		pos = page["online_scroll"].GetPos()
		basePos = int(float(page["online_list"].GetLineCount() - page["online_list"].GetViewLineCount()) * pos)
		if basePos != page["online_list"].GetBasePos():
			page["online_list"].SetBasePos(basePos)

	def GENERAL_OnlineSearchPlayer(self):
		page = self.pages[self.PAGE_GENERAL]

		playerName = page["online_search_edit"].GetText()
		if playerName == "":
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Du hast keinen Namen angegeben.")
			return

	def GENERAL_OnListHeaderClick(self, colIndex):
		sortDir = 0
		if admin.GetOnlinePlayerSortType() == colIndex and admin.GetOnlinePlayerSortDir() == 0:
			sortDir = 1
		chat.AppendChat(chat.CHAT_TYPE_INFO, "SortOnlinePlayer %d, %d" % (colIndex, sortDir))
		admin.SortOnlinePlayer(colIndex, sortDir)

		self.GENERAL_RefreshOnlineList()

	def GENERAL_OnListDoubleClick(self, pid):
		page = self.pages[self.PAGE_GENERAL]
		pageData = self.pageData[self.PAGE_GENERAL]

		if pid == 0:
			return

		if admin.IsObserverRunning() and admin.GetObserverPID() == pid:
			self.OnClickNaviButton(self.PAGE_OBSERVER)
			return

		(pid, name, map_index, channel, empire) = admin.GetOnlinePlayerByPID(pid)
		pageData["question_wnd"].SetText(localeInfo.ADMIN_MANAGER_GENERAL_QUESTION_TEXT % name)
		pageData["question_wnd"].SAFE_SetAcceptEvent(self.GENERAL_OnQuestionDlgAccept, name)
		pageData["question_wnd"].Open()

	def GENERAL_OnQuestionDlgAccept(self, name):
		page = self.pages[self.PAGE_GENERAL]
		pageData = self.pageData[self.PAGE_GENERAL]

		pageData["question_wnd"].Close()
		self.OBSERVER_StartObservation(name[0])

	#################################################
	## PAGE: MAPVIEWER FUNCTIONS
	#################################################

	def MAPVIEWER_Build(self):
		page = self.pages[self.PAGE_MAPVIEWER]

		wndAtlas = self.MapViewer_AtlasRenderer()
		wndAtlas.SetParent(page["atlas"])
		wndAtlas.SetPosition(0, 0)
		wndAtlas.SetSize(page["atlas"].GetWidth(), page["atlas"].GetHeight())
		wndAtlas.HideAtlas()
		wndAtlas.Show()
		page["atlas_wnd"] = wndAtlas

		wndAtlasToolTip = uiMiniMap.MapTextToolTip()
		wndAtlasToolTip.SetParent(wndAtlas)
		wndAtlasToolTip.Hide()
		page["atlas_tooltip"] = wndAtlasToolTip

	def MAPVIEWER_OnClosePage(self):
		pageData = self.pageData[self.PAGE_MAPVIEWER]

		if self.MAPVIEWER_IsRunning():
			pageData["stop_timer"] = app.GetTime() + 30

	def MAPVIEWER_OnOpenPage(self):
		pageData = self.pageData[self.PAGE_MAPVIEWER]

		if self.MAPVIEWER_IsRunning():
			if pageData.has_key("is_paused") and pageData["is_paused"] == TRUE:
				pageData["is_paused"] = FALSE
				admin.StartMapViewer(pageData["map_x"], pageData["map_y"])
			elif pageData.has_key("stop_timer") and pageData["stop_timer"] != 0:
				pageData["stop_timer"] = 0

	def MAPVIEWER_RefreshPage(self):
		self.MAPVIEWER_RefreshAtlasWindow()
		self.MAPVIEWER_RefreshMapSelection()
		self.MAPVIEWER_RefreshOptionButton(miniMap.ADMIN_SHOW_PC)
		self.MAPVIEWER_RefreshOptionButton(miniMap.ADMIN_SHOW_MOB)
		self.MAPVIEWER_RefreshOptionButton(miniMap.ADMIN_SHOW_STONE)
		self.MAPVIEWER_RefreshOptionButton(miniMap.ADMIN_SHOW_NPC)
		self.MAPVIEWER_RefreshStopButton()

		self.pageNeedRefresh[self.PAGE_MAPVIEWER] = FALSE

	def MAPVIEWER_RefreshAtlasWindow(self):
		page = self.pages[self.PAGE_MAPVIEWER]
		pageData = self.pageData[self.PAGE_MAPVIEWER]

		if self.MAPVIEWER_IsRunning():
			page["atlas_wnd"].ShowAtlas()
			page["no_select_wnd"].Hide()
		else:
			page["atlas_wnd"].HideAtlas()
			page["no_select_wnd"].Show()

	def MAPVIEWER_RefreshMapSelection(self):
		page = self.pages[self.PAGE_MAPVIEWER]

		oldSelection = page["select_list"].GetSelectedLine()
		oldScrollPos = page["select_scroll"].GetPos()

		page["select_list"].ClearItem()

		if self.MAPVIEWER_IsRunning():
			page["select_list"].SetSize(page["select_list"].GetWidth(), page["select_list"].GetStepSize() * 5)
			page["select_btn"].SetPosition(page["select_btn"].GetLeft(), page["select_list"].GetBottom() + 5)
			page["select_line"].Show()
		else:
			page["select_list"].SetSize(page["select_list"].GetWidth(), page["select_list"].GetStepSize() * 14)
			page["select_btn"].SetPosition(page["select_btn"].GetLeft(), page["stop_btn"].GetTop())
			page["select_line"].Hide()
		page["select_line"].SetPosition(page["select_line"].GetLeft(), page["select_btn"].GetBottom() + 6)
		page["select_scroll"].SetScrollBarSize(page["select_btn"].GetBottom() - page["select_scroll"].GetTop())

		for i in xrange(background.GetMapInfoCount()):
			if not self.MAPVIEWER_IsAvailableMap(i):
				continue

			name, x, y = background.GetMapInfoByIndex(i)
			page["select_list"].InsertItem(i, name.replace("_", " "))

		if oldSelection != -1:
			page["select_list"].SelectItem(oldSelection)

		self.MAPVIEWER_RefreshMapScrollBar(oldScrollPos)

	def MAPVIEWER_RefreshMapScrollBar(self, scrollPos):
		page = self.pages[self.PAGE_MAPVIEWER]

		if page["select_list"].GetItemCount() <= page["select_list"].GetViewItemCount():
			page["select_scroll"].Hide()
		else:
			page["select_scroll"].SetMiddleBarSize(float(page["select_list"].GetViewItemCount()) / float(page["select_list"].GetItemCount()))
			page["select_scroll"].SetPos(scrollPos)
			page["select_scroll"].Show()

	def MAPVIEWER_RefreshOptionButton(self, flag):
		page = self.pages[self.PAGE_MAPVIEWER]

		if self.MAPVIEWER_IsRunning():
			self.MAPVIEWER_RefreshOptionButtonText(flag)
			page["option_%d" % flag].Show()
		else:
			page["option_%d" % flag].Hide()

	def MAPVIEWER_RefreshOptionButtonText(self, flag):
		page = self.pages[self.PAGE_MAPVIEWER]

		text = {
			miniMap.ADMIN_SHOW_PC : {
				FALSE : localeInfo.ADMIN_MANAGER_MAPVIEWER_SHOW_PLAYER_BUTTON,
				TRUE : localeInfo.ADMIN_MANAGER_MAPVIEWER_HIDE_PLAYER_BUTTON,
			},
			miniMap.ADMIN_SHOW_MOB : {
				FALSE : localeInfo.ADMIN_MANAGER_MAPVIEWER_SHOW_MOB_BUTTON,
				TRUE : localeInfo.ADMIN_MANAGER_MAPVIEWER_HIDE_MOB_BUTTON,
			},
			miniMap.ADMIN_SHOW_STONE : {
				FALSE : localeInfo.ADMIN_MANAGER_MAPVIEWER_SHOW_STONE_BUTTON,
				TRUE : localeInfo.ADMIN_MANAGER_MAPVIEWER_HIDE_STONE_BUTTON,
			},
			miniMap.ADMIN_SHOW_NPC : {
				FALSE : localeInfo.ADMIN_MANAGER_MAPVIEWER_SHOW_NPC_BUTTON,
				TRUE : localeInfo.ADMIN_MANAGER_MAPVIEWER_HIDE_NPC_BUTTON,
			},
		}
		page["option_%d" % flag].SetText(text[flag][miniMap.IsAdminManagerAtlasFlagShown(flag)])

	def MAPVIEWER_RefreshStopButton(self):
		page = self.pages[self.PAGE_MAPVIEWER]

		if self.MAPVIEWER_IsRunning():
			page["stop_btn"].Show()
		else:
			page["stop_btn"].Hide()

	def MAPVIEWER_IsRunning(self):
		pageData = self.pageData[self.PAGE_MAPVIEWER]

		return pageData.has_key("map_name") and pageData["map_name"] != ""

	def MAPVIEWER_OnUpdate(self):
		page = self.pages[self.PAGE_MAPVIEWER]
		pageData = self.pageData[self.PAGE_MAPVIEWER]

		if self.IsShow() and self.currentPageIndex == self.PAGE_MAPVIEWER:
			page["atlas_tooltip"].Hide()

			if not miniMap.isShowAdminManagerAtlas():
				return

			(mouseX, mouseY) = wndMgr.GetMousePosition()
			(bFind, sName, fPosX, fPosY, dwTextColor) = miniMap.GetAdminManagerAtlasInfo(mouseX, mouseY)

			if FALSE == bFind:
				return

			page["atlas_tooltip"].SetTextColor(dwTextColor)
			page["atlas_tooltip"].SetText("%s (%d, %d)" % (sName, int(fPosX), int(fPosY)))

			(x, y) = page["atlas"].GetGlobalPosition()
			page["atlas_tooltip"].SetTooltipPosition(mouseX - x, mouseY - y)

			page["atlas_tooltip"].Show()
			page["atlas_tooltip"].SetTop()

		else:
			if pageData.has_key("stop_timer") and pageData["stop_timer"] != 0 and app.GetTime() >= pageData["stop_timer"]:
				pageData["stop_timer"] = 0
				pageData["is_paused"] = TRUE
				admin.StopMapViewer()

	def MAPVIEWER_IsAvailableMap(self, index):
		nonAvailList = ["metin2_map_wedding", "metin2_map_deviltower", "metin2_map_skipia_dungeon_boss", "metin2_map_guildwar", "metin2_map_guildflagwar", "metin2_map_oxevent"]

		path = background.GetMapPathByIndex(index)
		splitPath = path.split("/")
		folderName = splitPath[len(splitPath) - 1]

		if folderName in nonAvailList:
			return FALSE

		return TRUE

	def MAPVIEWER_OnSelectScroll(self):
		page = self.pages[self.PAGE_MAPVIEWER]

		pos = page["select_scroll"].GetPos()
		basePos = int(float(page["select_list"].GetItemCount() - page["select_list"].GetViewItemCount()) * pos)
		if basePos != page["select_list"].GetBasePos():
			page["select_list"].SetBasePos(basePos)

	def MAPVIEWER_SelectMap(self):
		page = self.pages[self.PAGE_MAPVIEWER]
		pageData = self.pageData[self.PAGE_MAPVIEWER]

		index = page["select_list"].GetSelectedItem(-1)
		if index == -1:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Wähle erst eine Karte.")
			return

		name, x, y = background.GetMapInfoByIndex(index)
		pageData["map_name"] = name
		pageData["map_x"] = x
		pageData["map_y"] = y
		admin.StartMapViewer(x, y)

	def MAPVIEWER_Stop(self):
		page = self.pages[self.PAGE_MAPVIEWER]
		pageData = self.pageData[self.PAGE_MAPVIEWER]

		if not self.MAPVIEWER_IsRunning():
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Der MapViewer läuft nicht.")
			return

		pageData["map_name"] = ""
		self.MAPVIEWER_RefreshPage()
		admin.StopMapViewer()

	def MAPVIEWER_OnClickOptionButton(self, flag):
		if miniMap.IsAdminManagerAtlasFlagShown(flag):
			miniMap.HideAdminManagerAtlasFlag(flag)
		else:
			miniMap.ShowAdminManagerAtlasFlag(flag)
		self.MAPVIEWER_RefreshOptionButtonText(flag)

	#################################################
	## PAGE: OBSERVER FUNCTIONS
	#################################################

	def OBSERVER_Build(self):
		page = self.pages[self.PAGE_OBSERVER]

		subPage = page["subpage_%d" % self.OBSERVER_NAVI_GENERAL]
		subPage["exp_tooltip"] = uiTaskBar.TaskBar.TextToolTip()
		subPage["exp_tooltip"].Hide()

		subPage = page["subpage_%d" % self.OBSERVER_NAVI_ITEM]
		subPage["item_tooltip"] = uiToolTip.ItemToolTip()
		subPage["item_tooltip"].HideToolTip()

	def OBSERVER_GetSubPageIndex(self):
		pageData = self.pageData[self.PAGE_OBSERVER]

		index = 0
		if admin.IsObserverRunning() or admin.IsObserverStopForced():
			if pageData.has_key("sub_page_index"):
				index = pageData["sub_page_index"]
		else:
			index = -1

		return index

	def OBSERVER_SetSubPageIndex(self, index):
		pageData = self.pageData[self.PAGE_OBSERVER]

		pageData["sub_page_index"] = index
		self.OBSERVER_Refresh()

	def OBSERVER_GetName(self):
		pageData = self.pageData[self.PAGE_OBSERVER]

		return pageData["observer_name"]

	def OBSERVER_OnStart(self):
		self.OBSERVER_OnClickNaviButton(self.OBSERVER_NAVI_GENERAL)
		self.OBSERVER_RefreshPage()
		self.OnClickNaviButton(self.PAGE_OBSERVER)

	def OBSERVER_RefreshPage(self):
		page = self.pages[self.PAGE_OBSERVER]

		self.OBSERVER_Refresh()

		if self.OBSERVER_GetSubPageIndex() != -1:
			self.OBSERVER_RefreshSubPage(self.OBSERVER_NAVI_GENERAL)
			self.OBSERVER_RefreshSubPage(self.OBSERVER_NAVI_ITEM)
			self.OBSERVER_RefreshSubPage(self.OBSERVER_NAVI_WHISPER)

		self.pageNeedRefresh[self.PAGE_OBSERVER] = FALSE

	def OBSERVER_Refresh(self):
		page = self.pages[self.PAGE_OBSERVER]

		subPageIndex = self.OBSERVER_GetSubPageIndex()
		if subPageIndex == -1:
			page["running_wnd"].Hide()
			page["stopped_wnd"].Show()
		else:
			page["stopped_edit"].KillFocus()
			page["stopped_edit"].SetText("")
			page["stopped_wnd"].Hide()
			page["running_wnd"].Show()

			for i in xrange(self.OBSERVER_NAVI_MAX_NUM):
				wnd = page["subpage_%d" % i]["wnd"]
				if i == subPageIndex:
					wnd.Show()
				else:
					wnd.Hide()

	def OBSERVER_RefreshSubPage(self, subPageIndex):
		if subPageIndex == self.OBSERVER_NAVI_GENERAL:
			self.OBSERVER_RefreshSubPageGeneral()
		elif subPageIndex == self.OBSERVER_NAVI_ITEM:
			self.OBSERVER_RefreshSubPageItem()
		elif subPageIndex == self.OBSERVER_NAVI_WHISPER:
			self.OBSERVER_RefreshSubPageWhisper()

	def OBSERVER_RefreshSubPageGeneral(self):
		page = self.pages[self.PAGE_OBSERVER]
		pageData = self.pageData[self.PAGE_OBSERVER]
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_GENERAL]

		pid = admin.GetObserverPID()
		try:
			(tmp_pid, name, map_index, channel, empire) = admin.GetOnlinePlayerByPID(pid)
		except:
			name = "[unkown]"
			map_index = 0
			channel = 0
			empire = 0

		pageData["observer_name"] = name

		faceImageName = self.OBSERVER_FACE_IMAGE_DICT[admin.GetObserverRaceNum()]
		subPage["face"].LoadImage(faceImageName)

		subPage["pid"].SetText(localeInfo.ADMIN_MANAGER_OBSERVER_GENERAL_PID % pid)
		subPage["name"].SetText(localeInfo.ADMIN_MANAGER_OBSERVER_GENERAL_NAME % name)
		if empire != 0:
			subPage["empire"].LoadImage(self.OBSERVER_EMPIRE_IMAGE_DICT[empire])
			subPage["empire"].Show()
		else:
			subPage["empire"].Hide()
		subPage["empire"].SetScale(0.5, 0.5)
		subPage["channel"].SetText(localeInfo.ADMIN_MANAGER_OBSERVER_GENERAL_CHANNEL % channel)
		subPage["map_info"].SetText(localeInfo.ADMIN_MANAGER_OBSERVER_GENERAL_MAP_INFO % (admin.GetObserverMapName(), map_index))

		self.OBSERVER_OnPointChange()
		self.OBSERVER_RefreshSkill()

	def OBSERVER_RefreshSubPageItem(self):
		self.OBSERVER_OnClickInventoryPageButton(0) # refresh inventory
		self.OBSERVER_RefreshEquipment() # refresh equipment

	def OBSERVER_RefreshSubPageWhisper(self):
		self.OBSERVER_RefreshWhisperNameList(FALSE) # refresh whisper name list
		self.OBSERVER_RefreshWhisperText(TRUE) # reset whisper text

	def OBSERVER_OnClosePage(self):
		page = self.pages[self.PAGE_OBSERVER]

		page["stopped_edit"].KillFocus()

	def OBSERVER_OnOpenPage(self):
		page = self.pages[self.PAGE_OBSERVER]

		if self.OBSERVER_GetSubPageIndex() == -1:
			page["stopped_edit"].SetFocus()

	def OBSERVER_StartObservation(self, name = ""):
		page = self.pages[self.PAGE_OBSERVER]

		if name == "":
			name = page["stopped_edit"].GetText()
			if name == "":
				chat.AppendChat(chat.CHAT_TYPE_INFO, "Es muss ein Name angegeben sein.")
				return

		admin.StartObserver(name)

	def OBSERVER_StopObservation(self):
		admin.StopObserver()
		self.OBSERVER_Refresh()

	def __OBSERVER_GetRealSkillSlot(self, slotIndex, skillGrade):
		return slotIndex + min(skill.SKILL_GRADE_COUNT-1, skillGrade) * skill.SKILL_GRADE_STEP_COUNT

	def OBSERVER_RefreshSkill(self):
		page = self.pages[self.PAGE_OBSERVER]
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_GENERAL]

		job = chr.RaceToJob(admin.GetObserverRaceNum())
		skillGroup = admin.GetObserverSkillGroup()
		subPage["skillgroup"].SetText(localeInfo.ADMIN_MANAGER_OBSERVER_GENERAL_SKILLGROUP % localeInfo.GetSkillGroupName(job, skillGroup))

		if skillGroup == 0:
			subPage["skill_wnd"].Hide()
		else:
			skillVnumList = playerSettingModule.SKILL_INDEX_DICT[job][skillGroup]

			for i in xrange(8):
				skillVnum = skillVnumList[i]
				skillLevel = admin.GetObserverSkillLevel(skillVnum)
				skillGrade = admin.GetObserverSkillMasterType(skillVnum)
				skillCoolTime = admin.GetObserverSkillCoolTime(skillVnum)
				skillElapsedCoolTime = admin.GetObserverESkillCoolTime(skillVnum)

				if skillGrade >= 1:
					skillLevel -= 20 - 1
					if skillGrade >= 2:
						skillLevel -= 10

				for j in xrange(skill.SKILL_GRADE_COUNT):
					slotIndex = self.__OBSERVER_GetRealSkillSlot(i + 1, j)

					subPage["skill"].ClearSlot(slotIndex)

					if skillVnum != 0:
						subPage["skill"].SetSkillSlotNew(slotIndex, skillVnum, j, skillLevel)
						subPage["skill"].SetCoverButton(slotIndex)

						if ((skillGrade == skill.SKILL_GRADE_COUNT) and j == (skill.SKILL_GRADE_COUNT - 1)) or (skillGrade == j):
							subPage["skill"].SetSlotCountNew(slotIndex, skillGrade, skillLevel)
							if skillCoolTime != 0 and skillElapsedCoolTime < skillCoolTime:
								subPage["skill"].SetSlotCoolTime(slotIndex, float(skillCoolTime) / 1000.0, float(skillElapsedCoolTime) / 1000.0)
						else:
							subPage["skill"].SetSlotCount(slotIndex, 0)
							subPage["skill"].DisableCoverButton(slotIndex)

			subPage["skill_wnd"].Show()

	def OBSERVER_OnOverInItemSlot(self, slotPos):
		page = self.pages[self.PAGE_OBSERVER]
		pageData = self.pageData[self.PAGE_OBSERVER]
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_ITEM]

		if slotPos < player.INVENTORY_PAGE_SIZE:
			slotPos += pageData["inventory_page"] * player.INVENTORY_PAGE_SIZE
		(itemID, itemVnum, itemCount, itemSocket, itemAttr) = admin.GetObserverItem(slotPos)

		subPage["item_tooltip"].ClearToolTip()
		subPage["item_tooltip"].AddItemData(itemVnum, itemSocket, itemAttr)
		subPage["item_tooltip"].AppendSpace(5)
		subPage["item_tooltip"].AppendTextLine(localeInfo.ADMIN_MANAGER_OBSERVER_ITEM_TOOLTIP_ID % itemID)
		subPage["item_tooltip"].ShowToolTip()

	def OBSERVER_OnOverOutItemSlot(self):
		page = self.pages[self.PAGE_OBSERVER]
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_ITEM]

		subPage["item_tooltip"].HideToolTip()

	def OBSERVER_OnClickInventoryPageButton(self, inventoryPageIndex):
		page = self.pages[self.PAGE_OBSERVER]
		pageData = self.pageData[self.PAGE_OBSERVER]
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_ITEM]

		pageData["inventory_page"] = inventoryPageIndex

		for i in xrange(player.INVENTORY_PAGE_COUNT):
			btn = subPage["inventory_page_%d" % (i + 1)]
			if i == inventoryPageIndex:
				btn.Down()
			else:
				btn.SetUp()

		self.OBSERVER_RefreshInventory()

	def OBSERVER_RefreshInventory(self, pageIndex = -1):
		page = self.pages[self.PAGE_OBSERVER]
		pageData = self.pageData[self.PAGE_OBSERVER]
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_ITEM]

		if pageIndex != -1 and pageIndex != pageData["inventory_page"]:
			return

		for i in xrange(player.INVENTORY_PAGE_SIZE):
			(itemID, itemVnum, itemCount, itemSocket, itemAttr) = admin.GetObserverItem(pageData["inventory_page"] * player.INVENTORY_PAGE_SIZE + i)
			if itemCount <= 1:
				itemCount = 0
			subPage["inventory"].SetItemSlot(i, itemVnum, itemCount)

			
	def OBSERVER_RefreshEquipment(self):
		page = self.pages[self.PAGE_OBSERVER]
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_ITEM]

		for i in xrange(player.EQUIPMENT_PAGE_COUNT):
			slotNumber = player.EQUIPMENT_SLOT_START + i
			(itemID, itemVnum, itemCount, itemSocket, itemAttr) = admin.GetObserverItem(slotNumber)
			if itemCount <= 1:
				itemCount = 0
			subPage["equipment"].SetItemSlot(slotNumber, itemVnum, itemCount)

	def OBSERVER_RefreshWhisperNameList(self, reselect = TRUE):
		page = self.pages[self.PAGE_OBSERVER]
		pageData = self.pageData[self.PAGE_OBSERVER]
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_WHISPER]

		selectedPID = 0
		if reselect and pageData.has_key("selected_whisper_pid"):
			selectedPID = pageData["selected_whisper_pid"]

		subPage["name_list"].ClearItem()
		for i in xrange(admin.GetObserverWhisperDlgCount()):
			pid = admin.GetObserverWhisperPIDByIdx(i)
			subPage["name_list"].InsertItem(pid, admin.GetObserverWhisperName(pid))
			if selectedPID == pid:
				subPage["name_list"].SelectItem(i)

		if subPage["name_list"].GetItemCount() <= subPage["name_list"].GetViewItemCount():
			subPage["name_scroll"].Hide()
		else:
			subPage["name_scroll"].SetMiddleBarSize(float(subPage["name_list"].GetViewItemCount()) / float(subPage["name_list"].GetItemCount()))
			subPage["name_scroll"].Show()

	def OBSERVER_RefreshWhisperText(self, reset = FALSE, resetScroll = FALSE):
		page = self.pages[self.PAGE_OBSERVER]
		pageData = self.pageData[self.PAGE_OBSERVER]
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_WHISPER]

		pid = 0
		if pageData.has_key("selected_whisper_pid"):
			pid = pageData["selected_whisper_pid"]

		oldLineCount = subPage["text"].GetLineCount()

		subPage["text"].Clear()
		subPage["text_scroll"].Hide()

		if pid == 0:
			return

		if reset:
			pageData["selected_whisper_pid"] = 0

		else:
			(tmp_pid, name, map_index, channel, empire) = admin.GetOnlinePlayerByPID(admin.GetObserverPID())
			senderNames = {
				admin.GetObserverPID() : name,
				pid : admin.GetObserverWhisperName(pid),
			}

			text = ""

			for i in xrange(admin.GetObserverWhisperMsgCount(pid)):
				senderPID, sentTime, msg = admin.GetObserverWhisperMsg(pid, i)
				senderName = senderNames[senderPID]

				text += senderName + " : " + msg + subPage["text"].RETURN_STRING

			if len(text) > 0:
				text = text[:-len("[ENTER]")]

			oldBasePos = subPage["text"].GetBasePos()

			subPage["text"].SetText(text)

			if subPage["text"].GetLineCount() > subPage["text"].GetViewLineCount():
				subPage["text_scroll"].SetMiddleBarSize(float(subPage["text"].GetViewLineCount()) / float(subPage["text"].GetLineCount()))

				if resetScroll == TRUE:
					subPage["text_scroll"].SetPos(1.0)
				else:
					newBasePos = max(0, oldBasePos + (subPage["text"].GetLineCount() - oldLineCount))
					subPage["text_scroll"].SetPos(float(newBasePos) / float(subPage["text"].GetLineCount() - subPage["text"].GetViewLineCount()))
					subPage["text"].SetBasePos(newBasePos)

				subPage["text_scroll"].Show()

	def OBSERVER_OnSelectWhisperName(self, pid, name):
		pageData = self.pageData[self.PAGE_OBSERVER]

		pageData["selected_whisper_pid"] = pid
		self.OBSERVER_RefreshWhisperText(FALSE, TRUE)

	def OBSERVER_OnWhisperNameScroll(self):
		page = self.pages[self.PAGE_OBSERVER]
		pageData = self.pageData[self.PAGE_OBSERVER]
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_WHISPER]

	def OBSERVER_OnWhisperTextScroll(self):
		page = self.pages[self.PAGE_OBSERVER]
		pageData = self.pageData[self.PAGE_OBSERVER]
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_WHISPER]

		pos = subPage["text_scroll"].GetPos()
		basePos = int(float(subPage["text"].GetLineCount() - subPage["text"].GetViewLineCount()) * pos)
		if basePos != subPage["text"].GetBasePos():
			subPage["text"].SetBasePos(basePos)

	def OBSERVER_OnClickNaviButton(self, index):
		page = self.pages[self.PAGE_OBSERVER]

		# set other buttons up
		for i in xrange(self.OBSERVER_NAVI_MAX_NUM):
			btn = page["navi_buttons"][i]
			if i == index:
				btn.Down()
			else:
				btn.SetUp()

		# set sub page
		self.OBSERVER_SetSubPageIndex(index)

	def OBSERVER_OnPointChange(self):
		page = self.pages[self.PAGE_OBSERVER]

		# GENERAL subpage
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_GENERAL]

		subPage["level"].SetText(localeInfo.ADMIN_MANAGER_OBSERVER_GENERAL_LEVEL % admin.GetObserverPoint(player.LEVEL))

		curVal = admin.GetObserverPoint(player.HP)
		maxVal = admin.GetObserverPoint(player.MAX_HP)
		subPage["hpbar"].SetPercentage(min(curVal, maxVal), maxVal)
		subPage["hptext"].SetText(localeInfo.ADMIN_MANAGER_OBSERVER_GENERAL_HP % (curVal, maxVal))

		curVal = admin.GetObserverPoint(player.SP)
		maxVal = admin.GetObserverPoint(player.MAX_SP)
		subPage["spbar"].SetPercentage(min(curVal, maxVal), maxVal)
		subPage["sptext"].SetText(localeInfo.ADMIN_MANAGER_OBSERVER_GENERAL_SP % (curVal, maxVal))

		curVal = admin.GetObserverPoint(player.EXP)
		maxVal = admin.GetObserverPoint(player.NEXT_EXP)
		for i in xrange(len(subPage["exp_points"])):
			subPage["exp_points"][i].Hide()
		expPerc = float(curVal) / float(maxVal)
		i = 0
		while expPerc >= 1.0 / float(len(subPage["exp_points"])) and i < len(subPage["exp_points"]):
			subPage["exp_points"][i].SetRenderingRect(0.0, 0.0, 0.0, 0.0)
			subPage["exp_points"][i].Show()
			expPerc -= 1.0 / float(len(subPage["exp_points"]))
			i += 1
		if i < len(subPage["exp_points"]):
			subPage["exp_points"][i].SetRenderingRect(0.0, expPerc / (1.0 / float(len(subPage["exp_points"]))) - 1.0, 0.0, 0.0)
			subPage["exp_points"][i].Show()
		subPage["exp_tooltip"].SetText("%s : %.2f%%" % (localeInfo.TASKBAR_EXP, float(curVal) / max(1, float(maxVal)) * 100))

		curVal = admin.GetObserverPoint(player.ELK)
		subPage["gold"].SetText(localeInfo.ADMIN_MANAGER_OBSERVER_GENERAL_GOLD % localeInfo.NumberToString(curVal))

		# ITEM subpage
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_ITEM]

		curVal = admin.GetObserverPoint(player.ELK)
		subPage["money"].SetText(localeInfo.NumberToMoneyString(curVal))

	def OBSERVER_OnWhisperUpdate(self, pid):
		page = self.pages[self.PAGE_OBSERVER]
		pageData = self.pageData[self.PAGE_OBSERVER]
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_WHISPER]

		current_pid = 0
		if pageData.has_key("selected_whisper_pid"):
			current_pid = pageData["selected_whisper_pid"]

		if pid == current_pid:
			self.OBSERVER_RefreshWhisperText()

		else:
			if not subPage["name_list"].HasItem(pid):
				self.OBSERVER_RefreshWhisperNameList()

	def OBSERVER_OnUpdate(self):
		page = self.pages[self.PAGE_OBSERVER]
		pageData = self.pageData[self.PAGE_OBSERVER]
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_GENERAL]
		subPageIndex = self.OBSERVER_GetSubPageIndex()

		if self.currentPageIndex == self.PAGE_OBSERVER:
			if subPageIndex == self.OBSERVER_NAVI_GENERAL and subPage["exp_point_bg"].IsInPosition():
				subPage["exp_tooltip"].Show()
			else:
				subPage["exp_tooltip"].Hide()

			if admin.IsObserverStopForced():
				if not pageData.has_key("last_retry"):
					pageData["last_retry"] = app.GetTime()
				if pageData["last_retry"] + 10 < app.GetTime():
					pageData["last_retry"] = app.GetTime()
					admin.StartObserver(self.OBSERVER_GetName(), FALSE)

	def OBSERVER_OnAfterRender(self):
		page = self.pages[self.PAGE_OBSERVER]
		subPageIndex = self.OBSERVER_GetSubPageIndex()

		if admin.IsObserverStopForced():
			subPageWnd = page["subpage_%d" % subPageIndex]["wnd"]

			x, y = subPageWnd.GetGlobalPosition()
			w = subPageWnd.GetWidth()
			h = subPageWnd.GetHeight()

			grp.SetColor(self.DISABLE_COLOR)
			grp.RenderBar(x - 5, y - 5, w + 5 * 2, h + 5 * 2)

	#################################################
	## NAVIGATION FUNCTIONS
	#################################################

	def OnClickNaviButton(self, index):
		# set other buttons up
		for i in xrange(self.PAGE_MAX_NUM):
			btn = self.naviBtnList[i]
			if i == index:
				btn.Down()
			else:
				btn.SetUp()

		# load page
		self.LoadPage(index)

	#################################################
	## EVENT FUNCTIONS
	#################################################

	def OnPlayerOnline(self, pid):
		self.GENERAL_AddOnlinePlayer(pid)

	def OnPlayerOffline(self, pid):
		self.GENERAL_EraseOnlinePlayer(pid)
