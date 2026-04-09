import numpy as np
import time

class CircuitSimulator:
    def __init__(self, num_nodes, components):
        self.num_equations = num_nodes - 1
        self.num_nodes_total = num_nodes
        self.components = components
        self.reference_node = num_nodes - 1
        self.G_matrix = np.zeros((self.num_equations, self.num_equations))
        self.I_vector = np.zeros(self.num_equations)

    def build_system_equations(self):
        for comp in self.components:
            n1, n2, R, E = comp
            if R <= 0:
                continue
            g = 1.0 / R
            I_eq = E * g
            if n1 != self.reference_node:
                self.G_matrix[n1, n1] += g
            if n2 != self.reference_node:
                self.G_matrix[n2, n2] += g
            if n1 != self.reference_node and n2 != self.reference_node:
                self.G_matrix[n1, n2] -= g
                self.G_matrix[n2, n1] -= g
            if n1 != self.reference_node:
                self.I_vector[n1] += I_eq
            if n2 != self.reference_node:
                self.I_vector[n2] -= I_eq

    def solve_nodal_voltages(self):
        self.fixed_build_system_equations()
        try:
            node_voltages_calc = np.linalg.solve(self.G_matrix, self.I_vector)
            all_node_voltages = np.append(node_voltages_calc, 0.0)
            return all_node_voltages
        except np.linalg.LinAlgError:
            return None

    def calculate_branch_currents(self, node_voltages):
        if node_voltages is None:
            return []
        currents = []
        for i, comp in enumerate(self.components):
            n1, n2, R, E = comp
            if R <= 0:
                currents.append(float('nan'))
                continue
            V1 = node_voltages[n1]
            V2 = node_voltages[n2]
            current = (V1 - V2 + E) / R
            currents.append(current)
        return currents

    def fixed_build_system_equations(self):
        for comp in self.components:
            n1, n2, R, E = comp
            if R <= 0:
                continue
            g = 1.0 / R
            I_eq = E * g
            if n1 != self.reference_node:
                self.G_matrix[n1, n1] += g
            if n2 != self.reference_node:
                self.G_matrix[n2, n2] += g
            if n1 != self.reference_node and n2 != self.reference_node:
                self.G_matrix[n1, n2] -= g
                self.G_matrix[n2, n1] -= g
            if n1 != self.reference_node:
                self.I_vector[n1] -= I_eq
            if n2 != self.reference_node:
                self.I_vector[n2] += I_eq

    def calculate_power_balance(self, node_voltages, currents):
        if node_voltages is None or not currents or len(currents) != len(self.components):
            return None, None, None
        total_power_generated = 0.0
        total_power_dissipated = 0.0
        for i, comp in enumerate(self.components):
            _, _, R, E = comp
            current = currents[i]
            if np.isnan(current):
                continue
            if E != 0:
                total_power_generated += E * current
            if R > 0:
                total_power_dissipated += (current**2) * R
        balance_error = total_power_generated - total_power_dissipated
        if total_power_generated == 0:
            relative_error_percent = 0.0
        else:
            relative_error_percent = (abs(balance_error) / abs(total_power_generated)) * 100
        return total_power_generated, total_power_dissipated, balance_error, relative_error_percent

def run_scenario(name, num_nodes, components):
    print(f"\n--- ЗАПУСК СЦЕНАРІЮ: {name} ---")
    start_time = time.perf_counter()
    simulator = CircuitSimulator(num_nodes, components)
    voltages = simulator.solve_nodal_voltages()
    currents = simulator.calculate_branch_currents(voltages)
    p_gen, p_diss, p_err_abs, p_err_rel = simulator.calculate_power_balance(voltages, currents)
    end_time = time.perf_counter()
    calc_time_ms = (end_time - start_time) * 1000
    print(f"Потенціали: {['{:.4f}V'.format(v) for v in voltages]}")
    print(f"Струми: {['{:.4f}A'.format(c) for c in currents]}")
    print(f"--- Валідація: {name} ---")
    if p_gen is not None:
        print(f"P (джерел, E*I):    {p_gen:.6f} Вт")
        print(f"P (навантаж., I^2*R): {p_diss:.6f} Вт")
        print(f"Абсолютна похибка: {p_err_abs:.2e} Вт")
        print(f"Відносна похибка:  {p_err_rel:.2e} %")
    print(f"Час обчислення: {calc_time_ms:.4f} мс")
    print(f"--- ЗАВЕРШЕННЯ СЦЕНАРІЮ: {name} ---")
    return {
        "name": name,
        "time_ms": calc_time_ms,
        "power_balance_error_percent": p_err_rel,
        "nodes": num_nodes,
        "branches": len(components)
    }

if __name__ == "__main__":
    print("="*50)
    print("=== ЗАПУСК ПОВНОГО (ВИПРАВЛЕНОГО) СКРИПТУ ===")
    print("="*50)
    results = []
    num_nodes_s1 = 4
    components_s1 = [
        (0, 3, 0.01, 10),
        (0, 1, 100, 0),
        (1, 3, 150, 0),
        (0, 2, 250, 0),
        (2, 3, 300, 0),
        (1, 2, 50, 0)
    ]
    results.append(run_scenario("Сценарій 1 (Міст)", num_nodes_s1, components_s1))
    num_nodes_s2 = 3
    components_s2 = [
        (0, 2, 1, 10),
        (1, 2, 2, 20),
        (0, 1, 5, 0)
    ]
    results.append(run_scenario("Сценарій 2 (3 вузли)", num_nodes_s2, components_s2))
    num_nodes_s3 = 5
    components_s3 = [
        (0, 4, 1, 50),
        (0, 1, 10, 0),
        (0, 2, 20, 0),
        (1, 2, 5, 0),
        (1, 3, 15, 0),
        (2, 3, 30, 0),
        (3, 4, 25, 0),
        (1, 4, 40, 0),
        (2, 4, 10, -10),
        (0, 3, 50, 0)
    ]
    results.append(run_scenario("Сценарій 3 (5 вузлів)", num_nodes_s3, components_s3))
    print("\n\n" + "="*50)
    print("=== РЕЗУЛЬТАТИ ДЛЯ ПОРІВНЯЛЬНОЇ ТАБЛИЦІ (Markdown) ===")
    print("="*50)
    header = "| Параметр |"
    divider = "| :--- |"
    for res in results:
        header += f" {res['name']} |"
        divider += " :--- |"
    print(header)
    print(divider)
    print(f"| К-сть вузлів | {results[0]['nodes']} | {results[1]['nodes']} | {results[2]['nodes']} |")
    print(f"| К-сть гілок | {results[0]['branches']} | {results[1]['branches']} | {results[2]['branches']} |")
    print(f"| Точність балансу потужності, % | {results[0]['power_balance_error_percent']:.2e} | {results[1]['power_balance_error_percent']:.2e} | {results[2]['power_balance_error_percent']:.2e} |")
    print(f"| Час обчислення, мс | {results[0]['time_ms']:.4f} | {results[1]['time_ms']:.4f} | {results[2]['time_ms']:.4f} |")
