import argparse, os

if __name__ == "__main__":
    import url, config, tool
else:
    import dcmake.url as url
    import dcmake.tool as tool
    import dcmake.config as config

def main():
    parser = argparse.ArgumentParser(description="Download github repository to CMake Project")
    parser.add_argument("-i", "--install", help="install github repository")
    parser.add_argument("-u", "--url", help="download file url")
    parser.add_argument("-o", "--output", help="output file path")
    parser.add_argument("-uz", "--unzip", help="unzip file", action="store_true")
    parser.add_argument("-c", "--clean", help="clean file", action="store_true")
    parser.add_argument("-v", "--version", help="DCMake Version", action="version", version=config.version)

    args = parser.parse_args()

    if not args.url is None or not args.output is None:
        if args.url.find(";") == -1: FileDownload = url.downloadFile(args.url, args.output)
        else:
            FileDownload = url.downloadFileList(args.url, args.output)
        if FileDownload:
            print(f"{config.colors["green"]}Download Success{config.colors["end"]}")
        else:
            print(f"{config.colors["red"]}Download Failed{config.colors["end"]}")
        if args.unzip:
            if args.url.find(";") == -1:
                tool.unzipFile(f"{args.output}/{args.url.split('/')[-1]}", args.output)
                if args.clean:
                    tool.deleteFileList(args.url, args.output)
            else:
                for file in args.url.split(";"):
                    fileName = file.spilt("/")[-1]
                    if fileName.endswith(".zip"):
                        tool.unzipFile(f"{args.output}/{fileName}", args.output)
                    if args.clean:
                        tool.deleteFileList(args.url, args.output)
        elif args.clean:
            tool.deleteFileList(args.url, args.output)

    if not args.install is None:
        if tool.checkGitAndCMake():
            if url.install(args.install):
                print(f"{config.colors["green"]}Install Success{config.colors["end"]}")
            else:
                print(f"{config.colors["red"]}Install Failed{config.colors["end"]}")
        else:
            print(f"{config.colors["red"]}Please install git or cmake{config.colors["end"]}")

if __name__ == "__main__":
    main()