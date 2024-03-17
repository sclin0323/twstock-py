import os

# 通过环境变量获取Railway设置的变量值
variable_value = os.getenv("OKX_ACC1_API_KEY")

# 使用变量值
print("Variable value:", variable_value)