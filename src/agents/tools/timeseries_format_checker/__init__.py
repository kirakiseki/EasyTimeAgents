from langchain_core.tools import BaseTool
from .main import time_series_format_checker_tool


class TimeSeriesFormatCheckerTool(BaseTool):
    """
    时间序列数据格式检查器：用于对用户上传的CSV数据集文件进行检查，检查其是否属于时间序列数据，是单变量还是多变量时间序列数据等。
    """

    name: str = "时间序列数据格式检查器"
    description: str = (
        "用于对用户上传的CSV数据集文件进行检查，检查其是否属于时间序列数据，是单变量还是多变量时间序列数据等。"
        "输入中仅包含一个参数，file_path: 为用户上传的数据集文件路径，输出为对数据的纯文本分析报告"
    )

    def _run(
        self,
        file_path: str,
    ) -> str:

        return time_series_format_checker_tool(file_path)
