from flask import Flask, request, render_template, redirect, url_for, jsonify, flash, session
 
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")
