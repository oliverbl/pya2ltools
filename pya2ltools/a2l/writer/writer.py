from ast import Tuple
from pathlib import Path
from typing import Any

from ..reader.reader import measurement, record_layout

from ..reader.util import format_hex

from ..model.mod_par_model import A2LIfData, A2LMemorySegment, A2LModPar

from ..model.model import (
    A2LBlob,
    A2LCompuTab,
    A2LCompuVTab,
    A2LCompuVTabRange,
    A2LInstance,
    A2LModCommon,
    A2LRecordLayout,
    A2LRecordLayoutAxisPts,
    A2LRecordLayoutNoAxisPts,
    A2LStructure,
    A2LStructureComponent,
    A2LTransformer,
    A2lFncValues,
    A2lLRescaleAxis,
)

from ..model.compu_methods import (
    A2LCompuMethod,
    A2LCompuMethodFormula,
    A2LCompuMethodLinear,
    A2LCompuMethodRational,
    A2LCompuMethodTableInterpolation,
    A2LCompuMethodTableNoInterpolation,
    A2LCompuMethodVerbalTable,
)

from ..model.characteristic_model import (
    A2LAxisDescription,
    A2LAxisDescriptionComAxis,
    A2LAxisDescriptionCurveAxis,
    A2LAxisDescriptionFixAxis,
    A2LAxisDescriptionResAxis,
    A2LAxisPts,
    A2LCharacteristic,
    A2LCharacteristicArray,
    A2LCharacteristicAscii,
    A2LCharacteristicCube4,
    A2LCharacteristicCuboid,
    A2LCharacteristicCurve,
    A2LCharacteristicMap,
    A2LCharacteristicTypedef,
    A2LCharacteristicValue,
    A2LMeasurement,
    A2LTypedefAxis,
)

from ..model.project_model import (
    A2ML,
    A2LFunction,
    A2LGroup,
    A2LHeader,
    A2LModule,
    A2LProject,
    A2lFile,
)
from . import template


def write_a2ml(a2ml: A2ML) -> str:
    return "/begin " + a2ml.content + "/end A2ML"


def write_mod_common(mod_common: A2LModCommon) -> str:
    return template.mod_common.format(
        description=mod_common.description,
        deposit=mod_common.deposit,
        byte_order=mod_common.byte_order.name,
        alignment_byte=mod_common.alignment_byte,
        alignment_word=mod_common.alignment_word,
        alignment_long=mod_common.alignment_long,
        alignment_float32_ieee=mod_common.alignment_float32_ieee,
        alignment_float64_ieee=mod_common.alignment_float64_ieee,
    )


def write_compu_method_identical(compu_method: A2LCompuMethod) -> str:
    return template.compu_method_identical.format(
        name=compu_method.name,
        description=compu_method.description,
        unit=compu_method.unit,
        format=compu_method.format,
    )


def write_compu_method_linear(compu_method: A2LCompuMethodLinear) -> str:
    status_string_ref = ""
    if compu_method.status_string_ref is not None:
        status_string_ref = (
            "\n\t\t\tSTATUS_STRING_REF " + compu_method.status_string_ref
        )

    return template.compu_method_linear.format(
        name=compu_method.name,
        description=compu_method.description,
        unit=compu_method.unit,
        format=compu_method.format,
        coeffs=" ".join([str(coeff) for coeff in compu_method.coeffs]),
        status_string_ref=status_string_ref,
    )


def write_compu_method_formula(compu_method: A2LCompuMethodFormula) -> str:
    formula_inv = ""
    if compu_method.formula_inv is not None:
        formula_inv = f'\n\t\t\t\t\t\tFORMULA_INV "{compu_method.formula_inv}"'

    return template.compu_method_formula.format(
        name=compu_method.name,
        description=compu_method.description,
        unit=compu_method.unit,
        format=compu_method.format,
        formula=compu_method.formula,
        formula_inv=formula_inv,
    )


def write_compu_method_rational(compu_method: A2LCompuMethodRational) -> str:
    status_string_ref = ""
    if compu_method.status_string_ref is not None:
        status_string_ref = (
            "\n\t\t\tSTATUS_STRING_REF " + compu_method.status_string_ref
        )
    return template.compu_method_rational.format(
        name=compu_method.name,
        description=compu_method.description,
        unit=compu_method.unit,
        format=compu_method.format,
        coeffs=" ".join([str(coeff) for coeff in compu_method.coeffs]),
        status_string_ref=status_string_ref,
    )


