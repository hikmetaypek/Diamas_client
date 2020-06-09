import uiScriptLocale
import player
import grp

BOARD_WIDTH = 500
BOARD_HEIGHT = 400

PAGE_X_DIST = 20
PAGE_TOP_DIST = 35
PAGE_BOT_DIST = 50

NAVI_BTN_WIDTH = 88
NAVI_BTN_HEIGHT = 21
NAVI_BTN_COUNT = 3
NAVI_BOT_DIST = 4

EQUIPMENT_START_INDEX = player.EQUIPMENT_SLOT_START

window = {
	"name" : "AdminManagerWindow",

	"x" : (SCREEN_WIDTH - BOARD_WIDTH) / 2,
	"y" : (SCREEN_HEIGHT - BOARD_HEIGHT) / 2,

	"style" : ("movable", "float",),

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,

			"children" :
			(
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : BOARD_WIDTH - 15,
					"color" : "yellow",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":0, "y":3, "text":uiScriptLocale.ADMIN_MANAGER_TITLE, "horizontal_align":"center", "text_horizontal_align":"center" },
					),
				},

				## Page1 : General
				{
					"name" : "page_general",
					"type" : "thinboard",

					"x" : PAGE_X_DIST,
					"y" : PAGE_TOP_DIST,

					"width" : BOARD_WIDTH - PAGE_X_DIST * 2,
					"height" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST),

					"children" :
					(
						{
							"name" : "general_online_player_table",
							"type" : "table",

							"x" : 10,
							"y" : 10,

							"width" : 300,
							"height" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST) - 20 - 30,

							"col_size" : [15, 35, 25, 15, 10],
							"header" : [uiScriptLocale.ADMIN_MANAGER_GENERAL_TABLE_PID,\
										uiScriptLocale.ADMIN_MANAGER_GENERAL_TABLE_NAME,\
										uiScriptLocale.ADMIN_MANAGER_GENERAL_TABLE_MAP_INDEX,\
										uiScriptLocale.ADMIN_MANAGER_GENERAL_TABLE_CHANNEL,\
										uiScriptLocale.ADMIN_MANAGER_GENERAL_TABLE_EMPIRE],
							"content" : (
								[1, "TestName1", 91, 1, 3],
								[2, "TestName2", 62, 3, 2],
								[3, "TestName3", 1, 4, 2],
								[4, "TestName4", 103, 4, 3],
								[5, "TestName5", 920000, 2, 1],
								[1, "TestName6", 91, 1, 3],
								[2, "TestName7", 62, 3, 2],
								[3, "TestName8", 1, 4, 2],
								[4, "TestName9", 103, 4, 3],
								[5, "TestName10", 920000, 2, 1],
								[1, "TestName11", 91, 1, 3],
								[2, "TestName12", 62, 3, 2],
								[3, "TestName13", 1, 4, 2],
								[4, "TestName14", 103, 4, 3],
								[5, "TestName15", 920000, 2, 1],
								[1, "TestName16", 91, 1, 3],
								[2, "TestName17", 62, 3, 2],
								[3, "TestName18", 1, 4, 2],
								[4, "TestName19", 103, 4, 3],
								[5, "TestName20", 920000, 2, 1],
							),
						},
						{
							"name" : "general_online_player_scrollbar",
							"type" : "scrollbar",

							"x" : 10 + 300 + 5,
							"y" : 10,

							"size" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST) - 20 - 30,
						},
						{
							"name" : "general_online_player_dividing_line",
							"type" : "line",

							"x" : 10 + 300 + 5 + 17 - 1,
							"y" : 10,

							"width" : 0,
							"height" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST) - 20 - 30,

							"color" : grp.GenerateColor(1.0, 1.0, 1.0, 0.8),
						},
						{
							"name" : "general_online_player_search_text",
							"type" : "text",

							"x" : 15,
							"y" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST) - 20 - 15,

							"text" : uiScriptLocale.ADMIN_MANAGER_GENERAL_SEARCH_PLAYER,
						},
						{
							"name" : "general_online_player_search_box",
							"type" : "slotbar",

							"x" : 15 + 75,
							"y" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST) - 20 - 16,

							"width" : 180,
							"height" : 18,

							"children" :
							(
								{
									"name" : "general_online_player_search_edit",
									"type" : "editline",

									"x" : 3,
									"y" : 3,

									"width" : 170,
									"height" : 18,

									"input_limit" : 24,
								},
							),
						},
						{
							"name" : "general_online_player_search_button",
							"type" : "button",

							"x" : 15 + 75 + 180 + 5,
							"y" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST) - 20 - 16,

							"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",

							"text" : uiScriptLocale.ADMIN_MANAGER_GENERAL_SEARCH_PLAYER_BUTTON,
						},
						{
							"name" : "general_main_information_window",

							"x" : 328,
							"y" : 15,

							"width" : BOARD_WIDTH - PAGE_X_DIST * 2 - 332,
							"height" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST) - 10 * 2,

							"children" :
							(
								{
									"name" : "general_current_user_count",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"horizontal_align" : "center",
									"text_horizontal_align" : "center",
								},
							),
						},
					),
				},

				## Page2 : MapViewer
				{
					"name" : "page_mapviewer",
					"type" : "thinboard",

					"x" : PAGE_X_DIST,
					"y" : PAGE_TOP_DIST,

					"width" : BOARD_WIDTH - PAGE_X_DIST * 2,
					"height" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST),

					"children" :
					(
						{
							"name" : "mapviewer_atlas",

							"x" : 10,
							"y" : 10,

							"width" : 300,
							"height" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST) - 20,
						},
						{
							"name" : "mapviewer_no_map_selected",

							"x" : 10,
							"y" : 10,

							"width" : 300,
							"height" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST) - 20,

							"children" :
							(
								{
									"name" : "mapviewer_no_map_line1",
									"type" : "line",

									"x" : 0,
									"y" : 0,

									"width" : 300,
									"height" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST) - 20,

									"color" : grp.GenerateColor(1.0, 1.0, 1.0, 0.8),
								},
								{
									"name" : "mapviewer_no_map_line1",
									"type" : "line",

									"x" : 300,
									"y" : 0,

									"width" : -300,
									"height" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST) - 20,

									"color" : grp.GenerateColor(1.0, 1.0, 1.0, 0.8),
								},
							),
						},
						{
							"name" : "mapviewer_dividing_line1",
							"type" : "line",

							"x" : 10 + 300 + 5,
							"y" : 10,

							"width" : 0,
							"height" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST) - 20,

							"color" : grp.GenerateColor(1.0, 1.0, 1.0, 0.8),
						},
						{
							"name" : "mapviewer_right_side",

							"x" : 10 + 300 + 10,
							"y" : 10,

							"width" : BOARD_WIDTH - PAGE_X_DIST * 2 - (10 + 300 + 10) - 10,
							"height" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST) - 20,

							"children" :
							(
								{
									"name" : "mapviewer_select_title",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"horizontal_align" : "center",
									"text_horizontal_align" : "center",

									"text" : uiScriptLocale.ADMIN_MANAGER_MAPVIEWER_SELECT_TITLE,
								},
								{
									"name" : "mapviewer_select_list",
									"type" : "listbox",

									"x" : 0,
									"y" : 20,

									"width" : BOARD_WIDTH - PAGE_X_DIST * 2 - (10 + 300 + 10) - 10 - 17,
									"height" : 17 * 5,
								},
								{
									"name" : "mapviewer_select_scrollbar",
									"type" : "scrollbar",

									"x" : BOARD_WIDTH - PAGE_X_DIST * 2 - (10 + 300 + 10) - 10 - 17,
									"y" : 20,

									"size" : 17 * 5 + 5 + 21,
								},
								{
									"name" : "mapviewer_select_button",
									"type" : "button",

									"x" : 0,
									"y" : 20 + 17 * 5 + 5,

									"horizontal_align" : "center",

									"default_image" : "d:/ymir work/ui/public/Large_Button_01.sub",
									"over_image" : "d:/ymir work/ui/public/Large_Button_02.sub",
									"down_image" : "d:/ymir work/ui/public/Large_Button_03.sub",

									"text" : uiScriptLocale.ADMIN_MANAGER_MAPVIEWER_SELECT_BUTTON,
								},
								{
									"name" : "mapviewer_dividing_line2",
									"type" : "line",

									"x" : 0,
									"y" : 20 + 17 * 5 + 5 + 27,

									"width" : BOARD_WIDTH - PAGE_X_DIST * 2 - (10 + 300 + 10) - 10 - 10 * 2,
									"height" : 0,

									"horizontal_align" : "center",

									"color" : grp.GenerateColor(1.0, 1.0, 1.0, 0.8),
								},
								{
									"name" : "mapviewer_option_player",
									"type" : "button",

									"x" : 0,
									"y" : 20 + 17 * 5 + 5 + 34 + (21 + 5) * 0,

									"default_image" : "d:/ymir work/ui/public/Large_Button_01.sub",
									"over_image" : "d:/ymir work/ui/public/Large_Button_02.sub",
									"down_image" : "d:/ymir work/ui/public/Large_Button_03.sub",

									"horizontal_align" : "center",
								},
								{
									"name" : "mapviewer_option_mob",
									"type" : "button",

									"x" : 0,
									"y" : 20 + 17 * 5 + 5 + 34 + (21 + 5) * 1,

									"default_image" : "d:/ymir work/ui/public/Large_Button_01.sub",
									"over_image" : "d:/ymir work/ui/public/Large_Button_02.sub",
									"down_image" : "d:/ymir work/ui/public/Large_Button_03.sub",

									"horizontal_align" : "center",
								},
								{
									"name" : "mapviewer_option_stone",
									"type" : "button",

									"x" : 0,
									"y" : 20 + 17 * 5 + 5 + 34 + (21 + 5) * 2,

									"default_image" : "d:/ymir work/ui/public/Large_Button_01.sub",
									"over_image" : "d:/ymir work/ui/public/Large_Button_02.sub",
									"down_image" : "d:/ymir work/ui/public/Large_Button_03.sub",

									"horizontal_align" : "center",
								},
								{
									"name" : "mapviewer_option_npc",
									"type" : "button",

									"x" : 0,
									"y" : 20 + 17 * 5 + 5 + 34 + (21 + 5) * 3,

									"default_image" : "d:/ymir work/ui/public/Large_Button_01.sub",
									"over_image" : "d:/ymir work/ui/public/Large_Button_02.sub",
									"down_image" : "d:/ymir work/ui/public/Large_Button_03.sub",

									"horizontal_align" : "center",
								},
								{
									"name" : "mapviewer_stop_button",
									"type" : "button",

									"x" : 0,
									"y" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST) - 20 - 21,

									"default_image" : "d:/ymir work/ui/public/Large_Button_01.sub",
									"over_image" : "d:/ymir work/ui/public/Large_Button_02.sub",
									"down_image" : "d:/ymir work/ui/public/Large_Button_03.sub",

									"horizontal_align" : "center",

									"text" : uiScriptLocale.ADMIN_MANAGER_MAPVIEWER_STOP_BUTTON,
								},
							),
						},
					),
				},

				## Page3 : Observer
				{
					"name" : "page_observer",
					"type" : "thinboard",

					"x" : PAGE_X_DIST,
					"y" : PAGE_TOP_DIST,

					"width" : BOARD_WIDTH - PAGE_X_DIST * 2,
					"height" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST),

					"children" :
					(
						{
							"name" : "observer_stopped_wnd",

							"x" : 0,
							"y" : 0,

							"width" : BOARD_WIDTH - PAGE_X_DIST * 2,
							"height" : 20 + 18 + 5 + 25,

							"vertical_align" : "center",

							"children" :
							(
								{
									"name" : "observer_stopped_title",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"horizontal_align" : "center",
									"text_horizontal_align" : "center",

									"text" : uiScriptLocale.ADMIN_MANAGER_OBSERVER_STOPPED_TITLE,
								},
								{
									"name" : "observer_stopped_name_box",
									"type" : "slotbar",

									"x" : 0,
									"y" : 20,

									"width" : 180,
									"height" : 18,

									"horizontal_align" : "center",

									"children" :
									(
										{
											"name" : "observer_stopped_name_edit",
											"type" : "editline",

											"x" : 3,
											"y" : 3,

											"width" : 170,
											"height" : 18,

											"input_limit" : 24,
										},
									),
								},
								{
									"name" : "observer_stopped_button",
									"type" : "button",

									"x" : 0,
									"y" : 20 + 18 + 5,

									"horizontal_align" : "center",

									"default_image" : "d:/ymir work/ui/public/XLarge_Button_01.sub",
									"over_image" : "d:/ymir work/ui/public/XLarge_Button_02.sub",
									"down_image" : "d:/ymir work/ui/public/XLarge_Button_03.sub",

									"text" : uiScriptLocale.ADMIN_MANAGER_OBSERVER_STOPPED_BUTTON,
								},
							),
						},
						# running window
						{
							"name" : "observer_running_wnd",

							"x" : 0,
							"y" : 0,

							"width" : BOARD_WIDTH - PAGE_X_DIST * 2,
							"height" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST),

							"children" :
							(
								# buttons
								{
									"name" : "observer_button_wnd",

									"x": 10,
									"y" : 10,

									"width" : 88,
									"height" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST) - 10 * 2,

									"children" :
									(
										{
											"name" : "observer_navi_title",
											"type" : "text",

											"x" : 0,
											"y" : 0,

											"horizontal_align" : "center",
											"text_horizontal_align" : "center",

											"text" : uiScriptLocale.ADMIN_MANAGER_OBSERVER_NAVI_TITLE,
										},
										{
											"name" : "observer_navi_button_1",
											"type" : "radio_button",

											"x" : 0,
											"y" : 20 + (21 + 5) * 0,

											"default_image" : "d:/ymir work/ui/public/Large_Button_01.sub",
											"over_image" : "d:/ymir work/ui/public/Large_Button_02.sub",
											"down_image" : "d:/ymir work/ui/public/Large_Button_03.sub",

											"text" : uiScriptLocale.ADMIN_MANAGER_OBSERVER_NAVI_BTN_1,
										},
										{
											"name" : "observer_navi_button_2",
											"type" : "radio_button",

											"x" : 0,
											"y" : 20 + (21 + 5) * 1,

											"default_image" : "d:/ymir work/ui/public/Large_Button_01.sub",
											"over_image" : "d:/ymir work/ui/public/Large_Button_02.sub",
											"down_image" : "d:/ymir work/ui/public/Large_Button_03.sub",

											"text" : uiScriptLocale.ADMIN_MANAGER_OBSERVER_NAVI_BTN_2,
										},
										{
											"name" : "observer_navi_button_3",
											"type" : "radio_button",

											"x" : 0,
											"y" : 20 + (21 + 5) * 2,

											"default_image" : "d:/ymir work/ui/public/Large_Button_01.sub",
											"over_image" : "d:/ymir work/ui/public/Large_Button_02.sub",
											"down_image" : "d:/ymir work/ui/public/Large_Button_03.sub",

											"text" : uiScriptLocale.ADMIN_MANAGER_OBSERVER_NAVI_BTN_3,
										},
										{
											"name" : "observer_stop_button",
											"type" : "button",

											"x" : 0,
											"y" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST) - 10 * 2 - 21,

											"default_image" : "d:/ymir work/ui/public/Large_Button_01.sub",
											"over_image" : "d:/ymir work/ui/public/Large_Button_02.sub",
											"down_image" : "d:/ymir work/ui/public/Large_Button_03.sub",

											"text" : uiScriptLocale.ADMIN_MANAGER_OBSERVER_STOP_BTN,
										},
									),
								},
								{
									"name" : "observer_navi_line",
									"type" : "line",

									"x" : 10 + 88 + 6,
									"y" : 10,

									"width" : 0,
									"height" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST) - 10 * 2,

									"color" : grp.GenerateColor(1.0, 1.0, 1.0, 0.8),
								},
								{
									"name" : "observer_subpage_general",

									"x" : 10 + 88 + 13,
									"y" : 10,

									"width" : BOARD_WIDTH - PAGE_X_DIST * 2 - (10 + 88 + 13) - 10,
									"height" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST) - 10 * 2,
									
									"children" :
									(
										{
											"name" : "observer_general_face",
											"type" : "image",

											"x" : 4,
											"y" : 4,
										},
										{
											"name" : "observer_general_face_slot",
											"type" : "image",

											"x" : 0,
											"y" : 0,

											"image" : "d:/ymir work/ui/game/windows/box_face.sub",
										},
										{
											"name" : "observer_general_pid",
											"type" : "text",

											"x" : 60,
											"y" : 0,
										},
										{
											"name" : "observer_general_name",
											"type" : "text",

											"x" : 60,
											"y" : 17,
										},
										{
											"name" : "observer_general_level",
											"type" : "text",

											"x" : 60,
											"y" : 34,
										},
										{
											"name" : "observer_general_hpgauge_bg",
											"type" : "image",

											"x" : 0,
											"y" : 55,

											"image" : "d:/ymir work/ui/pattern/gauge_bg.tga",

											"children" :
											(
												{
													"name" : "observer_general_hpgauge",
													"type" : "ani_image",

													"x" : 4,
													"y" : 0,

													"delay" : 6,

													"images" :
													(
														"d:/ymir work/ui/pattern/HPGauge/01.tga",
														"d:/ymir work/ui/pattern/HPGauge/02.tga",
														"d:/ymir work/ui/pattern/HPGauge/03.tga",
														"d:/ymir work/ui/pattern/HPGauge/04.tga",
														"d:/ymir work/ui/pattern/HPGauge/05.tga",
														"d:/ymir work/ui/pattern/HPGauge/06.tga",
														"d:/ymir work/ui/pattern/HPGauge/07.tga",
													),
												},
												{
													"name" : "observer_general_hptext",
													"type" : "text",

													"x" : 0,
													"y" : 0,

													"all_align" : TRUE,
													"outline" : TRUE,
												},
											),
										},
										{
											"name" : "observer_general_spgauge_bg",
											"type" : "image",

											"x" : 0,
											"y" : 67,

											"image" : "d:/ymir work/ui/pattern/gauge_bg.tga",

											"children" :
											(
												{
													"name" : "observer_general_spgauge",
													"type" : "ani_image",

													"x" : 4,
													"y" : 0,

													"delay" : 6,

													"images" :
													(
														"d:/ymir work/ui/pattern/SPGauge/01.tga",
														"d:/ymir work/ui/pattern/SPGauge/02.tga",
														"d:/ymir work/ui/pattern/SPGauge/03.tga",
														"d:/ymir work/ui/pattern/SPGauge/04.tga",
														"d:/ymir work/ui/pattern/SPGauge/05.tga",
														"d:/ymir work/ui/pattern/SPGauge/06.tga",
														"d:/ymir work/ui/pattern/SPGauge/07.tga",
													),
												},
												{
													"name" : "observer_general_sptext",
													"type" : "text",

													"x" : 0,
													"y" : 0,

													"all_align" : TRUE,
													"outline" : TRUE,
												},
											),
										},
										{
											"name" : "observer_general_exp_bg",
											"type" : "image",

											"x" : 0,
											"y" : 83,

											"image" : "d:/ymir work/ui/pattern/experience.tga",

											"children" :
											(
												{
													"name" : "observer_general_exp_1",
													"type" : "expanded_image",

													"x" : 3,
													"y" : 3,

													"image" : "d:/ymir work/ui/game/taskbar/exp_gauge_point.sub",
												},
												{
													"name" : "observer_general_exp_2",
													"type" : "expanded_image",

													"x" : 28,
													"y" : 3,

													"image" : "d:/ymir work/ui/game/taskbar/exp_gauge_point.sub",
												},
												{
													"name" : "observer_general_exp_3",
													"type" : "expanded_image",

													"x" : 53,
													"y" : 3,

													"image" : "d:/ymir work/ui/game/taskbar/exp_gauge_point.sub",
												},
												{
													"name" : "observer_general_exp_4",
													"type" : "expanded_image",

													"x" : 78,
													"y" : 3,

													"image" : "d:/ymir work/ui/game/taskbar/exp_gauge_point.sub",
												},
											),
										},
										{
											"name" : "observer_general_empire",
											"type" : "expanded_image",

											"x" : BOARD_WIDTH - PAGE_X_DIST * 2 - (10 + 88 + 13) - 10 - 64,
											"y" : 0,
										},
										{
											"name" : "observer_general_dividing_line1",
											"type" : "line",

											"x" : 0,
											"y" : 115,

											"width" : BOARD_WIDTH - PAGE_X_DIST * 2 - (10 + 88 + 13) - 10,
											"height" : 0,

											"color" : grp.GenerateColor(1.0, 1.0, 1.0, 0.8),
										},
										{
											"name" : "observer_general_channel",
											"type" : "text",

											"x" : 0,
											"y" : 123,
										},
										{
											"name" : "observer_general_map_info",
											"type" : "text",

											"x" : 0,
											"y" : 140,
										},
										{
											"name" : "observer_general_gold",
											"type" : "text",

											"x" : 0,
											"y" : 157,
										},
										{
											"name" : "observer_general_skillgroup",
											"type" : "text",

											"x" : 0,
											"y" : 174,
										},
										{
											"name" : "observer_general_dividing_line2",
											"type" : "line",

											"x" : 234,
											"y" : 123,

											"width" : 0,
											"height" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST) - 10 * 2 - 123,

											"horizontal_align" : "right",

											"color" : grp.GenerateColor(1.0, 1.0, 1.0, 0.8),
										},
										{
											"name" : "observer_general_skill_bg",
											"type" : "image",

											"x" : 227,
											"y" : 140,

											"horizontal_align" : "right",

											"image" : "d:/ymir work/ui/game/windows/skill_board.sub",

											"children" :
											(
												{
													"name" : "observer_general_skill_title",
													"type" : "text",

													"x" : 0,
													"y" : -17,

													"horizontal_align" : "center",
													"text_horizontal_align" : "center",

													"text" : uiScriptLocale.ADMIN_MANAGER_GENERAL_SKILL_TITLE,
												},
												{
													"name" : "observer_general_skill_slot",
													"type" : "slot",

													"x" : 3,
													"y" : 0,

													"width" : 223,
													"height" : 223,

													"image" : "d:/ymir work/ui/public/Slot_Base.sub",

													"slot" :
													(
														{"index": 1, "x": 1, "y":  4, "width":32, "height":32},
														{"index":21, "x":38, "y":  4, "width":32, "height":32},
														{"index":41, "x":75, "y":  4, "width":32, "height":32},

														{"index": 3, "x": 1, "y": 40, "width":32, "height":32},
														{"index":23, "x":38, "y": 40, "width":32, "height":32},
														{"index":43, "x":75, "y": 40, "width":32, "height":32},

														{"index": 5, "x": 1, "y": 76, "width":32, "height":32},
														{"index":25, "x":38, "y": 76, "width":32, "height":32},
														{"index":45, "x":75, "y": 76, "width":32, "height":32},

														{"index": 7, "x": 1, "y":112, "width":32, "height":32},
														{"index":27, "x":38, "y":112, "width":32, "height":32},
														{"index":47, "x":75, "y":112, "width":32, "height":32},

														####

														{"index": 2, "x":113, "y":  4, "width":32, "height":32},
														{"index":22, "x":150, "y":  4, "width":32, "height":32},
														{"index":42, "x":187, "y":  4, "width":32, "height":32},

														{"index": 4, "x":113, "y": 40, "width":32, "height":32},
														{"index":24, "x":150, "y": 40, "width":32, "height":32},
														{"index":44, "x":187, "y": 40, "width":32, "height":32},

														{"index": 6, "x":113, "y": 76, "width":32, "height":32},
														{"index":26, "x":150, "y": 76, "width":32, "height":32},
														{"index":46, "x":187, "y": 76, "width":32, "height":32},

														{"index": 8, "x":113, "y":112, "width":32, "height":32},
														{"index":28, "x":150, "y":112, "width":32, "height":32},
														{"index":48, "x":187, "y":112, "width":32, "height":32},
													),
												},
											),
										},
									),
								},
								{
									"name" : "observer_subpage_item",

									"x" : 10 + 88 + 13,
									"y" : 10,

									"width" : BOARD_WIDTH - PAGE_X_DIST * 2 - (10 + 88 + 13) - 10,
									"height" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST) - 10 * 2,

									"children" :
									(
										{
											"name" : "observer_item_equipment_base",
											"type" : "image",

											"x" : 0,
											"y" : 0,

											"image" : "d:/ymir work/ui/game/windows/equipment_base.sub",

											"children" :
											(
												{
													"name" : "observer_item_equipment_slot",
													"type" : "slot",

													"x" : 3,
													"y" : 3,

													"width" : 150,
													"height" : 182,

													"slot" : (
														{"index":EQUIPMENT_START_INDEX+0, "x":39, "y":37, "width":32, "height":64},
														{"index":EQUIPMENT_START_INDEX+1, "x":39, "y":2, "width":32, "height":32},
														{"index":EQUIPMENT_START_INDEX+2, "x":39, "y":145, "width":32, "height":32},
														{"index":EQUIPMENT_START_INDEX+3, "x":75, "y":67, "width":32, "height":32},
														{"index":EQUIPMENT_START_INDEX+4, "x":3, "y":3, "width":32, "height":96},
														{"index":EQUIPMENT_START_INDEX+5, "x":114, "y":84, "width":32, "height":32},
														{"index":EQUIPMENT_START_INDEX+6, "x":114, "y":52, "width":32, "height":32},
														{"index":EQUIPMENT_START_INDEX+7, "x":2, "y":113, "width":32, "height":32},
														{"index":EQUIPMENT_START_INDEX+8, "x":75, "y":113, "width":32, "height":32},
														{"index":EQUIPMENT_START_INDEX+9, "x":114, "y":1, "width":32, "height":32},
														{"index":EQUIPMENT_START_INDEX+10, "x":75, "y":35, "width":32, "height":32},
													),
												},
											),
										},
										{
											"name" : "observer_item_inventory_tab_01",
											"type" : "radio_button",

											"x" : 156 - 78,
											"y" : 191,

											"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_01.sub",
											"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_02.sub",
											"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_03.sub",
											"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_1,

											"children" :
											(
												{
													"name" : "observer_item_inventory_tab_01_text",
													"type" : "text",

													"x" : 0,
													"y" : 0,

													"all_align" : "center",

													"text" : "I",
												},
											),
										},
										{
											"name" : "observer_item_inventory_tab_02",
											"type" : "radio_button",

											"x" : 156 - 78,
											"y" : 191 + 22,

											"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_01.sub",
											"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_02.sub",
											"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_03.sub",
											"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_2,

											"children" :
											(
												{
													"name" : "observer_item_inventory_tab_02_text",
													"type" : "text",

													"x" : 0,
													"y" : 0,

													"all_align" : "center",

													"text" : "II",
												},
											),
										},
										{
											"name" : "observer_item_money_slot",
											"type" : "image",

											"x" : 156 - 130,
											"y" : 9 * 32 - 18,

											"image" : "d:/ymir work/ui/public/parameter_slot_05.sub",

											"children" :
											(
												{
													"name" : "observer_item_money_icon",
													"type" : "image",

													"x" : -18,
													"y" : 2,

													"image":"d:/ymir work/ui/game/windows/money_icon.sub",
												},
												{
													"name" : "observer_item_money_text",
													"type" : "text",

													"x" : 3,
													"y" : 3,

													"horizontal_align" : "right",
													"text_horizontal_align" : "right",
												},
											),
										},
										{
											"name" : "observer_item_inventory_slot",
											"type" : "grid_table",

											"x" : 165,
											"y" : 0,

											"start_index" : 0,
											"x_count" : 5,
											"y_count" : 9,
											"x_step" : 32,
											"y_step" : 32,

											"image" : "d:/ymir work/ui/public/Slot_Base.sub"
										},
									),
								},
								{
									"name" : "observer_subpage_whisper",

									"x" : 10 + 88 + 13,
									"y" : 10,

									"width" : BOARD_WIDTH - PAGE_X_DIST * 2 - (10 + 88 + 13) - 10,
									"height" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST) - 10 * 2,

									"children" :
									(
										{
											"name" : "observer_whisper_name_title",
											"type" : "text",

											"x" : 50,
											"y" : 0,

											"text_horizontal_align" : "center",

											"text" : uiScriptLocale.ADMIN_MANAGER_OBSERVER_WHISPER_NAME_TITLE,
										},
										{
											"name" : "observer_whisper_name_list",
											"type" : "listbox",

											"x" : 0,
											"y" : 20,

											"width" : 100,
											"height" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST) - 10 * 2 - 20,

											"border" : TRUE,
										},
										{
											"name" : "observer_whisper_name_scroll",
											"type" : "scrollbar",

											"x" : 105,
											"y" : 20,

											"size" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST) - 10 * 2 - 20,
										},
										{
											"name" : "observer_whisper_line",
											"type" : "line",

											"x" : 105 + 17 + 6,
											"y" : 0,

											"width" : 0,
											"height" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST) - 10 * 2,

											"color" : grp.GenerateColor(1.0, 1.0, 1.0, 0.8),
										},
										{
											"name" : "observer_whisper_text",
											"type" : "multi_text",

											"x" : 105 + 17 + 13,
											"y" : 0,

											"width" : BOARD_WIDTH - PAGE_X_DIST * 2 - (10 + 88 + 13) - 10 - (105 + 17 + 13) - 17 - 5,
											"height" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST) - 10 * 2,
										},
										{
											"name" : "observer_whisper_text_scroll",
											"type" : "scrollbar",

											"x" : 17,
											"y" : 0,

											"horizontal_align" : "right",

											"size" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST) - 10 * 2,
										},
									),
								},
							),
						},
					),
				},

				# Navigation Buttons
				{
					"name" : "navi_button_1",
					"type" : "radio_button",

					"x" : BOARD_WIDTH / (NAVI_BTN_COUNT + 1) * 1 - NAVI_BTN_WIDTH / 2,
					"y" : BOARD_HEIGHT - (PAGE_BOT_DIST + NAVI_BTN_HEIGHT) / 2 - NAVI_BOT_DIST,

					"default_image" : "d:/ymir work/ui/public/Large_Button_01.sub",
					"over_image" : "d:/ymir work/ui/public/Large_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/Large_Button_03.sub",

					"text" : uiScriptLocale.ADMIN_MANAGER_NAVI_BTN_1,
				},
				{
					"name" : "navi_button_2",
					"type" : "radio_button",

					"x" : BOARD_WIDTH / (NAVI_BTN_COUNT + 1) * 2 - NAVI_BTN_WIDTH / 2,
					"y" : BOARD_HEIGHT - (PAGE_BOT_DIST + NAVI_BTN_HEIGHT) / 2 - NAVI_BOT_DIST,

					"default_image" : "d:/ymir work/ui/public/Large_Button_01.sub",
					"over_image" : "d:/ymir work/ui/public/Large_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/Large_Button_03.sub",

					"text" : uiScriptLocale.ADMIN_MANAGER_NAVI_BTN_2,
				},
				{
					"name" : "navi_button_3",
					"type" : "radio_button",

					"x" : BOARD_WIDTH / (NAVI_BTN_COUNT + 1) * 3 - NAVI_BTN_WIDTH / 2,
					"y" : BOARD_HEIGHT - (PAGE_BOT_DIST + NAVI_BTN_HEIGHT) / 2 - NAVI_BOT_DIST,

					"default_image" : "d:/ymir work/ui/public/Large_Button_01.sub",
					"over_image" : "d:/ymir work/ui/public/Large_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/Large_Button_03.sub",

					"text" : uiScriptLocale.ADMIN_MANAGER_NAVI_BTN_3,
				},
			),
		},
	),
}
