import argparse
import ptj_parse
import ptj_generator

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="File that contain Java code.")
    parser.add_argument("-o", "--output", help="Where translated code will be saved.", default='out.py')
    parser.add_argument("-n", "--type_from_name",
                        help="When this option is specified, type is presumed based on identifiers.",
                        action='store_true')
    parser.add_argument("-s", "--translate_super",
                        help="Translate 'super' functions in python to their Java counterparts.", action='store_true')

    args = parser.parse_args()

    with file(args.input) as f:
        code = f.read()
        program = ptj_parse.generateProgram(code)
        g = ptj_generator.Generator(args.output, args.type_from_name)
        g.generateJavaCode(program)

    print args
