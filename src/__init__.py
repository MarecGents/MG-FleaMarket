import pathlib

from method import FileControl
from method import HttpControl
from method import MGDate
from method import PathControl

"""pyinstaller -F --noconsole -n main main.py"""
# HTTP request value
HTTP_PATH = "https://api.tarkov.dev/graphql"
HEADERS = {
	"Content-Type": "application/json",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
}
BODY = {
	"query": "query{\n  items(lang:zh){\n    id\n    name\n    shortName\n    basePrice\n    avg24hPrice    \n    low24hPrice\n    high24hPrice\n    sellFor{ \n      vendor{\n        name\n        __typename\n        }\n      price\n      currency\n      priceRUB\n    }\n    buyFor{ \n      vendor{\n        name\n        __typename\n      }\n      price\n      currency\n      priceRUB\n    }\n    fleaMarketFee\n  }\n}"
}
GIT_PWSH_PATH = PathControl.locateGivenFolderNamePathNearby(PathControl.getParentsFolderPath(__file__, 2), "Sync-Online-FleaMarket", [])
EXE_PATH = PathControl.getNowFolderPath(str(pathlib.Path().absolute()))

if __name__ == "__main__":
	
	_path = PathControl()
	_http = HttpControl()
	_file = FileControl()
	_date = MGDate()
	
	baseInfo = _http.getBaseInfoFromTarkovAPI(HTTP_PATH,HEADERS,BODY)
	year,month,day = _date.get_Date()
	
	pass
