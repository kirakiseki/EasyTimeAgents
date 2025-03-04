from .main import characteristic_extractor, CharacteristicExtractResult

from langchain_core.tools import BaseTool


class TimeSeriesCharacteristicsExtractorTool(BaseTool):
    """
    时间序列特征提取工具：可以提取时间序列数据的相关性、过渡、转移、季节性、趋势、平稳性特征。
    """

    name: str = "时间序列数据特征提取器"
    description: str = (
        "一个专为提取时间序列数据的关键特征（相关性、过渡、转移、季节性、趋势、平稳性）而优化的时间序列特征提取工具"
        "输入应为时间序列数据文件路径。该工具将提取时间序列数据的关键特征，并提供有关数据模式和趋势的见解。"
    )

    def _run(
        self,
        file_path: str,
    ) -> CharacteristicExtractResult:

        return characteristic_extractor(file_path)
