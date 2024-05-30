from typing import Dict, Any


class Event:
    def __init__(self, eventType: str, actuations: Dict[str, Any] = {}) -> None:
        """
        Initialize the Event object with the specified event type and optional actuations.

        Parameters:
        - eventType (str): The type of the event.
        - actuations (Dict[str, Any]): A dictionary containing actuations associated with the event. Default is an empty dictionary.

        Raises:
        - Exception: If an unexpected exception occurs during initialization.

        Usage:
        - event = Event("eventType", {"key": "value"})
        """
        try:
            self.__set_eventType(eventType)
            self.set_actuations(actuations)
        except Exception as e:
            raise Exception(f"Failed to initalize event objects due to: {e}")

    def set_actuations(self, actuationsDict: Dict[str, Any]):
        """
        Set the actuations for the event object, overwriting any previous actuations.

        Parameters:
        - actuationsDict (Dict[str, Any]): A dictionary containing actuations.

        Raises:
        - Exception: If the dictionary structure is invalid.

        Usage:
        - event.set_actuations({"key": "value"})
        """
        try:
            self.__validate_dict_structure(actuationsDict)
            self.__actuations = actuationsDict
        except Exception as e:
            raise Exception(f"Failed to set_actuations due to: {e}")

    def get_actuations(self):
        """
        Get the actuations associated with the event.

        Raises:
        - Exception: If failed to retrieve actuations.

        Usage:
        - actuations = event.get_actuations()
        """
        try:
            return self.__actuations
        except Exception as e:
            raise Exception(f"Failed to get_actuations due to: {e}")

    def __set_eventType(self, eventType: str):
        """
        Set the event type for the event object.

        Parameters:
        - eventType (str): The type of the event.

        Raises:
        - Exception: If the event type is not a valid string.

        Usage:
        - event.__set_eventType("eventType")
        """
        try:
            if type(eventType) == str:
                self.__eventType = eventType
            else:
                raise Exception(
                    f"eventType is not valid: eventType must be of type str it is of type {type(eventType)}"
                )
        except Exception as e:
            raise Exception(f"Failed to __set_eventType due to: {e}")

    def get_eventType(self):
        """
        Get the event type associated with the event.

        Raises:
        - Exception: If failed to retrieve the event type.

        Usage:
        - eventType = event.get_eventType()
        """
        try:
            return self.__eventType
        except Exception as e:
            raise Exception(f"Failed to get_eventType due to: {e}")

    def __validate_dict_structure(self, testDict):
        """
        Validate the dictionary structure to ensure keys are strings.

        Parameters:
        - testDict: The dictionary to validate.

        Raises:
        - Exception: If the input is not a dictionary or if any key is not a string.

        Usage:
        - event.__validate_dict_structure({"key": "value"})
        """
        if not isinstance(testDict, dict):
            raise Exception("Input must be a dictionary")

        for key, value in testDict.items():
            if not isinstance(key, str):
                raise Exception(
                    f"Dictionary key must be a string, but found {type(key)}"
                )

        # No need to check the value types since we allow any type for values
