"""module item
    define the Artwork class with
    label, date, agents (parts), classified as, id
    """

class Artwork:
    """Define Artwork class
    """

    def __init__(self, label, date, agent, classification, id):
        """init an Artwork object

        Args:
            label
            date
            agent
            classification
            id
        """
        self._label = label
        self._date = date
        self._agent= agent
        self._classification = classification
        self._id = id

    def get_label(self):
        """get label of the object

        Returns:
            label
        """
        return self._label

    def get_date(self):
        """get date of the object

        Returns:
            date
        """
        return self._date

    def get_agent(self):
        """get agent of the object

        Returns:
            agent
        """
        return self._agent

    def get_classification(self):
        """get classification of the object

        Returns:
            classification
        """
        return self._classification

    def to_tuple(self):
        """get a tuple of label, date, agent, classification and id of the object

        Returns:
           tuple
        """
        return (self._label, self._date, self._agent, self._classification, self._id)

    def to_xml(self):
        """get xml form of the object

        Returns:
            xml
        """
        pattern = '<artwork>'
        pattern += '<label>%s</label>'
        pattern += '<date>%s</date>'
        pattern += '<agent>%f</agent>'
        pattern += '<classification>%f</classification>'
        pattern += '</artwork>'
        return pattern % (self._label, self._date, self._agent, self._classification, self._id)

    def to_dict(self):
        """get dict form of the object

        Returns:
            dict
        """
        return {'label': self._label, 'date': self._date,
            'agent': self._agent, 'classification': self._classification,
            'id': self._id}
