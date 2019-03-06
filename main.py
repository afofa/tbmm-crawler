if __name__ == '__main__':
    import argparse
    import os
    from crawler import get_mp_list, get_mp_page
    from utils import save_json

    default_args = {
        "save_file" : 1,
        "json_path" : "tbmm.json",
        "mp_page" : 0,
        "verbose" : 1,
    }

    parser = argparse.ArgumentParser(description='Crawl TBMM webpage')
    parser.add_argument('-s', '--save-file', type=int, default=default_args["save_file"], help='save file?')
    parser.add_argument('-o', '--json-path', type=str, default=default_args["json_path"], help='path to save json file')
    parser.add_argument('-m', '--mp-page', type=int, default=default_args["mp_page"], help='add crawled mp page to json?')
    parser.add_argument('-v', '--verbose', type=int, default=default_args["verbose"], help='print result to terminal?')

    args = vars(parser.parse_args())

    # Return title and tbmm json
    title, tbmm = get_mp_list(is_add_mp_page=bool(args['mp_page']))

    if args["verbose"]:
        print("title: {}".format(title))
        print(tbmm)

    if args["save_file"]:
        if "/" in args["json_path"]:
            filepath, filename = os.path.split(args["json_path"])
            if filename == "":
                filename = default_args["json_path"]
            save_json(tbmm, args["json_path"], makedirs=[filepath])
        else:
            save_json(tbmm, args["json_path"])

    # # Get mp page
    # url = "https://www.tbmm.gov.tr/develop/owa/milletvekillerimiz_sd.bilgi?p_donem=27&p_sicil=7542"
    # print(get_mp_page(url))

