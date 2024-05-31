from typing import Any

from neomodel import StructuredNode, StructuredRel
from neomodel import RelationshipTo, RelationshipFrom
from neomodel import StringProperty, IntegerProperty, FloatProperty, DateTimeProperty, ArrayProperty


class FollowRel(StructuredRel):
    since = DateTimeProperty(default_now=True, index=True)


class SubscribeRel(StructuredRel):
    since = DateTimeProperty(default_now=True, index=True)


class ReadRel(StructuredRel):
    read_time = DateTimeProperty(default_now=True, index=True)


class Entity(StructuredNode):
    name = StringProperty(unique_index=True)

    reads = RelationshipTo("Paper", "read", model=ReadRel)
    follows = RelationshipTo("Entity", "follow", model=FollowRel)
    followers = RelationshipFrom("Entity", "follow", model=FollowRel)
    subscriptions = RelationshipTo("Venue", "subscribe", model=SubscribeRel)

    @property
    def serialize(self) -> dict[str, Any]:
        data = {"name": self.name}
        return data


class Paper(StructuredNode):
    paper_id = StringProperty(unique_index=True)
    arxiv_id = StringProperty()
    title = StringProperty()
    abstract = StringProperty()
    summary = StringProperty()
    publication_date = DateTimeProperty()
    reference_count = IntegerProperty()
    citation_count = IntegerProperty()
    pdf = StringProperty()
    # openai text-embedding-3-large cast to 1024
    embedding_te3l = ArrayProperty(FloatProperty())

    readers = RelationshipFrom("Entity", "read", model=ReadRel)
    references = RelationshipTo("Paper", "cite")
    citations = RelationshipFrom("Paper", "cite")

    @property
    def serialize(self) -> dict[str, Any]:
        data = {
            "paper_id": self.paper_id,
            "title": self.title,
            "abstract": self.abstract,
            "summary": self.summary,
            "publication_date": self.publication_date,
            "reference_count": self.reference_count,
            "citation_count": self.citation_count,
            "pdf": self.pdf,
        }
        return data


class Collection(StructuredNode):
    name = StringProperty(unique_index=True)

    papers = RelationshipTo("Paper", "contain")


class Venue(StructuredNode):
    name = StringProperty(unique_index=True)

    collections = RelationshipTo("Collection", "publish")
