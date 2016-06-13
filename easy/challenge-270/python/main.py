import sys


def main():
    result = []
    for i, line in enumerate(sys.stdin):
        for j, ch in enumerate(line[:-1]):
            while len(result) < (j + 1):
                result.append([])
            while len(result[j]) < (i + 1):
                result[j].append(' ')

            result[j][i] = ch

    for line in result:
        for ch in line:
            sys.stdout.write(ch)
        sys.stdout.write('\n')

if __name__ == '__main__':
    main()
