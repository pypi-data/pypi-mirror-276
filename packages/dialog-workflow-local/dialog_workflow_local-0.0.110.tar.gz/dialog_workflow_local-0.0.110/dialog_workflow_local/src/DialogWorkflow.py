import json
import random

from database_mysql_local.generic_crud import GenericCRUD
from language_remote.lang_code import LangCode
from logger_local.LoggerLocal import Logger
from message_local.CompoundMessage import CompoundMessage
from message_local.Recipient import Recipient
from user_context_remote.user_context import UserContext
from variable_local.variables_local import VariablesLocal

from .Constants import DIALOG_WORKFLOW_CODE_LOGGER_OBJECT, WorkflowActionEnum
from .ProfileContext import DialogWorkflowRecord
from .action import Action
from .utils import get_curr_state, update_profile_curr_state_in_db

user = UserContext()
logger = Logger.create_logger(object=DIALOG_WORKFLOW_CODE_LOGGER_OBJECT)
generic_crud = GenericCRUD(default_schema_name='dialog_workflow',
                           default_table_name='dialog_workflow_state',
                           default_view_table_name='dialog_workflow_state_view')


# TODO Please use MessagesLocal to store the message(s) recieved and anwers
# TODO Please use the function defined in avatar similar to get_dialog_workflow_avatar_profile_id( profile_id1, prompt, group_id, profile_id2...) using avatar_table and avtar_group_table
def get_dialog_workflow_record(profile_curr_state: int, lang_code: LangCode,
                               incoming_message: str = None) -> DialogWorkflowRecord:
    """Get all potential records in a specific state and choose randomly one of them"""
    logger.start(
        object={'profile_curr_state': profile_curr_state, 'language': lang_code})
    select_clause_value = ("state_id, parent_state_id, workflow_action_id, lang_code, parameter1, variable1_id, "
                           "result_logical, result_figure_min, result_figure_max, next_state_id, "
                           "no_feedback_milliseconds, next_state_id_if_there_is_no_feedback")
    where = "state_id = %s AND lang_code = %s"
    if incoming_message and not incoming_message.isdigit() and not all(
            x.isdigit() for x in incoming_message.split(',')):
        # can't be WorkflowActionEnum.MENU_ACTION, as it is expecting number(s)
        where += " AND workflow_action_id <> " + str(WorkflowActionEnum.MENU_ACTION.value)
    optional_records = generic_crud.select_multi_dict_by_where(
        where=where, params=(profile_curr_state, lang_code.value), select_clause_value=select_clause_value)
    if not optional_records:
        error_message = f"No records found for state_id: {profile_curr_state} and language: {lang_code}"
        logger.error(error_message)
        logger.end()
        raise Exception(error_message)
    dialog_workflow_record = DialogWorkflowRecord(random.choice(optional_records))
    logger.end(object={'dialog_workflow_record': str(dialog_workflow_record)})
    return dialog_workflow_record


def post_message(*, incoming_message: str) -> json or list[int]:
    """This function is supposed to serve as a POST request later on using REST API.
    It runs until needing input from the user, which it then sends a json to the user with the message and exits
    param: incoming_message: the message to send"""
    logger.start(object={'incoming_message': incoming_message})
    profile_id = user.get_effective_profile_id()
    lang_code = user.get_effective_profile_preferred_lang_code()
    # TODO Save the message using MessagesLocal (from DIALOG_WORKFLOW_PROFILE_ID, to UserContext.getEffectiveProfileId, ...)
    variables = VariablesLocal()
    profile_curr_state = get_curr_state(profile_id)
    got_response = incoming_message.strip() != ""  # This variable indicates if we must act now as we got a response from the user or as if we should send one to him
    init_action = Action(incoming_message=incoming_message, profile_id=profile_id,
                         lang_code=lang_code, profile_curr_state=profile_curr_state,
                         variables=variables)
    while True:
        dialog_workflow_record: DialogWorkflowRecord = get_dialog_workflow_record(
            init_action.profile_curr_state, lang_code, incoming_message=incoming_message)
        selected_act = init_action.act(dialog_workflow_record, got_response)
        outgoing_message = selected_act.get("outgoing_message")
        # TODO Save the message using MessagesLocal (from DIALOG_WORKFLOW_PROFILE_ID, to UserContext.getEffectiveProfileId, ...)
        if outgoing_message is not None:
            if isinstance(outgoing_message, dict):
                outgoing_compound_message = json.dumps(outgoing_message)
                logger.end(object={'outgoing_compound_message': outgoing_compound_message})
                return outgoing_compound_message
            elif not isinstance(outgoing_message, list):
                recipient = Recipient(profile_id=profile_id, preferred_lang_code_str=lang_code.value,
                                      user_id=user.get_effective_user_id(),
                                      first_name=user.get_real_name())
                outgoing_compound_message = CompoundMessage(
                    original_body=outgoing_message, recipients=[recipient]).get_compound_message_str()
            else:
                outgoing_compound_message = outgoing_message
            logger.end(object={'outgoing_compound_message': outgoing_compound_message})
            return outgoing_compound_message
        init_action.profile_curr_state = dialog_workflow_record.next_state_id if not selected_act.get(
            "is_state_changed") else init_action.profile_curr_state
        update_profile_curr_state_in_db(init_action.profile_curr_state, profile_id)
        got_response = False
