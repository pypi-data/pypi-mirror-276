from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_modules.fable_library.list import (choose, of_array, FSharpList)
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.string_ import (replace, to_text, printf)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import equals
from ..fable_modules.thoth_json_core.decode import (object, IOptionalGetter, string, IGetters)
from ..fable_modules.thoth_json_core.types import (Json, Decoder_1)
from ..fable_modules.thoth_json_python.decode import Decode_fromString
from ..fable_modules.thoth_json_python.encode import to_string
from ..Core.comment import Comment
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.publication import Publication
from .comment import (Comment_encoder, Comment_decoder, Comment_ROCrate_encoderDisambiguatingDescription, Comment_ROCrate_decoderDisambiguatingDescription, Comment_ISAJson_encoder)
from .context.rocrate.isa_publication_context import context_jsonvalue
from .decode import (Decode_uri, Decode_resizeArray, Decode_noAdditionalProperties)
from .encode import (try_include, try_include_seq, default_spaces)
from .ontology_annotation import (OntologyAnnotation_encoder, OntologyAnnotation_decoder, OntologyAnnotation_ROCrate_encoderDefinedTerm, OntologyAnnotation_ROCrate_decoderDefinedTerm)
from .person import (Person_ROCrate_encodeAuthorListString, Person_ROCrate_decodeAuthorListString)

def Publication_encoder(oa: Publication) -> Json:
    def chooser(tupled_arg: tuple[str, Json], oa: Any=oa) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1137(value: str, oa: Any=oa) -> Json:
        return Json(0, value)

    def _arrow1138(value_2: str, oa: Any=oa) -> Json:
        return Json(0, value_2)

    def _arrow1139(value_4: str, oa: Any=oa) -> Json:
        return Json(0, value_4)

    def _arrow1140(value_6: str, oa: Any=oa) -> Json:
        return Json(0, value_6)

    def _arrow1141(oa_1: OntologyAnnotation, oa: Any=oa) -> Json:
        return OntologyAnnotation_encoder(oa_1)

    def _arrow1142(comment: Comment, oa: Any=oa) -> Json:
        return Comment_encoder(comment)

    return Json(5, choose(chooser, of_array([try_include("pubMedID", _arrow1137, oa.PubMedID), try_include("doi", _arrow1138, oa.DOI), try_include("authorList", _arrow1139, oa.Authors), try_include("title", _arrow1140, oa.Title), try_include("status", _arrow1141, oa.Status), try_include_seq("comments", _arrow1142, oa.Comments)])))


