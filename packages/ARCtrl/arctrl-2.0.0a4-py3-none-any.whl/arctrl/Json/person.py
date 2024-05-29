from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_modules.fable_library.array_ import map
from ..fable_modules.fable_library.list import (choose, of_array, FSharpList)
from ..fable_modules.fable_library.option import default_arg
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.seq import try_pick
from ..fable_modules.fable_library.string_ import (replace, split, join, to_text, printf)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import (equals, to_enumerable)
from ..fable_modules.thoth_json_core.decode import (object, IOptionalGetter, string, IGetters, IRequiredGetter, map as map_1, array as array_2)
from ..fable_modules.thoth_json_core.types import (Json, Decoder_1)
from ..fable_modules.thoth_json_python.decode import Decode_fromString
from ..fable_modules.thoth_json_python.encode import to_string
from ..Core.comment import Comment
from ..Core.conversion import (Person_setCommentFromORCID, Person_setOrcidFromComments)
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.person import Person
from .comment import (Comment_encoder, Comment_decoder, Comment_ROCrate_encoderDisambiguatingDescription, Comment_ROCrate_decoderDisambiguatingDescription)
from .context.rocrate.isa_organization_context import context_jsonvalue
from .context.rocrate.isa_person_context import (context_jsonvalue as context_jsonvalue_1, context_minimal_json_value)
from .decode import (Decode_resizeArray, Decode_objectNoAdditionalProperties)
from .encode import (try_include, try_include_seq, default_spaces)
from .ontology_annotation import (OntologyAnnotation_encoder, OntologyAnnotation_decoder, OntologyAnnotation_ROCrate_encoderDefinedTerm, OntologyAnnotation_ROCrate_decoderDefinedTerm)

def Person_encoder(person: Person) -> Json:
    def chooser(tupled_arg: tuple[str, Json], person: Any=person) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1170(value: str, person: Any=person) -> Json:
        return Json(0, value)

    def _arrow1171(value_2: str, person: Any=person) -> Json:
        return Json(0, value_2)

    def _arrow1172(value_4: str, person: Any=person) -> Json:
        return Json(0, value_4)

    def _arrow1173(value_6: str, person: Any=person) -> Json:
        return Json(0, value_6)

    def _arrow1174(value_8: str, person: Any=person) -> Json:
        return Json(0, value_8)

    def _arrow1175(value_10: str, person: Any=person) -> Json:
        return Json(0, value_10)

    def _arrow1177(value_12: str, person: Any=person) -> Json:
        return Json(0, value_12)

    def _arrow1178(value_14: str, person: Any=person) -> Json:
        return Json(0, value_14)

    def _arrow1179(value_16: str, person: Any=person) -> Json:
        return Json(0, value_16)

    def _arrow1181(oa: OntologyAnnotation, person: Any=person) -> Json:
        return OntologyAnnotation_encoder(oa)

    def _arrow1182(comment: Comment, person: Any=person) -> Json:
        return Comment_encoder(comment)

    return Json(5, choose(chooser, of_array([try_include("firstName", _arrow1170, person.FirstName), try_include("lastName", _arrow1171, person.LastName), try_include("midInitials", _arrow1172, person.MidInitials), try_include("orcid", _arrow1173, person.ORCID), try_include("email", _arrow1174, person.EMail), try_include("phone", _arrow1175, person.Phone), try_include("fax", _arrow1177, person.Fax), try_include("address", _arrow1178, person.Address), try_include("affiliation", _arrow1179, person.Affiliation), try_include_seq("roles", _arrow1181, person.Roles), try_include_seq("comments", _arrow1182, person.Comments)])))