def write_compu_method_table_interpolation(
    compu_method: A2LCompuMethodTableInterpolation,
) -> str:
    return template.compu_method_table_interpolation.format(
        name=compu_method.name,
        description=compu_method.description,
        unit=compu_method.unit,
        format=compu_method.format,
        compu_tab_ref=compu_method.compu_tab_ref.name,
    )


def write_compu_method_table_no_interpolation(
    compu_method: A2LCompuMethodTableNoInterpolation,
) -> str:
    return template.compu_method_table_no_interpolation.format(
        name=compu_method.name,
        description=compu_method.description,
        unit=compu_method.unit,
        format=compu_method.format,
        compu_tab_ref=compu_method.compu_tab_ref.name,
    )


def write_compu_tab(compu_tab: A2LCompuTab) -> str:
    default_value = ""
    if compu_tab.default_value is not None:
        default_value = "\n\t\t\tDEFAULT_VALUE_NUMERIC " + str(compu_tab.default_value)

    return template.compu_tab.format(
        name=compu_tab.name,
        description=compu_tab.description,
        table_type=compu_tab.table_type,
        number_of_pairs=len(compu_tab.values),
        pairs="\n\t\t\t\t".join([f"{k} {v}" for k, v in compu_tab.values.items()]),
        default_value=default_value,
    )


def write_compu_method_verbal_table(compu_method: A2LCompuMethodVerbalTable) -> str:
    return template.compu_method_verbal_table.format(
        name=compu_method.name,
        description=compu_method.description,
        unit=compu_method.unit,
        format=compu_method.format,
        compu_tab_ref=compu_method.compu_tab_ref.name,
    )


def write_compu_vtab(compu_vtab: A2LCompuVTab) -> str:
    default_value = ""
    if compu_vtab.default_value is not None:
        default_value = '\n\t\t\t\tDEFAULT_VALUE "' + compu_vtab.default_value + '"'

    return template.compu_vtab.format(
        name=compu_vtab.name,
        description=compu_vtab.description,
        number_of_pairs=len(compu_vtab.values),
        pairs="\n\t\t\t\t".join([f'{k} "{v}"' for k, v in compu_vtab.values.items()]),
        default_value=default_value,
    )


def write_compu_vtab_range(compu_vtab_range: A2LCompuVTabRange) -> str:
    default_value = ""
    if compu_vtab_range.default_value is not None:
        default_value = (
            '\n\t\t\t\tDEFAULT_VALUE "' + compu_vtab_range.default_value + '"'
        )

    return template.compu_vtab_range.format(
        name=compu_vtab_range.name,
        description=compu_vtab_range.description,
        number_of_pairs=len(compu_vtab_range.values),
        pairs="\n\t\t\t\t".join(
            [f'{k[0]} {k[1]} "{v}"' for k, v in compu_vtab_range.values.items()]
        ),
        default_value=default_value,
    )


def write_if_data(if_data: A2LIfData) -> str:
    return "/begin IF_DATA " + if_data.name + "".join(if_data.content) + "/end IF_DATA"


def write_measurement(measurement: A2LMeasurement) -> str:
    optional_args = ""
    if measurement.format is not None:
        optional_args += f'\n\t\t\t\tFORMAT "{measurement.format}"'
    if measurement.display_identifier is not None:
        optional_args += (
            "\n\t\t\t\tDISPLAY_IDENTIFIER " + measurement.display_identifier
        )
    if measurement.discrete:
        optional_args += "\n\t\t\t\tDISCRETE"
    if measurement.bitmask is not None:
        optional_args += "\n\t\t\t\tBIT_MASK " + format_hex(measurement.bitmask)
    if measurement.matrix_dim is not None:
        optional_args += "\n\t\t\t\tMATRIX_DIM " + " ".join(
            [str(m) for m in measurement.matrix_dim]
        )
    for if_data in measurement.if_data:
        optional_args += "\n\t\t\t\t" + write_if_data(if_data)
    # if measurement.annotations:
    if measurement.virtual is not None:
        optional_args += "\n" + template.virtual.format(
            elements="\t\t\t\\n".join(measurement.virtual.variables)
        )

    if measurement.symbol_link is not None:
        optional_args += f'\n\t\t\t\tSYMBOL_LINK "{measurement.symbol_link.symbol_name}" {measurement.symbol_link.offset}'

    return template.measurement.format(
        name=measurement.name,
        description=measurement.description,
        datatype=measurement.datatype,
        compu_method=measurement.compu_method.name,
        offset_1=measurement.offset_1,
        offset_2=measurement.offset_2,
        min=str(measurement.min),
        max=str(measurement.max),
        ecu_address=format_hex(measurement.ecu_address),
        optional_args=optional_args,
    )


