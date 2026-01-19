import pathlib
from method import FileControl
from method import HttpControl
from method import MGDate
from method import PathControl
from method import GitControl
import static_value

"""pyinstaller -F --onefile --noconsole --distpath .\Build\dist --workpath .\Build\build src/main.py"""

# HTTP request value
HTTP_PATH = "https://api.tarkov.dev/graphql"
HEADERS = {
	"Content-Type": "application/json",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
}
BODY = {
	"query": "query{\n  items(lang:zh){\n    id\n    name\n    shortName\n    basePrice\n    avg24hPrice    \n    low24hPrice\n    high24hPrice\n  }\n}"
}

#path value

# EXE_PATH = PathControl.locateGivenFolderNamePathNearby(PathControl.getParentsFolderPath(__file__, 2), "MGFleaMarket", [])
EXE_PATH = PathControl.getNowFolderPath(str(pathlib.Path().absolute()))
GIT_PWSH_PATH = EXE_PATH
APP_ROOT_PATH = EXE_PATH

def priceCreat(base_info, itemJson):
	pricesJson = {}
	for it in base_info:
		itemId = it["id"]
		if itemId not in itemJson:
			continue
		priceGet = {
			"base" : it["basePrice"],
			"avg" : it["avg24hPrice"],
			"low" : it["low24hPrice"],
			"high" : it["high24hPrice"]
		}
		price = caculatePrice(priceGet)
		pricesJson[itemId] = price
		pass
	return pricesJson

baseWeight = 0.1
def caculatePrice(priceGet):
	"""
	   计算加权价格 P
	   :param base_weight_full: 当四项全有时，basePrice 的权重（建议 0.1～0.2）
	   """

	# 情况1: 只有 base
	if priceGet["avg"] is None:
		return priceGet["base"]

	# 情况2: 有 base + avg24，但缺少 low/high
	if priceGet["low"] is None or priceGet["high"] is None:
		# 可自定义此场景的权重，例如 30% base + 70% avg
		return 0.15 * priceGet["base"] + 0.85 * priceGet["avg"]

	# 情况3: 四项全有
	y = baseWeight
	x = (1 - y) / (80 * y)

	avg_part = 9 * x * priceGet["avg"]
	range_part = x * (priceGet["low"] + priceGet["high"]) / 2.0
	return y * priceGet["base"] + 8 * y * (avg_part + range_part)

def priceJsonRebuild(priceJson, date):
	return {
		"date":date,
		"prices":priceJson
	}
	pass

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
	priceJson = priceJsonRebuild(priceJson,_date.get_Date())

	if priceJson:
		debugPrint("priceJson got")
	_file.saveJsonFileByAbsolutePath(PRICE_PATH,priceJson)
	_git.gitRefresh(GIT_PWSH_PATH, message=f"{_date.get_Date()} update")
	debugPrint("end")

	pass


