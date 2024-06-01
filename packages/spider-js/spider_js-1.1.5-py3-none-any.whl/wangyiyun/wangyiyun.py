from pprint import pprint

import requests
SPLASH_URL='http://192.168.99.100:32768/execute' # 换成自己的host即可
LUA_SOURCE='''
treat = require("treat")
function main(splash, args)
    splash.private_mode_enabled = false
    local url_path = args.url_path
    splash:on_request(function(request)
        if (string.find(request.url, url_path) ~= nil) then
            request:enable_response_body()
        end
    end)
    local body = nil
    splash:on_response(function(response)
        if (string.find(response.url, url_path) ~= nil) then
            body = treat.as_string(response.body)
        end
    end)
    splash:go(args.url)
    local input = splash:select('input')
    input:send_text(args.key)
    input:send_keys('<Return>')
    splash:wait(1)
    return  body
end
'''
params={
    'lua_source':LUA_SOURCE,
    'url':'https://music.163.com/#/search/m/',
    'key':'房东的猫',
    'url_path':'suggest/web'
}
data = requests.get(SPLASH_URL,params).json()
print(data)