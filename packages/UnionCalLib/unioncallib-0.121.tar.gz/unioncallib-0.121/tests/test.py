import importlib.util
import sys

# 模块路径
module_path = "/Users/yukyulai/Downloads/ChemCal/ChemUtil/main_library/equation.py"

# 加载模块
spec = importlib.util.spec_from_file_location("equation", module_path)
equation = importlib.util.module_from_spec(spec)
sys.modules["equation"] = equation

spec.loader.exec_module(equation)
eq = equation

eq.add_reactant("Cl2")
eq.add_product("HCIO")
eq.add_product("HCI")
eq.add_reactant("H2O")
eq.balance()