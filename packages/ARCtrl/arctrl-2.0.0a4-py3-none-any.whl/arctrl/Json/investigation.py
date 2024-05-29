from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_modules.fable_library.list import (choose, of_array, unzip, FSharpList, empty)
from ..fable_modules.fable_library.option import default_arg
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.seq import (concat, map)
from ..fable_modules.fable_library.seq2 import distinct_by
from ..fable_modules.fable_library.string_ import (to_text, printf, to_fail)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import (equals, string_hash)
from ..fable_modules.thoth_json_core.decode import (object, IRequiredGetter, string, IOptionalGetter, IGetters, list_1 as list_1_1)
from ..fable_modules.thoth_json_core.types import (Json, Decoder_1)
from ..fable_modules.thoth_json_python.decode import Decode_fromString
from ..fable_modules.thoth_json_python.encode import to_string
from ..Core.arc_types import (ArcAssay, ArcStudy, ArcInvestigation)
from ..Core.comment import Comment
from ..Core.Helper.identifier import create_missing_identifier
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.ontology_source_reference import OntologySourceReference
from ..Core.person import Person
from ..Core.publication import Publication
from ..Core.Table.composite_cell import CompositeCell
from .assay import (Assay_encoder, Assay_decoder, Assay_encoderCompressed, Assay_decoderCompressed)
from .comment import (Comment_encoder, Comment_decoder, Comment_ROCrate_encoder, Comment_ROCrate_decoder, Comment_ISAJson_encoder, Comment_ISAJson_decoder)
from .context.rocrate.isa_investigation_context import context_jsonvalue
from .context.rocrate.rocrate_context import (conforms_to_jsonvalue, context_jsonvalue as context_jsonvalue_1)
from .decode import (Decode_resizeArray, Decode_objectNoAdditionalProperties)
from .encode import (try_include, try_include_seq, default_spaces)
from .ontology_source_reference import (OntologySourceReference_encoder, OntologySourceReference_decoder, OntologySourceReference_ROCrate_encoder, OntologySourceReference_ROCrate_decoder, OntologySourceReference_ISAJson_encoder, OntologySourceReference_ISAJson_decoder)
from .person import (Person_encoder, Person_decoder, Person_ROCrate_encoder, Person_ROCrate_decoder, Person_ISAJson_encoder, Person_ISAJson_decoder)
from .publication import (Publication_encoder, Publication_decoder, Publication_ROCrate_encoder, Publication_ROCrate_decoder, Publication_ISAJson_encoder, Publication_ISAJson_decoder)
from .study import (Study_encoder, Study_decoder, Study_encoderCompressed, Study_decoderCompressed, Study_ROCrate_encoder, Study_ROCrate_decoder, Study_ISAJson_encoder, Study_ISAJson_decoder)
from .Table.compression import (decode, encode)

def Investigation_encoder(inv: ArcInvestigation) -> Json:
    def chooser(tupled_arg: tuple[str, Json], inv: Any=inv) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1813(value_1: str, inv: Any=inv) -> Json:
        return Json(0, value_1)

    def _arrow1814(value_3: str, inv: Any=inv) -> Json:
        return Json(0, value_3)

    def _arrow1815(value_5: str, inv: Any=inv) -> Json:
        return Json(0, value_5)

    def _arrow1816(value_7: str, inv: Any=inv) -> Json:
        return Json(0, value_7)

    def _arrow1817(osr: OntologySourceReference, inv: Any=inv) -> Json:
        return OntologySourceReference_encoder(osr)

    def _arrow1818(oa: Publication, inv: Any=inv) -> Json:
        return Publication_encoder(oa)

    def _arrow1819(person: Person, inv: Any=inv) -> Json:
        return Person_encoder(person)

    def _arrow1820(assay: ArcAssay, inv: Any=inv) -> Json:
        return Assay_encoder(assay)

    def _arrow1821(study: ArcStudy, inv: Any=inv) -> Json:
        return Study_encoder(study)

    def _arrow1822(value_9: str, inv: Any=inv) -> Json:
        return Json(0, value_9)

    def _arrow1823(comment: Comment, inv: Any=inv) -> Json:
        return Comment_encoder(comment)

    return Json(5, choose(chooser, of_array([("Identifier", Json(0, inv.Identifier)), try_include("Title", _arrow1813, inv.Title), try_include("Description", _arrow1814, inv.Description), try_include("SubmissionDate", _arrow1815, inv.SubmissionDate), try_include("PublicReleaseDate", _arrow1816, inv.PublicReleaseDate), try_include_seq("OntologySourceReferences", _arrow1817, inv.OntologySourceReferences), try_include_seq("Publications", _arrow1818, inv.Publications), try_include_seq("Contacts", _arrow1819, inv.Contacts), try_include_seq("Assays", _arrow1820, inv.Assays), try_include_seq("Studies", _arrow1821, inv.Studies), try_include_seq("RegisteredStudyIdentifiers", _arrow1822, inv.RegisteredStudyIdentifiers), try_include_seq("Comments", _arrow1823, inv.Comments)])))


