"""Module to keep track of the score.

There is nothing in this module that can create a xml score file. That's
because the only way to create a score is by scoring the data, visually. Once
you have the score file, you can work with it programmatically with this
module.

"""
from logging import getLogger
lg = getLogger(__name__)

from xml.etree.ElementTree import tostring, parse
from xml.dom.minidom import parseString


class Scores():
    """Class to return nicely formatted information from xml.

    Parameters
    ----------
    xml_file : str
        path to xml file
    root : instance of xml.etree.ElementTree.Element, optional
        xml structure with information about sleep staging

    Attributes
    ----------
    root : instance of xml.etree.ElementTree.Element
        xml structure with information about sleep staging
    xml_file : str
        path to xml file

    Notes
    -----
    If root is not given, xml will be read from file. If both are given, it
    overwrites filename with root.

    """
    def __init__(self, xml_file, root=None):
        self.xml_file = xml_file
        self.root = root

        if root is None:
            self.load()
        else:
            self.save()

    def get_rater(self):
        """Returns the name of the rater.

        Notes
        -----
        TODO: what if we have more raters?

        """
        return list(self.root)[0].get('name')

    def get_epochs(self, stages_of_interest=None):
        """Get epochs (all or only those of interest).

        Parameters
        ----------
        stages_of_interest : tuple of str
            sleep stages that you want.

        Returns
        -------
        list of dict
            each epoch is defined by start_time and end_time (in s in reference
            to the start of the recordings) and a string of the sleep stage.
            If you specify stages_of_interest, only epochs belonging to those
            stages will be included (can be an empty list).

        """
        all_epochs = list(self.root)[0]
        epochs = []
        for epoch in all_epochs:
            epochs.append({'start_time': int(list(epoch)[0].text),
                           'end_time': int(list(epoch)[1].text),
                           'stage': list(epoch)[2].text,
                           })

        if stages_of_interest is not None:
            epochs = [x for x in epochs if x['stage'] in stages_of_interest]

        return epochs

    def get_stage_for_epoch(self, id_epoch):
        """Return stage for one specific epoch.

        Parameters
        ----------
        id_epoch : str
            index of the epoch

        Returns
        -------
        stage : str
            description of the stage.

        """
        all_epochs = list(self.root)[0]
        for epoch in all_epochs:
            if epoch.get('id') == id_epoch:
                break
        return list(epoch)[2].text

    def set_stage_for_epoch(self, id_epoch, stage):
        """Change the stage for one specific epoch.

        Parameters
        ----------
        id_epoch : str
            index of the epoch
        stage : str
            description of the stage.

        Raises
        ------
        KeyError
            When the id_epoch is not in the list of epochs.

        """
        found = False

        all_epochs = list(self.root)[0]
        for epoch in all_epochs:
            if epoch.get('id') == id_epoch:
                list(epoch)[2].text = stage
                found = True
                break

        if not found:
            raise KeyError(id_epoch + ' not found')

        self.save()

    def load(self):
        """Load xml from file."""
        lg.info('Loading ' + self.xml_file)
        xml = parse(self.xml_file)
        root = xml.getroot()
        root.text = root.text.strip()
        for rater in root:
            rater.text = rater.text.strip()
            rater.tail = rater.tail.strip()
            for epochs in rater:
                epochs.text = epochs.text.strip()
                epochs.tail = epochs.tail.strip()
                for values in epochs:
                    values.tail = values.tail.strip()
        self.root = root

    def save(self):
        """Save xml to file."""
        xml = parseString(tostring(self.root))
        lg.info('Saving ' + self.xml_file)
        with open(self.xml_file, 'w') as f:
            f.write(xml.toprettyxml())
