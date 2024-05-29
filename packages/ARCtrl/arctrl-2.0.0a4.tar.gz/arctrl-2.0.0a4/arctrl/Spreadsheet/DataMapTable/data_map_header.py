from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.list import (map, FSharpList, is_empty, head, tail, try_find_index, of_array, singleton)
from ...fable_modules.fable_library.option import map as map_1
from ...fable_modules.fable_library.string_ import (to_fail, printf)
from ...fable_modules.fable_library.util import equals
from ...fable_modules.fs_spreadsheet.Cells.fs_cell import FsCell
from ...Core.Table.composite_cell import CompositeCell
from ...Core.Table.composite_header import (CompositeHeader, IOType)
from ...Core.Table.data_map import (DataMapAux_explicationHeader, DataMapAux_unitHeader, DataMapAux_objectTypeHeader, DataMapAux_descriptionHeader, DataMapAux_generatedByHeader)
from ..AnnotationTable.composite_cell import (term_from_fs_cells, free_text_from_fs_cells, data_from_fs_cells)

def ActivePattern__007CTerm_007C__007C(category_string: str, category_header: CompositeHeader, cells: FSharpList[FsCell]) -> tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None:
    def _007CAC_007C__007C(s: str, category_string: Any=category_string, category_header: Any=category_header, cells: Any=cells) -> CompositeHeader | None:
        if s == category_string:
            return category_header

        else: 
            return None


    def _007CTSRColumnHeaderRaw_007C__007C(s_1: str, category_string: Any=category_string, category_header: Any=category_header, cells: Any=cells) -> str | None:
        if s_1.find("Term Source REF") == 0:
            return s_1

        else: 
            return None


    def _007CTANColumnHeaderRaw_007C__007C(s_2: str, category_string: Any=category_string, category_header: Any=category_header, cells: Any=cells) -> str | None:
        if s_2.find("Term Accession Number") == 0:
            return s_2

        else: 
            return None


    def mapping(c: FsCell, category_string: Any=category_string, category_header: Any=category_header, cells: Any=cells) -> str:
        return c.ValueAsString()

    cell_values: FSharpList[str] = map(mapping, cells)
    (pattern_matching_result, header) = (None, None)
    if not is_empty(cell_values):
        active_pattern_result: CompositeHeader | None = _007CAC_007C__007C(head(cell_values))
        if active_pattern_result is not None:
            if is_empty(tail(cell_values)):
                pattern_matching_result = 0
                header = active_pattern_result

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        def _arrow935(cells_1: FSharpList[FsCell], category_string: Any=category_string, category_header: Any=category_header, cells: Any=cells) -> CompositeCell:
            return term_from_fs_cells(None, None, cells_1)

        return (header, _arrow935)

    elif pattern_matching_result == 1:
        (pattern_matching_result_1, header_1) = (None, None)
        if not is_empty(cell_values):
            active_pattern_result_1: CompositeHeader | None = _007CAC_007C__007C(head(cell_values))
            if active_pattern_result_1 is not None:
                if not is_empty(tail(cell_values)):
                    if _007CTSRColumnHeaderRaw_007C__007C(head(tail(cell_values))) is not None:
                        if not is_empty(tail(tail(cell_values))):
                            if _007CTANColumnHeaderRaw_007C__007C(head(tail(tail(cell_values)))) is not None:
                                if is_empty(tail(tail(tail(cell_values)))):
                                    pattern_matching_result_1 = 0
                                    header_1 = active_pattern_result_1

                                else: 
                                    pattern_matching_result_1 = 1


                            else: 
                                pattern_matching_result_1 = 1


                        else: 
                            pattern_matching_result_1 = 1


                    else: 
                        pattern_matching_result_1 = 1


                else: 
                    pattern_matching_result_1 = 1


            else: 
                pattern_matching_result_1 = 1


        else: 
            pattern_matching_result_1 = 1

        if pattern_matching_result_1 == 0:
            def _arrow936(cells_2: FSharpList[FsCell], category_string: Any=category_string, category_header: Any=category_header, cells: Any=cells) -> CompositeCell:
                return term_from_fs_cells(1, 2, cells_2)

            return (header_1, _arrow936)

        elif pattern_matching_result_1 == 1:
            (pattern_matching_result_2, header_2) = (None, None)
            if not is_empty(cell_values):
                active_pattern_result_4: CompositeHeader | None = _007CAC_007C__007C(head(cell_values))
                if active_pattern_result_4 is not None:
                    if not is_empty(tail(cell_values)):
                        if _007CTANColumnHeaderRaw_007C__007C(head(tail(cell_values))) is not None:
                            if not is_empty(tail(tail(cell_values))):
                                if _007CTSRColumnHeaderRaw_007C__007C(head(tail(tail(cell_values)))) is not None:
                                    if is_empty(tail(tail(tail(cell_values)))):
                                        pattern_matching_result_2 = 0
                                        header_2 = active_pattern_result_4

                                    else: 
                                        pattern_matching_result_2 = 1


                                else: 
                                    pattern_matching_result_2 = 1


                            else: 
                                pattern_matching_result_2 = 1


                        else: 
                            pattern_matching_result_2 = 1


                    else: 
                        pattern_matching_result_2 = 1


                else: 
                    pattern_matching_result_2 = 1


            else: 
                pattern_matching_result_2 = 1

            if pattern_matching_result_2 == 0:
                def _arrow937(cells_3: FSharpList[FsCell], category_string: Any=category_string, category_header: Any=category_header, cells: Any=cells) -> CompositeCell:
                    return term_from_fs_cells(2, 1, cells_3)

                return (header_2, _arrow937)

            elif pattern_matching_result_2 == 1:
                return None