def write_mod_par(mod_par: A2LModPar):
    def write_segment(segment: A2LMemorySegment):
        if_data = ""
        if segment.if_data:
            if_data = "\n\t\t\t\t" + "\n\t\t\t\t".join(
                [write_if_data(i) for i in segment.if_data]
            )

        return template.memory_segment.format(
            name=segment.name,
            description=segment.description,
            program_type=segment.program_type,
            memory_type=segment.memory_type,
            location=segment.location,
            address=format_hex(segment.address),
            size=format_hex(segment.size),
            offsets=" ".join([str(i) for i in segment.offsets]),
            if_data=if_data,
        )

    def write_system_constant(name, val):
        return f'SYSTEM_CONSTANT "{name}" "{val}"'

    segments = "\n\t\t\t".join(
        [write_segment(segment) for segment in mod_par.memory_segments]
    )
    system_constants = ""
    if mod_par.system_constants:
        system_constants = "\n\t\t\t" + "\n\t\t\t".join(
            [write_system_constant(k, v) for k, v in mod_par.system_constants.items()]
        )
    return template.mod_par.format(
        description=mod_par.description,
        number_of_interfaces=mod_par.number_of_interfaces,
        memory_segments=segments,
        system_constants=system_constants,
    )


def write_record_layout(record_layout: A2LRecordLayout) -> str:
    writers = {
        A2LRecordLayoutAxisPts: lambda x: f"{x.axis} {x.position} {x.datatype} {x.index_mode} {x.addressing_mode}",
        A2LRecordLayoutNoAxisPts: lambda x: f"{x.axis} {x.position} {x.datatype}",
        A2lLRescaleAxis: lambda x: f"{x.axis} {x.position} {x.datatype} {x.map_position} {x.index_mode} {x.addressing_mode}",
        A2lFncValues: lambda x: f"FNC_VALUES {x.position} {x.datatype} {x.index_mode} {x.addressing_mode}",
    }

    fields = ""
    for field in record_layout.fields:
        fields += "\n\t\t\t\t" + writers[type(field)](field)
    return template.record_layout.format(name=record_layout.name, fields=fields)


def write_axis_desc(axis_desc: A2LAxisDescription):
    types = {
        A2LAxisDescription: "STD_AXIS",
        A2LAxisDescriptionComAxis: "COM_AXIS",
        A2LAxisDescriptionCurveAxis: "CURVE_AXIS",
        A2LAxisDescriptionFixAxis: "FIX_AXIS",
        A2LAxisDescriptionResAxis: "RES_AXIS",
    }

    optional_args = ""

    if isinstance(axis_desc, A2LAxisDescriptionFixAxis):
        if axis_desc.par_dist:
            optional_args += f"\n\t\t\t\tFIX_AXIS_PAR_DIST {' '.join([str(s) for s in axis_desc.par_dist])}"
        if axis_desc.par_list:
            optional_args += template.fix_axis_par_list.format(
                values=" ".join([str(s) for s in axis_desc.par_list])
            )
    if isinstance(axis_desc, A2LAxisDescriptionComAxis):
        optional_args += f"\n\t\t\t\t\tAXIS_PTS_REF {axis_desc.axis_pts_ref.name}"

    if isinstance(axis_desc, A2LAxisDescriptionCurveAxis):
        optional_args += f"\n\t\t\t\t\tCURVE_AXIS_REF {axis_desc.curve_axis_ref.name}"

    if axis_desc.monotony is not None:
        optional_args += f"\n\t\t\t\t\t\tMONOTONY {axis_desc.monotony}"

    return template.axis_description.format(
        type=types[type(axis_desc)],
        measurement=axis_desc.measurement.name
        if axis_desc.measurement is not None
        else "NO_INPUT_QUANTITY",
        compu_method=axis_desc.compu_method.name
        if axis_desc.compu_method is not None
        else "NO_COMPU_METHOD",
        size=axis_desc.size,
        min=axis_desc.min,
        max=axis_desc.max,
        optional_args=optional_args,
    )


