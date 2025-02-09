from flask import Flask, request, render_template, redirect, url_for
import json

app = Flask(__name__)

def load_blog():
    """
    this function loads the jsonfile with all the data of the blog
    """
    with open('blog_posts.json', 'r') as file:
         return json.load(file)

def save_blog(posts):
    """
    this file saves the data to the blog
    """
    with open('blog_posts.json', 'w') as file:
        json.dump(posts, file)

def fetch_post_by_id(post_id):
    """
    this function finds a certain post inside the blog by a given id
    """
    posts = load_blog()
  #  print(posts)
    for post in posts:
        if post["id"] == post_id:
            return post
    return None


@app.route('/')
def index():
    """
    this is the base route where you get by entering the http
    """
    blog_posts = load_blog()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    this route adds a new blog entry with manually given data
    and adds automatically an id to it
    """
    if request.method == 'POST':
        new_post = {
            "id": len(load_blog())+1,
            "author": request.form['author'],
            "title": request.form['title'],
            "content":request.form['content']
        }
        posts = load_blog()
        posts.append(new_post)
        save_blog(posts)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:post_id>', methods=['GET', 'POST'])
def delete(post_id):
    """
    this rout deletes a blog entry
    """
    posts = load_blog()
    posts = [post for post in posts if post["id"] != post_id]
    save_blog(posts)
    return redirect(url_for('index'))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    this route updates an existing entry.
    """
    posts = load_blog()
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404
    if request.method == 'POST':
        post['id'] = post['id']
        post["author"] = request.form.get('author', post['author'])
        post["title"] = request.form.get('title', post['title'])
        post["content"] = request.form.get('content', post['content'])
        for index, new_post in enumerate(posts):
            if new_post['id'] == post_id:
                posts[index] = post
                break
        save_blog(posts)
        return redirect(url_for('index'))
    return render_template('update.html' ,post=post)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5004, debug=True)