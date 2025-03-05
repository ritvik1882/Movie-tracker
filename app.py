from flask import Flask, jsonify, request, send_from_directory
import sqlite3

app = Flask(__name__)

# Database initialization on startup
def init_db():
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS watchlist
                 (user_id TEXT, movie_id INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS watched
                 (user_id TEXT, movie_id INTEGER)''')
    conn.commit()
    conn.close()

init_db()

# Serve static files
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# API endpoints
@app.route('/api/watchlist', methods=['GET', 'POST', 'DELETE'])
def handle_watchlist():
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    
    if request.method == 'GET':
        # For demo, using fixed user_id '1'
        c.execute('SELECT movie_id FROM watchlist WHERE user_id = ?', ('1',))
        movies = [row[0] for row in c.fetchall()]
        conn.close()
        return jsonify(movies)
        
    elif request.method == 'POST':
        data = request.json
        movie_id = data.get('movie_id')
        c.execute('INSERT INTO watchlist (user_id, movie_id) VALUES (?, ?)', ('1', movie_id))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})
        
    elif request.method == 'DELETE':
        movie_id = request.args.get('movie_id')
        c.execute('DELETE FROM watchlist WHERE user_id = ? AND movie_id = ?', ('1', movie_id))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})

@app.route('/api/watched', methods=['GET', 'POST', 'DELETE'])
def handle_watched():
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    
    if request.method == 'GET':
        c.execute('SELECT movie_id FROM watched WHERE user_id = ?', ('1',))
        movies = [row[0] for row in c.fetchall()]
        conn.close()
        return jsonify(movies)
        
    elif request.method == 'POST':
        data = request.json
        movie_id = data.get('movie_id')
        # Remove from watchlist if present
        c.execute('DELETE FROM watchlist WHERE user_id = ? AND movie_id = ?', ('1', movie_id))
        # Add to watched
        c.execute('INSERT INTO watched (user_id, movie_id) VALUES (?, ?)', ('1', movie_id))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})
        
    elif request.method == 'DELETE':
        movie_id = request.args.get('movie_id')
        c.execute('DELETE FROM watched WHERE user_id = ? AND movie_id = ?', ('1', movie_id))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