def get_chararacteristic_typedef_args(typedef: A2LCharacteristicTypedef) -> dict:
    types = {
        A2LCharacteristicValue: "VALUE",
        A2LCharacteristicArray: "VAL_BLK",
        A2LCharacteristicAscii: "ASCII",
        A2LCharacteristicCurve: "CURVE",
        A2LCharacteristicMap: "MAP",
        A2LCharacteristicCuboid: "CUBOID",
        A2LCharacteristicCube4: "CUBE_4",
    }

    args = {}
    optional_args = ""
    if typedef.extended_max is not None:
        optional_args += (
            f"\n\t\t\t\tEXTENDED_LIMITS {typedef.extended_min} {typedef.extended_max}"
        )
    if isinstance(typedef, A2LCharacteristicArray):
        optional_args += (
            f"\n\t\t\t\tMATRIX_DIM {' '.join([str(s) for s in typedef.matrix_dim])}"
        )
    if isinstance(typedef, A2LCharacteristicAscii):
        optional_args += f"\n\t\t\t\tNUMBER {typedef.size}"
    if (
        isinstance(typedef, A2LCharacteristicCurve)
        or isinstance(typedef, A2LCharacteristicCube4)
        or isinstance(typedef, A2LCharacteristicCuboid)
    ):
        for axis in typedef.axis_descriptions:
            optional_args += "\n" + write_axis_desc(axis)
    if typedef.bitmask is not None:
        optional_args += f"\n\t\t\t\tBIT_MASK {format_hex(typedef.bitmask)}"
    if typedef.phys_unit is not None:
        optional_args += f"\n\t\t\t\tPHYS_UNIT {typedef.phys_unit}"
    if typedef.format is not None:
        optional_args += f"\n\t\t\t\tFORMAT {typedef.format}"
    if typedef.discrete:
        optional_args += f"\n\t\t\t\tDISCRETE"

    args["type"] = types[type(typedef)]
    args["optional_args"] = optional_args
    args["record_layout"] = typedef.record_layout.name
    args["max_diff"] = typedef.maxdiff
    args["conversion"] = (
        typedef.compu_method.name
        if typedef.compu_method is not None
        else "NO_COMPU_METHOD"
    )
    args["min"] = typedef.min
    args["max"] = typedef.max
    return args


def write_characteristic(characteristic: A2LCharacteristic):
    args = get_chararacteristic_typedef_args(characteristic.typedef)

    if characteristic.display_identifier is not None:
        args[
            "optional_args"
        ] += f"\n\t\t\t\tDISPLAY_IDENTIFIER {characteristic.display_identifier}"

    if characteristic.model_link is not None:
        args["optional_args"] += f"\n\t\t\t\tMODEL_LINK {characteristic.model_link}"

    if characteristic.annotations:
        for a in characteristic.annotations:
            args["optional_args"] += template.annotation.format(
                label=a.label, text=a.text, origin=a.origin
            )
    if characteristic.dependent_characteristic is not None:
        args["optional_args"] += template.dependent_or_virtual_characteristic.format(
            type="DEPENDENT_CHARACTERISTIC",
            formula=characteristic.dependent_characteristic.formula,
            values="\n\t\t\t\t".join(
                [v.name for v in characteristic.dependent_characteristic.variables]
            ),
        )
    if characteristic.virtual_characteristic is not None:
        args["optional_args"] += template.dependent_or_virtual_characteristic.format(
            type="VIRTUAL_CHARACTERISTIC",
            formula=characteristic.virtual_characteristic.formula,
            values="\n\t\t\t\t".join(
                [v.name for v in characteristic.virtual_characteristic.variables]
            ),
        )

    if characteristic.symbol_link is not None:
        args[
            "optional_args"
        ] += f'\n\t\t\t\tSYMBOL_LINK "{characteristic.symbol_link.symbol_name}" {characteristic.symbol_link.offset}'

    return template.characteristic.format(
        name=characteristic.name,
        description=characteristic.description,
        ecu_address=format_hex(characteristic.ecu_address),
        **args,
    )


