import argparse
from shapes39.shapes.interpreter import Interpreter
from shapes39.shapes.parser import Parser
from time import time
import cProfile

def main():
    arg_parser = argparse.ArgumentParser(description="Shapes Interpreter for Python 3.9")
    arg_parser.add_argument("path", type=str, help="path of file to interpret. if the given path doesn't have a file format, it defaults to .png")
    arg_parser.add_argument("-t", '--time', type=float, help="seconds to wait for every step")
    arg_parser.add_argument("-v", '--verbose', action='store_true',help="print extra stuff (good for debugging)")
    arg_parser.add_argument("-d", '--debug', action='store_true',help="shows what the program sees (also good for debugging)")
    arg_parser.add_argument("-p", "--profile", action='store_true', help="cprofile the parsing")
    
    args = arg_parser.parse_args()
    
    if args.profile:
        print("|profiling...|")
        cProfile.runctx("Parser(args.path, args.debug).parse_shapes()", globals(), locals(), sort="tottime")
        print("|profiled!|")
        exit()

    path = args.path

    if args.path[-4:] != ".png":
        path = args.path+".png"
        
    print(f"|parsing {path}...|")
    parser = Parser(path, args.debug)
    parse_start = time()
    shapes = parser.parse_shapes()
    parse_end = time()
    print(f"|parsed! {round(parse_end-parse_start, 3)} seconds elapsed|")
    if args.debug:
        print(f"|shapes found: {[f'{s.get_shape_type().name} : {[len(h.points) for h in s.get_holes()]}' for s in shapes if s.outer is None]}|")
    print("--------------------------------------")
    t=args.time
    if args.time is None:
        t=0

    interpreter = Interpreter(shapes, args.verbose, t)
    interpreter.run()


if __name__ == "__main__":
    main()
