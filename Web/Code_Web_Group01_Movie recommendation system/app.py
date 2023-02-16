from flask import Blueprint, Flask, redirect, url_for, render_template
main = Blueprint('main', __name__)
 
import json
from engine import RecommendationEngine
 
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
from flask import Flask, request

@main.route("/<int:user_id>/ratings/top/<int:count>", methods=["GET"])
def top_ratings(user_id, count):
    logger.debug("User %s TOP ratings requested", user_id)
    top_ratings1 = recommendation_engine.get_top_ratings(user_id,count)
    #print(json.dump(top_ratings))
    return top_ratings1

@main.route("/API/<int:user_id>/ratings/top/<int:count>", methods=["GET"])
def top_ratings_API(user_id, count):
    logger.debug("User %s TOP ratings requested", user_id)
    top_ratings1 = recommendation_engine.get_top_ratings(user_id,count)
    #print(json.dump(top_ratings))
    return json.dumps(top_ratings1)
 
@main.route("/<int:user_id>/ratings/<int:movie_id>", methods=["GET"])
def movie_ratings(user_id, movie_id):
    logger.debug("User %s rating requested for movie %s", user_id, movie_id)
    ratings = recommendation_engine.get_ratings_for_movie_ids(user_id, [movie_id])
    return json.dumps(ratings)
 
 
@main.route("/<int:user_id>/ratings", methods = ["POST"])
def add_ratings(user_id):
    # get the ratings from the Flask POST request object
    ratings_list = request.form.keys()[0].strip().split("\n")
    ratings_list = map(lambda x: x.split(","), ratings_list)
    # create a list with the format required by the negine (user_id, movie_id, rating)
    ratings = map(lambda x: (user_id, int(x[0]), float(x[1])), ratings_list)
    # add them to the model using then engine API
    recommendation_engine.add_ratings(ratings)
 
    return json.dumps(ratings)
 
def top_ratings1(user_id, count):
    logger.debug("User %s TOP ratings requested", user_id)
    top_ratings = recommendation_engine.get_top_ratings(user_id,count)
    #print(json.dump(top_ratings))
    print(type(top_ratings))
    return top_ratings

def movie_ratings1(user_id, movie_id):
    logger.debug("User %s rating requested for movie %s", user_id, movie_id)
    ratings = recommendation_engine.get_ratings_for_movie_ids(user_id, [movie_id])
    return json.dumps(ratings)

def convertString (ConvertSt):
    ConvertSt = ConvertSt.replace(" ","")
    ConvertSt = ConvertSt.replace('"',"")
    ConvertSt = ConvertSt.replace("]","")
    ConvertSt = ConvertSt.replace("[","")
    string = ConvertSt.split(",")
    return string[0],string[1],string[2]

@main.route("/add", methods = ["POST"])
def add():
    value_list =[]
    value = []
    value.append(int(request.form["user_id"]))
    value.append(int(request.form["movie_id"]))
    value.append(float(request.form["ratings"]))
    value_list.append(value)

    recommendation_engine.add_ratings(value_list)
    #print("type of list:", type(value_list))
    print(value_list)
    return render_template("template.html")

#test
@main.route("/", methods=["GET","POST"])
def hello():
    
    if request.method == "GET": 
        return render_template("template.html")
    else:
        iduser = int(request.form["iduser"])
        toprating = request.form["toprating"]
        idphim = request.form["idphim"]
        if (toprating != "" and idphim == ""):
            link1= top_ratings1(iduser,int(toprating))
            return render_template("template.html", contain = link1, iduser=iduser,toprating=toprating)
        elif (toprating == "" and idphim != "") :
            link2= movie_ratings1(iduser,int(idphim))
            tenphim,diemRating,count = convertString(link2)
            return render_template("template.html",iduser=iduser,idphim=idphim, tenphim= tenphim, diemRating=diemRating, count= count)
        else :
            link1= top_ratings1(iduser,int(toprating))
            link2= movie_ratings1(iduser,int(idphim))
            tenphim,diemRating,count = convertString(link2)
            return render_template("template.html",contain = link1, iduser=iduser,idphim=idphim, toprating=toprating, tenphim= tenphim, diemRating=diemRating, count= count)

def create_app(spark_context, dataset_path):
    global recommendation_engine 

    recommendation_engine = RecommendationEngine(spark_context, dataset_path)    
    
    app = Flask(__name__)
    app.register_blueprint(main)
    return app

