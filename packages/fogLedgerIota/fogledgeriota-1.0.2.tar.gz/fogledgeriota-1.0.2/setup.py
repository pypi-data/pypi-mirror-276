from setuptools import setup, find_packages

setup(
    name="fogLedgerIota",
    version="1.0.2",
    description='Plugin to build DLTs in Fogbed.',
    long_description='Plugin to build DLT in Fogbed. Suport IOTA. \
        The FogLedger is a plugin for [Fogbed](https://github.com/larsid/FogLedger-Iota). It allows you to emulate a fog network with distributed ledgers. \
        Currently, FogLedger has suport for IOTA. IOTA is a groundbreaking cryptocurrency designed for the Internet of Things (IoT), \
        Offering feeless transactions and scalability for machine-to-machine communication. \
        Its unique Tangle ledger utilizes a directed acyclic graph (DAG) for efficient data transfer and decentralized consensus, \
        making it ideal for securing and facilitating microtransactions in IoT ecosystems.',
    keywords=['networking', 'emulator', 'protocol', 'Internet', 'dlt', 'iota', 'fog'],
    url='https://github.com/larsid/FogLedger-Iota/tree/v1.0.0',
    author='Weslei Santos',
    author_email='weslei.eng.comp@gmail.com',
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Emulators"
    ],
    install_requires = [
        'numpy>=1.24.2',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    package_data={'fogLedgerIota': ['iota/data/*.sh', 'iota/data/*.json']}
)
