from flask import Flask, request, render_template, redirect, url_for
import json

app = Flask(__name__)

def load_blog():
    with open('blog_posts.json', 'r') as file:
         return json.load(file)

def save_blog(posts):
    with open('blog_posts.json', 'w') as file:
        json.dump(posts, file)

def fetch_post_by_id(post_id):
    posts = load_blog()
  #  print(posts)
    for post in posts:
        if post["id"] == post_id:
            return post
    return None


@app.route('/')
def index():
    blog_posts = load_blog()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
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
    posts = load_blog()
    posts = [post for post in posts if post["id"] != post_id]
    save_blog(posts)
    return redirect(url_for('index'))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):

    posts = load_blog()
    post = fetch_post_by_id(post_id)
    print(post)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        print(post['author'])
        post["author"] = request.form['author']
        post["title"] = request.form['title']
        post["content"] = request.form['content']
        save_blog(posts)
        return redirect(url_for('index'))

    return render_template('update.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5004, debug=True)