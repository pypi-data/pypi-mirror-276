import copy
import json
from typing import TextIO, Dict, Union, Any, List
import os
from queue import Queue

from test2va.generator.core.GUI import GUIEvent, GUIMethod, GUIElement, GUIControl
from test2va.generator.core.Mutant import MutantInfoPerEvent
from test2va.generator.exceptions.MethodGeneratorException import MethodGeneratorException
from test2va.generator.core.Method import Statement, Header

TAB_CONSTANT = "    "
END_OF_STATEMENT_CONSTANT = ";\n"


# def write_header_java(method: GUIMethod, method_file: TextIO):
#
#     method_file.write("public void " + method.get_name() + "(")
#
#     # write the parameter list
#     parameter = method.get_para()
#
#     # Empty parameter evaluate to False, means there is not mutant detected
#     if not parameter:
#         method_file.write("String para) {")
#         return
#
#     # parameter list is not empty
#     class_name = parameter.get('event_element_class')
#
#     if class_name == 'android.widget.EditText':
#         method_file.write("String para) {")
#     else:
#         method_file.write("String para) {")


# def get_test2va_action_statement(event_control: dict, event_element: dict) -> str:
#     """
#     This method will look into the combination of click/input + Text/CD + opt(ResourceId) to find the supporting
#     dsfsd APIs
#     :param event_control:
#     :param event_element:
#     :return: the statement of dsfsd API invocation
#     """
#     method_lookup_id = ""
#     argument_list = []
#
#     # add control id
#     if event_control['name'] == "replaceText":
#         method_lookup_id += "input"
#     elif event_control['name'] == "click":
#         method_lookup_id += "click"
#     else:
#         raise MethodGeneratorException("unsupported control name: " + event_control['name'])
#
#     # add element id
#     not_found_flag = 'Key not found'
#     text = event_element.get('text', not_found_flag)
#     content_desc = event_element.get('content-desc', not_found_flag)
#     resource_id = event_element.get('resource-id', not_found_flag)
#
#     # add text or cd
#     if text is not None and text != not_found_flag:
#         method_lookup_id += '-text'
#         argument_list.append("\"" + event_element['text'] + "\"")
#     elif content_desc is not None and content_desc != not_found_flag:
#         method_lookup_id += '-cd'
#         argument_list.append("\"" + event_element['content-desc'] + "\"")
#
#     # add id
#     if resource_id is not None and resource_id != not_found_flag:
#         method_lookup_id += '-id'
#         argument_list.append("\"" + event_element['resource-id'] + "\"")
#
#     invocation_string = test2va_METHOD_MAP.get(method_lookup_id) + "("
#     arg_index = 0
#     arg_length = len(argument_list)
#     while (arg_index < arg_length):
#         invocation_string += argument_list[arg_index]
#         arg_index += 1
#         # not adding comma(,) for last argument in the list
#         if arg_index != arg_length:
#             invocation_string += ", "
#
#     invocation_string += ")"


# def write_body_java(method: GUIMethod, method_file: TextIO):
#
#     mutant_index = method.get_para()['event_index']
#     event_index = 0
#     for event in method.get_events():
#         # get the feature dictionary of event control and element
#         event_control = event.get_gui_control().get_control_features()
#         event_element = event.get_gui_element().get_all_features()
#         if mutant_index != event_index:
#             method_file.write(TAB_CONSTANT)
#             method_file.write(get_test2va_action_statement(event_control, event_element))
#             method_file.write(END_OF_STATEMENT_CONSTANT)
#         else:
#             pass
#         # write action
#         event_index += 1


def get_output_file_path(input_file_path):
    """
    if input_file_path is task_method_generator/input/package.name_CreateLabel.java_parsed.json
    Then the output_file_path is task_method_generator/output/package.name/CreateLabel.txt
    And the directory path is task_method_generator/output/package.name/

    :param input_file_path: path of java_res.json
    :return:
    """
    # Replace 'java_parsed.json' with '.txt''
    output_file_path = input_file_path.replace('.java_res.json', '.txt')
    # Replace 'input' with 'output'
    output_file_path = output_file_path.replace('input', 'output')

    index = output_file_path.rfind('_')
    output_directory = output_file_path[:index] + '/'
    output_full_path = output_file_path[:index] + '/' + output_file_path[index + 1:]

    return output_directory, output_full_path

