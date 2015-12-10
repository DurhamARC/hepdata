from ordereddict import OrderedDict

__author__ = 'eamonnmaguire'


def process_independent_variables(table_contents, x_axes,
                                  independent_variable_headers):
    if table_contents["independent_variables"]:
        for x_axis in table_contents["independent_variables"]:

            if x_axis["values"]:
                units = x_axis['header']['units'] if 'units' in x_axis[
                    'header'] else ''
                x_header = x_axis['header']['name']
                if units is not '':
                    x_header += ' [' + units + "]"
                x_axes[x_header] = []

                # if x_header not in x_headers:
                independent_variable_headers.append(
                    {"name": x_header, "colspan": 1})
                for value in x_axis["values"]:
                    x_axes[x_header].append(value)


def process_dependent_variables(group_count, record, table_contents,
                                tmp_values, independent_variables,
                                dependent_variable_headers):
    for y_axis in table_contents["dependent_variables"]:

        qualifiers = {}
        if "qualifiers" in y_axis:
            for qualifier in y_axis["qualifiers"]:
                # colspan = len(y_axis["qualifiers"][qualifier])
                qualifier_name = qualifier["name"]

                if qualifier_name not in qualifiers:
                    qualifiers[qualifier_name] = 0
                else:
                    qualifiers[qualifier_name] += 1
                    count = qualifiers[qualifier_name]
                    qualifier_name = "{0}-{1}".format(qualifier_name, count)

                if qualifier_name not in record["qualifiers"].keys():
                    record["qualifier_order"].append(qualifier_name)
                    record["qualifiers"][qualifier_name] = []

                record["qualifiers"][qualifier_name].append(
                    {"type": qualifier["name"],
                     "value": str(qualifier["value"]) + (
                     ' ' + qualifier['units'] if 'units' in qualifier else ''),
                     "colspan": 1, "group": group_count})

            # attempt column merge
            for qualifier in record["qualifiers"]:
                values = record["qualifiers"][qualifier]
                merged_values = []
                last_value = None
                for counter, value in enumerate(values):
                    if not last_value:
                        last_value = value
                    else:
                        if last_value["type"] == value["type"] \
                                and last_value["value"] == value["value"]:

                            last_value["colspan"] += 1
                        else:
                            merged_values.append(last_value)
                            last_value = value

                    if counter == len(values) - 1:
                        merged_values.append(last_value)

                record["qualifiers"][qualifier] = merged_values

        units = y_axis['header']['units'] if 'units' in y_axis[
            'header'] else ''
        y_header = y_axis['header']['name']
        if units is not '':
            y_header += ' [' + units + ']'
        dependent_variable_headers.append({"name": y_header, "colspan": 1})

        count = 0
        for value in y_axis["values"]:

            if count not in tmp_values.keys():
                x = []
                for x_header in independent_variables:
                    x.append(independent_variables[x_header][count])
                tmp_values[count] = {"x": x, "y": []}

            y_record = value
            y_record["group"] = group_count

            if "errors" not in y_record:
                y_record["errors"] = [{"symerror": 0, "hide": True}]
            else:
                # process the labels to ensure uniqueness
                observed_error_labels = {}
                for error in y_record["errors"]:
                    error_label = error.get("label")

                    if error_label not in observed_error_labels:
                        observed_error_labels[error_label] = 0
                    observed_error_labels[error_label] += 1

                    if observed_error_labels[error_label] > 1:
                        error["label"] = error_label + "_" + str(
                            observed_error_labels[error_label])

            tmp_values[count]["y"].append(y_record)
            count += 1

        group_count += 1


def generate_table_structure(table_contents):
    """
    Creates a renderable structure from the table structure we've defined.
    :param table_contents:
    :return: a dictionary encompassing the qualifiers, headers and values
    """

    record = {"name": table_contents["name"],
              "description": table_contents["title"], "qualifiers": {},
              "qualifier_order": [], "headers": [],
              "review": table_contents["review"],
              "associated_files": table_contents["associated_files"],
              "keywords": {},
              "values": []}

    # add in keywords
    for keyword in table_contents['keywords']:
        if keyword.name not in record['keywords']:
            record['keywords'][keyword.name] = []

        if keyword.value not in record['keywords'][keyword.name]:
            record['keywords'][keyword.name].append(keyword.value)

    tmp_values = {}
    x_axes = OrderedDict()
    x_headers = []
    process_independent_variables(table_contents, x_axes, x_headers)
    record["x_count"] = len(x_headers)
    record["headers"] += x_headers

    group_count = 0
    yheaders = []

    process_dependent_variables(group_count, record, table_contents,
                                tmp_values, x_axes, yheaders)

    # attempt column merge
    last_yheader = None
    for counter, yheader in enumerate(yheaders):
        if not last_yheader:
            last_yheader = yheader
        else:
            if last_yheader["name"] == yheader["name"]:
                last_yheader["colspan"] += 1
            else:
                record["headers"].append(last_yheader)
                last_yheader = yheader
        if counter == len(yheaders) - 1:
            record["headers"].append(last_yheader)

    for tmp_value in tmp_values:
        record["values"].append(tmp_values[tmp_value])

    return record