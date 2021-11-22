## La classe Règle

class Regle:
    conclusion = []

    def __init__(self, premises, conclusion):
        self.premises = premises
        self.conclusion = conclusion
        self.ruleID = 0

    def afficher(self):
        i = 0
        prem = ''
        while i < len(self.premises):
            prem += self.premises[i] + ' ,'
            i += 1
        print(f'si {prem} alors {self.conclusion}')


## La classe Fait

class Fait:  # class Fait
    def __init__(self, fait):
        self.fait = fait
        self.flag = -1

    def afficher(self):
        print(self.fait, ' ,explication: ', self.flag)


def remove_et(l):  # supprimer 'et' de chaque règle
    f = l.split()
    while 'et' in f:
        f.remove('et')
    return f


# récuperer la base des règles à partir d'un fichier texte
def BR_parsing(path):
    BR = []
    with open(path, mode="r") as file:
        lines = file.readlines()
    lines = [line.strip('\n') for line in lines]
    i = 0
    while i < len(lines):
        prems = remove_et(lines[i].split('alors')[0])  # recuperer les premisses
        prems.remove('si')
        prems.pop(0)
        con = remove_et(lines[i].split('alors')[1])  # recuperer la conclusion
        r = Regle(prems, con)
        r.ruleID = i + 1
        BR.append(r)
        i += 1
    return BR


def BF_parsing(path):  # recupérer la base des faits à partir d'un fichier texte
    BF = []
    with open(path, mode="r") as file:
        lines = file.readlines()
    lines = [line.strip('\n') for line in lines]
    i = 0
    while i < len(lines):
        l = lines[i].split().pop(1).split(',')
        j = 0
        while j < len(l):
            f = Fait(l[j])
            BF.append(f)
            j += 1
        i += 1
    return BF


def applicable_rules(BR, temp):  # filtrer BR pour avoir la liste des regles applicables
    app_rule_list = []
    r = 0
    for r in range(len(BR)):
        r_premises = BR[r].premises
        p = 0
        for p in range(len(r_premises)):
            test = r_premises[p] in temp  # p est dans la base des faits
            if test == False:
                break
        app_rule_list.append(test)
    return app_rule_list


# extract a list of all unique premises and conclusions and facts, c'est l'etat de la base saturee
def unique_list(BR, temp):
    i = 0
    l = temp.copy()  # temp est la base des faits initiale
    while i < len(BR):
        rule = BR[i]
        for p in range(len(rule.premises)):
            if ((rule.premises[p] in temp) == False) & ((rule.premises[p] in l) == False):
                l.append(rule.premises[p])
        for c in range(len(rule.conclusion)):
            if ((rule.conclusion[c] in temp) == False) & ((rule.conclusion[c] in l) == False):
                l.append(rule.conclusion[c])
        i += 1
    return l


def forward_chaining(BR, BF, temp, but, conf_res):
    i = 0  # nombre d'itération
    ul = unique_list(BR, temp)
    l = []
    with open('trace.txt', mode="w", encoding='utf-8') as trace:
        applicable_rules_list = applicable_rules(BR, temp)
        if not (any(applicable_rules_list)):
            l.append("impossible d'avancer, aucune règle est applicable")
            trace.writelines(l)
            return False
        while any(applicable_rules_list):
            i += 1
            if conf_res == '2':
                rule_index = len(applicable_rules_list) - 1 - applicable_rules_list[::-1].index(True)
            else:
                rule_index = applicable_rules_list.index(True)
            ##########################ajouter la conclusion à la base des faits###########################################################
            for j in range(len(BR[rule_index].conclusion)):
                new_fait = Fait(BR[rule_index].conclusion[j])
                new_fait.flag = BR[rule_index].ruleID
                if new_fait.fait in temp:
                    continue
                BF.append(new_fait)
                temp.append(new_fait.fait)
            ################################### ecriture dans le fichier trace ####################################################
            l.append('le numéro correspondant à la règle appliquée est : ' + str(BR[rule_index].ruleID) + '\n')
            l.append("le numéro de l'itération est  " + str(i) + ' ,voici la nouvelle BF : ' + '\n')
            l.append('[' + ' , '.join(temp) + ']' + '\n')
            l.append('----------------------- \n')
            print('règle appliqué : ', BR[rule_index].ruleID)
            print('itération num ', i, ',nouvelle BF : ')
            print(temp)
            # verifier si le but est atteint
            if len(temp) == len(ul):
                print(' la base est saturée ')
                l.append(' la base est saturée ')
                print('---------------------------')
            if but in temp:
                l.append(' but atteint ')
                trace.writelines(l)
                return True  # exit si on atteint le but
            del BR[rule_index]  # deleting the used rule
            applicable_rules_list = applicable_rules(BR, temp)
            if not (any(applicable_rules(BR, temp))):
                l.append(" impossible d'avancer ")
                trace.writelines(l)
                return False


def concluding_rules(BR, but):  # les regles qui concluent sur le but
    rule_list = []
    for i in range(len(BR)):
        r_conclusions = BR[i].conclusion
        if but in r_conclusions:
            rule_list.append(BR[i])
    return rule_list


def prouver(regle, BF, temp, BR, conf_res):
    proved = True
    for p in regle.premises:
        if p not in temp:
            proved = backward_chaining(BR, BF, temp, p, conf_res)
            if not proved:
                break
    return proved


def backward_chaining(BR, BF, temp, but, conf_res):
    i = 0  # nombre d'itération
    l = []
    ul = unique_list(BR, temp)
    with open('trace.txt', mode="a", encoding='utf-8') as trace:
        regles = concluding_rules(BR, but)
        #### conflict resolution ###
        if conf_res == '2':  # last first
            regles.reverse()
        elif conf_res == '3':  # most premises
            regles.sort(key=lambda r: len(r.premises), reverse=True)
        # else normal order
        for rule in regles:
            i += 1
            ##########################prouver les regles###########################################################
            satisfied = prouver(rule, BF, temp, BR, conf_res)
            if satisfied:
                # Ajouter ses conclusions au BF
                for c in rule.conclusion:
                    new_fait = Fait(c)
                    new_fait.flag = rule.ruleID
                    if new_fait.fait in temp:
                        continue
                    temp.append(new_fait.fait)
                    BF.append(new_fait)
                ################################### ecriture dans le fichier trace ####################################################
                l.append('le numéro correspondant à la règle appliquée est : ' + str(rule.ruleID) + '\n')
                l.append("le numéro de l'itération est  " + str(i) + ' ,voici la nouvelle BF : ' + '\n')
                l.append('[' + ' , '.join(temp) + ']' + '\n')
                l.append('----------------------- \n')
                print('règle appliqué : ', rule.ruleID)
                print('itération num ', i, ',nouvelle BF : ')
                print(temp)
            if but in temp:
                trace.writelines(l)
                return True

        if len(temp) == len(ul):
            print(' la base est saturée ')
            l.append(' la base est saturée ')
            print('---------------------------')
        trace.writelines(l)
        return False