#
# def get_mutant_info(mutant_result_file_path) -> dict:
#     """
#     This method reads the mutant_result_report info such as successful path to extract the mutant element and mutant index
#     key features: mutant_indices = []
#                   mutant_elements = {
#                    "index1" : [element 1, element 2] (mutant_element_list),
#                    "index2" : [element 1, element 2, element 3]
#                   }
#     :param mutant_result_file_path:
#     :return: mutant_info
#     """
#     with open(mutant_result_file_path, 'r') as file:
#         # 1. Load the data from the file
#         json_data = json.load(file)
#
#         # 2. collect the mutant index
#         mutant_index_list = []
#         event_num = len(json_data['basic_path'])
#         index = 0
#         while index < event_num:
#             if json_data[str(index)]['mutable']:
#                 mutant_index_list.append(index)
#             index += 1
#
#         # 3. collect the mutant elements for each GUI element from a given index (e.g., "index1")
#         mutant_elements = {}
#         for index in mutant_index_list:
#             # index not exist
#             if str(index) not in json_data:
#                 raise MethodGeneratorException("index not exist in mutant result file: " + str(index))
#             # successful_path is empty
#             if not json_data[str(index)]['successful_paths']:
#                 raise MethodGeneratorException("successful_path with index " + str(index) +
#                                                " is empty, please check detector algorithm.")
#
#             # find successful_paths
#             successful_paths = json_data[str(index)]['successful_paths']
#
#             # put all the detected mutable elements in the mutant_element_list
#             mutant_element_num = len(successful_paths)
#             mutant_count = 0
#             mutant_element_list = []
#             while mutant_count < mutant_element_num:
#                 mutant_element: GUIElement = update_element(successful_paths[mutant_count][index])
#                 mutant_element_list.append(mutant_element)
#                 mutant_count += 1
#
#             # adding the detected mutant list with a label of index
#             # "index1" : [element 1, element 2] (mutant_element_list),
#             mutant_elements[str(index)] = mutant_element_list
#
#     mutant_info = {'mutant_indices': mutant_index_list,
#                    'mutant_elements': mutant_elements}
#
#     return mutant_info
#
#
# def get_parameter_list(mutant_info) -> list:
#     """
#     This method reads the mutant_info to prepare the parameter list.
#     For example, for the first mutant element in mutant_info
#     The parameter list may look like:
#         - String text1 or String text1, String id1
#         - String cd1 or String cd1, String id1
#         - String id1
#
#     It depends on the features of the element.
#     The features priority is text-cd with optional id
#
#     :param mutant_info:
#     :return:
#     """
#
#     mutant_num = len(mutant_info['mutant_indices'])
#
#     pass
#
#
# def generate_static_statements(text, content_desc, resource_id, action: GUIControl):
#     """
#     This method is used to generate the static statement(s) to reproduce the event
#     For example, onEventInputByText(text, resource_id)
#     :param action: GUIControl
#     :param text: feature of GUIELement
#     :param content_desc: feature of GUIELement
#     :param resource_id: feature of GUIELement
#     :return:
#     """
#     statements = ''
#
#     if text is not None and text != "":  # the element has text
#         if resource_id is not None and resource_id != "":  # element has optional resource_id
#             # control is an input
#             if action.get_control_feature('name') == 'replaceText':
#                 statements += (f"{TAB_CONSTANT}onEventInputByText(\"{text}\", \"{resource_id}\", "
#                                f"\"{action.get_control_feature('value')}\")")
#                 statements += END_OF_STATEMENT_CONSTANT
#             # control is a click
#             elif action.get_control_feature('name') == 'click':
#                 statements += f"{TAB_CONSTANT}onEventClickingByText(\"{text}\", \"{resource_id}\")"
#                 statements += END_OF_STATEMENT_CONSTANT
#
#             else:
#                 raise MethodGeneratorException("The action control is not supported: " +
#                                                action.get_control_feature('name'))
#
#         else:  # element has no optional resource_id
#             # control is an input
#             if action.get_control_feature('name') == 'replaceText':
#                 statements += (f"{TAB_CONSTANT}onEventInputByText(\"{text}\", "
#                                f"\"{action.get_control_feature('value')}\")")
#                 statements += END_OF_STATEMENT_CONSTANT
#             # control is a click
#             elif action.get_control_feature('name') == 'click':
#                 statements += f"{TAB_CONSTANT}onEventClickingByText(\"{text}\")"
#                 statements += END_OF_STATEMENT_CONSTANT
#
#             else:
#                 raise MethodGeneratorException("The action control is not supported: " +
#                                                action.get_control_feature('name'))
#
#     elif content_desc is not None and content_desc != "":  # the element has content_desc
#         if resource_id is not None and resource_id != "":  # element has optional resource_id
#             # control is an input
#             if action.get_control_feature('name') == 'replaceText':
#                 statements += (f"{TAB_CONSTANT}onEventInputByCD(\"{content_desc}\", \"{resource_id}\", "
#                                f"\"{action.get_control_feature('value')}\")")
#                 statements += END_OF_STATEMENT_CONSTANT
#             # control is a click
#             elif action.get_control_feature('name') == 'click':
#                 statements += f"{TAB_CONSTANT}onEventClickingByCD(\"{content_desc}\", \"{resource_id}\")"
#                 statements += END_OF_STATEMENT_CONSTANT
#
#             else:
#                 raise MethodGeneratorException("The action control is not supported: " +
#                                                action.get_control_feature('name'))
#         else:  # element has no optional resource_id
#             # control is an input
#             if action.get_control_feature('name') == 'replaceText':
#                 statements += (f"{TAB_CONSTANT}onEventInputByCD(\"{content_desc}\", "
#                                f"\"{action.get_control_feature('value')}\")")
#                 statements += END_OF_STATEMENT_CONSTANT
#             # control is a click
#             elif action.get_control_feature('name') == 'click':
#                 statements += f"{TAB_CONSTANT}onEventClickingByCD(\"{content_desc}\")"
#                 statements += END_OF_STATEMENT_CONSTANT
#
#             else:
#                 raise MethodGeneratorException("The action control is not supported: " +
#                                                action.get_control_feature('name'))
#
#     elif resource_id is not None and resource_id != "":  # the element has resource_id alone
#         # control is an input
#         if action.get_control_feature('name') == 'replaceText':
#             statements += (f"{TAB_CONSTANT}onEventInputByResourceId(\"{resource_id}\", "
#                            f"\"{action.get_control_feature('value')}\")")
#             statements += END_OF_STATEMENT_CONSTANT
#         # control is a click
#         elif action.get_control_feature('name') == 'click':
#             statements += f"{TAB_CONSTANT}onEventClickingByResourceId(\"{resource_id}\")"
#             statements += END_OF_STATEMENT_CONSTANT
#
#         else:
#             raise MethodGeneratorException("The action control is not supported: " +
#                                            action.get_control_feature('name'))
#
#     else:
#         raise MethodGeneratorException("all identifiers (text, content_desc, resource_id) are either none or empty, "
#                                        "cannot locate the element")
#
#     return statements
#
#
# def generate_mutant_statements(text: str, content_desc: str, resource_id: str, action: GUIControl,
#                                mutant_element_list: list, mutant_count: int) -> list:
#     """
#     This method is used to generate the statement to reproduce the event with an alternative choice.
#     For example,
#     if (text1 == "delete")
#         onEventInputByText(text1)
#
#     :param text:
#     :param content_desc:
#     :param resource_id:
#     :param action:
#     :param mutant_info:
#     :param mutant_count:
#     :return:
#     """
#
#     statements = ''  # the final statements that will return
#     para_index = 0  # index of parameter
#     para_list = []
#     mutant_count = len(mutant_element_list)
#
#     # write statement for each mutant element of the target event
#     while para_index < mutant_count:
#         # element is an edittext
#         if action.get_control_feature('name') == 'replaceText':
#             if text is not None and text != "":
#                 if resource_id is not None and resource_id != "":
#                     pass
#                 else:
#                     pass
#
#             elif content_desc is not None and content_desc != "":
#                 if resource_id is not None and resource_id != "":
#                     pass
#                 else:
#                     pass
#
#             elif resource_id is not None and resource_id != "":
#                 pass
#             else:
#                 raise MethodGeneratorException("all identifiers (text, content_desc, resource_id) are either none or "
#                                                "empty, cannot locate the element")
#
#         # element is not an edittext
#         find_shared_identifier(text, content_desc)
#     #
#     #     if text is not None and text != "":  # the element has text
#     #         if resource_id is not None and resource_id != "":  # element has optional resource_id
#     #             # control is an input
#     #             if action.get_control_feature('name') == 'replaceText':
#     #                 statements += (f"{TAB_CONSTANT}onEventInputByText(\"{text}\", \"{resource_id}\", "
#     #                                f"\"{action.get_control_feature('value')}\")")
#     #                 statements += END_OF_STATEMENT_CONSTANT
#     #             # control is a click
#     #             elif action.get_control_feature('name') == 'click':
#     #                 statements += f"{TAB_CONSTANT}onEventClickingByText(\"{text}\", \"{resource_id}\")"
#     #                 statements += END_OF_STATEMENT_CONSTANT
#     #
#     #             else:
#     #                 raise MethodGeneratorException("The action control is not supported: " +
#     #                                                action.get_control_feature('name'))
#     #
#     #         else:  # element has no optional resource_id
#     #             # control is an input
#     #             if action.get_control_feature('name') == 'replaceText':
#     #                 statements += (f"{TAB_CONSTANT}onEventInputByText(\"{text}\", "
#     #                                f"\"{action.get_control_feature('value')}\")")
#     #                 statements += END_OF_STATEMENT_CONSTANT
#     #             # control is a click
#     #             elif action.get_control_feature('name') == 'click':
#     #                 statements += f"{TAB_CONSTANT}onEventClickingByText(\"{text}\")"
#     #                 statements += END_OF_STATEMENT_CONSTANT
#     #
#     #             else:
#     #                 raise MethodGeneratorException("The action control is not supported: " +
#     #                                                action.get_control_feature('name'))
#     #
#     #     elif content_desc is not None and content_desc != "":  # the element has content_desc
#     #         if resource_id is not None and resource_id != "":  # element has optional resource_id
#     #             # control is an input
#     #             if action.get_control_feature('name') == 'replaceText':
#     #                 statements += (f"{TAB_CONSTANT}onEventInputByCD(\"{content_desc}\", \"{resource_id}\", "
#     #                                f"\"{action.get_control_feature('value')}\")")
#     #                 statements += END_OF_STATEMENT_CONSTANT
#     #             # control is a click
#     #             elif action.get_control_feature('name') == 'click':
#     #                 statements += f"{TAB_CONSTANT}onEventClickingByCD(\"{content_desc}\", \"{resource_id}\")"
#     #                 statements += END_OF_STATEMENT_CONSTANT
#     #
#     #             else:
#     #                 raise MethodGeneratorException("The action control is not supported: " +
#     #                                                action.get_control_feature('name'))
#     #         else:  # element has no optional resource_id
#     #             # control is an input
#     #             if action.get_control_feature('name') == 'replaceText':
#     #                 statements += (f"{TAB_CONSTANT}onEventInputByCD(\"{content_desc}\", "
#     #                                f"\"{action.get_control_feature('value')}\")")
#     #                 statements += END_OF_STATEMENT_CONSTANT
#     #             # control is a click
#     #             elif action.get_control_feature('name') == 'click':
#     #                 statements += f"{TAB_CONSTANT}onEventClickingByCD(\"{content_desc}\")"
#     #                 statements += END_OF_STATEMENT_CONSTANT
#     #
#     #             else:
#     #                 raise MethodGeneratorException("The action control is not supported: " +
#     #                                                action.get_control_feature('name'))
#     #
#     #     elif resource_id is not None and resource_id != "":  # the element has resource_id alone
#     #         # control is an input
#     #         if action.get_control_feature('name') == 'replaceText':
#     #             statements += (f"{TAB_CONSTANT}onEventInputByResourceId(\"{resource_id}\", "
#     #                            f"\"{action.get_control_feature('value')}\")")
#     #             statements += END_OF_STATEMENT_CONSTANT
#     #         # control is a click
#     #         elif action.get_control_feature('name') == 'click':
#     #             statements += f"{TAB_CONSTANT}onEventClickingByResourceId(\"{resource_id}\")"
#     #             statements += END_OF_STATEMENT_CONSTANT
#     #
#     #         else:
#     #             raise MethodGeneratorException("The action control is not supported: " +
#     #                                            action.get_control_feature('name'))
#     #
#     #     else:
#     #         raise MethodGeneratorException("all identifiers (text, content_desc, resource_id) are either none or empty, "
#     #                                        "cannot locate the element")
#
#



