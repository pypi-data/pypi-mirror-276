from common import print_warning, getProcessByName
from debuger import Debugger, exit_gracefully
import signal
import yaml
import argparse
from pathlib import Path


yaml_str = '''
name: observer.exe
path: E:/github/appknife/_build-x64/Release/observer.exe
breakpoints: 
  - observer!Subject::detach
  - observer!Subject::notify
  - observer!ConcreteObeserver::*
  - observer!ConcreteSubject::*
'''


class Monitor:
    def __init__(self, debugger: Debugger):
        signal.signal(signal.SIGINT, exit_gracefully)
        self.debugger = debugger

    def run(self):
        try:
            self.debugger.start()
            while self.debugger.is_alive():
                pass
        except Exception as errtxt:
            print_warning(errtxt)


def adjust_file_path(filename: str) -> str:
    if Path(filename).is_file():
        return filename

    newpath = Path.cwd().joinpath(filename)
    if Path(newpath).is_file():
        return str(newpath.absolute())

    return None


def get_exe_file_path(yamlPath: str, exePath: str) -> str:
    if not exePath:
        return ''

    # 绝对路径
    if Path(exePath).is_file():
        return exePath
    # 相对路径
    newPath = Path(yamlPath).parent.joinpath(exePath)
    if Path(newPath).is_file():
        return str(newPath.absolute())

    return None


def main():
    parser = argparse.ArgumentParser()
    parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter
    parser.add_argument('file', help="set the yaml config file")
    args = parser.parse_args()

    filepath = adjust_file_path(args.file)
    if not filepath:
        print_warning(f'cannot find the file: {args.file}')
        exit()

    config = None
    with open(filepath, 'r', encoding='UTF-8') as stream:
        config = yaml.safe_load(stream)

        pid = getProcessByName(config['name'])
        logfilepath = Path(filepath).with_suffix('.cst')  # short for callstack
        exepath = config['path'] if 'path' in config else ''
        exepath = get_exe_file_path(filepath, exepath)

        debugger = Debugger(pid, exepath, logfilepath=logfilepath)
        debugger.setDaemon(True)
        for bp in config['breakpoints']:
            debugger.addBreakPoint(bp)

        monitor = Monitor(debugger)
        monitor.run()


if __name__ == "__main__":
    main()
