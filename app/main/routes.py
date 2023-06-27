from datetime import datetime
from flask import current_app, render_template, flash, g, jsonify, redirect, request, url_for
from flask_babel import _, get_locale
from flask_login import current_user, login_required, login_user, logout_user
from langdetect import detect, LangDetectException
from werkzeug.urls import url_parse

from app import db
from app.main.forms import EditProfileForm, EmptyForm, PostForm, SearchForm
from app.models import User, Post
from app.translate import translate
from app.main import bp

@bp.before_request
def before_request():
  # Updates the last seen time of the user.
  #
  # Parameters:
  #   None
  #
  # Returns:
  #   None

  if current_user.is_authenticated:
    current_user.last_seen = datetime.utcnow()
    db.session.commit()
    g.search_form = SearchForm()
  g.locale = str(get_locale())

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
  form = PostForm()

  if form.validate_on_submit():
    try:
      language = detect(form.post.data)
    except LangDetectException:
      language = ''
    post = Post(body=form.post.data, title=form.title.data, author=current_user, language=language)
    db.session.add(post)
    db.session.commit()
    flash(_('Your post is now live!'))
    return redirect(url_for('main.index'))

  page = request.args.get('page', 1, type=int)
  posts = current_user.followed_posts().paginate(
    page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
  show_pagination = posts.total > posts.per_page
  next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None
  prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None
  return render_template('index.html', form=form, posts=posts.items, title=_('Home'), show_pagination=show_pagination, next_url=next_url, prev_url=prev_url)


@bp.route('/user/<username>')
@login_required
def user(username):
  user = User.query.filter_by(username=username).first_or_404()
  page = request.args.get('page', 1, type=int)
  posts = user.posts.order_by(Post.timestamp.desc()).paginate(page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
  next_url = url_for('main.user', username=user.username, page=posts.next_num) if posts.has_next else None
  prev_url = url_for('main.user', username=user.username, page=posts.prev_num) if posts.has_prev else None

  form = EmptyForm()

  return render_template('user.html', user=user, posts=posts, next_url=next_url, prev_url=prev_url, form=form)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
  form = EditProfileForm(current_user.username)

  if form.validate_on_submit():
    current_user.username = form.username.data
    current_user.about_me = form.about_me.data
    current_user.first_name = form.first_name.data
    current_user.middle_name = form.middle_name.data
    current_user.last_name = form.last_name.data
    db.session.commit()
    flash(_('Your changes have been saved.'))
    return redirect(url_for('main.edit_profile'))
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.about_me.data = current_user.about_me
    form.first_name.data = current_user.first_name
    form.middle_name.data = current_user.middle_name
    form.last_name.data = current_user.last_name
  return render_template('edit_profile.html', title=_('Edit Profile'), form=form)

@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
  # Follows a user.
  #
  # Parameters:
  #   username (str): The username of the user to follow.
  #
  # Returns:
  #   str: The user page.

  form = EmptyForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=username).first()
    if user is None:
      flash(_('User %(username)s not found.', username=username))
      return redirect(url_for('main.index'))
    if user == current_user:
      flash(_('You cannot follow yourself!'))
      return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are now following %(username)s!', username=username))
    return redirect(url_for('main.user', username=username))
  else:
    return redirect(url_for('main.index'))

@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
  # Unfollows a user.
  #
  # Parameters:
  #   username (str): The username of the user to unfollow.
  #
  # Returns:
  #   str: The user page.

  form = EmptyForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=username).first()
    if user is None:
      flash(_('User %(username)s not found.', username=username))
      return redirect(url_for('main.index'))
    if user == current_user:
      flash(_('You cannot unfollow yourself!'))
      return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are no longer following %(username)s.', username=username))
    return redirect(url_for('main.user', username=username))
  else:
    return redirect(url_for('main.index'))

@bp.route('/explore')
@login_required
def explore():
  # Returns the explore page.
  #
  # Parameters:
  #   None
  #
  # Returns:
  #   str: The explore page.

  page = request.args.get('page', 1, type=int)
  posts = Post.query.order_by(Post.timestamp.desc()).paginate(
    page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False
  )
  show_pagination = posts.total > posts.per_page
  next_url = url_for('main.explore', page=posts.next_num) if posts.has_next else None
  prev_url = url_for('main.explore', page=posts.prev_num) if posts.has_prev else None

  return render_template('index.html', title=_('Explore'), posts=posts.items, show_pagination=show_pagination, next_url=next_url, prev_url=prev_url)

@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
  # Translates text.
  #
  # Parameters:
  #   None
  #
  # Returns:
  #   str: The translated text.
  # translated_text = {'text': translate(request.form['text'], request.form['source_language'], request.form['dest_language'])}
  return jsonify(
    {
      'text': translate(request.json.get('text', False), request.json.get('source_language', False), request.json.get('dest_language', False))
    }
  )

@bp.route('/search')
@login_required
def search():
  # Searches for posts.
  #
  # Parameters:
  #   None
  #
  # Returns:
  #   str: The search page.

  if not g.search_form.validate():
    return redirect(url_for('main.explore'))
  page = request.args.get('page', 1, type=int)
  posts, total = Post.search(g.search_form.q.data, page, current_app.config['POSTS_PER_PAGE'])
  next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
    if total > page * current_app.config['POSTS_PER_PAGE'] else None
  prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
    if page > 1 else None
  return render_template('search.html', title=_('Search'), posts=posts, next_url=next_url, prev_url=prev_url)