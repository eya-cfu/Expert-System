from Module import *
import sys, getopt


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "f:r:")
    except getopt.GetoptError:
        print('main.py -f <base_faits> -r <base_regles> \n choisir parmi les fichiers du dossier')
        sys.exit(2)
    BF = []
    BR = []
    for opt, arg in opts:
        if opt == '-f':
            BF = BF_parsing(arg)
        elif opt == '-r':
            BR = BR_parsing(arg)
        else:
            print('main.py -f <base_faits> -r <base_regles> \n choisir parmi les fichiers du dossier')
            sys.exit(2)

    print('La base des règles :')
    for i in range(len(BR)):
        print(BR[i].premises, ' ---> ', BR[i].conclusion, '; ruleID = ', BR[i].ruleID)
    print('_______________________________')

    temp = []
    for j in range(len(BF)):
        temp.append(BF[j].fait)
    print('La base des faits :')
    print(temp)
    print('_______________________________')
    but = input("donnez le but recherché:\n")

    conf_res = input('donnez la stratégie de résolution de conflits: first (1), last (2), most premises (3)\n')
    BR1 = BR.copy()
    BF1 = BF.copy()
    temp1 = temp.copy()
    l = []
    chaining = input('Forward Chaining (1) OR Backward Chaining (2) ?\n')
    with open('trace.txt', mode="w", encoding='utf-8') as trace:
        if but in temp1:
            print('le but est déja dans la liste intiale des faits')
            test = True
        elif chaining == '1':
            print('applying forward chaining')
            test = forward_chaining(BR1, BF1, temp1, but, conf_res)
        else:
            print('applying backward chaining')
            test = backward_chaining(BR1, BF1, temp1, but, conf_res)
        if test:
            l.append("but atteint")
            trace.writelines(l)
            print("but atteint")
        else:
            l.append("impossible d'avancer")
            trace.writelines(l)
            print("impossible d'avancer")


if __name__ == "__main__":
    main(sys.argv[1:])
