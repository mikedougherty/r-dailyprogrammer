#!env nim-run
import streams

var i = 0
var result : seq[seq[char]] = newSeq[seq[char]]()

while not endoffile(stdin):
    let line = stdin.readLine
    for j, ch in line[0..<line.len]:
        while result.len < (j + 1):
            result &= newSeq[char]()

        while result[j].len < (i + 1):
            result[j] &= ' '

        result[j][i] = ch
    i += 1

for line in result:
    for ch in line:
        stdout.write(ch)
    stdout.write("\n")
