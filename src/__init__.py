import pathlib
from method import FileControl
from method import HttpControl
from method import MGDate
from method import PathControl
from method import GitControl
import static_value

"""pyinstaller -F --noconsole -n main src/__init__.py"""
# HTTP request value
HTTP_PATH = "https://api.tarkov.dev/graphql"
HEADERS = {
	"Content-Type": "application/json",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
}
BODY = {
	"query": "query{\n  items(lang:zh){\n    id\n    name\n    shortName\n    basePrice\n    avg24hPrice    \n    low24hPrice\n    high24hPrice\n    sellFor{ \n      vendor{\n        name\n        __typename\n        }\n      price\n      currency\n      priceRUB\n    }\n    buyFor{ \n      vendor{\n        name\n        __typename\n      }\n      price\n      currency\n      priceRUB\n    }\n    fleaMarketFee\n  }\n}"
}

#path value
# GIT_PWSH_PATH = PathControl.locateGivenFolderNamePathNearby(PathControl.getParentsFolderPath(__file__, 2), "Sync-Online-FleaMarket", [])
# APP_ROOT_PATH = PathControl.locateGivenFolderNamePathNearby(PathControl.getParentsFolderPath(__file__, 2), "Sync-Online-FleaMarket", [])
EXE_PATH = PathControl.getNowFolderPath(str(pathlib.Path().absolute()))
GIT_PWSH_PATH = EXE_PATH
APP_ROOT_PATH = EXE_PATH

def priceCreat(base_info, itemJson):
	pricesJson = {}
	for it in base_info:
		if len(it['buyFor']) == 0:
			continue
			pass
		v = 0
		for it2 in it["buyFor"]:
			if it2["vendor"]['name'] == "跳蚤市场":
				v = 1
				pass
			pass
		if v != 1:
			continue
			pass
		itemId = it["id"]
		if itemId not in itemJson:
			continue
			pass
		avg = it["avg24hPrice"]
		base = it["basePrice"]
		if not avg and base:
			pricesJson[itemId] = base
			continue
			pass
		pricesJson[itemId] = avg
		pass
	return pricesJson

def debugPrint(message):
	print(f"Debug --> {message}.\n")
	pass

if __name__ == "__main__":
	
	_path = PathControl()
	_http = HttpControl()
	_file = FileControl()
	_date = MGDate()
	_git = GitControl()

	_git.gitPull(GIT_PWSH_PATH)
	
	baseInfo = (_http.getBaseInfoFromTarkovAPI(HTTP_PATH,HEADERS,BODY))["data"]["items"]
	if baseInfo:
		debugPrint("baseInfo got")
	# year,month,day = _date.get_Date()
	itemBaseInfo = {
		"date":_date.get_Date(),
		"items":baseInfo
	}
	ITEMS_BASE_INFO_PATH = _path.combineFolderPathWithRelativePath(APP_ROOT_PATH,static_value.ITEMS_BASE_INFO)
	ITEMS_PATH = _path.combineFolderPathWithRelativePath(APP_ROOT_PATH,static_value.ITEMS)
	PRICE_PATH = _path.combineFolderPathWithRelativePath(APP_ROOT_PATH,static_value.PRICE)

	_file.saveJsonFileByAbsolutePath(ITEMS_BASE_INFO_PATH,itemBaseInfo)
	priceJson = priceCreat(baseInfo,_file.getJsonFileByAbsolutePath(ITEMS_PATH))
	if priceJson:
		debugPrint("priceJson got")
	_file.saveJsonFileByAbsolutePath(PRICE_PATH,priceJson)
	_git.gitRefresh(GIT_PWSH_PATH, f"{_date.get_Date()} update")
	debugPrint("end")
	pass


