from __future__ import annotations

from clicksearch import *

if typing.TYPE_CHECKING:
    from typing import Any, Callable, Mapping


class ChallengeIcons(Number):
    icons = ("terror", "combat", "arcane", "investigation")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, skip_filters=[Number.filter_number], **kwargs)

    def fetch(
        self, item: Mapping, default: Any | type = MissingField
    ) -> tuple[int, int, int, int]:
        """Returns all icon values in `item` as a tuple."""
        return tuple(self.validate(item.get(icon, 0)) for icon in self.icons)

    @fieldfilter("--terror")
    def filter_terror(self, arg: Callable, value: Any, options: dict) -> bool:
        """Filter on number of terror icons."""
        return self.filter_number(arg, value[0], options)

    @fieldfilter("--combat")
    def filter_combat(self, arg: Callable, value: Any, options: dict) -> bool:
        """Filter on number of combat icons."""
        return self.filter_number(arg, value[1], options)

    @fieldfilter("--arcane")
    def filter_arcane(self, arg: Callable, value: Any, options: dict) -> bool:
        """Filter on number of arcance icons."""
        return self.filter_number(arg, value[2], options)

    @fieldfilter("--investigation")
    def filter_investigation(self, arg: Callable, value: Any, options: dict) -> bool:
        """Filter on number of investigation icons."""
        return self.filter_number(arg, value[3], options)

    def format_value(self, value: tuple[int, int, int, int]) -> str:
        """Return a string representation of `value`."""
        if sum(value) == 0:
            return "No Icons"
        terror, combat, arcane, investigation = value
        return (
            click.style("T" * terror, fg="green") if terror else ""
            + click.style("C" * combat, fg="red") if combat else ""
            + click.style("A" * arcane, fg="magenta") if arcane else ""
            + click.style("I" * investigation, fg="yellow") if investigation else ""
        )

    def format_brief(self, value: Any) -> str:
        """Returns a brief formatted version of `value` for this field."""
        value = self.format_value(value)
        return (
            click.style("[", fg="blue")
            + value
            + click.style("]", fg="blue")
        ) if value != "No Icons" else value


class Test(ModelBase):
    """Test application."""

    name = String()
    descriptor = String(verbosity=1, standalone=True, styles={"fg": "yellow"})
    subtypes = SeparatedString(
        optname="subtype", separator=".", verbosity=1, standalone=True, styles={"fg": "magenta"}
    )
    unique = Flag(helpname="uniqueness")
    faction = Choice(
        choices={
            "Agency": "The Agency",
            "Cthulhu": None,
            "Hastur": None,
            "Miskatonic University": None,
            "Neutral": None,
            "Shub-Niggurath": None,
            "Silver Twilight": None,
            "Syndicate": None,
            "The Agency": None,
            "Yog-Sothoth": None,
        },
        inclusive=True,
    )
    cardtype = Choice(
        choices=["Character", "Event", "Story", "Support"],
        keyname="type",
        optname="type",
        realname="Card Type",
        inclusive=True,
    )
    cost = Number(specials=["X"])
    skill = Number(specials=["X"], implied={"cardtype": "Character"})
    icons = ChallengeIcons(implied={"cardtype": "Character"})
    restricted = Flag(verbosity=2)
    banned = Flag(verbosity=2)


def testsource(options):
    yield {"name": "Blackwood Associate", "descriptor": None, "type": "Character", "faction": "The Agency", "unique": False, "subtypes": "Investigator.", "text": "", "cost": 1, "skill": 1, "terror": 0, "combat": 1, "arcane": 0, "investigation": 0, "transient": False, "steadfast": None, "era": "CCG", "id": None, "set": "AE", "setname": "Arkham Edition", "setid": None, "flavor": None, "illustrator": None, "max": 4, "banned": False, "restricted": False}
    yield {"name": "Requisitions Officer", "descriptor": None, "type": "Character", "faction": "The Agency", "unique": False, "subtypes": "Government.", "text": "Action: pay 3 to attach an Attachment support card from any player's discard pile to Requisitions Officer.", "cost": 3, "skill": 3, "terror": 0, "combat": 1, "arcane": 1, "investigation": 0, "transient": False, "steadfast": None, "era": "CCG", "id": None, "set": "FC", "setname": "Forgotten Cities", "setid": None, "flavor": None, "illustrator": None, "max": 4, "banned": False, "restricted": False}




if __name__ == "__main__":
    Test.cli()
