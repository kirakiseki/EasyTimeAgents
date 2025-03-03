import pandas as pd
import re


def time_series_format_checker_tool(path: str) -> str:
    if path == "NO_UPLOAD_FILE":
        return "分析失败：无法获取上传的文件，请检查文件路径。"

    try:
        df = pd.read_csv(path)
    except Exception as e:
        return f"分析失败：上传的文件无法读取，请检查文件路径和文件格式。错误信息：{str(e)}"

    if df.empty:
        return "分析失败：上传的文件为空，请检查文件内容。"

    columns = df.columns.tolist()
    if len(columns) < 1 or columns[0].lower() != "date":
        return '分析失败：非法的时间序列数据格式，请确保第一列为日期列且名称为"date"。'

    if len(columns) < 2:
        return "分析失败：非法的时间序列数据格式，请确保至少有两列数据。"

    if not pd.to_datetime(df[columns[0]], errors="coerce").notnull().all():
        return "分析失败：日期列格式错误，请确保日期列的格式为合法的日期格式。"

    def get_time_freq_chinese_desc(series: pd.Series) -> str:
        freq_str = pd.infer_freq(series).upper()
        diff = pd.to_datetime(df[columns[0]], errors="coerce").diff().mode()[0]

        if not freq_str and not diff:
            return "无法推断数据频率"

        unit_mapping = {"H": "小时", "D": "天", "M": "月", "T": "分钟", "S": "秒"}

        # "15T" → 15 + T
        match = re.match(r"^(\d*)([A-Za-z]+)$", freq_str)
        if not match:
            return freq_str

        num_part, unit_part = match.groups()

        chinese_unit = unit_mapping.get(unit_part, unit_part)

        if num_part:
            return f"{num_part}{chinese_unit} ({diff})"
        else:
            return f"{chinese_unit} ({diff})"

    report = f"""数据分析成功！    
此文件是一个合法的时间序列数据文件，
数据集共包含{len(df)}行数据，时间列为"{columns[0]}"，时间范围为"{df[columns[0]].min()}至{df[columns[0]].max()}，数据频率为"{get_time_freq_chinese_desc(df[columns[0]])}"。
"""
    data_columns = columns[1:]
    if len(data_columns) == 1:
        report += f'时间序列数据类型为单变量时间序列数据（Univariate Time Series），共有1个数据列为"{data_columns[0]}"。'
    else:
        if len(set(data_columns)) != len(data_columns):
            return "时间序列数据列名重复，请确保每一列数据的列名唯一。"
        report += f'时间序列数据类型为多变量时间序列数据（Multivariate Time Series），共有{len(data_columns)}个数据列为"{'", "'.join(data_columns)}"。'

    return report
