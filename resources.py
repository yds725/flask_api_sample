from flask_restful import Resource, fields, reqparse, marshal_with, abort
from flask import request
from models import db, Movie, User

movie_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'year': fields.String,
    'rating': fields.String,
    'released': fields.String,
    'runtime': fields.String,
    'genre': fields.String,
    'director': fields.String,
    'writer': fields.String,
    'actors': fields.String,
    'plot': fields.String,
    'language': fields.String,
    'country': fields.String,
    'awards': fields.String,
    'poster': fields.String,
    'metascore': fields.String,
    'imdbRating': fields.Float,
    'uri': fields.Url('movie', absolute=True)

}

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('title', type=str, required=True, location='json')
parser.add_argument('year', type=str, required=True, location='json')
parser.add_argument('rating', type=str, location='json')
parser.add_argument('released', type=str, location='json')
parser.add_argument('runtime', type=str, location='json')
parser.add_argument('genre', type=str, location='json')
parser.add_argument('director', type=str, location='json')
parser.add_argument('writer', type=str, location='json')
parser.add_argument('actors', type=str, location='json')
parser.add_argument('plot', type=str, location='json')
parser.add_argument('language', type=str, location='json')
parser.add_argument('country', type=str, location='json')
parser.add_argument('awards', type=str, location='json')
parser.add_argument('poster', type=str, location='json')
parser.add_argument('metascore', type=str, location='json')
parser.add_argument('imdbRating', type=float, location='json')


class MovieResource(Resource):
    @marshal_with(movie_fields)
    def get(self, id):
        movie = Movie.query.get(id)

        if not movie:
            abort(404, message="Movie {} doesn't exist".format(id))

        return movie

    def delete(self, id):
        movie = Movie.query.get(id)
        if not movie:
            abort(404, message="Todo {} doesn't exist".format(id))
        db.session.delete(todo)
        db.session.commit()
        return {}, 204

    @marshal_with(movie_fields)
    def put(self, id):
        parsed_args = parser.parse_args()
        movie = Movie.query.get(id)
        
        if not movie:
            abort(404, message="Todo {} doesn't exist".format(id))
        
        movie.title = parsed_args['title']
        movie.year = parsed_args['year']
        movie.rating = parsed_args['rating']
        movie.released = parsed_args['released']
        movie.runtime = parsed_args['runtime']
        movie.genre = parsed_args['genre']
        movie.director = parsed_args['director']
        movie.writer = parsed_args['writer']
        movie.actors = parsed_args['actors']
        movie.plot = parsed_args['plot']
        movie.language = parsed_args['language']
        movie.country = parsed_args['country']
        movie.awards = parsed_args['awards']
        movie.poster = parsed_args['poster']
        movie.metascore = parsed_args['metascore']
        movie.imdbRating = parsed_args['imdbRating']
        
        db.session.add(movie)
        db.session.commit()
        
        return movie, 201


class MovieListResource(Resource):
    @marshal_with(movie_fields)
    def get(self):
        query_parser = reqparse.RequestParser()
        query_parser.add_argument('limit', type=int)
        query_parser.add_argument('offset', type=int)
        query_parser.add_argument('filter', type=str)

        query_args = query_parser.parse_args()

        limit = None
        offset = None
        q_filter = None

        if query_args['limit']:
            limit = query_args['limit']
        if query_args['offset']:
            offset = query_args['offset']
        if query_args['filter']:
            q_filter = query_args['filter']

        movies = Movie.query

        if q_filter:
            movies = movies.filter(
                Movie.title.like(q_filter) |
                Movie.year.like(q_filter) |
                Movie.rating.like(q_filter) |
                Movie.runtime.like(q_filter) |
                Movie.genre.like(q_filter) |
                Movie.director.like(q_filter) |
                Movie.writer.like(q_filter) |
                Movie.actors.like(q_filter) |
                Movie.plot.like(q_filter) |
                Movie.language.like(q_filter) |
                Movie.country.like(q_filter) |
                Movie.awards.like(q_filter)
            )
        if limit or offset:
            movies = movies.offset(offset).limit(limit)

        
        return movies.all()

    @marshal_with(movie_fields)
    def post(self):
        parsed_args = parser.parse_args()
        # parsed_args = request.get_json()
        print("POST")
        movie = Movie(
            title=parsed_args['title'],
            year=parsed_args['year'],
            rating=parsed_args['rating'],
            released=parsed_args['released'],
            runtime=parsed_args['runtime'],
            genre=parsed_args['genre'],
            director=parsed_args['director'],
            writer=parsed_args['writer'],
            actors=parsed_args['actors'],
            plot=parsed_args['plot'],
            language=parsed_args['language'],
            country=parsed_args['country'],
            awards=parsed_args['awards'],
            poster=parsed_args['poster'],
            metascore=parsed_args['metascore'],
            imdbRating=parsed_args['imdbRating']
        )

        db.session.add(movie)
        db.session.commit()
        return movie, 201