def ActivePattern__007CExplication_007C__007C(cells: FSharpList[FsCell]) -> tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None:
    active_pattern_result: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None = ActivePattern__007CTerm_007C__007C("Explication", DataMapAux_explicationHeader, cells)
    if active_pattern_result is not None:
        r: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] = active_pattern_result
        return r

    else: 
        return None



def ActivePattern__007CUnit_007C__007C(cells: FSharpList[FsCell]) -> tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None:
    active_pattern_result: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None = ActivePattern__007CTerm_007C__007C("Unit", DataMapAux_unitHeader, cells)
    if active_pattern_result is not None:
        r: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] = active_pattern_result
        return r

    else: 
        return None



def ActivePattern__007CObjectType_007C__007C(cells: FSharpList[FsCell]) -> tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None:
    active_pattern_result: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None = ActivePattern__007CTerm_007C__007C("Object Type", DataMapAux_objectTypeHeader, cells)
    if active_pattern_result is not None:
        r: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] = active_pattern_result
        return r

    else: 
        return None



def ActivePattern__007CDescription_007C__007C(cells: FSharpList[FsCell]) -> tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None:
    def mapping(c: FsCell, cells: Any=cells) -> str:
        return c.ValueAsString()

    cell_values: FSharpList[str] = map(mapping, cells)
    (pattern_matching_result,) = (None,)
    if not is_empty(cell_values):
        if head(cell_values) == "Description":
            if is_empty(tail(cell_values)):
                pattern_matching_result = 0

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        def _arrow938(cells_1: FSharpList[FsCell], cells: Any=cells) -> CompositeCell:
            return free_text_from_fs_cells(cells_1)

        return (DataMapAux_descriptionHeader, _arrow938)

    elif pattern_matching_result == 1:
        return None



def ActivePattern__007CGeneratedBy_007C__007C(cells: FSharpList[FsCell]) -> tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None:
    def mapping(c: FsCell, cells: Any=cells) -> str:
        return c.ValueAsString()

    cell_values: FSharpList[str] = map(mapping, cells)
    (pattern_matching_result,) = (None,)
    if not is_empty(cell_values):
        if head(cell_values) == "Generated By":
            if is_empty(tail(cell_values)):
                pattern_matching_result = 0

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        def _arrow939(cells_1: FSharpList[FsCell], cells: Any=cells) -> CompositeCell:
            return free_text_from_fs_cells(cells_1)

        return (DataMapAux_generatedByHeader, _arrow939)

    elif pattern_matching_result == 1:
        return None



def ActivePattern__007CData_007C__007C(cells: FSharpList[FsCell]) -> tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None:
    def mapping(c: FsCell, cells: Any=cells) -> str:
        return c.ValueAsString()

    cell_values: FSharpList[str] = map(mapping, cells)
    (pattern_matching_result, cols) = (None, None)
    if not is_empty(cell_values):
        if head(cell_values) == "Data":
            pattern_matching_result = 0
            cols = tail(cell_values)

        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        def mapping_1(y: int, cells: Any=cells) -> int:
            return 1 + y

        def predicate(s: str, cells: Any=cells) -> bool:
            return s.find("Data Format") == 0

        format: int | None = map_1(mapping_1, try_find_index(predicate, cols))
        def mapping_2(y_1: int, cells: Any=cells) -> int:
            return 1 + y_1

        def predicate_1(s_1: str, cells: Any=cells) -> bool:
            return s_1.find("Data Selector Format") == 0

        selector_format: int | None = map_1(mapping_2, try_find_index(predicate_1, cols))
        def _arrow940(cells_1: FSharpList[FsCell], cells: Any=cells) -> CompositeCell:
            return data_from_fs_cells(format, selector_format, cells_1)

        return (CompositeHeader(11, IOType(2)), _arrow940)

    elif pattern_matching_result == 1:
        return None



