import subprocess

def test_n(target):
    cmd = ['csh', 'plltest.sh', '26e6', str(target), '1']
    print(*cmd, sep=' ')
    out = subprocess.check_output(cmd).decode('utf8')
    lines = out.split('\n')
    lines = [l for l in lines if len(l)!=0]

    if len(lines) == 0:
        return None

    er = [le.strip() for le in lines if le.startswith('error')]
    er = er[0]
    er = er[len('error = '):]
    er = float(er)
    data_res = dict([[item.strip() for item in data.split('=')] for data in lines])
    return [data_res, er]


def get_err_tab(target):
    r = []
    for i in range(1, 256):
        t = test_n(target*i)
        if t == None:
            continue

        t[1] = t[1]/i
        t.append(float(t[0]['Fout']))
        t.append(i)
        
        r.append(t)
    return r

def get_target_err(freq, target):
    n = round(freq/target)
    a = target*n
    er = freq - a
    return [er/target, n]

def main():
    err_t = get_err_tab(48000*64)
    freq_1, freq_2, freq_3 = 1/1.25e-6, 1/8.5e-7, 1/4e-7
    for item in err_t:
        freq = item[2]
        item.extend(get_target_err(freq, freq_2))
        item.extend(get_target_err(freq, freq_3))

    err_t = [i for i in err_t if abs(i[1])<1e-5 and i[5]<256 and abs(i[6])<0.3]
    for item in err_t:
        #item[0] = 0
        print(*item, sep='\t')

main()
