from translate import Translator
# for geolocation translation
from argostranslate import translate as geo_translater
from argostranslate import package

package.update_package_index()
available_packages = package.get_available_packages()
zh_en_package = next(p for p in available_packages if p.from_code == "zh" and p.to_code == "en")
package.install_from_path(zh_en_package.download())

# for ISP
isp_translator = Translator(to_lang="en", from_lang="zh")


from_file = open('ip.merge.txt', 'r')
to_file = open('new.ip.merge.txt', 'w')

line_count = 0

geo_cache = {}
isp_cache = {}

for line in from_file:
    line_count += 1

    if (line_count % 100) == 0:
        print(f'processed lines: {line_count}')

    keys = line.strip().split('|')
    # sip|eip|country|region|province|city|isp
    for i in range(len(keys)):
        key = keys[i]
        if i < 2:
            continue
        elif i < 6:
            if any('\u4e00' <= char <= '\u9fff' for char in key):
                #check cache first
                if key in geo_cache.keys():
                    key_en = geo_cache[key]
                else:
                    key_en = geo_translater.translate(key, "zh", "en")
                    # cache translation result
                    geo_cache[key] = key_en

                line = line.replace(key, key_en)
        else:
            if any('\u4e00' <= char <= '\u9fff' for char in key):
                #check cache first
                if key in isp_cache.keys():
                    key_en = isp_cache[key]
                else:
                    key_en = isp_translator.translate(key)
                    # cache translation result
                    isp_cache[key] = key_en

                line = line.replace(key, key_en)
    to_file.write(line)

from_file.close()
to_file.close()
