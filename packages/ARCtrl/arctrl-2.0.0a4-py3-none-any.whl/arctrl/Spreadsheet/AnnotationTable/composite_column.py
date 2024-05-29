from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.array_ import map as map_2
from ...fable_modules.fable_library.list import (map, FSharpList, item, of_array, singleton as singleton_1)
from ...fable_modules.fable_library.range import range_big_int
from ...fable_modules.fable_library.seq import (to_array, delay, map as map_1, exists, to_list, append, singleton, empty)
from ...fable_modules.fable_library.types import (to_string, Array)
from ...fable_modules.fable_library.util import IEnumerable_1
from ...fable_modules.fs_spreadsheet.Cells.fs_cell import FsCell
from ...fable_modules.fs_spreadsheet.fs_address import FsAddress__get_RowNumber
from ...fable_modules.fs_spreadsheet.fs_column import FsColumn
from ...fable_modules.fs_spreadsheet.Ranges.fs_range_address import FsRangeAddress__get_LastAddress
from ...fable_modules.fs_spreadsheet.Ranges.fs_range_base import FsRangeBase__get_RangeAddress
from ...Core.Table.composite_cell import CompositeCell
from ...Core.Table.composite_column import CompositeColumn
from ...Core.Table.composite_header import (IOType, CompositeHeader)
from .composite_cell import to_fs_cells as to_fs_cells_1
from .composite_header import (from_fs_cells, to_fs_cells)

def fix_deprecated_ioheader(col: FsColumn) -> FsColumn:
    match_value: IOType = IOType.of_string(col.Item(1).ValueAsString())
    if match_value.tag == 4:
        return col

    elif match_value.tag == 0:
        col.Item(1).SetValueAs(to_string(CompositeHeader(11, IOType(0))))
        return col

    else: 
        col.Item(1).SetValueAs(to_string(CompositeHeader(12, match_value)))
        return col



def from_fs_columns(columns: FSharpList[FsColumn]) -> CompositeColumn:
    def mapping(c: FsColumn, columns: Any=columns) -> FsCell:
        return c.Item(1)

    pattern_input: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] = from_fs_cells(map(mapping, columns))
    l: int = FsAddress__get_RowNumber(FsRangeAddress__get_LastAddress(FsRangeBase__get_RangeAddress(item(0, columns)))) or 0
    def _arrow888(__unit: None=None, columns: Any=columns) -> IEnumerable_1[CompositeCell]:
        def _arrow887(i: int) -> CompositeCell:
            def mapping_1(c_1: FsColumn) -> FsCell:
                return c_1.Item(i)

            return pattern_input[1](map(mapping_1, columns))

        return map_1(_arrow887, range_big_int(2, 1, l))

    cells_1: Array[CompositeCell] = to_array(delay(_arrow888))
    return CompositeColumn.create(pattern_input[0], cells_1)


