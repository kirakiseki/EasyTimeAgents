from langchain_core.tools import BaseTool

from .jupyter_kernel import JupyterKernel

kernel = JupyterKernel(".")


class JupyterNotebook(BaseTool):
    """
    可以执行Python代码片段的代码执行工具，用于数据分析和可视化任务
    """

    name: str = "Python代码执行工具"
    description: str = (
        "一个专为准确执行数据分析和可视化任务而优化的Python代码执行工具"
        "用于执行执行数据分析和可视化任务的Python代码片段，包含Pandas、Numpy和Matplotlib等常见的数据分析库。"
        "代码将会使用Jupyter Notebook的方式执行，代码上下文在执行后会被保留。"
        "为了更好的渲染表格数据，请使用df.to_markdown()方法将Pandas DataFrame转换为Markdown格式输出。"
    )

    def _run(
        self,
        code: str,
    ) -> str:

        code = (
            """
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import scipy.stats as stats

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

"""
            + code
        )

        result, _ = kernel.execute_code(code)
        return result
