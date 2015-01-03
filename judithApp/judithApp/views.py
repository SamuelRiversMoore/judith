
#requests_cache.install_cache('github_cache', backend='sqlite', expire_after=180)
import time
import requests
import requests_cache

from flask import Flask, render_template, request, jsonify

from judithApp import app

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        first = request.form.get('first')
        response = first
        return response
        # user inputs
#        first = request.form.get('first')
#        second = request.form.get('second')
        # api call
#        url = "https://api.github.com/search/users?q=location:{0}+language:{1}".format(first, second)
#        now = time.ctime(int(time.time()))
#        response = requests.get(url)
#        print "Time: {0} / Used Cache: {1}".format(now, response.from_cache)
        # return json
#        return jsonify(response.json())
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
