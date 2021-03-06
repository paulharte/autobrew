from flask import Blueprint, render_template, request
from injector import inject

from autobrew.brew.brew import sort_brews
from autobrew.brew.brewService import BrewService

brew_blueprint = Blueprint("brews", __name__, url_prefix="/brews")


@brew_blueprint.route("/", methods=["GET"])
@inject
def view_brews(brew_service: BrewService):
    brews = brew_service.get_all()
    return render_template("brews.html", all_brews=sort_brews(brews))


@brew_blueprint.route("/new", methods=["GET"])
@inject
def new_brew(brew_service: BrewService):
    if not request.args or "name" not in request.args:
        return render_template(
            "error.html", message="You need to give a new brew a name"
        )
    name = request.args.get("name")
    brew_service.new(name)
    brews = brew_service.get_all()
    return render_template("brews.html", all_brews=sort_brews(brews))
