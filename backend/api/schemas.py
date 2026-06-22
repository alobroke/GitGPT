from pydantic import BaseModel


class RepositoryRequest(
    BaseModel
):
    repo_url: str


class QuestionRequest(
    BaseModel
):
    repository: str
    question: str


class Source(
    BaseModel
):
    file: str
    name: str


class QuestionResponse(
    BaseModel
):
    answer: str