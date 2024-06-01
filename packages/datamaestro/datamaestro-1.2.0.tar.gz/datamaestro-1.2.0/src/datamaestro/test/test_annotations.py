from datamaestro.annotations.agreement import useragreement
from datamaestro.definitions import AbstractDataset


def test_useragreements(context):
    # Fake dataset
    class t(AbstractDataset):
        pass

    useragreement("test")(t(None))
