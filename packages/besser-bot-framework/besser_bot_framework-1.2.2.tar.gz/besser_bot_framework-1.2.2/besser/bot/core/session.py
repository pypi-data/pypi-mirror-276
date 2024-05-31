import logging
from typing import Any, TYPE_CHECKING

from besser.bot.core.transition import Transition
from besser.bot.core.file import File
from besser.bot.nlp.intent_classifier.intent_classifier_prediction import IntentClassifierPrediction

if TYPE_CHECKING:
    from besser.bot.core.bot import Bot
    from besser.bot.core.state import State
    from besser.bot.platforms.platform import Platform


class Session:
    """A user session in a bot execution.

    When a user starts interacting with a bot, a session is assigned to him/her to store user related information, such
    as the current state of the bot, the conversation history, the detected intent with its parameters or any user's
    private data. A session can be accessed from the body of the states to read/write user information.

    Args:
        session_id (str): The session id, which must unique among all bot sessions
        bot (Bot): The bot the session belongs to
        platform (Platform): The platform where the session has been created

    Attributes:
        _id (str): The session id, which must unique among all bot sessions
        _bot (str): The bot the session belongs to
        _platform (str): The platform where the session has been created
        _current_state (str): The current state in the bot for this session
        _dictionary (str): Storage of private data for this session
        _message (str): The last message sent to the bot by this session
        _predicted_intent (str): The last predicted intent for this session
        _file: File or None: The last file sent to the bot.
        chat_history (str): The session chat history
        flags (dict[str, bool]): A dictionary of boolean flags.
            A `predicted_intent flag` is set to true when an intent is received. When the evaluation of the
            current state's transitions is done, the flag is set to false. It may happen that a transition different
            from the one associated with this intent is triggered (e.g. one evaluating some condition). In the following
            state, if there is a transition associated with the same intent, it should not be triggered as the time for
            this intent passed (unless the same intent is detected, in such case the flag will be set to true again).
            Another flag `file_flag` is used for the same purpose but for files sent by the user
    """

    def __init__(
            self,
            session_id: str,
            bot: 'Bot',
            platform: 'Platform',
    ):
        self._id: str = session_id
        self._bot: 'Bot' = bot
        self._platform: 'Platform' = platform
        self._current_state: 'State' = self._bot.initial_state()
        self._dictionary: dict[str, Any] = {}
        self._message: str or None = None
        self._predicted_intent: IntentClassifierPrediction or None = None
        self._file: File or None = None
        self.chat_history: list[tuple[str, int]] = []
        self.flags: dict[str, bool] = {
            'predicted_intent': False,
            'file': False
        }

    @property
    def id(self):
        """str: The session id."""
        return self._id

    @property
    def platform(self):
        """Platform: The session platform."""
        return self._platform

    @property
    def current_state(self):
        """State: The current bot state of the session."""
        return self._current_state

    @property
    def message(self):
        """str: The last message sent to the bot."""
        return self._message

    @message.setter
    def message(self, message):
        """
        Set the last message sent to the bot.
        Args:
            message (str): the message to set in the session
        """
        self.chat_history.append((message, 1))
        self._message = message
        
    @property
    def file(self):
        """str: The last file sent to the bot."""
        return self._file

    @file.setter
    def file(self, file: File):
        """
        Set the last file sent to the bot.
        Args:
            file (File): the file to set in the session
        """
        self.chat_history.append((file.get_json_string(), 1))
        self._file = file
        self.flags['file'] = True

    @property
    def predicted_intent(self):
        """str: The last predicted intent for this session."""
        return self._predicted_intent

    @predicted_intent.setter
    def predicted_intent(self, predicted_intent: IntentClassifierPrediction):
        """
        Set the last predicted intent for this session.
        Args:
            predicted_intent (File): the last predicted intent
        """
        self._predicted_intent = predicted_intent
        self.flags['predicted_intent'] = True

    def set(self, key: str, value: Any) -> None:
        """Set an entry to the session private data storage.

        Args:
            key (str): the entry key
            value (Any): the entry value
        """
        self._dictionary[key] = value

    def get(self, key: str) -> Any:
        """Get an entry of the session private data storage.

        Args:
            key (str): the entry key

        Returns:
            Any: the entry value, or None if the key does not exist
        """
        if key not in self._dictionary:
            return None
        return self._dictionary[key]

    def delete(self, key: str) -> None:
        """Delete an entry of the session private data storage.

        Args:
            key (str): the entry key
        """
        del self._dictionary[key]

    def move(self, transition: Transition):
        """Move to another bot state.

        Args:
            transition (Transition): the transition that points to the bot state to move
        """
        logging.info(transition.log())
        self._bot._monitoring_db_insert_transition(self, transition)
        if any(transition.dest is global_state for global_state in self._bot.global_state_component):
            self.set("prev_state", self.current_state)
        self._current_state = transition.dest
        self._current_state.run(self)

    def reply(self, message: str) -> None:
        """A bot message (usually a reply to a user message) is sent to the session platform to show it to the user.

        Args:
            message (str): the bot reply
        """
        # Multi-platform
        self._platform.reply(self, message)
