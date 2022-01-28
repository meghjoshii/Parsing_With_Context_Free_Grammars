"""
COMS W4705 - Natural Language Processing
Homework 2 - Parsing with Context Free Grammars 
Yassine Benajiba
"""

import math
import sys
from collections import defaultdict
from math import fsum
from types import DynamicClassAttribute

class Pcfg(object): 
    """
    Represent a probabilistic context free grammar. 
    """

    def __init__(self, grammar_file): 
        self.rhs_to_rules = defaultdict(list)
        self.lhs_to_rules = defaultdict(list)
        self.startsymbol = None 
        self.read_rules(grammar_file)      
 
    def read_rules(self,grammar_file):
        
        for line in grammar_file: 
            line = line.strip()
            if line and not line.startswith("#"):
                if "->" in line: 
                    rule = self.parse_rule(line.strip())
                    lhs, rhs, prob = rule
                    self.rhs_to_rules[rhs].append(rule)
                    self.lhs_to_rules[lhs].append(rule)
                else: 
                    startsymbol, prob = line.rsplit(";")
                    self.startsymbol = startsymbol.strip()
                    
     
    def parse_rule(self,rule_s):
        
        lhs, other = rule_s.split("->")
        lhs = lhs.strip()
        rhs_s, prob_s = other.rsplit(";",1) 
        prob = float(prob_s)
        rhs = tuple(rhs_s.strip().split())
        return (lhs, rhs, prob)


    def verify_grammar(self):
        total_probability = float(0.0)

        for nonterminal in self.lhs_to_rules:
            if not nonterminal.isupper():
                return False

        for prod in self.lhs_to_rules[nonterminal]:
            prod_rule = prod[1]

            if len(prod_rule) > 2 or len(prod) < 1:
                return False

            if len(prod_rule) == 2:
                if not (prod_rule[0].isupper() and prod_rule[1].isupper()):
                    return False

            if len(prod_rule) == 1:
                if prod_rule[0] in self.lhs_to_rules:
                    return False

            for prod_triplet in self.lhs_to_rules[nonterminal]:
                total_probability = total_probability + prod_triplet[2]

            if not math.isclose(total_probability, float(1.0), abs_tol=0.0001):
                return False
                
        return True



if __name__ == "__main__":
    with open(sys.argv[1],'r') as grammar_file:
        grammar = Pcfg(grammar_file)
        a = grammar.verify_grammar()
        print(a)
