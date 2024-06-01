# 解析开始
def vm3u8(text):
    parsed_data = {}
    data = text.replace('"', '')
    lines = data.strip().split('\n')
    for line in lines:
        if line.startswith('#'):  # m3u8标签
            if not ':' in line:  # 避免报错
                continue
            
            key, value = line[1:].split(':', 1)
            value = value.rstrip(',')  # 去末尾，
            
            # 分离= > 分离， > 展开 > 两两成对 > 变成字典
            if ',' in value:  # 可二次解析
                first,*mid,end = value.split('=')
                # split和展开写成一行,只是看起来复杂点
                opened = [first, *(element for sublist in [i.split(',') for i in mid] for element in sublist), end]
                m = [[opened[i], opened[i + 1]] for i in range(0, len(opened), 2)]
                value = {i:j for i,j in m}  # 二维列表变成字典
            
            if key in parsed_data:  # 重复key,可追加
                if not isinstance(parsed_data[key], list):  # 升级成列表
                    parsed_data[key] = [parsed_data[key]]
                parsed_data[key].append(value)
            
            # 没有重复{，正常添加
            else:
                parsed_data[key] = value
        else:  # 片段链接
            parsed_data.setdefault('url', []).append(line)
    return parsed_data

if __name__ == '__main__':
    f = open('index.m3u8')
    txt = f.read()
    f.close()
    print(vm3u8(txt))
    

