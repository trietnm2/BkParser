from py4j.java_gateway import JavaGateway

BKPARSER_JAR = "BKParser-1.0.jar"


def get_bkparser(jar_file):
    gateway = JavaGateway.launch_gateway(classpath=jar_file, die_on_exit=True)
    parser = gateway.jvm.vn.edu.hust.nlp.parser.BKParser()
    return parser


class BKParser:
    def __init__(self, jar_file=BKPARSER_JAR):
        try:
            self.__model = get_bkparser(jar_file)
        except:
            raise RuntimeError("Can not init model. Check log file!")

    def parse(self, txt):
        result = []
        res = self.__model.parse(text)
        for tokenList in res:
            for token in tokenList:
                # CoNLL-U Format
                # https://universaldependencies.org/format.html
                # id, form, lemma, uPOSTag, xPOSTag, feats, head, depRel, deps, misc
                line = token.toString()
                if line == '':
                    continue
                result.append(line.split("\t"))
        return result


if __name__ == '__main__':
    parser = BKParser()
    text = 'Cuối cùng, đoàn quân của HLV Conte đã hoàn thành nhiệm vụ này khi vượt qua đối thủ với tỷ số 4-2'
    print(parser.parse(text))