def _arrow1149(get: IGetters) -> Publication:
    def _arrow1143(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("pubMedID", Decode_uri)

    def _arrow1144(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("doi", string)

    def _arrow1145(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("authorList", string)

    def _arrow1146(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("title", string)

    def _arrow1147(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("status", OntologyAnnotation_decoder)

    def _arrow1148(__unit: None=None) -> Array[Comment] | None:
        arg_11: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_decoder)
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("comments", arg_11)

    return Publication(_arrow1143(), _arrow1144(), _arrow1145(), _arrow1146(), _arrow1147(), _arrow1148())


Publication_decoder: Decoder_1[Publication] = object(_arrow1149)

def Publication_ROCrate_genID(p: Publication) -> str:
    match_value: str | None = p.DOI
    if match_value is None:
        match_value_1: str | None = p.PubMedID
        if match_value_1 is None:
            match_value_2: str | None = p.Title
            if match_value_2 is None:
                return "#EmptyPublication"

            else: 
                return "#Pub_" + replace(match_value_2, " ", "_")


        else: 
            return match_value_1


    else: 
        return match_value



def Publication_ROCrate_encoder(oa: Publication) -> Json:
    def chooser(tupled_arg: tuple[str, Json], oa: Any=oa) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1150(value_2: str, oa: Any=oa) -> Json:
        return Json(0, value_2)

    def _arrow1151(value_4: str, oa: Any=oa) -> Json:
        return Json(0, value_4)

    def _arrow1152(author_list: str, oa: Any=oa) -> Json:
        return Person_ROCrate_encodeAuthorListString(author_list)

    def _arrow1153(value_6: str, oa: Any=oa) -> Json:
        return Json(0, value_6)

    def _arrow1154(oa_1: OntologyAnnotation, oa: Any=oa) -> Json:
        return OntologyAnnotation_ROCrate_encoderDefinedTerm(oa_1)

    def _arrow1155(comment: Comment, oa: Any=oa) -> Json:
        return Comment_ROCrate_encoderDisambiguatingDescription(comment)

    return Json(5, choose(chooser, of_array([("@id", Json(0, Publication_ROCrate_genID(oa))), ("@type", Json(0, "Publication")), try_include("pubMedID", _arrow1150, oa.PubMedID), try_include("doi", _arrow1151, oa.DOI), try_include("authorList", _arrow1152, oa.Authors), try_include("title", _arrow1153, oa.Title), try_include("status", _arrow1154, oa.Status), try_include_seq("comments", _arrow1155, oa.Comments), ("@context", context_jsonvalue)])))


def _arrow1162(get: IGetters) -> Publication:
    def _arrow1156(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("pubMedID", Decode_uri)

    def _arrow1157(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("doi", string)

    def _arrow1158(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("authorList", Person_ROCrate_decodeAuthorListString)

    def _arrow1159(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("title", string)

    def _arrow1160(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("status", OntologyAnnotation_ROCrate_decoderDefinedTerm)

    def _arrow1161(__unit: None=None) -> Array[Comment] | None:
        arg_11: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_ROCrate_decoderDisambiguatingDescription)
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("comments", arg_11)

    return Publication(_arrow1156(), _arrow1157(), _arrow1158(), _arrow1159(), _arrow1160(), _arrow1161())


Publication_ROCrate_decoder: Decoder_1[Publication] = object(_arrow1162)

def Publication_ISAJson_encoder(oa: Publication) -> Json:
    def chooser(tupled_arg: tuple[str, Json], oa: Any=oa) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1164(value: str, oa: Any=oa) -> Json:
        return Json(0, value)

    def _arrow1165(value_2: str, oa: Any=oa) -> Json:
        return Json(0, value_2)

    def _arrow1166(value_4: str, oa: Any=oa) -> Json:
        return Json(0, value_4)

    def _arrow1167(value_6: str, oa: Any=oa) -> Json:
        return Json(0, value_6)

    def _arrow1168(oa_1: OntologyAnnotation, oa: Any=oa) -> Json:
        return OntologyAnnotation_encoder(oa_1)

    return Json(5, choose(chooser, of_array([try_include("pubMedID", _arrow1164, oa.PubMedID), try_include("doi", _arrow1165, oa.DOI), try_include("authorList", _arrow1166, oa.Authors), try_include("title", _arrow1167, oa.Title), try_include("status", _arrow1168, oa.Status), try_include_seq("comments", Comment_ISAJson_encoder, oa.Comments)])))


Publication_ISAJson_allowedFields: FSharpList[str] = of_array(["pubMedID", "doi", "authorList", "title", "status", "comments"])

Publication_ISAJson_decoder: Decoder_1[Publication] = Decode_noAdditionalProperties(Publication_ISAJson_allowedFields, Publication_decoder)

def ARCtrl_Publication__Publication_fromJsonString_Static_Z721C83C5(s: str) -> Publication:
    match_value: FSharpResult_2[Publication, str] = Decode_fromString(Publication_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Publication__Publication_toJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[Publication], str]:
    def _arrow1169(obj: Publication, spaces: Any=spaces) -> str:
        value: Json = Publication_encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow1169


def ARCtrl_Publication__Publication_fromROCrateJsonString_Static_Z721C83C5(s: str) -> Publication:
    match_value: FSharpResult_2[Publication, str] = Decode_fromString(Publication_ROCrate_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Publication__Publication_toROCrateJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[Publication], str]:
    def _arrow1176(obj: Publication, spaces: Any=spaces) -> str:
        value: Json = Publication_ROCrate_encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow1176


def ARCtrl_Publication__Publication_toISAJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[Publication], str]:
    def _arrow1180(obj: Publication, spaces: Any=spaces) -> str:
        value: Json = Publication_ISAJson_encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow1180


def ARCtrl_Publication__Publication_fromISAJsonString_Static_Z721C83C5(s: str) -> Publication:
    match_value: FSharpResult_2[Publication, str] = Decode_fromString(Publication_ISAJson_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



__all__ = ["Publication_encoder", "Publication_decoder", "Publication_ROCrate_genID", "Publication_ROCrate_encoder", "Publication_ROCrate_decoder", "Publication_ISAJson_encoder", "Publication_ISAJson_allowedFields", "Publication_ISAJson_decoder", "ARCtrl_Publication__Publication_fromJsonString_Static_Z721C83C5", "ARCtrl_Publication__Publication_toJsonString_Static_71136F3F", "ARCtrl_Publication__Publication_fromROCrateJsonString_Static_Z721C83C5", "ARCtrl_Publication__Publication_toROCrateJsonString_Static_71136F3F", "ARCtrl_Publication__Publication_toISAJsonString_Static_71136F3F", "ARCtrl_Publication__Publication_fromISAJsonString_Static_Z721C83C5"]

