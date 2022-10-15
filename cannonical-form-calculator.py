'''
@author  : Nasrullah
@created : 13.10.2022
@github  : github.com/nasdevs
'''

import re
import os
import itertools
import pandas as pd
from IPython.display import display

class CannonicalForm:
    def rules(self):
        rules = '''
        Rules formula writing:
        proposition : only use letters
        A   : uppercase for proposition
        a   : lowercase for negation
        AND : use symbol . or & or nothing
        OR  : use symbol + or |
        Example formula:
        - (A+B')+C(A'+C'D') ❌
        - (A+b)+C(a+cd) ✔️
        - (A | b) | C(a|cd) ✔️
        - (A | b)+ C(a+c&d) ✔️
        '''

        print(re.sub(' {4,}', '', rules))

    def main(self):
        self.rules()
        while True:
            formula = re.sub('\s', '', str(input('Input formula : ')))
            if not re.search('[^a-zA-Z+.|&)(~]', formula): break
            os.system('cls')
            print(f'Invalid formula!')
            self.rules()
        
        elements = sorted(set(''.join(re.findall('[a-zA-Z]', formula.upper()))))

        combination = list(itertools.product([0, 1], repeat=len(elements)))
        ToT = pd.DataFrame(combination, columns=sorted(elements))

        operators = {
            '+': '|',
            '.': '&',
            '+(': '|(',
            ')+': ')|',
            '.(': '&(',
            ').': ')&',
            ')(': ')&(',
            ').(': ')&('
        }

        # normalization
        x = re.findall('[a-zA-Z][(]', formula)
        x.extend(re.findall('[)][a-zA-Z]', formula))

        literal = re.findall('[a-zA-Z]+', formula)
        term = re.findall('[^a-zA-Z]+', formula)

        normal_operation = formula
        for i in x:
            normal_operation = normal_operation.replace(i, '&'.join(list(i)))
        for i in term:
            normal_operation = normal_operation.replace(i, operators[i] if i in operators.keys() else i)
        for i in literal:
            if len(i) != 1:
                normal_operation = normal_operation.replace(i, '&'.join(list(i)))

        # add negation
        for col in elements:
            ToT[col.lower()] = ~ToT[col]+2

        # processing
        normal_operation_syntax = ''
        for i, x in enumerate(list(normal_operation)):
            normal_operation_syntax += 'ToT.'+x if x.isalpha() else x

        ToT[formula] = eval(normal_operation_syntax) 

        # SOP
        sop_result = ToT[formula] == 1
        sop_ToT = ToT[sop_result].loc[:, elements]
        sop_values = [''.join([element if val else element+"'" for element, val in zip(elements, vals)]) for vals in sop_ToT.values]

        sigma = sop_ToT.index.to_series().apply(lambda x: "m"+str(x)).values
        sop = pd.DataFrame(sop_ToT.index.to_series(), columns=['index']).set_index('index')
        sop['SOP'] = sop_values

        # POS
        pos_result = ToT[formula] == 0
        pos_ToT = ToT[pos_result].loc[:, elements]
        pos_values = [f'''({'+'.join([element if not val else element+"'" for element, val in zip(elements, vals)])})''' for vals in pos_ToT.values]

        pi = pos_ToT.index.to_series().apply(lambda x: "M"+str(x)).values
        pos = pd.DataFrame(pos_ToT.index.to_series(), columns=['index']).set_index('index')
        pos['POS'] = list(map(lambda x: re.sub('[)(]', '', x), pos_values))

        # Show Table of Truth
        print('=====Table of Truth=====')
        display(ToT)

        print('\n-----------SOP----------')
        display(ToT[sop_result])

        print('\n-----------POS----------')
        display(ToT[pos_result])

        # Converted
        print('\n=========Result=========')
        print('-----------SOP----------')
        print(f'Σ({" + ".join(sigma)})')
        print(f'Σ({", ".join(sigma).replace("m", "")})')
        print(f'SOP : {" + ".join(sop_values)}')

        print('\n-----------POS----------')
        print(f'Π({" . ".join(pi)})')
        print(f'Π({", ".join(pi).replace("M", "")})')
        print(f'POS : {" . ".join(pos_values)}')

if __name__ == '__main__':
    CannonicalForm().main()
