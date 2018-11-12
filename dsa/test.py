import argparse

def parseArguments():

    parser = argparse.ArgumentParser()

    parser.add_argument("datapipeline_name", help="datapipeline_name", type=str)
    parser.add_argument("template_path", help="template_path", type=str)

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    # Parse the arguments
    args = parseArguments()

    print(args.datapipeline_name)
