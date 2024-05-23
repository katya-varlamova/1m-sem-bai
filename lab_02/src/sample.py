
# This py is only to illustrate how to use fuzzython library

#region PYTHON CODE

from adjective import Adjective
from fsets.polygon import Polygon
from fsets.trapezoid import Trapezoid
from ruleblock import RuleBlock
from systems.tsukamoto import TsukamotoSystem
from variable import Variable


print('--- START ---')

# --- Variables ---


cold = Polygon((0,1), (15,1), (20,0))  # Rect.build_from((15,1), (20,0))
normal = Trapezoid((15,0), (20,1), (30,1), (35,0))
hot = Polygon((30,0), (35,1), (40,1))  # Rect.build_from((30,0), (35,1))

cold = Adjective('cold', cold)
normal = Adjective('normal', normal)
hot = Adjective('hot', hot)

temp = Variable('temp', '°C', cold, normal, hot)
#temp.value = 33


short = Polygon((0,1), (10,1), (15,0))
usual = Trapezoid((10,0), (15,1), (25,1), (30,0))
large = Polygon((25,0), (30,1), (40,1))

short = Adjective('short', short)
usual = Adjective('usual', usual)
large = Adjective('large', large)

time = Variable('time', 'min', short, usual, large, defuzzification='COG', default=0)


scope = locals()

rule1 = 'if temp is cold or temp is normal then time is short with 0.5'
rule2 = 'if temp is normal then time is usual'
rule3 = 'if temp is hot then time is large'

rule4 = 'if temp is cold then z = temp*0.1'
rule5 = 'if temp is normal then z=temp*0.3 + 1'
rule6 = 'if temp is hot then z=temp*0.6 + 2'



inputs = {'temp':33}

short = Adjective('short', Polygon((0,1), (15,1), (25,0)))
large = Adjective('large', Polygon((15,0), (25,1), (40,1)))

time = Variable('time', 'min', short, large, defuzzification='COG', default=0)
scope = locals()

block = RuleBlock('second', operators=('MIN', 'MAX', 'ZADEH'), activation='MIN')
block.add_rule('t:if temp is cold then time is short', scope)
block.add_rule('t:if temp is normal then time is large with 0.5', scope)
block.add_rule('t:if temp is hot then time is large', scope)

tsukamoto = TsukamotoSystem('tsk', block)
res = tsukamoto.compute(inputs)
print(res)
tsukamoto.dump('example_tsukamoto.txt')



