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
    descr = request.args.get("description")
    brew_service.new(name, descr)
    brews = brew_service.get_all()
    return render_template("brews.html", all_brews=sort_brews(brews))


@brew_blueprint.route("/update", methods=["GET"])
@inject
def update_brew(brew_service: BrewService):
    if not request.args or "name" not in request.args:
        return render_template(
            "error.html", message="You need to give a new brew a name"
        )
    brew_id = request.args.get("brew_id")
    name = request.args.get("updated_name")
    descr = request.args.get("updated_description")
    brew_service.get_all()
    brew = brew_service.get_by_id(brew_id)
    brew.name = name
    brew.description = descr
    brews = brew_service.save(brew)
    return render_template("brews.html", all_brews=sort_brews(brews))


@brew_blueprint.route("/set_active", methods=["GET"])
def set_active(brew_service: BrewService):
    if not request.args or "id" not in request.args:
        return render_template("error.html", message="Invalid request")
    brew_id = str(request.args.get("id"))
    brew = brew_service.set_active(brew_id)
    return render_template(
        "success.html",
        message='Brew "%s" successfully activated' % brew.get_display_name(),
    )

@brew_blueprint.route("/set_inactive", methods=["GET"])
def set_inactive(brew_service: BrewService):
    if not request.args or "id" not in request.args:
        return render_template("error.html", message="Invalid request")
    brew_id = str(request.args.get("id"))
    brew = brew_service.set_inactive(brew_id)
    return render_template(
        "success.html",
        message='Brew "%s" successfully inactivated' % brew.get_display_name(),
    )