def to_fs_columns(column: CompositeColumn) -> FSharpList[FSharpList[FsCell]]:
    def predicate(c: CompositeCell, column: Any=column) -> bool:
        return c.is_unitized

    has_unit: bool = exists(predicate, column.Cells)
    is_term: bool = column.Header.IsTermColumn
    is_data: bool = column.Header.IsDataColumn
    header: FSharpList[FsCell] = to_fs_cells(has_unit, column.Header)
    def mapping(cell: CompositeCell, column: Any=column) -> FSharpList[FsCell]:
        return to_fs_cells_1(is_term, has_unit, cell)

    cells: Array[FSharpList[FsCell]] = map_2(mapping, column.Cells, None)
    if has_unit:
        def _arrow894(__unit: None=None, column: Any=column) -> IEnumerable_1[FsCell]:
            def _arrow893(__unit: None=None) -> IEnumerable_1[FsCell]:
                def _arrow892(i: int) -> FsCell:
                    return item(0, cells[i])

                return map_1(_arrow892, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(item(0, header)), delay(_arrow893))

        def _arrow897(__unit: None=None, column: Any=column) -> IEnumerable_1[FsCell]:
            def _arrow896(__unit: None=None) -> IEnumerable_1[FsCell]:
                def _arrow895(i_1: int) -> FsCell:
                    return item(1, cells[i_1])

                return map_1(_arrow895, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(item(1, header)), delay(_arrow896))

        def _arrow900(__unit: None=None, column: Any=column) -> IEnumerable_1[FsCell]:
            def _arrow899(__unit: None=None) -> IEnumerable_1[FsCell]:
                def _arrow898(i_2: int) -> FsCell:
                    return item(2, cells[i_2])

                return map_1(_arrow898, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(item(2, header)), delay(_arrow899))

        def _arrow903(__unit: None=None, column: Any=column) -> IEnumerable_1[FsCell]:
            def _arrow902(__unit: None=None) -> IEnumerable_1[FsCell]:
                def _arrow901(i_3: int) -> FsCell:
                    return item(3, cells[i_3])

                return map_1(_arrow901, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(item(3, header)), delay(_arrow902))

        return of_array([to_list(delay(_arrow894)), to_list(delay(_arrow897)), to_list(delay(_arrow900)), to_list(delay(_arrow903))])

    elif is_term:
        def _arrow909(__unit: None=None, column: Any=column) -> IEnumerable_1[FsCell]:
            def _arrow908(__unit: None=None) -> IEnumerable_1[FsCell]:
                def _arrow907(i_4: int) -> FsCell:
                    return item(0, cells[i_4])

                return map_1(_arrow907, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(item(0, header)), delay(_arrow908))

        def _arrow912(__unit: None=None, column: Any=column) -> IEnumerable_1[FsCell]:
            def _arrow911(__unit: None=None) -> IEnumerable_1[FsCell]:
                def _arrow910(i_5: int) -> FsCell:
                    return item(1, cells[i_5])

                return map_1(_arrow910, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(item(1, header)), delay(_arrow911))

        def _arrow915(__unit: None=None, column: Any=column) -> IEnumerable_1[FsCell]:
            def _arrow914(__unit: None=None) -> IEnumerable_1[FsCell]:
                def _arrow913(i_6: int) -> FsCell:
                    return item(2, cells[i_6])

                return map_1(_arrow913, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(item(2, header)), delay(_arrow914))

        return of_array([to_list(delay(_arrow909)), to_list(delay(_arrow912)), to_list(delay(_arrow915))])

    elif is_data:
        def predicate_1(c_1: CompositeCell, column: Any=column) -> bool:
            return c_1.AsData.Format is not None

        has_format: bool = exists(predicate_1, column.Cells)
        def predicate_2(c_2: CompositeCell, column: Any=column) -> bool:
            return c_2.AsData.SelectorFormat is not None

        has_selector_format: bool = exists(predicate_2, column.Cells)
        def _arrow927(__unit: None=None, column: Any=column) -> IEnumerable_1[FSharpList[FsCell]]:
            def _arrow918(__unit: None=None) -> IEnumerable_1[FsCell]:
                def _arrow917(__unit: None=None) -> IEnumerable_1[FsCell]:
                    def _arrow916(i_7: int) -> FsCell:
                        return item(0, cells[i_7])

                    return map_1(_arrow916, range_big_int(0, 1, len(column.Cells) - 1))

                return append(singleton(item(0, header)), delay(_arrow917))

            def _arrow926(__unit: None=None) -> IEnumerable_1[FSharpList[FsCell]]:
                def _arrow921(__unit: None=None) -> IEnumerable_1[FsCell]:
                    def _arrow920(__unit: None=None) -> IEnumerable_1[FsCell]:
                        def _arrow919(i_8: int) -> FsCell:
                            return item(1, cells[i_8])

                        return map_1(_arrow919, range_big_int(0, 1, len(column.Cells) - 1))

                    return append(singleton(item(1, header)), delay(_arrow920))

                def _arrow925(__unit: None=None) -> IEnumerable_1[FSharpList[FsCell]]:
                    def _arrow924(__unit: None=None) -> IEnumerable_1[FsCell]:
                        def _arrow923(__unit: None=None) -> IEnumerable_1[FsCell]:
                            def _arrow922(i_9: int) -> FsCell:
                                return item(2, cells[i_9])

                            return map_1(_arrow922, range_big_int(0, 1, len(column.Cells) - 1))

                        return append(singleton(item(2, header)), delay(_arrow923))

                    return singleton(to_list(delay(_arrow924))) if has_selector_format else empty()

                return append(singleton(to_list(delay(_arrow921))) if has_format else empty(), delay(_arrow925))

            return append(singleton(to_list(delay(_arrow918))), delay(_arrow926))

        return to_list(delay(_arrow927))

    else: 
        def _arrow930(__unit: None=None, column: Any=column) -> IEnumerable_1[FsCell]:
            def _arrow929(__unit: None=None) -> IEnumerable_1[FsCell]:
                def _arrow928(i_10: int) -> FsCell:
                    return item(0, cells[i_10])

                return map_1(_arrow928, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(item(0, header)), delay(_arrow929))

        return singleton_1(to_list(delay(_arrow930)))



__all__ = ["fix_deprecated_ioheader", "from_fs_columns", "to_fs_columns"]

