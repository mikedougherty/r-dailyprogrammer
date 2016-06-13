#!env python3
import sys
import os
import os.path
import subprocess
import shlex


def run(cmd, stdin=None, collect_stdout=False):
    if isinstance(cmd, str):
        cmd = shlex.split(cmd)

    kwargs = dict(
        stderr=sys.stderr,
        stdout=sys.stdout
    )
    if collect_stdout:
        kwargs['stdout'] = subprocess.PIPE

    if stdin is not None:
        kwargs['stdin'] = stdin

    proc = subprocess.Popen(cmd, **kwargs)
    proc.wait()
    if collect_stdout:
        stdout = proc.stdout.read().decode('utf8')
        proc.stdout = stdout

    return proc

def main(root_dir, work_dir, *cmds):
    print(root_dir, work_dir, cmds)
    os.chdir(os.path.join(root_dir, work_dir))
    failures = 0
    total = 0
    for input_file_name in sorted(os.listdir('inputs')):
        failed = False
        total += 1
        input_file_path = os.path.join('inputs', input_file_name)
        output_file_path = os.path.join('outputs', input_file_name)
        if not os.path.exists(output_file_path):
            output_file_path = None

        for cmd in cmds[:-1]:
            sys.stderr.write("Running prep {cmd!r}\n".format(cmd=cmd))
            proc = run(cmd)
            if proc.returncode == 0:
                continue

            sys.stderr.write("Failed to run prep {cmd!r} in {workdir!r} (returncode={retcode})\n".format(
                workdir=os.getcwd(), cmd=cmd, retcode=proc.returncode)
            )
            failed = True
            break

        if not failed:
            cmd = cmds[-1]
            sys.stderr.write("Running {cmd!r} with {input!r}\n".format(cmd=cmd, input=input_file_path))
            proc = run(cmd, stdin=open(input_file_path), collect_stdout=True)
            if proc.returncode != 0:
                sys.stderr.write("Failed to run {cmd!r} with {ifile!r} in {workdir!r} (returncode={retcode})\n".format(
                    workdir=os.getcwd(), cmd=cmd, ifile=input_file_path, retcode=proc.returncode)
                )
                failed = True

            if output_file_path is not None:
                expected = open(output_file_path).read()
                if proc.stdout != expected:
                    sys.stderr.write("Expected:\n{expected!r}\nActual:\n{output!r}\n".format(
                        expected=expected, output=proc.output
                    ))
                    failed = True
            else:
                sys.stderr.write("Got:\n{output}\n".format(output=proc.output))

        if failed:
            failures += 1
            sys.stderr.write('Failed\n')
        else:
            sys.stderr.write('Success\n')

    sys.exit(failures)

if __name__ == '__main__':
    main(os.path.dirname(__file__), *sys.argv[1:])
