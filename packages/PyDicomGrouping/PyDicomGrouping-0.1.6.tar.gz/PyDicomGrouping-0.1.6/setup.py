from setuptools import setup, find_packages
setup(
    name = "PyDicomGrouping",
    version = "0.1.6",
    author = "Kaixuan,Zhao",
    author_email = "kaixuan_zhao@163.com",
    include_package_data=True,
    package_data = {
        "":["**/*.pkl","**/*.json","**/*.xlsx","**/*.rkey","**/*.so"]
    },
    packages = find_packages(),
    python_requires=">=3.8.0,<4",
    install_requires = ["numpy",
                        "pandas",
                        "nibabel",
                        "pydicom",
                        "alive_progress",
                        "selenium"],
)