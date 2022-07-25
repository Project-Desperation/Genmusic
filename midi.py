from struct import unpack
from argparse import ArgumentParser

commands = []

default_key_dict = {0: 'Z', 2: 'X', 4: 'C', 5: 'V', 7: 'B', 9: 'N', 11: 'M',
                    1: 'z', 3: 'x', 6: 'v', 8: 'b', 10: 'n',
                    12: 'A', 14: 'S', 16: 'D', 17: 'F', 19: 'G', 21: 'H', 23: 'J',
                    13: 'a', 15: 's', 18: 'f', 20: 'g', 22: 'h',
                    24: 'Q', 25: 'q', 26: 'W', 27: 'w', 28: 'E', 29: 'R', 30: 'r', 31: 'T', 32: 't', 33: 'Y', 34: 'y',
                    35: 'U'}

# 36: '1', 38: '2', 40: '3', 41: '4', 43: '5', 45: '6', 47: '7',
# 37: '(', 39: ')', 42: "'", 44: '[', 46: ']',

def read_vlq(f):
    result = ''
    buffer = unpack('B', f.read(1))[0]
    length = 1
    while buffer > 127:
        result += '{0:{fill}{n}b}'.format(buffer - 128, fill='0', n=7)
        buffer = unpack('B', f.read(1))[0]
        length += 1

    result += '{0:{fill}{n}b}'.format(buffer, fill='0', n=7)
    return int(result, 2), length


def parse_event(evt, param, t):
    global commands
    if 128 <= evt <= 143:
        print('Note Off event.')
    elif 144 <= evt <= 159:
        commands.append((t, unpack('>BB', param)[0]))
        print('Note On event.', unpack('>BB', param))
    elif 176 <= evt <= 191:
        print('Control Change.')
    elif 192 <= evt <= 207:
        print('Program Change.')


def parse_midi(file):
    with open(file, 'rb') as f:
        # HEADER
        if f.read(4) != b'MThd':
            raise Exception('not a midi file!')
        len_of_header = unpack('>L', f.read(4))[0]
        header_info = unpack('>hhh', f.read(6))
        tot_tracks = header_info[1]
        commands = [[] for _ in range(tot_tracks)]

        ''' ================================== '''
        for track in range(tot_tracks):
            track_head = f.read(4)
            if track_head != b'MTrk':
                if track_head != b'':
                    raise Exception('not a midi file!')
                else:
                    break

            # length of track
            len_of_track = unpack('>L', f.read(4))[0]
            print('New Track======================================')
            print('len_of_track ', len_of_track)

            counter = 0
            t = 0
            last_event = None
            while True:
                delta_t, len_ = read_vlq(f)
                counter += len_
                t += delta_t
                event_code = f.read(1)
                event_type = unpack('>B', event_code)[0]
                counter += 1
                print('T ', t, ' event_type ', event_type, end='')
                if event_type == 255:
                    meta_type = f.read(1)
                    counter += 1
                    print(' - meta_type ', meta_type, end='')
                    data_len, len_ = read_vlq(f)
                    counter += len_
                    data = f.read(data_len)
                    counter += data_len
                    print(' - ', data)
                elif event_type <= 127:
                    if 144 <= last_event <= 159:
                        # print(' Note On event.', end='')
                        param = unpack('>BB', event_code + f.read(1))
                        commands[track].append((t, param[0], param[1]))
                        print('Note On event.', param)
                    else:
                        parse_event(last_event, event_code + f.read(1), t)
                    counter += 1
                else:
                    if 128 <= event_type <= 143:
                        # print(' Note Off event.', end='')
                        parse_event(event_type, f.read(2), t)
                        counter += 2
                    elif 144 <= event_type <= 159:
                        # print(' Note On event.', end='')
                        param = unpack('>BB', f.read(2))
                        commands[track].append((t, param[0], param[1]))
                        print('Note On event.', param)
                        counter += 2
                    elif 176 <= event_type <= 191:
                        # print(' Control Change.', end='')
                        parse_event(event_type, f.read(2), t)
                        counter += 2
                    elif 192 <= event_type <= 207:
                        # print(' Program Change.', end='')
                        parse_event(event_type, f.read(1), t)
                        counter += 1
                    elif 208 <= event_type <= 223:
                        print(' DX', end='')
                        f.read(2)
                        counter += 2
                    elif 224 <= event_type <= 254:
                        print(' EX', end='')
                        f.read(2)
                        counter += 2
                    last_event = event_type

                # print(counter)
                if counter == len_of_track:
                    break
    return commands, header_info


def calc_rest(delta_t, tick):
    res = ''
    rest_type = '+-=.'
    for i in range(len(rest_type)):
        tmp = int(delta_t / tick)
        res += rest_type[i] * tmp
        delta_t -= tick * tmp
        tick /= 2
    return res


def to_genshin_commands(commands, tick, tracks='ALL', key_dic=None, start=50):
    if key_dic is None:
        global default_key_dict
        key_dic = default_key_dict
    if not isinstance(tracks, list):
        tracks = range(len(commands))
    cmds = []
    for track in tracks:
        cmds.extend(commands[track])
    cmds.sort(key=lambda x: x[0])
    t = 0
    res = ''
    for cmd in cmds:
        if cmd[2] <= 0:
            continue
        delta_t = cmd[0] - t
        res += calc_rest(delta_t, tick)
        if key_dic.get(cmd[1] - start):
            res += key_dic[cmd[1] - start]
        else:
            res += 'O'
        t = cmd[0]
        # 转调特殊处理
        # if res[-6:] == 'FRO+FR': start -= 2  # 紫罗兰
        # if res[-8:] == 'AQO=.NHO':
        #     start -= 4
        #     print(len(res))
    return res


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input', default='勾指起誓.mid', help='midi文件路径')
    parser.add_argument('--output', default='music\勾指起誓.txt', help='输出路径')
    parser.add_argument('--start', type=int, default=48, help='低音do（原神按键Z）对应midi编号')
    parser.add_argument('--BPM', type=int, default=85, help='Beat Per Minute，每分钟节拍数')
    args = parser.parse_args()

    commands, header_info = parse_midi(args.input)
    res = to_genshin_commands(commands, header_info[2] / 2, start=args.start)
    res = '{:.5f}\n'.format(30 / args.BPM) + res
    with open(args.output, 'w') as f:
        f.write(res)
