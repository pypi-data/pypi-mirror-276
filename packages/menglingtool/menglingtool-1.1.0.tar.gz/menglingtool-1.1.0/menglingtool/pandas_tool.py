import pandas as pd
from pandas import DataFrame
_to_dict = DataFrame.to_dict
_to_excel = DataFrame.to_excel


def setGlobalCustomDF():
    def to_dict(self, orient="records"):
        return _to_dict(self, orient=orient)

    def to_excel(self, filename, index=False):
        return _to_excel(self, filename, index=index)

    DataFrame.to_dict = to_dict
    DataFrame.to_excel = to_excel


def defaultDF():
    DataFrame.to_dict = _to_dict
    DataFrame.to_excel = _to_excel


def merge_df_to_excel(filename: str, *dfs, sheets: list = None, index=False):
    if sheets is None: sheets = []
    # 名称补齐
    [sheets.append(f'Sheet{i}') for i in range(len(sheets) + 1, len(dfs) + 1)]

    writer = pd.ExcelWriter(filename)
    for df, sheet in zip(dfs, sheets):
        df.to_excel(writer, sheet_name=sheet, index=index)
    # writer.save()
    writer.close()


def merge_dts_to_excel(filename: str, *dtss, sheets: list = None, index=False):
    return merge_df_to_excel(filename, *[DataFrame(data=dts).fillna('') for dts in dtss], sheets=sheets, index=index)