def write_characteristic_typedef(typedef_characteristic: A2LCharacteristicTypedef):
    args = get_chararacteristic_typedef_args(typedef_characteristic.typedef)
    return template.typedef_characteristic.format(
        name=typedef_characteristic.name,
        description=typedef_characteristic.description,
        **args,
    )


def write_axis_pts(axis: A2LAxisPts):
    optional_args = ""
    if axis.display_identifier is not None:
        optional_args += f"\n\t\t\t\tDISPLAY_IDENTIFIER {axis.display_identifier}"

    if axis.symbol_link is not None:
        optional_args += f'\n\t\t\t\tSYMBOL_LINK "{axis.symbol_link.symbol_name}" {axis.symbol_link.offset}'

    return template.axis_pts.format(
        name=axis.name,
        description=axis.description,
        ecu_address=format_hex(axis.ecu_address),
        record_layout=axis.record_layout.name,
        measurement=axis.measurement.name,
        offset=axis.offset,
        compu_method=axis.compu_method.name if axis.compu_method else "NO_COMPU_METHOD",
        max=axis.max,
        min=axis.min,
        max_number_sample_points=axis.max_number_sample_points,
        optional_args=optional_args,
    )


def write_function(function: A2LFunction):
    members = ""

    if function.sub_functions:
        members += template.function_member.format(
            name="SUB_FUNCTION",
            values="\n\t\t\t\t".join([v.name for v in function.sub_functions]),
        )

    if function.ref_characteristics:
        members += template.function_member.format(
            name="REF_CHARACTERISTIC",
            values="\n\t\t\t\t".join([v.name for v in function.ref_characteristics]),
        )
    if function.def_characteristics:
        members += template.function_member.format(
            name="DEF_CHARACTERISTIC",
            values="\n\t\t\t\t".join([v.name for v in function.def_characteristics]),
        )
    if function.in_measurements:
        members += template.function_member.format(
            name="IN_MEASUREMENT",
            values="\n\t\t\t\t".join([v.name for v in function.in_measurements]),
        )
    if function.out_measurements:
        members += template.function_member.format(
            name="OUT_MEASUREMENT",
            values="\n\t\t\t\t".join([v.name for v in function.out_measurements]),
        )
    if function.loc_measurements:
        members += template.function_member.format(
            name="LOC_MEASUREMENT",
            values="\n\t\t\t\t".join([v.name for v in function.loc_measurements]),
        )

    return template.function.format(
        name=function.name,
        description=function.description,
        members=members,
    )


def write_group(group: A2LGroup):
    members = ""

    if group.root:
        members += "\n\t\t\t\tROOT"

    if group.sub_groups:
        members += template.function_member.format(
            name="SUB_GROUP",
            values="\n\t\t\t\t".join([v.name for v in group.sub_groups]),
        )

    if group.function_lists:
        members += template.function_member.format(
            name="FUNCTION_LIST",
            values="\n\t\t\t\t".join([v.name for v in group.function_lists]),
        )
    if group.characteristics:
        members += template.function_member.format(
            name="REF_CHARACTERISTIC",
            values="\n\t\t\t\t".join([v.name for v in group.characteristics]),
        )
    if group.measurements:
        members += template.function_member.format(
            name="REF_MEASUREMENT",
            values="\n\t\t\t\t".join([v.name for v in group.measurements]),
        )
    return template.group.format(
        name=group.name,
        description=group.description,
        members=members,
    )


def write_instance(instance: A2LInstance) -> str:
    optional_args = ""
    if instance.display_identifier is not None:
        optional_args += f"\n\t\t\t\tDISPLAY_IDENTIFIER {instance.display_identifier}"
    if instance.matrix_dim is not None:
        m = " ".join([str(x) for x in instance.matrix_dim])
        optional_args += f"\n\t\t\t\tMATRIX_DIM {m}"
    return template.instance.format(
        name=instance.name,
        description=instance.description,
        reference=instance.reference.name,
        ecu_address=format_hex(instance.ecu_address),
        optional_args=optional_args,
    )