def _arrow1194(get: IGetters) -> Person:
    def _arrow1183(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("orcid", string)

    def _arrow1184(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("lastName", string)

    def _arrow1185(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("firstName", string)

    def _arrow1186(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("midInitials", string)

    def _arrow1187(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("email", string)

    def _arrow1188(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("phone", string)

    def _arrow1189(__unit: None=None) -> str | None:
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("fax", string)

    def _arrow1190(__unit: None=None) -> str | None:
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("address", string)

    def _arrow1191(__unit: None=None) -> str | None:
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("affiliation", string)

    def _arrow1192(__unit: None=None) -> Array[OntologyAnnotation] | None:
        arg_19: Decoder_1[Array[OntologyAnnotation]] = Decode_resizeArray(OntologyAnnotation_decoder)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("roles", arg_19)

    def _arrow1193(__unit: None=None) -> Array[Comment] | None:
        arg_21: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_decoder)
        object_arg_10: IOptionalGetter = get.Optional
        return object_arg_10.Field("comments", arg_21)

    return Person(_arrow1183(), _arrow1184(), _arrow1185(), _arrow1186(), _arrow1187(), _arrow1188(), _arrow1189(), _arrow1190(), _arrow1191(), _arrow1192(), _arrow1193())


Person_decoder: Decoder_1[Person] = object(_arrow1194)

def Person_ROCrate_genID(p: Person) -> str:
    def chooser(c: Comment, p: Any=p) -> str | None:
        matchValue: str | None = c.Name
        matchValue_1: str | None = c.Value
        (pattern_matching_result, n, v) = (None, None, None)
        if matchValue is not None:
            if matchValue_1 is not None:
                pattern_matching_result = 0
                n = matchValue
                v = matchValue_1

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            if True if (True if (n == "orcid") else (n == "Orcid")) else (n == "ORCID"):
                return v

            else: 
                return None


        elif pattern_matching_result == 1:
            return None


    orcid: str | None = try_pick(chooser, p.Comments)
    if orcid is None:
        match_value_1: str | None = p.EMail
        if match_value_1 is None:
            matchValue_2: str | None = p.FirstName
            matchValue_3: str | None = p.MidInitials
            matchValue_4: str | None = p.LastName
            (pattern_matching_result_1, fn, ln, mn, fn_1, ln_1, ln_2, fn_2) = (None, None, None, None, None, None, None, None)
            if matchValue_2 is None:
                if matchValue_3 is None:
                    if matchValue_4 is not None:
                        pattern_matching_result_1 = 2
                        ln_2 = matchValue_4

                    else: 
                        pattern_matching_result_1 = 4


                else: 
                    pattern_matching_result_1 = 4


            elif matchValue_3 is None:
                if matchValue_4 is None:
                    pattern_matching_result_1 = 3
                    fn_2 = matchValue_2

                else: 
                    pattern_matching_result_1 = 1
                    fn_1 = matchValue_2
                    ln_1 = matchValue_4


            elif matchValue_4 is not None:
                pattern_matching_result_1 = 0
                fn = matchValue_2
                ln = matchValue_4
                mn = matchValue_3

            else: 
                pattern_matching_result_1 = 4

            if pattern_matching_result_1 == 0:
                return (((("#" + replace(fn, " ", "_")) + "_") + replace(mn, " ", "_")) + "_") + replace(ln, " ", "_")

            elif pattern_matching_result_1 == 1:
                return (("#" + replace(fn_1, " ", "_")) + "_") + replace(ln_1, " ", "_")

            elif pattern_matching_result_1 == 2:
                return "#" + replace(ln_2, " ", "_")

            elif pattern_matching_result_1 == 3:
                return "#" + replace(fn_2, " ", "_")

            elif pattern_matching_result_1 == 4:
                return "#EmptyPerson"


        else: 
            return match_value_1


    else: 
        return orcid



def Person_ROCrate_Affiliation_encoder(affiliation: str) -> Json:
    return Json(5, to_enumerable([("@type", Json(0, "Organization")), ("@id", Json(0, replace(("#Organization_" + affiliation) + "", " ", "_"))), ("name", Json(0, affiliation)), ("@context", context_jsonvalue)]))


def _arrow1195(get: IGetters) -> str:
    object_arg: IRequiredGetter = get.Required
    return object_arg.Field("name", string)


Person_ROCrate_Affiliation_decoder: Decoder_1[str] = object(_arrow1195)

def Person_ROCrate_encoder(oa: Person) -> Json:
    def chooser(tupled_arg: tuple[str, Json], oa: Any=oa) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1196(value_2: str, oa: Any=oa) -> Json:
        return Json(0, value_2)

    def _arrow1197(value_4: str, oa: Any=oa) -> Json:
        return Json(0, value_4)

    def _arrow1198(value_6: str, oa: Any=oa) -> Json:
        return Json(0, value_6)

    def _arrow1199(value_8: str, oa: Any=oa) -> Json:
        return Json(0, value_8)

    def _arrow1200(value_10: str, oa: Any=oa) -> Json:
        return Json(0, value_10)

    def _arrow1201(value_12: str, oa: Any=oa) -> Json:
        return Json(0, value_12)

    def _arrow1202(value_14: str, oa: Any=oa) -> Json:
        return Json(0, value_14)

    def _arrow1203(value_16: str, oa: Any=oa) -> Json:
        return Json(0, value_16)

    def _arrow1204(affiliation: str, oa: Any=oa) -> Json:
        return Person_ROCrate_Affiliation_encoder(affiliation)

    def _arrow1205(oa_1: OntologyAnnotation, oa: Any=oa) -> Json:
        return OntologyAnnotation_ROCrate_encoderDefinedTerm(oa_1)

    def _arrow1206(comment: Comment, oa: Any=oa) -> Json:
        return Comment_ROCrate_encoderDisambiguatingDescription(comment)

    return Json(5, choose(chooser, of_array([("@id", Json(0, Person_ROCrate_genID(oa))), ("@type", Json(0, "Person")), try_include("orcid", _arrow1196, oa.ORCID), try_include("firstName", _arrow1197, oa.FirstName), try_include("lastName", _arrow1198, oa.LastName), try_include("midInitials", _arrow1199, oa.MidInitials), try_include("email", _arrow1200, oa.EMail), try_include("phone", _arrow1201, oa.Phone), try_include("fax", _arrow1202, oa.Fax), try_include("address", _arrow1203, oa.Address), try_include("affiliation", _arrow1204, oa.Affiliation), try_include_seq("roles", _arrow1205, oa.Roles), try_include_seq("comments", _arrow1206, oa.Comments), ("@context", context_jsonvalue_1)])))


def _arrow1218(get: IGetters) -> Person:
    def _arrow1207(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("orcid", string)

    def _arrow1208(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("lastName", string)

    def _arrow1209(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("firstName", string)

    def _arrow1210(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("midInitials", string)

    def _arrow1211(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("email", string)

    def _arrow1212(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("phone", string)

    def _arrow1213(__unit: None=None) -> str | None:
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("fax", string)

    def _arrow1214(__unit: None=None) -> str | None:
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("address", string)

    def _arrow1215(__unit: None=None) -> str | None:
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("affiliation", Person_ROCrate_Affiliation_decoder)

    def _arrow1216(__unit: None=None) -> Array[OntologyAnnotation] | None:
        arg_19: Decoder_1[Array[OntologyAnnotation]] = Decode_resizeArray(OntologyAnnotation_ROCrate_decoderDefinedTerm)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("roles", arg_19)

    def _arrow1217(__unit: None=None) -> Array[Comment] | None:
        arg_21: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_ROCrate_decoderDisambiguatingDescription)
        object_arg_10: IOptionalGetter = get.Optional
        return object_arg_10.Field("comments", arg_21)

    return Person(_arrow1207(), _arrow1208(), _arrow1209(), _arrow1210(), _arrow1211(), _arrow1212(), _arrow1213(), _arrow1214(), _arrow1215(), _arrow1216(), _arrow1217())


Person_ROCrate_decoder: Decoder_1[Person] = object(_arrow1218)

def Person_ROCrate_encodeAuthorListString(author_list: str) -> Json:
    def encode_single(name: str, author_list: Any=author_list) -> Json:
        def chooser(tupled_arg: tuple[str, Json], name: Any=name) -> tuple[str, Json] | None:
            v: Json = tupled_arg[1]
            if equals(v, Json(3)):
                return None

            else: 
                return (tupled_arg[0], v)


        def _arrow1219(value_1: str, name: Any=name) -> Json:
            return Json(0, value_1)

        return Json(5, choose(chooser, of_array([("@type", Json(0, "Person")), try_include("name", _arrow1219, name), ("@context", context_minimal_json_value)])))

    def mapping(s: str, author_list: Any=author_list) -> str:
        return s.strip()

    return Json(6, map(encode_single, map(mapping, split(author_list, ["\t" if (author_list.find("\t") >= 0) else (";" if (author_list.find(";") >= 0) else ",")], None, 0), None), None))


def ctor(v: Array[str]) -> str:
    return join(", ", v)


def _arrow1221(get: IGetters) -> str:
    def _arrow1220(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("name", string)

    return default_arg(_arrow1220(), "")


Person_ROCrate_decodeAuthorListString: Decoder_1[str] = map_1(ctor, array_2(object(_arrow1221)))

Person_ISAJson_allowedFields: FSharpList[str] = of_array(["@id", "firstName", "lastName", "midInitials", "email", "phone", "fax", "address", "affiliation", "roles", "comments", "@type", "@context"])

def Person_ISAJson_encoder(person: Person) -> Json:
    person_1: Person = Person_setCommentFromORCID(person)
    def chooser(tupled_arg: tuple[str, Json], person: Any=person) -> tuple[str, Json] | None:
        v: Json = tupled_arg[1]
        if equals(v, Json(3)):
            return None

        else: 
            return (tupled_arg[0], v)


    def _arrow1223(value: str, person: Any=person) -> Json:
        return Json(0, value)

    def _arrow1224(value_2: str, person: Any=person) -> Json:
        return Json(0, value_2)

    def _arrow1225(value_4: str, person: Any=person) -> Json:
        return Json(0, value_4)

    def _arrow1226(value_6: str, person: Any=person) -> Json:
        return Json(0, value_6)

    def _arrow1227(value_8: str, person: Any=person) -> Json:
        return Json(0, value_8)

    def _arrow1228(value_10: str, person: Any=person) -> Json:
        return Json(0, value_10)

    def _arrow1229(value_12: str, person: Any=person) -> Json:
        return Json(0, value_12)

    def _arrow1230(value_14: str, person: Any=person) -> Json:
        return Json(0, value_14)

    def _arrow1231(oa: OntologyAnnotation, person: Any=person) -> Json:
        return OntologyAnnotation_encoder(oa)

    def _arrow1232(comment: Comment, person: Any=person) -> Json:
        return Comment_encoder(comment)

    return Json(5, choose(chooser, of_array([try_include("firstName", _arrow1223, person_1.FirstName), try_include("lastName", _arrow1224, person_1.LastName), try_include("midInitials", _arrow1225, person_1.MidInitials), try_include("email", _arrow1226, person_1.EMail), try_include("phone", _arrow1227, person_1.Phone), try_include("fax", _arrow1228, person_1.Fax), try_include("address", _arrow1229, person_1.Address), try_include("affiliation", _arrow1230, person_1.Affiliation), try_include_seq("roles", _arrow1231, person_1.Roles), try_include_seq("comments", _arrow1232, person_1.Comments)])))


def _arrow1243(get: IGetters) -> Person:
    def _arrow1233(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("lastName", string)

    def _arrow1234(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("firstName", string)

    def _arrow1235(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("midInitials", string)

    def _arrow1236(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("email", string)

    def _arrow1237(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("phone", string)

    def _arrow1238(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("fax", string)

    def _arrow1239(__unit: None=None) -> str | None:
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("address", string)

    def _arrow1240(__unit: None=None) -> str | None:
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("affiliation", string)

    def _arrow1241(__unit: None=None) -> Array[OntologyAnnotation] | None:
        arg_17: Decoder_1[Array[OntologyAnnotation]] = Decode_resizeArray(OntologyAnnotation_decoder)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("roles", arg_17)

    def _arrow1242(__unit: None=None) -> Array[Comment] | None:
        arg_19: Decoder_1[Array[Comment]] = Decode_resizeArray(Comment_decoder)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("comments", arg_19)

    return Person_setOrcidFromComments(Person(None, _arrow1233(), _arrow1234(), _arrow1235(), _arrow1236(), _arrow1237(), _arrow1238(), _arrow1239(), _arrow1240(), _arrow1241(), _arrow1242()))


Person_ISAJson_decoder: Decoder_1[Person] = Decode_objectNoAdditionalProperties(Person_ISAJson_allowedFields, _arrow1243)

def ARCtrl_Person__Person_fromJsonString_Static_Z721C83C5(s: str) -> Person:
    match_value: FSharpResult_2[Person, str] = Decode_fromString(Person_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Person__Person_toJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[Person], str]:
    def _arrow1244(obj: Person, spaces: Any=spaces) -> str:
        value: Json = Person_encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow1244


def ARCtrl_Person__Person_fromROCrateJsonString_Static_Z721C83C5(s: str) -> Person:
    match_value: FSharpResult_2[Person, str] = Decode_fromString(Person_ROCrate_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Person__Person_toROCrateJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[Person], str]:
    def _arrow1245(obj: Person, spaces: Any=spaces) -> str:
        value: Json = Person_ROCrate_encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow1245


def ARCtrl_Person__Person_toISAJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[Person], str]:
    def _arrow1246(obj: Person, spaces: Any=spaces) -> str:
        value: Json = Person_ISAJson_encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow1246


def ARCtrl_Person__Person_fromISAJsonString_Static_Z721C83C5(s: str) -> Person:
    match_value: FSharpResult_2[Person, str] = Decode_fromString(Person_ISAJson_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



__all__ = ["Person_encoder", "Person_decoder", "Person_ROCrate_genID", "Person_ROCrate_Affiliation_encoder", "Person_ROCrate_Affiliation_decoder", "Person_ROCrate_encoder", "Person_ROCrate_decoder", "Person_ROCrate_encodeAuthorListString", "Person_ROCrate_decodeAuthorListString", "Person_ISAJson_allowedFields", "Person_ISAJson_encoder", "Person_ISAJson_decoder", "ARCtrl_Person__Person_fromJsonString_Static_Z721C83C5", "ARCtrl_Person__Person_toJsonString_Static_71136F3F", "ARCtrl_Person__Person_fromROCrateJsonString_Static_Z721C83C5", "ARCtrl_Person__Person_toROCrateJsonString_Static_71136F3F", "ARCtrl_Person__Person_toISAJsonString_Static_71136F3F", "ARCtrl_Person__Person_fromISAJsonString_Static_Z721C83C5"]