def ActivePattern__007CFreeText_007C__007C(cells: FSharpList[FsCell]) -> tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None:
    def mapping(c: FsCell, cells: Any=cells) -> str:
        return c.ValueAsString()

    cell_values: FSharpList[str] = map(mapping, cells)
    (pattern_matching_result, text) = (None, None)
    if not is_empty(cell_values):
        if is_empty(tail(cell_values)):
            pattern_matching_result = 0
            text = head(cell_values)

        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        def _arrow941(cells_1: FSharpList[FsCell], cells: Any=cells) -> CompositeCell:
            return free_text_from_fs_cells(cells_1)

        return (CompositeHeader(13, text), _arrow941)

    elif pattern_matching_result == 1:
        return None



def from_fs_cells(cells: FSharpList[FsCell]) -> tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]]:
    active_pattern_result: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None = ActivePattern__007CData_007C__007C(cells)
    if active_pattern_result is not None:
        d: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] = active_pattern_result
        return d

    else: 
        active_pattern_result_1: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None = ActivePattern__007CExplication_007C__007C(cells)
        if active_pattern_result_1 is not None:
            e: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] = active_pattern_result_1
            return e

        else: 
            active_pattern_result_2: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None = ActivePattern__007CUnit_007C__007C(cells)
            if active_pattern_result_2 is not None:
                u: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] = active_pattern_result_2
                return u

            else: 
                active_pattern_result_3: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None = ActivePattern__007CObjectType_007C__007C(cells)
                if active_pattern_result_3 is not None:
                    ot: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] = active_pattern_result_3
                    return ot

                else: 
                    active_pattern_result_4: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None = ActivePattern__007CDescription_007C__007C(cells)
                    if active_pattern_result_4 is not None:
                        d_1: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] = active_pattern_result_4
                        return d_1

                    else: 
                        active_pattern_result_5: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None = ActivePattern__007CGeneratedBy_007C__007C(cells)
                        if active_pattern_result_5 is not None:
                            gb: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] = active_pattern_result_5
                            return gb

                        else: 
                            active_pattern_result_6: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] | None = ActivePattern__007CFreeText_007C__007C(cells)
                            if active_pattern_result_6 is not None:
                                ft: tuple[CompositeHeader, Callable[[FSharpList[FsCell]], CompositeCell]] = active_pattern_result_6
                                return ft

                            else: 
                                return to_fail(printf("Could not parse header group %O"))(cells)









def to_fs_cells(header: CompositeHeader) -> FSharpList[FsCell]:
    (pattern_matching_result, text) = (None, None)
    if header.tag == 11:
        if header.fields[0].tag == 2:
            pattern_matching_result = 0

        elif equals(header, DataMapAux_explicationHeader):
            pattern_matching_result = 1

        elif equals(header, DataMapAux_unitHeader):
            pattern_matching_result = 2

        elif equals(header, DataMapAux_objectTypeHeader):
            pattern_matching_result = 3

        else: 
            pattern_matching_result = 5


    elif header.tag == 13:
        if equals(header, DataMapAux_explicationHeader):
            pattern_matching_result = 1

        elif equals(header, DataMapAux_unitHeader):
            pattern_matching_result = 2

        elif equals(header, DataMapAux_objectTypeHeader):
            pattern_matching_result = 3

        else: 
            pattern_matching_result = 4
            text = header.fields[0]


    elif equals(header, DataMapAux_explicationHeader):
        pattern_matching_result = 1

    elif equals(header, DataMapAux_unitHeader):
        pattern_matching_result = 2

    elif equals(header, DataMapAux_objectTypeHeader):
        pattern_matching_result = 3

    else: 
        pattern_matching_result = 5

    if pattern_matching_result == 0:
        return of_array([FsCell("Data"), FsCell("Data Format"), FsCell("Data Selector Format")])

    elif pattern_matching_result == 1:
        return of_array([FsCell("Explication"), FsCell("Term Source REF"), FsCell("Term Accession Number")])

    elif pattern_matching_result == 2:
        return of_array([FsCell("Unit"), FsCell("Term Source REF"), FsCell("Term Accession Number")])

    elif pattern_matching_result == 3:
        return of_array([FsCell("Object Type"), FsCell("Term Source REF"), FsCell("Term Accession Number")])

    elif pattern_matching_result == 4:
        return singleton(FsCell(text))

    elif pattern_matching_result == 5:
        return to_fail(printf("Could not parse DataMap header %O."))(header)



__all__ = ["ActivePattern__007CTerm_007C__007C", "ActivePattern__007CExplication_007C__007C", "ActivePattern__007CUnit_007C__007C", "ActivePattern__007CObjectType_007C__007C", "ActivePattern__007CDescription_007C__007C", "ActivePattern__007CGeneratedBy_007C__007C", "ActivePattern__007CData_007C__007C", "ActivePattern__007CFreeText_007C__007C", "from_fs_cells", "to_fs_cells"]

