from adjective import Adjective
from fsets.polygon import Polygon
from fsets.gaussian import Gaussian
from fsets.trapezoid import Trapezoid
from ruleblock import RuleBlock
from systems.tsukamoto import TsukamotoSystem
from variable import Variable
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import random
def DrawVarFuncs(fs, interval, labs, title):
    fig = plt.figure(figsize=(10, 6))
    x = np.linspace(interval[0], interval[1], 1000)
    for i in range(len(labs)):
        
        y = [fs[i](j) for j in x]
        plt.plot(x, y, label=labs[i])
    plt.legend()
    plt.xlabel(title)
    plt.ylabel("степень принадлежности")
    pdf = PdfPages('img/variable_' + title + ".pdf")
    pdf.savefig(fig)
    pdf.close()
    plt.clf()
def DrawResult(n_it, auto_velocities, leader_velocities):
    fig = plt.figure(figsize=(10, 6))
    x = [i for i in range(n_it)]

    plt.plot(x, auto_velocities, label='автопилот')
    plt.plot(x, leader_velocities, label='лидер')

    plt.grid()
    plt.xlabel("Модельное время")
    plt.ylabel("Скорость, м/с")

    plt.legend()
    pdf = PdfPages('img/' + "result_" + str(n_it) + "_iters.pdf")
    pdf.savefig(fig)
    pdf.close()
    plt.clf()
def PrintResultTable(iters, times, stds):
    for i in range(len(iters)):
        print("\hline {} & {:.2f} & {:.2f} \\\\".format(iters[i], times[i], stds[i]))
def CreateSystem():
    # Определение переменных
    ## distance
    less_func = Gaussian(25, 30)
    less = Adjective('less', less_func )
    normal_func = Gaussian(100, 15)
    normal = Adjective('normal', normal_func )
    more_func = Gaussian(175, 30)
    more = Adjective('more', more_func )
    
    distance = Variable('distance', 'km', less, normal, more)
    DrawVarFuncs([less_func, normal_func, more_func],
                  [-50, 250],
                  ['less', 'normal', 'more'],
                  'distance')

    ## distance_change
    to_leader_func = Gaussian(-50, 20)
    to_leader = Adjective('to_leader', to_leader_func )
    same_func = Gaussian(0, 10)
    same = Adjective('same', same_func )
    from_leader_func = Gaussian(50,20)
    from_leader = Adjective('from_leader', from_leader_func )
    
    distance_change = Variable('distance_change', 'km', to_leader, same, from_leader )
    
    DrawVarFuncs([to_leader_func, same_func, from_leader_func],
                  [-100, 100],
                  ['to_leader', 'same', 'from_leader'],
                  'distance_change')

    
    ## autopilot_control
    slowdown_func = Polygon((-50,1), (-25,1), (-5,0))
    slowdown = Adjective('slowdown', slowdown_func )
    maintain_speed_func = Trapezoid((-10,0), (-5,1), (5,1), (10,0))
    maintain_speed = Adjective('maintain_speed',  maintain_speed_func)
    speed_up_func = Polygon((5,0), (25,1), (50,1))
    speed_up = Adjective('speed_up',speed_up_func)
          
    autopilot_control = Variable('autopilot_control', 'km', slowdown, maintain_speed, speed_up)
    DrawVarFuncs([slowdown_func, maintain_speed_func, speed_up_func],
                  [-50, 50],
                  ['slowdown', 'maintain_speed', 'speed_up'],
                  'autopilot_control')
    scope = locals()

    # Создание блока правил
    block = RuleBlock('autopilot_control', operators=('MIN', 'MAX', 'ZADEH'), activation='MAX')

    r1 = 't:if distance is less then autopilot_control is slowdown'
    r2 = 't:if distance_change is to_leader and distance is normal then autopilot_control is slowdown'
    r3 = 't:if distance_change is same and distance is normal then autopilot_control is maintain_speed'
    r4 = 't:if distance_change is from_leader and distance is normal then autopilot_control is speed_up'
    r5 = 't:if distance is more then autopilot_control is speed_up'
    
    block.add_rules(r1, r2, r3, r4, r5, scope = scope)
    # Создание системы
    tsukamoto = TsukamotoSystem('auto_pilot_system', block)
    return tsukamoto


#n_it_arr = list(map(int, np.linspace(20, 500, 50)))

n_it_arr = [10, 100,200, 500, 1000]
time_work = []
std_arr = []

dt = 1 
initial_distance = 50
initial_auto_velocity = 20 
initial_leader_velocity = 50

leader_velocities = []
auto_velocities = []
system = CreateSystem()
for n_it in n_it_arr:
    time_start = time.time()
    leader_velocities = initial_leader_velocity + 20 * np.sin(np.linspace(0, 10, n_it))
    #leader_velocities = [initial_leader_velocity] * n_it
    
    auto_velocities = []
    
    prev_distance = cur_distance = initial_distance
    cur_velocity = initial_auto_velocity

    for i in range(n_it):
        auto_velocities.append(cur_velocity)
        velocity_change = system.compute({'distance': cur_distance, 'distance_change': cur_distance - prev_distance})['autopilot_control']

        cur_velocity += velocity_change

        prev_distance = cur_distance
        cur_distance += (leader_velocities[i] - cur_velocity) * dt

    time_work.append(time.time() - time_start)
    std_arr.append(np.sqrt(np.std(np.array(auto_velocities) - np.array(leader_velocities))))

    DrawResult(n_it, auto_velocities, leader_velocities)
##fig = plt.figure(figsize=(10, 6))
##plt.plot(n_it_arr, time_work)
##plt.xlabel("Модельное время")
##plt.ylabel("Реальное время (с)")
##pdf = PdfPages('img/' + "result_time.pdf")
##pdf.savefig(fig)
##pdf.close()
##plt.clf()
##
##fig = plt.figure(figsize=(10, 6))
##plt.plot(n_it_arr, std_arr)
##plt.xlabel("Модельное время")
##plt.ylabel("СКО")
##pdf = PdfPages('img/' + "result_std.pdf")
##pdf.savefig(fig)
##pdf.close()
##plt.clf()
PrintResultTable(n_it_arr, time_work, std_arr)


