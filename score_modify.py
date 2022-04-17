import argparse

keys = 'ZXCVBNMASDFGHJQWERTYUiop[]'
rest = 'O'
kDic = {}
for i in range(len(keys)):
    kDic[keys[i]] = i


def step_modify(score, step):
    res = ''
    global keys, rest
    for k in score:
        if k in keys:
            target = kDic[k] + step
            if 0 <= target < len(keys):
                res += keys[target]
            else:
                res += rest
        else:
            res += k
    return res


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode')
    parser.add_argument('--path')
    parser.add_argument('--step', type=int, default=2)
    parser.add_argument('--output', default='modRes.txt')
    args = parser.parse_args()

    with open(args.path, 'r') as f:
        score = f.read()
    with open(args.output, 'w') as f:
        f.write(step_modify(score, args.step))
