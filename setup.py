from setuptools import setup

with open("README.rst") as f:
    long_description = f.read()

# Install the core dependencies listed in requirements.txt (ignoring comments).
with open("requirements.txt") as f:
    requirements = [line.strip() for line in f
                    if line.strip() and not line.startswith("#")]

setup(
    name="bayesianflexifit",
    version="0.1.0",
    description="Flexible Bayesian model fitting with nested sampling.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Adam Carnall",
    url="https://github.com/ACCarnall/bayesianflexifit",
    packages=["bff"],
    install_requires=requirements,
    extras_require={"mpi": ["mpi4py"],
                    "examples": ["matplotlib", "corner"]},
    python_requires=">=3.6",
)
