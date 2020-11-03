from py4j.java_gateway import JavaGateway

class Token:
    def __init__(self, conll):
        # CoNLL-U Format
        # https://universaldependencies.org/format.html
        # id, form, lemma, uPOSTag, xPOSTag, feats, head, depRel, deps, misc
        conll = conll.split("\t")
        self.id = conll[0]
        self.form = conll[1]
        self.lemma = conll[2]
        self.uPOSTag = conll[3]
        self.xPOSTag = conll[4]
        self.feats = conll[5]
        self.head = conll[6]
        self.depRel = conll[7]
        self.deps = conll[8]
        self.misc = conll[9]

class BKParser:
    def __init__(self, jar_file="BKParser-1.0.jar"):
        try:
            self.__model = self.get_bkparser(jar_file)
        except:
            raise RuntimeError("Can not init model. Check log file!")

    def get_bkparser(self, jar_file):
        gateway = JavaGateway.launch_gateway(classpath=jar_file, die_on_exit=True)
        parser = gateway.jvm.vn.edu.hust.nlp.parser.BKParser()
        return parser

    def parse(self, text):
        result = []
        res = self.__model.parse(text)
        for tokenList in res:
            for tokenC in tokenList:
                line = tokenC.toString()
                if line == '':
                    continue
                token = Token(line)
                result.append(token)
        return result


if __name__ == '__main__':
    parser = BKParser()
    text = 'Cuối cùng, đoàn quân của HLV Conte đã hoàn thành nhiệm vụ này khi vượt qua đối thủ với tỷ số 4-2'
    print(parser.parse(text))
