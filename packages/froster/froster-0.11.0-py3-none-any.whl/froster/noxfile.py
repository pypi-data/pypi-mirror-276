import nox

# @nox.session
# def lint(session):
#     session.install("flake8")
#     session.run("flake8", "froster.py")

@nox.session
def tests(session):
    # same as pip install .
    session.install("../.")
    session.run("froster", "--version")