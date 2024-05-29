from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_modules.fable_library.list import (of_array, choose)
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.string_ import (replace, to_text, printf)
from ..fable_modules.fable_library.types import (to_string, Array)
from ..fable_modules.fable_library.util import (int32_to_string, equals)
from ..fable_modules.thoth_json_core.decode import (one_of, map, int_1, float_1, string, object, IOptionalGetter, IGetters)
from ..fable_modules.thoth_json_core.types import (Decoder_1, Json)
from ..fable_modules.thoth_json_python.decode import Decode_fromString
from ..fable_modules.thoth_json_python.encode import to_string as to_string_1
from ..Core.comment import Comment
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.uri import URIModule_toString
from .comment import (Comment_encoder, Comment_decoder, Comment_ROCrate_encoderDisambiguatingDescription, Comment_ROCrate_decoderDisambiguatingDescription)
from .context.rocrate.isa_ontology_annotation_context import context_jsonvalue
from .context.rocrate.property_value_context import context_jsonvalue as context_jsonvalue_1
from .decode import Decode_resizeArray
from .encode import (try_include, try_include_seq, default_spaces)
from .string_table import (encode_string, decode_string)

AnnotationValue_decoder: Decoder_1[str] = one_of(of_array([map(int32_to_string, int_1), map(to_string, float_1), string]))

def OntologyAnnotation_encoder(oa: OntologyAnnotation) -> Json:
    def chooser(tupled_arg: tuple[str, Json], oa: Any=oa) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1066(value: str, oa: Any=oa) -> Json:
        return Json(0, value)

    def _arrow1067(value_2: str, oa: Any=oa) -> Json:
        return Json(0, value_2)

    def _arrow1068(value_4: str, oa: Any=oa) -> Json:
        return Json(0, value_4)

    def _arrow1069(comment: Comment, oa: Any=oa) -> Json:
        return Comment_encoder(comment)

    return Json(5, choose(chooser, of_array([try_include("annotationValue", _arrow1066, oa.Name), try_include("termSource", _arrow1067, oa.TermSourceREF), try_include("termAccession", _arrow1068, oa.TermAccessionNumber), try_include_seq("comments", _arrow1069, oa.Comments)])))


