from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.list import (of_array, FSharpList, exists, to_array, map, collect, sort_by, length, head, iterate_indexed)
from ...fable_modules.fable_library.map_util import add_to_dict
from ...fable_modules.fable_library.reflection import enum_type
from ...fable_modules.fable_library.seq import (try_find, to_list)
from ...fable_modules.fable_library.string_ import (to_fail, printf)
from ...fable_modules.fable_library.types import Array
from ...fable_modules.fable_library.util import (IEnumerable_1, compare_primitives)
from ...fable_modules.fs_spreadsheet.Cells.fs_cell import FsCell
from ...fable_modules.fs_spreadsheet.Cells.fs_cells_collection import Dictionary_tryGet
from ...fable_modules.fs_spreadsheet.fs_address import (FsAddress__ctor_Z37302880, FsAddress)
from ...fable_modules.fs_spreadsheet.fs_column import FsColumn
from ...fable_modules.fs_spreadsheet.fs_worksheet import FsWorksheet
from ...fable_modules.fs_spreadsheet.Ranges.fs_range_address import FsRangeAddress__ctor_7E77A4A0
from ...fable_modules.fs_spreadsheet.Ranges.fs_range_base import FsRangeBase__Cell_Z3407A44B
from ...fable_modules.fs_spreadsheet.Tables.fs_table import FsTable
from ...Core.Table.composite_column import CompositeColumn
from ...Core.Table.data_map import (DataMap_addColumns_6369C010, DataMap_init, DataMap, DataMap__get_Table)
from ..AnnotationTable.arc_table import (Aux_List_groupWhen, classify_column_order)
from .data_map_column import (from_fs_columns, to_fs_columns)

helper_column_strings: FSharpList[str] = of_array(["Term Source REF", "Term Accession Number", "Data Format", "Data Selector Format"])

def group_columns_by_header(columns: FSharpList[FsColumn]) -> FSharpList[FSharpList[FsColumn]]:
    def f(c: FsColumn, columns: Any=columns) -> bool:
        v: str = c.Item(1).ValueAsString()
        def predicate(s: str, c: Any=c) -> bool:
            return v.find(s) == 0

        return not exists(predicate, helper_column_strings)

    return Aux_List_groupWhen(f, columns)


def try_data_map_table(sheet: FsWorksheet) -> FsTable | None:
    def predicate(t: FsTable, sheet: Any=sheet) -> bool:
        return t.Name.find("datamapTable") == 0

    return try_find(predicate, sheet.Tables)


def compose_columns(columns: IEnumerable_1[FsColumn]) -> Array[CompositeColumn]:
    def _arrow971(columns_2: FSharpList[FsColumn], columns: Any=columns) -> CompositeColumn:
        return from_fs_columns(columns_2)

    return to_array(map(_arrow971, group_columns_by_header(to_list(columns))))


def try_from_fs_worksheet(sheet: FsWorksheet) -> DataMap | None:
    try: 
        match_value: FsTable | None = try_data_map_table(sheet)
        if match_value is None:
            return None

        else: 
            t: FsTable = match_value
            return DataMap_addColumns_6369C010(compose_columns(t.GetColumns(sheet.CellCollection)), True)(DataMap_init())


    except Exception as err:
        arg: str = sheet.Name
        arg_1: str = str(err)
        return to_fail(printf("Could not parse datamap table with name \"%s\":\n%s"))(arg)(arg_1)



def to_fs_worksheet(table: DataMap) -> FsWorksheet:
    string_count: Any = dict([])
    ws: FsWorksheet = FsWorksheet("isa_datamap")
    if len(DataMap__get_Table(table).Columns) == 0:
        return ws

    else: 
        def _arrow972(column_1: CompositeColumn, table: Any=table) -> FSharpList[FSharpList[FsCell]]:
            return to_fs_columns(column_1)

        def _arrow973(column: CompositeColumn, table: Any=table) -> enum_type("ARCtrl.Spreadsheet.ArcTable.ColumnOrder", int, [("InputClass", 1.0), ("ProtocolClass", 2.0), ("ParamsClass", 3.0), ("OutputClass", 4.0)]):
            return classify_column_order(column)

        class ObjectExpr974:
            @property
            def Compare(self) -> Callable[[enum_type("ARCtrl.Spreadsheet.ArcTable.ColumnOrder", int, [("InputClass", 1.0), ("ProtocolClass", 2.0), ("ParamsClass", 3.0), ("OutputClass", 4.0)]), enum_type("ARCtrl.Spreadsheet.ArcTable.ColumnOrder", int, [("InputClass", 1.0), ("ProtocolClass", 2.0), ("ParamsClass", 3.0), ("OutputClass", 4.0)])], int]:
                return compare_primitives

        columns: FSharpList[FSharpList[FsCell]] = collect(_arrow972, sort_by(_arrow973, of_array(DataMap__get_Table(table).Columns), ObjectExpr974()))
        max_row: int = length(head(columns)) or 0
        max_col: int = length(columns) or 0
        fs_table: FsTable = ws.Table("datamapTable", FsRangeAddress__ctor_7E77A4A0(FsAddress__ctor_Z37302880(1, 1), FsAddress__ctor_Z37302880(max_row, max_col)))
        def action_1(col_i: int, col: FSharpList[FsCell], table: Any=table) -> None:
            def action(row_i: int, cell: FsCell, col_i: Any=col_i, col: Any=col) -> None:
                value: str
                v: str = cell.ValueAsString()
                if row_i == 0:
                    match_value: str | None = Dictionary_tryGet(v, string_count)
                    if match_value is None:
                        add_to_dict(string_count, cell.ValueAsString(), "")
                        value = v

                    else: 
                        spaces: str = match_value
                        string_count[v] = spaces + " "
                        value = (v + " ") + spaces


                else: 
                    value = v

                address: FsAddress = FsAddress__ctor_Z37302880(row_i + 1, col_i + 1)
                FsRangeBase__Cell_Z3407A44B(fs_table, address, ws.CellCollection).SetValueAs(value)

            iterate_indexed(action, col)

        iterate_indexed(action_1, columns)
        return ws



__all__ = ["helper_column_strings", "group_columns_by_header", "try_data_map_table", "compose_columns", "try_from_fs_worksheet", "to_fs_worksheet"]