def write_typedef_axis(typedef_axis: A2LTypedefAxis) -> str:
    return template.typedef_axis.format(
        name=typedef_axis.name,
        description=typedef_axis.description,
        measurement=typedef_axis.measurement.name,
        record_layout=typedef_axis.record_layout.name,
        compu_method=typedef_axis.compu_method.name
        if typedef_axis.compu_method
        else "NO_COMPU_METHOD",
        max_diff=typedef_axis.max_diff,
        max_number_of_axis_points=typedef_axis.max_number_of_axis_points,
        lower_limit=typedef_axis.lower_limit,
        upper_limit=typedef_axis.upper_limit,
    )


def write_structure(structure: A2LStructure) -> str:
    def write_component(component: A2LStructureComponent) -> str:
        return template.structure_component.format(
            name=component.name,
            type=component.datatype,
            offset=component.offset,
        )

    components = "\t\t\t".join([write_component(c) for c in structure.components])
    return template.typefef_structure.format(
        name=structure.name,
        description=structure.description,
        total_size=structure.size,
        components=components,
    )


def write_transformer(transformer: A2LTransformer) -> str:
    input = template.function_member.format(
        name="TRANSFORMER_IN_OBJECTS",
        values="\n\t\t\t\t".join([v.name for v in transformer.in_objects]),
    )
    output = template.function_member.format(
        name="TRANSFORMER_OUT_OBJECTS",
        values="\n\t\t\t\t".join([v.name for v in transformer.out_objects]),
    )
    return template.transformer.format(
        name=transformer.name,
        version=transformer.version,
        dll_32bit=transformer.name_32bit_dll,
        dll_64bit=transformer.name_64bit_dll,
        timeout=transformer.timeout_in_ms,
        event=transformer.event,
        reverse=transformer.reverse_transformer.name,
        input=input,
        output=output,
    )


def write_blob(blob: A2LBlob) -> str:
    return template.blob.format(
        name=blob.name,
        description=blob.description,
        ecu_address=format_hex(blob.ecu_address),
        size=blob.number_of_bytes,
        calibration_access=blob.calibration_access,
    )


def write_element(element: Any) -> str:
    writers = {
        A2ML: write_a2ml,
        A2LIfData: lambda x: "\t\t" + write_if_data(x),
        A2LCharacteristic: write_characteristic,
        A2LCharacteristicTypedef: write_characteristic_typedef,
        A2LCompuMethod: write_compu_method_identical,
        A2LCompuMethodLinear: write_compu_method_linear,
        A2LCompuMethodFormula: write_compu_method_formula,
        A2LCompuMethodRational: write_compu_method_rational,
        A2LCompuMethodTableInterpolation: write_compu_method_table_interpolation,
        A2LCompuTab: write_compu_tab,
        A2LCompuMethodTableNoInterpolation: write_compu_method_table_no_interpolation,
        A2LCompuMethodVerbalTable: write_compu_method_verbal_table,
        A2LCompuVTab: write_compu_vtab,
        A2LCompuVTabRange: write_compu_vtab_range,
        A2LMeasurement: write_measurement,
        A2LFunction: write_function,
        A2LGroup: write_group,
        A2LInstance: write_instance,
        A2LModCommon: write_mod_common,
        A2LModPar: write_mod_par,
        A2LRecordLayout: write_record_layout,
        A2LStructure: write_structure,
        A2LTypedefAxis: write_typedef_axis,
        A2LAxisPts: write_axis_pts,
        A2LTransformer: write_transformer,
        A2LBlob: write_blob,
    }

    if not type(element) in writers:
        # raise Exception(f"Element {element} not supported")
        return ""
    return writers[type(element)](element)


def write_module(module: A2LModule) -> str:
    content = "\n".join([write_element(element) for element in module.global_list])
    return template.module.format(
        name=module.name,
        description=module.description,
        elements=content,
    )


def write_header(header: A2LHeader) -> str:
    return template.header.format(
        description=header.description,
        version=header.version,
        project_number=header.project_number,
    )


def write_project(project: A2LProject) -> str:
    content = "".join([write_module(module) for module in project.modules])

    return template.project.format(
        name=project.name,
        description=project.description,
        header=write_header(project.header) if project.header else "",
        modules=content,
    )


def write_a2l_file(file: A2lFile, output_path: Path):
    major, minor = file.asap2_version.split(".")

    content = template.a2l_file.format(
        asap2_version_major=major,
        asap2_version_minor=minor,
        project=write_project(file.project),
    )

    content = content.replace("\t", "  ")

    with output_path.open("w", encoding="utf-8") as f:
        f.write(content)
