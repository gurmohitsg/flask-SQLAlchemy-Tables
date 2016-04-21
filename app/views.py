from flask import  request, flash, url_for, redirect, render_template
from sqlalchemy import or_
from app import app, db
from .models import User, UserEmails

@app.route('/')
@app.route('/show')
def show_all():
	reachable_at = {}
	sort_by = request.args.get('SortBy')
	sort_by = request.args.get('SortBy')
	if sort_by:
		global users
		if sort_by == 'id':
			users = User.query.order_by(User.id)
		elif sort_by == 'name':
			users = User.query.order_by(User.display_name)
		elif sort_by == 's_id':
			users = User.query.order_by(User.signing_identity)
		elif sort_by == 'key':
			users = User.query.order_by(User.signing_key)
		elif sort_by == 'stat':
			users = User.query.order_by(User.status)
	elif request.args.get('filterById') or request.args.get('filterByName') or request.args.get('filterBySign') or request.args.get('filterByStatus'):
		global users
		print("yeee")
		users = User.query.filter(or_(User.display_name==request.args.get('filterByName'),
		User.id==request.args.get('filterById'),
		User.signing_identity==request.args.get('filterBySign'),
		User.status==request.args.get('filterByStatus')))
	else:
		users = User.query.all()
	for u in users:
		emails = u.reachable_at.all();
		email_list=[] 
		for e in emails:
			email_list.append(e.emails)
		reachable_at.update({u.id:email_list})
		print(reachable_at)
	return render_template('show_all.html', users = users, reachable_at = reachable_at , row=0)


@app.route('/add', methods = ['GET', 'POST'])
def new():
	if request.method == 'POST':
		if not request.form['name'] or not request.form['sign_id']:
			flash("Please Enter the details")
			return redirect(url_for('new'))
		elif not request.form['emails[]']: 
			flash("Please enter atleast one other email")
		else:
			u = User(display_name=request.form['name'], signing_identity=request.form['sign_id'])
			db.session.add(u)
			print("Data Added")
			emails = request.form.getlist('emails[]')
			p = UserEmails(emails=request.form['sign_id'],contact=u)
			db.session.add(u)
			for e in emails:
				if e:
					p = UserEmails(emails=e,contact=u)
					db.session.add(u)
			db.session.commit()
			flash('User added successfully')
	return render_template('add.html')
