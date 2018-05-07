import logging
import traceback
from datetime import datetime

import common_utils as cmu

from awsLexAlexa.event_handler import EventHandler, LEX

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

ev = EventHandler()

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M"


@ev.register_intent(intent='newEvents')
def addNewEvent(event):
    try:
        date = event.get_slot('date')
        startTime = event.get_slot('startTime')
        endTime = event.get_slot('endTime')
        text = event.get_slot('text')

        logger.debug('slots\n'
                     'date: {}\n'
                     'startTime: {}\n'
                     'endTime: {}\n'
                     'text: {}\n'.format(date, startTime, endTime, text))
        now = datetime.now()
        action = None

        if event.is_confirmed():
            logger.debug('status confirmed')
            cmu.insert_event(text, date, startTime, endTime)
            msg = 'Added date {} in {}, from {} to {}'.format(text, date, startTime, endTime)
            if event.bot_platform == LEX:
                action = event.close_response(msg=msg,
                                              fulfilled=True)
            else:
                action = event.end_response(msg=msg)
        elif event.is_denied():
            logger.error('Denied status')
            action = event.delegate_response()

        else:
            if 'date' not in event.sessionAttributes:
                logger.debug('date not in session')
                if date:
                    if datetime.strptime(date, DATE_FORMAT) <= now:
                        action = event.elicit_slot_response(
                            elicit_slot='date',
                            msg='The date can not be in the past.\nPlease, tell me other date.',
                            reprompt_msg='Please, tell me other date which not be in past.')
                    elif datetime.strptime(date, DATE_FORMAT) > now:
                        event.set_sessionAttributes('date', date)
                else:
                    action = event.elicit_slot_response(
                        elicit_slot='date',
                        msg='When the event start?',
                        reprompt_msg='Please, I need to know when the even start?'
                    )

            elif 'startTime' not in event.sessionAttributes:
                logger.debug('startTime not in session')
                if startTime:
                    event.set_sessionAttributes('startTime')
                else:
                    action = event.elicit_slot_response(
                        elicit_slot='startTime',
                        msg='When the event start?',
                        reprompt_msg='Please, I need to know when the even start?'
                    )

            elif 'endTime' not in event.sessionAttributes:
                logger.debug('endTime not in session')
                if endTime:
                    logger.debug('endTime filled')
                    if startTime and endTime and datetime.strptime(startTime, TIME_FORMAT) >= datetime.strptime(endTime,
                                                                                                                TIME_FORMAT):
                        logger.debug('endTime is after startTime')
                        action = event.elicit_slot_response(
                            elicit_slot='endTime',
                            msg='You can not finalize the event before to start\n'
                                'Please, tell me other final time.',
                            reprompt_msg='You can not finalize the event before to start\n'
                                         'Please, tell me other final time.'
                        )

                    elif startTime and endTime and datetime.strptime(startTime, TIME_FORMAT) > datetime.strptime(
                            endTime,
                            TIME_FORMAT):
                        logger.debug('endTime is ok')
                        event.set_sessionAttributes('endTime', endTime)

                else:
                    logger.debug('endTime empty')
                    action = event.elicit_slot_response(
                        elicit_slot='endTime',
                        msg='When the event end?',
                        reprompt_msg='Please, I need to know when the even end?'
                    )

            elif 'text' not in event.sessionAttributes:
                logger.debug('text not in session')
                if text:
                    event.set_sessionAttributes('text', text)
                else:
                    action = event.elicit_slot_response(
                        elicit_slot='text',
                        msg='I need add some text to the event.\n'
                            'What text do you want to add?',
                        reprompt_msg='I need add some text to the event.\n'
                                     'What text do you want to add?',
                    )
            else:
                action = event.delegate_response()

    except Exception as f:
        logger.error(traceback.format_exc())

    if action is None:
        action = event.delegate_response()
    return action


@ev.register_intent(intent='QueryEvents')
def query_n_events(event):
    msg = ''
    try:
        n_events = event.get_slot('n')
        eventos = cmu.get_n_events(n_events)
        text_format = "{} on {} from {} to {}\n"
        if 'Items' in eventos and len(eventos.get('Items')) > 0:
            for date in eventos.get('Items'):
                logger.debug(date)
                text = date.get('text')
                day = date.get('day')
                end = date.get('end')
                start = date.get('start')
                msg += text_format.format(text, day, start, end)
        else:
            msg = 'No events registered'
    except:
        logger.error(traceback.format_exc())

    if event.bot_platform == LEX:
        return event.close_response(msg, fulfilled=True)
    else:
        return event.end_response(msg)


@ev.register_intent(intent='RemoveEvent')
def delete_event(event):
    event_date = event.get_slot('date')
    try:
        if event.is_confirmed():
            cmu.remove_event(event_date)
            logger.debug('Event eliminated')
            msg = 'The event was correctly removed'
            if event.bot_platform == LEX:
                action = event.close_response(msg, fulfilled=True)
            else:
                action = event.end_response(msg)
        elif event.is_denied():
            logger.error('Denied status')
            action = event.delegate_response()

        else:
            if event_date:
                evento = cmu.get_event(event_date)
                text_format = "{} on {} from {} to {}\n"
                if 'Item' in evento and len(evento.get('Item')) > 0:
                    date = evento.get('Item')
                    logger.debug(date)
                    text = date.get('text')
                    day = date.get('day')
                    end = date.get('end')
                    start = date.get('start')
                    msg = text_format.format(text, day, start, end)
                    action = event.confirm_intent_response(
                        msg='Do you want to delete {} ?'.format(msg),
                        reprompt_msg='I need to confirm that you want to delete the event {}\n '
                                     'Do you want to delete it?'.format(msg)
                    )

                else:
                    logger.debug('There arent events on {]'.format(event_date))
                    msg = 'There are not events on that date'
                    if event.bot_platform == LEX:
                        action = event.close_response(msg, fulfilled=True)
                    else:
                        action = event.end_response(msg)
            else:
                action = event.delegate_response()
    except:
        logger.error(traceback.format_exc())

    return action


@ev.handler_intent(intent='AMAZON.HelpIntent')
def get_welcome_response(event):
    # TODO: Update messages with desired ones
    intro_msg = "Hi, this is the SKILL_NAME, what can I do for you?"
    help_1_msg = "You can ask me for INTENT1, INTENT2 or INTENT3."
    help_2_msg = '<speak><p>For INTENT1, say <prosody rate="x-slow">utterance1</prosody>.</p>' \
                 '<p>For INTENT2, say <prosody rate="x-slow">utterance2</prosody>.</p>' \
                 '<p>For INTENT3, say <prosody rate="x-slow">utterance3</prosody>.</p></speak>'
    if event.get_sessionAttributes('new'):  # Called from on_launch
        action = event.elicit_intent_response(msg=intro_msg,
                                              reprompt_msg=help_1_msg)

    else:  # Called when intent is AMAZON.HelpIntent
        action = event.elicit_intent_response(msg=help_1_msg,
                                              reprompt_msg=help_2_msg,
                                              reprompt_type='SSML')
    return action


@ev.handler_intent(intent='AMAZON.CancelIntent')
@ev.handler_intent(intent='AMAZON.StopIntent')
def handle_session_end_request(event):
    msg = "It was a pleasure to assist you, goodbye."
    action = event.end_response(msg=msg)
    # TODO: Add cleanup logic here if necessary
    return action


def lambda_handler(event, context):
    logger.debug('Request:\n {}'.format(event))
    action = ev.execute(event)
    logger.debug('Response:\n {}'.format(action))
    return action
