from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user, login_fresh, confirm_login

from albumy.emails import send_confirm_email, send_reset_password_email
from albumy.extensions import db
from albumy.forms.auth import LoginForm, RegisterForm, ForgetPasswordForm, ResetPasswordForm
from albumy.models import User
from albumy.settings import Operations
from albumy.utils import generate_token, validate_token, redirect_back

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data.lower()).first()
		if user is not None and user.validate_password(form.password.data):
			if login_user(user, form.remember_me.data):
				flash('Login success', 'info')
				return redirect_back()
			else:
				flash('Your account is blocked', 'warning')
				return redirect(url_for('main.index'))
		flash('Invalid email or password', 'warning')
	return render_template('auth/login.html', form=form)

@auth_bp.route('/re-authenticate', methods=['GET', 'POST'])
@login_required
def re_authenticate():
	if login_fresh():
		return redirect(url_for('main.index'))

	form = LoginForm()
	if form.validate_on_submit() and current_user.validate_password(form.password.data):
		confirm_login()
		return redirect_back()
	return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
	logout_user()
	flash('Logout success', 'info')
	return redirect(url_for('main.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = RegisterForm()
	if form.validate_on_submit():
		user = User(name=form.name.data, email=form.email.data, username=form.username.data, role_id = 4, confirmed=True)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		token = generate_token(user=user, operation='confirm')
		send_confirm_email(user=user, token=token)
		flash('注册成功，请登录', 'info')
		return redirect(url_for('.login'))
	return render_template('auth/register.html', form=form)

@auth_bp.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if validate_token(user=curren_user, token=token, operation=Operations.CONFIRM):
		flash('Account confirmed', 'success')
		return redirect(url_for('main.index'))
	else:
		flash('Invalide or expired toekn', 'danger')
		return redirect(url_for('.resend_confirm_email'))

@auth_bp.route('/resend-confirm-email')
@login_required
def resend_confirm_email():
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	token = generate_token(user=current_user, operation=Operations.CONFIRM)
	send_confirm_email(user=current_user, token=token)
	flash('New email sent', 'info')
	return redirect(url_for('main.index'))

@auth_bp.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = ForgetPasswordForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			token = generate_token(user=user, operation=Operations.RESET_PASSWORD)
			send_reset_password_email(user=user, token=token)
			flash('Password reset email sent, check your inbox.', 'info')
			return redirect(url_for('.login'))
		flash('Invalid email', 'warning')
		return redirect(url_for('.forget_password'))
	return render_template('auth/reset_password.html', form=form)

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data.lower()).first()
		if user is None:
			return redirect(url_for('main.index'))
		if validate_token(user=user, token=token, operation=Operations.RESET_PASSWORD, new_password=form.password.data):
			flash('Password updated.', 'success')
			return redirect(url_for('.login'))
		else:
			flash('Invalid or expired link.', 'danger')
			return redirect(url_for('.forget_password'))
	return render_template('auth/reset_password.html', form=form)
