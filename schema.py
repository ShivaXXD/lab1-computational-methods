# Модель: Математичне моделювання та аналіз струмів у електричних колах постійного струму за законами Кірхгофа (5 семестр)
# Автор: Власійчук Данило АІ-235

!pip install schemdraw

import schemdraw
import schemdraw.elements as elm
from IPython.display import display

# ---------------------------
# СЦЕНАРІЙ 1
# ---------------------------
def draw_scenario_1_fixed():
    d = schemdraw.Drawing(unit=3)

    N0 = (0, 4)
    N1 = (-3, 0)
    N2 = (3, 0)
    N3_GND = (0, -4)

    d += elm.Dot(label='0').at(N0)
    d += elm.Dot(label='1').at(N1)
    d += elm.Dot(label='2').at(N2)
    d += elm.Ground().at(N3_GND).label('3 (GND)')

    d += elm.Line().at(N0).tox(N0[0] - 5)
    d += elm.SourceV(E=10, R=0.01).down().toy(N3_GND).label('E=10V\nR=0.01Ω', loc='left')
    d += elm.Line().tox(N3_GND)

    d += elm.Resistor(R=100).at(N0).to(N1).label('100Ω')
    d += elm.Resistor(R=150).at(N1).to(N3_GND).label('150Ω')
    d += elm.Resistor(R=250).at(N0).to(N2).label('250Ω')
    d += elm.Resistor(R=300).at(N2).to(N3_GND).label('300Ω')
    d += elm.Resistor(R=50).at(N1).to(N2).label('50Ω', loc='bottom')

    d += elm.Label("Рисунок 1 - Схема для Сценарію 1", fontsize=16).at((-3, 6))

    return d


# ---------------------------
# СЦЕНАРІЙ 2
# ---------------------------
def draw_scenario_2_fixed():
    d = schemdraw.Drawing(unit=3)

    N0 = (-3, 4)
    N1 = (3, 4)
    N2_GND = (0, 0)

    d += elm.Dot(label='0').at(N0)
    d += elm.Dot(label='1').at(N1)
    d += elm.Ground().at(N2_GND).label('2 (GND)')

    d += elm.Line().at(N0).down().length(1)
    d += elm.Resistor(R=1).down().label('1Ω')
    d += elm.SourceV(E=10).down().label('10V')
    d += elm.Line().to(N2_GND)

    d += elm.Line().at(N1).down().length(1)
    d += elm.Resistor(R=2).down().label('2Ω')
    d += elm.SourceV(E=20).down().label('20V')
    d += elm.Line().to(N2_GND)

    d += elm.Resistor(R=5).at(N0).to(N1).label('5Ω')

    d += elm.Label("Рисунок 2 - Схема для Сценарію 2", fontsize=16).at((-3, 6))

    return d


# ---------------------------
# СЦЕНАРІЙ 3
# ---------------------------
def draw_scenario_3_fixed():
    d = schemdraw.Drawing(unit=3)

    N0 = (0, 8)
    N1 = (6, 8)
    N2 = (6, 4)
    N3 = (0, 4)
    N4_GND = (3, 0)

    d += elm.Dot(label='0').at(N0)
    d += elm.Dot(label='1').at(N1)
    d += elm.Dot(label='2').at(N2)
    d += elm.Dot(label='3').at(N3)
    d += elm.Ground().at(N4_GND).label('4 (GND)')

    d += elm.Line().at(N0).tox(N0[0]-3)
    d += elm.SourceV(E=50).down().toy(N4_GND).label('E=50V', loc='left')
    d += elm.Resistor(R=1).label('1Ω', loc='left')
    d += elm.Line().to(N4_GND)

    d += elm.Resistor(R=10).at(N0).to(N1).label('10Ω')
    d += elm.Resistor(R=20).at(N0).to(N2).label('20Ω', loc='bottom')
    d += elm.Resistor(R=5).at(N1).to(N2).label('5Ω')
    d += elm.Resistor(R=15).at(N1).to(N3).label('15Ω')
    d += elm.Resistor(R=30).at(N2).to(N3).label('30Ω')
    d += elm.Resistor(R=25).at(N3).to(N4_GND).label('25Ω')

    d += elm.Line().at(N1).tox(N1[0]+3)
    d += elm.Resistor(R=40).down().toy(N4_GND).label('40Ω', loc='right')
    d += elm.Line().to(N4_GND)

    d += elm.Line().at(N2).tox(N2[0]+1.5)
    d += elm.SourceV(E=10).reverse().label('E=-10V', loc='right').down().toy(N4_GND)
    d += elm.Resistor(R=10).label('10Ω', loc='right')
    d += elm.Line().to(N4_GND)

    d += elm.Resistor(R=50).at(N0).to(N3).label('50Ω')

    d += elm.Label("Рисунок 3 - Схема для Сценарію 3", fontsize=16).at((0, 10))

    return d


# ---------------------------
# ВИВЕДЕННЯ Й ЗБЕРЕЖЕННЯ
# ---------------------------

# Схема 1
d1 = draw_scenario_1_fixed()
display(d1.draw())
d1.save("scenario_1.png")

# Схема 2
d2 = draw_scenario_2_fixed()
display(d2.draw())
d2.save("scenario_2.png")

# Схема 3
d3 = draw_scenario_3_fixed()
display(d3.draw())
d3.save("scenario_3.png")

print("Готово! Файли збережено:")
print("scenario_1.png")
print("scenario_2.png")
print("scenario_3.png")
