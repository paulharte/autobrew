
from flask import Flask, render_template

app = Flask(__name__)
app.debug = True


@app.route('/')
def brew_monitor():
    return render_template('main_template.html', room_temp=str(19.0), brew_temp=str(22.0))


if __name__ == '__main__':
    app.run()