def _arrow1074(get: IGetters) -> OntologyAnnotation:
    def _arrow1070(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("annotationValue", AnnotationValue_decoder)

    def _arrow1071(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("termSource", string)

    def _arrow1072(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("termAccession", string)

    def _arrow1073(__unit: None=None) -> Array[Comment] | None:
        arg_7: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_decoder)
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("comments", arg_7)

    return OntologyAnnotation.create(_arrow1070(), _arrow1071(), _arrow1072(), _arrow1073())


OntologyAnnotation_decoder: Decoder_1[OntologyAnnotation] = object(_arrow1074)

def OntologyAnnotation_compressedEncoder(string_table: Any, oa: OntologyAnnotation) -> Json:
    def chooser(tupled_arg: tuple[str, Json], string_table: Any=string_table, oa: Any=oa) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1076(s: str, string_table: Any=string_table, oa: Any=oa) -> Json:
        return encode_string(string_table, s)

    def _arrow1077(s_1: str, string_table: Any=string_table, oa: Any=oa) -> Json:
        return encode_string(string_table, s_1)

    def _arrow1078(s_2: str, string_table: Any=string_table, oa: Any=oa) -> Json:
        return encode_string(string_table, s_2)

    def _arrow1079(comment: Comment, string_table: Any=string_table, oa: Any=oa) -> Json:
        return Comment_encoder(comment)

    return Json(5, choose(chooser, of_array([try_include("a", _arrow1076, oa.Name), try_include("ts", _arrow1077, oa.TermSourceREF), try_include("ta", _arrow1078, oa.TermAccessionNumber), try_include_seq("comments", _arrow1079, oa.Comments)])))


def OntologyAnnotation_compressedDecoder(string_table: Array[str]) -> Decoder_1[OntologyAnnotation]:
    def _arrow1084(get: IGetters, string_table: Any=string_table) -> OntologyAnnotation:
        def _arrow1080(__unit: None=None) -> str | None:
            arg_1: Decoder_1[str] = decode_string(string_table)
            object_arg: IOptionalGetter = get.Optional
            return object_arg.Field("a", arg_1)

        def _arrow1081(__unit: None=None) -> str | None:
            arg_3: Decoder_1[str] = decode_string(string_table)
            object_arg_1: IOptionalGetter = get.Optional
            return object_arg_1.Field("ts", arg_3)

        def _arrow1082(__unit: None=None) -> str | None:
            arg_5: Decoder_1[str] = decode_string(string_table)
            object_arg_2: IOptionalGetter = get.Optional
            return object_arg_2.Field("ta", arg_5)

        def _arrow1083(__unit: None=None) -> Array[Comment] | None:
            arg_7: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_decoder)
            object_arg_3: IOptionalGetter = get.Optional
            return object_arg_3.Field("comments", arg_7)

        return OntologyAnnotation(_arrow1080(), _arrow1081(), _arrow1082(), _arrow1083())

    return object(_arrow1084)


def OntologyAnnotation_ROCrate_genID(o: OntologyAnnotation) -> str:
    match_value: str | None = o.TermAccessionNumber
    if match_value is None:
        match_value_1: str | None = o.TermSourceREF
        if match_value_1 is None:
            match_value_2: str | None = o.Name
            if match_value_2 is None:
                return "#DummyOntologyAnnotation"

            else: 
                return "#UserTerm_" + replace(match_value_2, " ", "_")


        else: 
            return "#" + replace(match_value_1, " ", "_")


    else: 
        return URIModule_toString(match_value)



def OntologyAnnotation_ROCrate_encoderDefinedTerm(oa: OntologyAnnotation) -> Json:
    def chooser(tupled_arg: tuple[str, Json], oa: Any=oa) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1085(value_2: str, oa: Any=oa) -> Json:
        return Json(0, value_2)

    def _arrow1086(value_4: str, oa: Any=oa) -> Json:
        return Json(0, value_4)

    def _arrow1087(value_6: str, oa: Any=oa) -> Json:
        return Json(0, value_6)

    def _arrow1088(comment: Comment, oa: Any=oa) -> Json:
        return Comment_ROCrate_encoderDisambiguatingDescription(comment)

    return Json(5, choose(chooser, of_array([("@id", Json(0, OntologyAnnotation_ROCrate_genID(oa))), ("@type", Json(0, "OntologyAnnotation")), try_include("annotationValue", _arrow1085, oa.Name), try_include("termSource", _arrow1086, oa.TermSourceREF), try_include("termAccession", _arrow1087, oa.TermAccessionNumber), try_include_seq("comments", _arrow1088, oa.Comments), ("@context", context_jsonvalue)])))


def _arrow1093(get: IGetters) -> OntologyAnnotation:
    def _arrow1089(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("annotationValue", AnnotationValue_decoder)

    def _arrow1090(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("termSource", string)

    def _arrow1091(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("termAccession", string)

    def _arrow1092(__unit: None=None) -> Array[Comment] | None:
        arg_7: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_ROCrate_decoderDisambiguatingDescription)
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("comments", arg_7)

    return OntologyAnnotation.create(_arrow1089(), _arrow1090(), _arrow1091(), _arrow1092())


OntologyAnnotation_ROCrate_decoderDefinedTerm: Decoder_1[OntologyAnnotation] = object(_arrow1093)

def OntologyAnnotation_ROCrate_encoderPropertyValue(oa: OntologyAnnotation) -> Json:
    def chooser(tupled_arg: tuple[str, Json], oa: Any=oa) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1094(value_2: str, oa: Any=oa) -> Json:
        return Json(0, value_2)

    def _arrow1095(value_4: str, oa: Any=oa) -> Json:
        return Json(0, value_4)

    def _arrow1096(comment: Comment, oa: Any=oa) -> Json:
        return Comment_ROCrate_encoderDisambiguatingDescription(comment)

    return Json(5, choose(chooser, of_array([("@id", Json(0, OntologyAnnotation_ROCrate_genID(oa))), ("@type", Json(0, "PropertyValue")), try_include("category", _arrow1094, oa.Name), try_include("categoryCode", _arrow1095, oa.TermAccessionNumber), try_include_seq("comments", _arrow1096, oa.Comments), ("@context", context_jsonvalue_1)])))


def _arrow1100(get: IGetters) -> OntologyAnnotation:
    def _arrow1097(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("category", string)

    def _arrow1098(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("categoryCode", string)

    def _arrow1099(__unit: None=None) -> Array[Comment] | None:
        arg_5: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_ROCrate_decoderDisambiguatingDescription)
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("comments", arg_5)

    return OntologyAnnotation.create(_arrow1097(), None, _arrow1098(), _arrow1099())


OntologyAnnotation_ROCrate_decoderPropertyValue: Decoder_1[OntologyAnnotation] = object(_arrow1100)

OntologyAnnotation_ISAJson_encoder: Callable[[OntologyAnnotation], Json] = OntologyAnnotation_encoder

OntologyAnnotation_ISAJson_decoder: Decoder_1[OntologyAnnotation] = OntologyAnnotation_decoder

def ARCtrl_OntologyAnnotation__OntologyAnnotation_fromJsonString_Static_Z721C83C5(s: str) -> OntologyAnnotation:
    match_value: FSharpResult_2[OntologyAnnotation, str] = Decode_fromString(OntologyAnnotation_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_OntologyAnnotation__OntologyAnnotation_toJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[OntologyAnnotation], str]:
    def _arrow1101(obj: OntologyAnnotation, spaces: Any=spaces) -> str:
        value: Json = OntologyAnnotation_encoder(obj)
        return to_string_1(default_spaces(spaces), value)

    return _arrow1101


def ARCtrl_OntologyAnnotation__OntologyAnnotation_fromROCrateJsonString_Static_Z721C83C5(s: str) -> OntologyAnnotation:
    match_value: FSharpResult_2[OntologyAnnotation, str] = Decode_fromString(OntologyAnnotation_ROCrate_decoderDefinedTerm, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_OntologyAnnotation__OntologyAnnotation_toROCrateJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[OntologyAnnotation], str]:
    def _arrow1102(obj: OntologyAnnotation, spaces: Any=spaces) -> str:
        value: Json = OntologyAnnotation_ROCrate_encoderDefinedTerm(obj)
        return to_string_1(default_spaces(spaces), value)

    return _arrow1102


def ARCtrl_OntologyAnnotation__OntologyAnnotation_toISAJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[OntologyAnnotation], str]:
    def _arrow1103(obj: OntologyAnnotation, spaces: Any=spaces) -> str:
        value: Json = OntologyAnnotation_ISAJson_encoder(obj)
        return to_string_1(default_spaces(spaces), value)

    return _arrow1103


def ARCtrl_OntologyAnnotation__OntologyAnnotation_fromISAJsonString_Static_Z721C83C5(s: str) -> OntologyAnnotation:
    match_value: FSharpResult_2[OntologyAnnotation, str] = Decode_fromString(OntologyAnnotation_ISAJson_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



__all__ = ["AnnotationValue_decoder", "OntologyAnnotation_encoder", "OntologyAnnotation_decoder", "OntologyAnnotation_compressedEncoder", "OntologyAnnotation_compressedDecoder", "OntologyAnnotation_ROCrate_genID", "OntologyAnnotation_ROCrate_encoderDefinedTerm", "OntologyAnnotation_ROCrate_decoderDefinedTerm", "OntologyAnnotation_ROCrate_encoderPropertyValue", "OntologyAnnotation_ROCrate_decoderPropertyValue", "OntologyAnnotation_ISAJson_encoder", "OntologyAnnotation_ISAJson_decoder", "ARCtrl_OntologyAnnotation__OntologyAnnotation_fromJsonString_Static_Z721C83C5", "ARCtrl_OntologyAnnotation__OntologyAnnotation_toJsonString_Static_71136F3F", "ARCtrl_OntologyAnnotation__OntologyAnnotation_fromROCrateJsonString_Static_Z721C83C5", "ARCtrl_OntologyAnnotation__OntologyAnnotation_toROCrateJsonString_Static_71136F3F", "ARCtrl_OntologyAnnotation__OntologyAnnotation_toISAJsonString_Static_71136F3F", "ARCtrl_OntologyAnnotation__OntologyAnnotation_fromISAJsonString_Static_Z721C83C5"]