def write_body_java(statement_queue: Queue, method_file: TextIO, language: str ='java'):
    """
    This method will write the whole body of the java method.
    The method style we follow is:
        method_name() {
            statement 1;
            statement 2;
            . . .
        }
    :param statement_queue: the queue that stores all the Statement obj
    :param method_file: the output io
    :param language: default java
    :return: void
    """
    method_file.write(" {\n")  # beginning bracket
    # Dequeue every statement in the statement_queue
    while not statement_queue.empty():
        statement: Statement = statement_queue.get()
        method_file.write(statement.to_code(language))
    method_file.write("}")  # end bracket


def write_header_java(header: Header, method_file: TextIO, language: str ='java'):
    """
    This method will write the header of the method in java
    For example, "public void method_name (parameter list ...)"
    :param header:
    :param method_file:
    :return:
    """
    method_file.write(header.to_code(language))


def add_mutant_event_statements(statement_queue: Queue, original_event: GUIEvent, event_mutant_info: MutantInfoPerEvent) -> Queue:
    """
    This method adds mutable event and its replaceable mutants to statement queue
    For click event, will add the events (parameterized original mutable events and the replaceable events)
    For input event, will only add the replaceable event, an original event with parameterized input value.

    :param event_mutant_info: all mutant information of the original event
    :param statement_queue: the statement queue the original event will generate
    :param original_event: original mutable event
    :return:
    """

    if event_mutant_info.is_input_event():
        replaceable_event_statement: Statement = (
            Statement(original_event, True, event_mutant_info.get_input_mutant_parameter()))
        statement_queue.put(replaceable_event_statement)
    elif event_mutant_info.is_click_event():
        index = 0
        for replaceable_event in event_mutant_info.get_mutant_replaceable_events():
            replaceable_event_statement: Statement = (
                Statement(replaceable_event, True, event_mutant_info.get_click_mutant_parameter_by_index(index)))
            statement_queue.put(replaceable_event_statement)
            index += 1
    else:
        raise MethodGeneratorException("original event is not click nor input event")

    return statement_queue


