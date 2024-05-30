from setuptools import setup


required_packages = [
    "pandas",
    "pydantic",
    "scikit-learn",
    "pyyaml",
]

torch_required_packages = ["torch", "torchvision", "torchaudio"]

dev_required_packages = [
    "mypy",
    "ruff",
    "setuptools",
    "build"
    "twine"
]

extras_require = {
    "dev": dev_required_packages,
    "torch": torch_required_packages,
}

setup(
    name="faps-hassan-rady",
    version="1.0.0",
    description="FAPS project: Predictive Maintenance in Manufacturing",
    author="Hassan Rady",
    license="MIT",
    install_requires=required_packages,
    extras_require=extras_require,
)
