"""-----------------------------------------------------------------------------
Parse Env:
    Parse an environment variable depending on certain constraints:

    name                REQUIRED (for debugging)
    value               DEPENDS
    default             OPTIONAL
    data_type           "bool" | "string" | "int" | "float" + case vairations
    required            OPTIONAL
    empty_str_valid     OPTIONAL

Note:
    The last parameter only matters for "string" type variables but allows
    REQUIRED variables to be valid if they are an empty string (versus) None.
-----------------------------------------------------------------------------"""
def PARSE_ENV(  name=None,      value=None,
                default=None,   data_type="string",
                required=False, empty_str_valid=False):
    #---------------------------------------
    # Check if REQUIRED.
    #---------------------------------------
    # Check if required.
    if name is None:
        raise Exception("Missing variable name attempting to parse.")
    if value is None:
        if required == True:
            if default is None:
                raise Exception("Missing required environment variable '%s'" %
                        name)
            return default
        return None
    #---------------------------------------
    # Check data-type..
    #---------------------------------------
    if data_type is None:
        raise Exception("Parser data-type must not be none when parsing env var.")
    data_type = data_type.lower()
    #---------------------------------------
    # Check for STRING.
    #---------------------------------------
    if data_type in ("string", "str"):
        if value == "":
            if empty_str_valid == True:
                return ""
            raise Exception(
                    "Invalid string environment variable '%s' must not be an empty string" % name)
        return value
    #---------------------------------------
    # Check for BOOL.
    #---------------------------------------
    if data_type in ("bool", "boolean"):
        return parse_bool(name, value, required)
    #---------------------------------------
    # Check for INT.
    #---------------------------------------
    if data_type in ("int", "integer"):
        return parse_int(name, value, required)
    #---------------------------------------
    # Check for FLOAT.
    #---------------------------------------
    if data_type in ("float", "decimal"):
        return parse_int(name, value, required)

"""-----------------------------------------------------------------------------
# Parse boolean values (1, true, True, yes, etc...)
-----------------------------------------------------------------------------"""
def parse_bool(name, value, required):
    if value.lower() in ("1", "true", "t", "yes", "y"):
        return True
    if value.lower() in ("0", "false", "f", "no", "n"):
        return False
    if required == True:
        raise Exception("Invalid required boolean environment variable '%s' must be set." % name)

"""-----------------------------------------------------------------------------
Parse int values (cannot be floats)
-----------------------------------------------------------------------------"""
def parse_int(name, value, required):
    try:
        return int(value)
    except Exception as ex:
        if required == True:
            raise Exception("Invalid required integer environment variable '%s' must be set." % name)
        raise Warning("Invalid integer data-type for non-required environment variable '%s'. This variable will be unset" % name)
        return None

"""-----------------------------------------------------------------------------
Parse int values (CAN be integers)
-----------------------------------------------------------------------------"""
def parse_float(name, value, required):
    try:
        return float(value)
    except Exception as ex:
        if required == True:
            raise Exception("Invalid required float environment variable '%s' must be set." % name)
        raise Warning("Invalid float data-type for non-required environment variable '%s'. This variable will be unset" % name)
        return None

#-------------------------------------------------------------------------------
# Unit tests. Feel free to add your own.
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    # Test some cases with ([name], [value], [default], [data_type], [required], [error], [empty_str_valid])
    def run_test(test):
        name = test[0]
        value = test[1]
        default = test[2]
        data_type = test[3]
        required = test[4]
        empty_str_valid = test[5]
        error = test[6]
        # Pass the default paramaters if the test param is None (except for "name" and "value".
        if data_type is None:
            data_type = "string"
        if required is None:
            required = False
        if empty_str_valid is None:
            empty_str_valid = True
        try:
            parsed = PARSE_ENV(name, value, default, data_type, required, empty_str_valid)
            if error == True:
                print("FAILED_ERROR:\n\t%s => %s" % (name, parsed))
                return
            print("PASSED:\n\t%s => %s" % (name, parsed))
        except Exception as ex:
            if error == False:
                print("FAILED:\n\t%s => %s" % (name, str(ex)))
                return
            print("PASSED_ERROR:\n\t%s" % name)
    # Define some tests.
    tests = [
        ["STRING_A", "foo", "req_defult_foo", "String", True, None, False],
        ["STRING_B", "foo", "opt_default_foo", "String", False , None, False],
        ["STRING_C", None, "default_string", "str", True, None, True],
        ["STRING_D", None, "default_string", "str", False, None, False],
        ["STRING_E", "", None, "string", True, None, False],
        ["STRING_F", "", None, "string", True, False, True],
        [None, "foo", "error", "String", False , None, True],
        ["BOOL_A", "Yes", None, "bool", True, None, False],
        ["BOOL_B", "no", None, "bool", True, None, False],
        ["BOOL_C", "false", None, "bool", False, None, False],
        ["BOOL_D", None, None, "boolean", True, None, True],
        ["BOOL_E", "", None, "bool", True, None, True],
        ["BOOL_F", "wat", None, "bool", True, None, True],
        ["INT_A", None, None, "INTEGER", True, None, True],
        ["INT_B", None, None, "INTEGER", False, None, False],
        ["INT_C", "123", None, "INTEGER", False, None, False],
        ["INT_D", "ABC", None, "INTEGER", True, None, True],
        ["INT_D", "123.123", None, "INTEGER", True, None, True],
        ["FLOAT_A", "123", None, "float", True, None, False],
        ["FLOAT_B", "", 123.1, "float", True, None, True],
    ] 
    # Run the tests.
    for test in tests:
        run_test(test)