def generate_statement_queue(method: GUIMethod, mutant_result_file_path=None) -> Queue:
    """
    Generate a queue of statements for mutable and non-mutable events, and the replaceable mutant
    events for mutable events.
    :param method:
    :param mutant_result_file_path:
    :return:
    """
    statement_queue = Queue()

    event_index = 0
    for event in method.get_events():

        event_mutant_info = MutantInfoPerEvent(mutant_result_file_path, event,
                                               event_index)
        # mutable flag
        mutable_flag = event_mutant_info.is_mutable_event()
        # event is non-mutable event
        if not mutable_flag:
            statement_queue.put(Statement(event))
        # event is mutable event
        else:
            # add mutable event and its replaceable mutants to statement queue
            statement_queue = add_mutant_event_statements(statement_queue, event, event_mutant_info)

        event_index += 1

    return statement_queue


def generate(method: GUIMethod, language: str, mutant_result_file_path: str):
    """
    Generating the method by given basic method and mutant result.

    :param method: The basic method obj of GUIMethod type
    :param language: now only support "java"
    :param mutant_result_file_path: The file path where it stores the mutant results.
    :return: none
    """

    # get output file path
    output_directory, output_full_path = get_output_file_path(mutant_result_file_path)

    method_path = ""
    if language.lower() == "java":
        method_path = output_full_path.replace(".txt", ".java.txt")
    else:
        raise MethodGeneratorException("language not supported: " + language)

    # create a statement queue
    statement_queue = generate_statement_queue(method, mutant_result_file_path)

    # create header based on statements
    header: Header = Header(statement_queue, method)

    # Open method file to write method
    # Check whether the directory path exists or not
    is_exist = os.path.exists(output_directory)
    if not is_exist:
        # Create a new directory
        os.makedirs(output_directory)

    with open(method_path, 'w') as method_file:

        write_header_java(header, method_file)
        write_body_java(statement_queue, method_file)

