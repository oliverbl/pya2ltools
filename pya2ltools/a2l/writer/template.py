from ..reader.reader import axis_pts, characteristic, typedef_characteristic


TAB = "\t"

a2l_file = """\
ASAP2_VERSION {asap2_version_major} {asap2_version_minor}
{project}
"""

project = """\
/begin PROJECT {name} "{description}"

{header}

{modules}\
/end PROJECT\
"""

header = """\
/begin HEADER "{description}"
\tVERSION "{version}"
\tPROJECT_NO {project_number}
/end HEADER\
"""

module = """\
    /begin MODULE {name} "{description}"
    
{elements}
    /end MODULE
"""


mod_common = """\
    /begin MOD_COMMON "{description}"
      DEPOSIT {deposit}
      BYTE_ORDER {byte_order}
      ALIGNMENT_BYTE {alignment_byte}
      ALIGNMENT_WORD {alignment_word}
      ALIGNMENT_LONG {alignment_long}
      ALIGNMENT_FLOAT32_IEEE {alignment_float32_ieee}
      ALIGNMENT_FLOAT64_IEEE {alignment_float64_ieee}
    /end MOD_COMMON
"""

compu_method_identical = """\
    /begin COMPU_METHOD {name}
        "{description}"
        IDENTICAL "{format}" "{unit}"
    /end COMPU_METHOD
"""
compu_method_linear = """\
    /begin COMPU_METHOD {name}
        "{description}"
        LINEAR "{format}" "{unit}"
        COEFFS_LINEAR {coeffs}{status_string_ref}
    /end COMPU_METHOD
"""
compu_method_formula = """\
    /begin COMPU_METHOD {name}
        "{description}"
        FORM
        "{format}"
        "{unit}"
        /begin FORMULA
            "{formula}"{formula_inv}
        /end FORMULA
    /end COMPU_METHOD
"""
compu_method_rational = """\
    /begin COMPU_METHOD {name}
        "{description}"
        RAT_FUNC "{format}" "{unit}"
        COEFFS {coeffs}{status_string_ref}
    /end COMPU_METHOD
"""
compu_method_table_interpolation = """\
    /begin COMPU_METHOD {name}
      "{description}" 
      TAB_INTP "{format}" "{unit}"
      COMPU_TAB_REF {compu_tab_ref}
    /end COMPU_METHOD     
"""
compu_method_table_no_interpolation = """\
    /begin COMPU_METHOD {name}
      "{description}" 
      TAB_NOINTP "{format}" "{unit}"
      COMPU_TAB_REF {compu_tab_ref}
    /end COMPU_METHOD     
"""

compu_tab = """\
    /begin COMPU_TAB {name}
        "{description}"
        {table_type}
        {number_of_pairs}
        {pairs}{default_value}
    /end COMPU_TAB
"""
compu_method_verbal_table = """\
    /begin COMPU_METHOD {name}
        "{description}"
        TAB_VERB
        "{format}"
        "{unit}"
        COMPU_TAB_REF {compu_tab_ref}
    /end COMPU_METHOD
"""
compu_vtab = """\
    /begin COMPU_VTAB {name}
        "{description}"
        TAB_VERB {number_of_pairs}
        {pairs}{default_value}
    /end COMPU_VTAB
"""
compu_vtab_range = """\
    /begin COMPU_VTAB_RANGE {name}
        "{description}"
        {number_of_pairs}
        {pairs}{default_value}
    /end COMPU_VTAB_RANGE
"""
measurement = """\
    /begin MEASUREMENT {name}
        "{description}"
        {datatype} {compu_method} {offset_1} {offset_2} {min} {max}
        ECU_ADDRESS {ecu_address}\
{optional_args}
    /end MEASUREMENT
"""
virtual = """\
        /begin VIRTUAL
            {elements}
        /end VIRTUAL\
"""

mod_par = """\
    /begin MOD_PAR "{description}"
        NO_OF_INTERFACES {number_of_interfaces}
{memory_segments}{system_constants}

    /end MOD_PAR
"""
memory_segment = """\
        /begin MEMORY_SEGMENT {name}
            "{description}"
            {program_type} {memory_type} {location} {address} {size} {offsets}{if_data}
        /end MEMORY_SEGMENT
"""

record_layout = """\
    /begin RECORD_LAYOUT {name}{fields}
    /end RECORD_LAYOUT
"""

characteristic = """\
    /begin CHARACTERISTIC {name}
        "{description}"
        {type}
        {ecu_address}
        {record_layout}
        {max_diff}
        {conversion}
        {min} {max}{optional_args}
    /end CHARACTERISTIC
"""
axis_description = """\
        /begin AXIS_DESCR
            {type} 
            {measurement}
            {compu_method}
            {size}
            {min} {max} {optional_args}
        /end AXIS_DESCR\
"""
fix_axis_par_list = """
            /begin FIX_AXIS_PAR_LIST
                {values}
            /end FIX_AXIS_PAR_LIST\
"""
annotation = """
      /begin ANNOTATION
        ANNOTATION_LABEL "{label}"
        ANNOTATION_ORIGIN "{origin}"
        /begin ANNOTATION_TEXT
          "{text}"
        /end ANNOTATION_TEXT
      /end ANNOTATION\
"""

axis_pts = """\
    /begin AXIS_PTS {name}
        "{description}"
        {ecu_address}
        {measurement}
        {record_layout}
        {offset}
        {compu_method}
        {max_number_sample_points}
        {min} {max}{optional_args}
    /end AXIS_PTS
"""
dependent_or_virtual_characteristic = """
        /begin {type}
            "{formula}"
            {values}
        /end {type}\
"""

function = """
    /begin FUNCTION {name} "{description}"\
    {members}
    /end FUNCTION\
"""
function_member = """
        /begin {name}
            {values}
        /end {name}\
"""
group = """
    /begin GROUP {name} "{description}"\
    {members}
    /end GROUP\
"""

typedef_characteristic = """\
    /begin TYPEDEF_CHARACTERISTIC {name}
        "{description}"
        {type}
        {record_layout}
        {max_diff}
        {conversion}
        {min} {max}{optional_args}
    /end TYPEDEF_CHARACTERISTIC
"""

instance = """
    /begin INSTANCE {name}
        "{description}"
        {reference}
        {ecu_address}{optional_args}
    /end INSTANCE\
"""
typedef_axis = """
    /begin TYPEDEF_AXIS {name}
        "{description}"
        {measurement}
        {record_layout}
        {max_diff}
        {compu_method}
        {max_number_of_axis_points}
        {lower_limit}
        {upper_limit}
    /end TYPEDEF_AXIS\
"""

typefef_structure = """
    /begin TYPEDEF_STRUCTURE {name}
        "{description}"
        {total_size}{components}
    /end TYPEDEF_STRUCTURE\
"""
structure_component = """
        /begin STRUCTURE_COMPONENT
            {name} {type}
            {offset}
        /end STRUCTURE_COMPONENT\
"""

transformer = """
    /begin TRANSFORMER {name}
        "{version}"
        "{dll_32bit}"
        "{dll_64bit}"
        {timeout}
        {event}
        {reverse}{input}{output}
    /end TRANSFORMER\
"""

blob = """
    /begin BLOB {name}
        "{description}"
        {ecu_address}
        {size}
        CALIBRATION_ACCESS {calibration_access}
    /end BLOB
"""
