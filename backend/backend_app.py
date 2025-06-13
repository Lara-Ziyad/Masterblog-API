from flask import Flask, jsonify, request

from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)

# New endpoint: Add a post
@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()

    # Check for missing fields
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        missing_fields = []
        if not title:
            missing_fields.append('title')
        if not content:
            missing_fields.append('content')
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    # Generate new unique ID
    new_id = max(post['id'] for post in POSTS) + 1 if POSTS else 1

    # Create new post
    new_post = {
        "id": new_id,
        "title": title,
        "content": content
    }

    # Add to list
    POSTS.append(new_post)

    # Return the new post with status 201
    return jsonify(new_post), 201



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
