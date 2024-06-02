import argparse

if __name__ == "__main__":
    import url as url
    import tool as tool
else:
    import dcmake.url as url
    import dcmake.tool as tool

def main():
    parser = argparse.ArgumentParser(description="Download github repository to CMake Project")
    parser.add_argument("-i", "--install", help="install github repository")
    parser.add_argument("-u", "--url", help="download file url")
    parser.add_argument("-o", "--output", help="output file path")

    args = parser.parse_args()

    if not args.url is None or not args.output is None:
        if url.downloadFile(args.url, args.output):
            print("\033[92mDownload Success\033[0m")
        else:
            print("\033[91mDownload Failed\033[0m")

    if not args.install is None:
        if tool.checkGitAndCMake():
            if url.install(args.install):
                print("\033[92mInstall Success\033[0m")
            else:
                print("\033[91mInstall Failed\033[0m")
        else:
            print("\033[91mPlease install git or cmake\033[0m")

if __name__ == "__main__":
    main()