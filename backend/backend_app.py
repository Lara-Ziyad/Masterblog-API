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


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    # Search for the post with the given id
    post_to_delete = next((post for post in POSTS if post['id'] == id), None)

    if post_to_delete is None:
        return jsonify({"error": f"Post with id {id} not found."}), 404

    # Remove the post from the list
    POSTS.remove(post_to_delete)

    return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    # Search for the post with the given id
    post_to_update = next((post for post in POSTS if post['id'] == id), None)

    if post_to_update is None:
        return jsonify({"error": f"Post with id {id} not found."}), 404

    # Get new data from the request body
    data = request.get_json()

    # Update the post fields if provided
    new_title = data.get('title')
    new_content = data.get('content')

    if new_title is not None:
        post_to_update['title'] = new_title

    if new_content is not None:
        post_to_update['content'] = new_content

    # Return the updated post
    return jsonify(post_to_update), 200

@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    # Get query parameters from the URL
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()

    # Filter posts that match the search criteria
    matching_posts = [
        post for post in POSTS
        if (title_query in post['title'].lower() or not title_query)
        and (content_query in post['content'].lower() or not content_query)
    ]

    # Return the matching posts
    return jsonify(matching_posts), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
