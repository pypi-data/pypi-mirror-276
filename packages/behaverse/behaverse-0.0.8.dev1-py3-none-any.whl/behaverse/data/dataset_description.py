"""Dataset information and additional metadata class."""


class DatasetDescription():
    """Contains additional metadata about the dataset."""
    def __init__(self, name) -> None:
        """Initialize the DatasetDescription class.

        Args:
            name: Name of the dataset.
        """
        self.name = name

        # TODO load attributes from the registry

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f'<DatasetDescription {self.name}>'