def _arrow1836(get: IGetters) -> ArcInvestigation:
    def _arrow1824(__unit: None=None) -> str:
        object_arg: IRequiredGetter = get.Required
        return object_arg.Field("Identifier", string)

    def _arrow1825(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("Title", string)

    def _arrow1826(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("Description", string)

    def _arrow1827(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("SubmissionDate", string)

    def _arrow1828(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("PublicReleaseDate", string)

    def _arrow1829(__unit: None=None) -> Array[OntologySourceReference] | None:
        arg_11: Decoder_1[Array[OntologySourceReference]] = Decode_resizeArray(OntologySourceReference_decoder)
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("OntologySourceReferences", arg_11)

    def _arrow1830(__unit: None=None) -> Array[Publication] | None:
        arg_13: Decoder_1[Array[Publication]] = Decode_resizeArray(Publication_decoder)
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("Publications", arg_13)

    def _arrow1831(__unit: None=None) -> Array[Person] | None:
        arg_15: Decoder_1[Array[Person]] = Decode_resizeArray(Person_decoder)
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("Contacts", arg_15)

    def _arrow1832(__unit: None=None) -> Array[ArcAssay] | None:
        arg_17: Decoder_1[Array[ArcAssay]] = Decode_resizeArray(Assay_decoder)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("Assays", arg_17)

    def _arrow1833(__unit: None=None) -> Array[ArcStudy] | None:
        arg_19: Decoder_1[Array[ArcStudy]] = Decode_resizeArray(Study_decoder)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("Studies", arg_19)

    def _arrow1834(__unit: None=None) -> Array[str] | None:
        arg_21: Decoder_1[Array[str]] = Decode_resizeArray(string)
        object_arg_10: IOptionalGetter = get.Optional
        return object_arg_10.Field("RegisteredStudyIdentifiers", arg_21)

    def _arrow1835(__unit: None=None) -> Array[Comment] | None:
        arg_23: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_decoder)
        object_arg_11: IOptionalGetter = get.Optional
        return object_arg_11.Field("Comments", arg_23)

    return ArcInvestigation(_arrow1824(), _arrow1825(), _arrow1826(), _arrow1827(), _arrow1828(), _arrow1829(), _arrow1830(), _arrow1831(), _arrow1832(), _arrow1833(), _arrow1834(), _arrow1835())


Investigation_decoder: Decoder_1[ArcInvestigation] = object(_arrow1836)

def Investigation_encoderCompressed(string_table: Any, oa_table: Any, cell_table: Any, inv: ArcInvestigation) -> Json:
    def chooser(tupled_arg: tuple[str, Json], string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1837(value_1: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> Json:
        return Json(0, value_1)

    def _arrow1838(value_3: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> Json:
        return Json(0, value_3)

    def _arrow1839(value_5: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> Json:
        return Json(0, value_5)

    def _arrow1840(value_7: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> Json:
        return Json(0, value_7)

    def _arrow1841(osr: OntologySourceReference, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> Json:
        return OntologySourceReference_encoder(osr)

    def _arrow1842(oa: Publication, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> Json:
        return Publication_encoder(oa)

    def _arrow1843(person: Person, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> Json:
        return Person_encoder(person)

    def _arrow1844(assay: ArcAssay, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> Json:
        return Assay_encoderCompressed(string_table, oa_table, cell_table, assay)

    def _arrow1845(study: ArcStudy, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> Json:
        return Study_encoderCompressed(string_table, oa_table, cell_table, study)

    def _arrow1846(value_9: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> Json:
        return Json(0, value_9)

    def _arrow1847(comment: Comment, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, inv: Any=inv) -> Json:
        return Comment_encoder(comment)

    return Json(5, choose(chooser, of_array([("Identifier", Json(0, inv.Identifier)), try_include("Title", _arrow1837, inv.Title), try_include("Description", _arrow1838, inv.Description), try_include("SubmissionDate", _arrow1839, inv.SubmissionDate), try_include("PublicReleaseDate", _arrow1840, inv.PublicReleaseDate), try_include_seq("OntologySourceReferences", _arrow1841, inv.OntologySourceReferences), try_include_seq("Publications", _arrow1842, inv.Publications), try_include_seq("Contacts", _arrow1843, inv.Contacts), try_include_seq("Assays", _arrow1844, inv.Assays), try_include_seq("Studies", _arrow1845, inv.Studies), try_include_seq("RegisteredStudyIdentifiers", _arrow1846, inv.RegisteredStudyIdentifiers), try_include_seq("Comments", _arrow1847, inv.Comments)])))


def Investigation_decoderCompressed(string_table: Array[str], oa_table: Array[OntologyAnnotation], cell_table: Array[CompositeCell]) -> Decoder_1[ArcInvestigation]:
    def _arrow1860(get: IGetters, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table) -> ArcInvestigation:
        def _arrow1848(__unit: None=None) -> str:
            object_arg: IRequiredGetter = get.Required
            return object_arg.Field("Identifier", string)

        def _arrow1849(__unit: None=None) -> str | None:
            object_arg_1: IOptionalGetter = get.Optional
            return object_arg_1.Field("Title", string)

        def _arrow1850(__unit: None=None) -> str | None:
            object_arg_2: IOptionalGetter = get.Optional
            return object_arg_2.Field("Description", string)

        def _arrow1851(__unit: None=None) -> str | None:
            object_arg_3: IOptionalGetter = get.Optional
            return object_arg_3.Field("SubmissionDate", string)

        def _arrow1852(__unit: None=None) -> str | None:
            object_arg_4: IOptionalGetter = get.Optional
            return object_arg_4.Field("PublicReleaseDate", string)

        def _arrow1853(__unit: None=None) -> Array[OntologySourceReference] | None:
            arg_11: Decoder_1[Array[OntologySourceReference]] = Decode_resizeArray(OntologySourceReference_decoder)
            object_arg_5: IOptionalGetter = get.Optional
            return object_arg_5.Field("OntologySourceReferences", arg_11)

        def _arrow1854(__unit: None=None) -> Array[Publication] | None:
            arg_13: Decoder_1[Array[Publication]] = Decode_resizeArray(Publication_decoder)
            object_arg_6: IOptionalGetter = get.Optional
            return object_arg_6.Field("Publications", arg_13)

        def _arrow1855(__unit: None=None) -> Array[Person] | None:
            arg_15: Decoder_1[Array[Person]] = Decode_resizeArray(Person_decoder)
            object_arg_7: IOptionalGetter = get.Optional
            return object_arg_7.Field("Contacts", arg_15)

        def _arrow1856(__unit: None=None) -> Array[ArcAssay] | None:
            arg_17: Decoder_1[Array[ArcAssay]] = Decode_resizeArray(Assay_decoderCompressed(string_table, oa_table, cell_table))
            object_arg_8: IOptionalGetter = get.Optional
            return object_arg_8.Field("Assays", arg_17)

        def _arrow1857(__unit: None=None) -> Array[ArcStudy] | None:
            arg_19: Decoder_1[Array[ArcStudy]] = Decode_resizeArray(Study_decoderCompressed(string_table, oa_table, cell_table))
            object_arg_9: IOptionalGetter = get.Optional
            return object_arg_9.Field("Studies", arg_19)

        def _arrow1858(__unit: None=None) -> Array[str] | None:
            arg_21: Decoder_1[Array[str]] = Decode_resizeArray(string)
            object_arg_10: IOptionalGetter = get.Optional
            return object_arg_10.Field("RegisteredStudyIdentifiers", arg_21)

        def _arrow1859(__unit: None=None) -> Array[Comment] | None:
            arg_23: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_decoder)
            object_arg_11: IOptionalGetter = get.Optional
            return object_arg_11.Field("Comments", arg_23)

        return ArcInvestigation(_arrow1848(), _arrow1849(), _arrow1850(), _arrow1851(), _arrow1852(), _arrow1853(), _arrow1854(), _arrow1855(), _arrow1856(), _arrow1857(), _arrow1858(), _arrow1859())

    return object(_arrow1860)


def Investigation_ROCrate_genID(i: ArcInvestigation) -> str:
    return "./"


def Investigation_ROCrate_encoder(oa: ArcInvestigation) -> Json:
    def chooser(tupled_arg: tuple[str, Json], oa: Any=oa) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1861(value_5: str, oa: Any=oa) -> Json:
        return Json(0, value_5)

    def _arrow1862(value_7: str, oa: Any=oa) -> Json:
        return Json(0, value_7)

    def _arrow1863(value_9: str, oa: Any=oa) -> Json:
        return Json(0, value_9)

    def _arrow1864(value_11: str, oa: Any=oa) -> Json:
        return Json(0, value_11)

    def _arrow1865(osr: OntologySourceReference, oa: Any=oa) -> Json:
        return OntologySourceReference_ROCrate_encoder(osr)

    def _arrow1866(oa_1: Publication, oa: Any=oa) -> Json:
        return Publication_ROCrate_encoder(oa_1)

    def _arrow1867(oa_2: Person, oa: Any=oa) -> Json:
        return Person_ROCrate_encoder(oa_2)

    def _arrow1868(s: ArcStudy, oa: Any=oa) -> Json:
        return Study_ROCrate_encoder(None, s)

    def _arrow1869(comment: Comment, oa: Any=oa) -> Json:
        return Comment_ROCrate_encoder(comment)

    return Json(5, choose(chooser, of_array([("@id", Json(0, Investigation_ROCrate_genID(oa))), ("@type", Json(0, "Investigation")), ("additionalType", Json(0, "Investigation")), ("identifier", Json(0, oa.Identifier)), ("filename", Json(0, ArcInvestigation.FileName())), try_include("title", _arrow1861, oa.Title), try_include("description", _arrow1862, oa.Description), try_include("submissionDate", _arrow1863, oa.SubmissionDate), try_include("publicReleaseDate", _arrow1864, oa.PublicReleaseDate), try_include_seq("ontologySourceReferences", _arrow1865, oa.OntologySourceReferences), try_include_seq("publications", _arrow1866, oa.Publications), try_include_seq("people", _arrow1867, oa.Contacts), try_include_seq("studies", _arrow1868, oa.Studies), try_include_seq("comments", _arrow1869, oa.Comments), ("@context", context_jsonvalue)])))


def _arrow1881(get: IGetters) -> ArcInvestigation:
    identifier: str
    match_value: str | None
    object_arg: IOptionalGetter = get.Optional
    match_value = object_arg.Field("identifier", string)
    identifier = create_missing_identifier() if (match_value is None) else match_value
    def _arrow1870(__unit: None=None) -> FSharpList[tuple[ArcStudy, FSharpList[ArcAssay]]] | None:
        arg_3: Decoder_1[FSharpList[tuple[ArcStudy, FSharpList[ArcAssay]]]] = list_1_1(Study_ROCrate_decoder)
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("studies", arg_3)

    pattern_input: tuple[FSharpList[ArcStudy], FSharpList[FSharpList[ArcAssay]]] = unzip(default_arg(_arrow1870(), empty()))
    studies_raw: FSharpList[ArcStudy] = pattern_input[0]
    def projection(a: ArcAssay) -> str:
        return a.Identifier

    class ObjectExpr1872:
        @property
        def Equals(self) -> Callable[[str, str], bool]:
            def _arrow1871(x: str, y: str) -> bool:
                return x == y

            return _arrow1871

        @property
        def GetHashCode(self) -> Callable[[str], int]:
            return string_hash

    assays: Array[ArcAssay] = list(distinct_by(projection, concat(pattern_input[1]), ObjectExpr1872()))
    studies: Array[ArcStudy] = list(studies_raw)
    def mapping(a_1: ArcStudy) -> str:
        return a_1.Identifier

    study_identifiers: Array[str] = list(map(mapping, studies_raw))
    def _arrow1873(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("title", string)

    def _arrow1874(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("description", string)

    def _arrow1875(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("submissionDate", string)

    def _arrow1876(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("publicReleaseDate", string)

    def _arrow1877(__unit: None=None) -> Array[OntologySourceReference] | None:
        arg_13: Decoder_1[Array[OntologySourceReference]] = Decode_resizeArray(OntologySourceReference_ROCrate_decoder)
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("ontologySourceReferences", arg_13)

    def _arrow1878(__unit: None=None) -> Array[Publication] | None:
        arg_15: Decoder_1[Array[Publication]] = Decode_resizeArray(Publication_ROCrate_decoder)
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("publications", arg_15)

    def _arrow1879(__unit: None=None) -> Array[Person] | None:
        arg_17: Decoder_1[Array[Person]] = Decode_resizeArray(Person_ROCrate_decoder)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("people", arg_17)

    def _arrow1880(__unit: None=None) -> Array[Comment] | None:
        arg_19: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_ROCrate_decoder)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("comments", arg_19)

    return ArcInvestigation(identifier, _arrow1873(), _arrow1874(), _arrow1875(), _arrow1876(), _arrow1877(), _arrow1878(), _arrow1879(), assays, studies, study_identifiers, _arrow1880())


Investigation_ROCrate_decoder: Decoder_1[ArcInvestigation] = object(_arrow1881)

def Investigation_ROCrate_encodeRoCrate(oa: ArcInvestigation) -> Json:
    def chooser(tupled_arg: tuple[str, Json], oa: Any=oa) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1883(value: str, oa: Any=oa) -> Json:
        return Json(0, value)

    def _arrow1884(value_2: str, oa: Any=oa) -> Json:
        return Json(0, value_2)

    def _arrow1885(oa_1: ArcInvestigation, oa: Any=oa) -> Json:
        return Investigation_ROCrate_encoder(oa_1)

    return Json(5, choose(chooser, of_array([try_include("@type", _arrow1883, "CreativeWork"), try_include("@id", _arrow1884, "ro-crate-metadata.json"), try_include("about", _arrow1885, oa), ("conformsTo", conforms_to_jsonvalue), ("@context", context_jsonvalue_1)])))


Investigation_ISAJson_allowedFields: FSharpList[str] = of_array(["@id", "filename", "identifier", "title", "description", "submissionDate", "publicReleaseDate", "ontologySourceReferences", "publications", "people", "studies", "comments", "@type", "@context"])

def Investigation_ISAJson_encoder(inv: ArcInvestigation) -> Json:
    def chooser(tupled_arg: tuple[str, Json], inv: Any=inv) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1887(value_2: str, inv: Any=inv) -> Json:
        return Json(0, value_2)

    def _arrow1888(value_4: str, inv: Any=inv) -> Json:
        return Json(0, value_4)

    def _arrow1889(value_6: str, inv: Any=inv) -> Json:
        return Json(0, value_6)

    def _arrow1890(value_8: str, inv: Any=inv) -> Json:
        return Json(0, value_8)

    def _arrow1891(oa: Publication, inv: Any=inv) -> Json:
        return Publication_ISAJson_encoder(oa)

    def _arrow1892(person: Person, inv: Any=inv) -> Json:
        return Person_ISAJson_encoder(person)

    def _arrow1893(s: ArcStudy, inv: Any=inv) -> Json:
        return Study_ISAJson_encoder(None, s)

    return Json(5, choose(chooser, of_array([("filename", Json(0, ArcInvestigation.FileName())), ("identifier", Json(0, inv.Identifier)), try_include("title", _arrow1887, inv.Title), try_include("description", _arrow1888, inv.Description), try_include("submissionDate", _arrow1889, inv.SubmissionDate), try_include("publicReleaseDate", _arrow1890, inv.PublicReleaseDate), try_include_seq("ontologySourceReferences", OntologySourceReference_ISAJson_encoder, inv.OntologySourceReferences), try_include_seq("publications", _arrow1891, inv.Publications), try_include_seq("people", _arrow1892, inv.Contacts), try_include_seq("studies", _arrow1893, inv.Studies), try_include_seq("comments", Comment_ISAJson_encoder, inv.Comments)])))


def _arrow1909(get: IGetters) -> ArcInvestigation:
    identifer: str
    match_value: str | None
    object_arg: IOptionalGetter = get.Optional
    match_value = object_arg.Field("identifier", string)
    identifer = create_missing_identifier() if (match_value is None) else match_value
    def _arrow1898(__unit: None=None) -> FSharpList[tuple[ArcStudy, FSharpList[ArcAssay]]] | None:
        arg_3: Decoder_1[FSharpList[tuple[ArcStudy, FSharpList[ArcAssay]]]] = list_1_1(Study_ISAJson_decoder)
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("studies", arg_3)

    pattern_input: tuple[FSharpList[ArcStudy], FSharpList[FSharpList[ArcAssay]]] = unzip(default_arg(_arrow1898(), empty()))
    studies_raw: FSharpList[ArcStudy] = pattern_input[0]
    def projection(a: ArcAssay) -> str:
        return a.Identifier

    class ObjectExpr1900:
        @property
        def Equals(self) -> Callable[[str, str], bool]:
            def _arrow1899(x: str, y: str) -> bool:
                return x == y

            return _arrow1899

        @property
        def GetHashCode(self) -> Callable[[str], int]:
            return string_hash

    assays: Array[ArcAssay] = list(distinct_by(projection, concat(pattern_input[1]), ObjectExpr1900()))
    studies: Array[ArcStudy] = list(studies_raw)
    def mapping(a_1: ArcStudy) -> str:
        return a_1.Identifier

    study_identifiers: Array[str] = list(map(mapping, studies_raw))
    def _arrow1901(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("title", string)

    def _arrow1902(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("description", string)

    def _arrow1903(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("submissionDate", string)

    def _arrow1904(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("publicReleaseDate", string)

    def _arrow1905(__unit: None=None) -> Array[OntologySourceReference] | None:
        arg_13: Decoder_1[Array[OntologySourceReference]] = Decode_resizeArray(OntologySourceReference_ISAJson_decoder)
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("ontologySourceReferences", arg_13)

    def _arrow1906(__unit: None=None) -> Array[Publication] | None:
        arg_15: Decoder_1[Array[Publication]] = Decode_resizeArray(Publication_ISAJson_decoder)
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("publications", arg_15)

    def _arrow1907(__unit: None=None) -> Array[Person] | None:
        arg_17: Decoder_1[Array[Person]] = Decode_resizeArray(Person_ISAJson_decoder)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("people", arg_17)

    def _arrow1908(__unit: None=None) -> Array[Comment] | None:
        arg_19: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_ISAJson_decoder)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("comments", arg_19)

    return ArcInvestigation(identifer, _arrow1901(), _arrow1902(), _arrow1903(), _arrow1904(), _arrow1905(), _arrow1906(), _arrow1907(), assays, studies, study_identifiers, _arrow1908())


Investigation_ISAJson_decoder: Decoder_1[ArcInvestigation] = Decode_objectNoAdditionalProperties(Investigation_ISAJson_allowedFields, _arrow1909)

def ARCtrl_ArcInvestigation__ArcInvestigation_fromJsonString_Static_Z721C83C5(s: str) -> ArcInvestigation:
    match_value: FSharpResult_2[ArcInvestigation, str] = Decode_fromString(Investigation_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_ArcInvestigation__ArcInvestigation_toJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[ArcInvestigation], str]:
    def _arrow1910(obj: ArcInvestigation, spaces: Any=spaces) -> str:
        value: Json = Investigation_encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow1910


def ARCtrl_ArcInvestigation__ArcInvestigation_fromCompressedJsonString_Static_Z721C83C5(s: str) -> ArcInvestigation:
    try: 
        match_value: FSharpResult_2[ArcInvestigation, str] = Decode_fromString(decode(Investigation_decoderCompressed), s)
        if match_value.tag == 1:
            raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

        else: 
            return match_value.fields[0]


    except Exception as e_1:
        arg_1: str = str(e_1)
        return to_fail(printf("Error. Unable to parse json string to ArcStudy: %s"))(arg_1)



def ARCtrl_ArcInvestigation__ArcInvestigation_toCompressedJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[ArcInvestigation], str]:
    def _arrow1911(obj: ArcInvestigation, spaces: Any=spaces) -> str:
        return to_string(default_arg(spaces, 0), encode(Investigation_encoderCompressed, obj))

    return _arrow1911


def ARCtrl_ArcInvestigation__ArcInvestigation_fromROCrateJsonString_Static_Z721C83C5(s: str) -> ArcInvestigation:
    match_value: FSharpResult_2[ArcInvestigation, str] = Decode_fromString(Investigation_ROCrate_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_ArcInvestigation__ArcInvestigation_toROCrateJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[ArcInvestigation], str]:
    def _arrow1912(obj: ArcInvestigation, spaces: Any=spaces) -> str:
        value: Json = Investigation_ROCrate_encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow1912


def ARCtrl_ArcInvestigation__ArcInvestigation_toISAJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[ArcInvestigation], str]:
    def _arrow1913(obj: ArcInvestigation, spaces: Any=spaces) -> str:
        value: Json = Investigation_ISAJson_encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow1913


def ARCtrl_ArcInvestigation__ArcInvestigation_fromISAJsonString_Static_Z721C83C5(s: str) -> ArcInvestigation:
    match_value: FSharpResult_2[ArcInvestigation, str] = Decode_fromString(Investigation_ISAJson_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



__all__ = ["Investigation_encoder", "Investigation_decoder", "Investigation_encoderCompressed", "Investigation_decoderCompressed", "Investigation_ROCrate_genID", "Investigation_ROCrate_encoder", "Investigation_ROCrate_decoder", "Investigation_ROCrate_encodeRoCrate", "Investigation_ISAJson_allowedFields", "Investigation_ISAJson_encoder", "Investigation_ISAJson_decoder", "ARCtrl_ArcInvestigation__ArcInvestigation_fromJsonString_Static_Z721C83C5", "ARCtrl_ArcInvestigation__ArcInvestigation_toJsonString_Static_71136F3F", "ARCtrl_ArcInvestigation__ArcInvestigation_fromCompressedJsonString_Static_Z721C83C5", "ARCtrl_ArcInvestigation__ArcInvestigation_toCompressedJsonString_Static_71136F3F", "ARCtrl_ArcInvestigation__ArcInvestigation_fromROCrateJsonString_Static_Z721C83C5", "ARCtrl_ArcInvestigation__ArcInvestigation_toROCrateJsonString_Static_71136F3F", "ARCtrl_ArcInvestigation__ArcInvestigation_toISAJsonString_Static_71136F3F", "ARCtrl_ArcInvestigation__ArcInvestigation_fromISAJsonString_Static_Z721C83C5"]

