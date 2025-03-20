import os
from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'
# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'  # Redirect to login page if not authenticated

# Dummy User Database
users = {'admin': {'password': '1234'}}

# Configure upload folder
UPLOAD_FOLDER = "static/uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Connect to MySQL Database
db = pymysql.connect(
    host='localhost',       
    user='root',            
    password='1234',        
    database='formsdb'      
)
def fetch_data(table_name):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    cursor.close()
    return data

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    return User(user_id) if user_id in users else None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('admin'))
    return render_template('admin_login.html')

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@app.route('/student_registration')
def student_registration():
    headers = ["ID","Full Name", "Email", "Phone Number", "Date of Birth", "Address", "Course", "College Name"]
    data = fetch_data('student_registration')  # Ensure `fetch_data` is implemented correctly
    return render_template('student_registration.html', form={"headers": headers, "data": data})

@app.route('/event_registration')
def event_registration():
    headers = ["ID","Full Name", "Email", "Phone Number", "Event Name", "Ticket Type", "Payment Status"]
    data = fetch_data('event_registration')
    return render_template('event_registration.html', form={"headers":headers,"data":data})

@app.route('/employee_registration')
def employee_registration():
    headers = ["ID", "Full Name", "Email", "Phone Number", "Employee ID", "Department", "Joining Date"]
    data = fetch_data('employee_registration')
    return render_template('employee_registration.html', form={"headers":headers,"data":data})

@app.route('/workshop_registration')
def workshop_registration():
    headers = ["ID", "Full Name", "Email", "Phone Number", "Workshop Name", "Preferred Date", "Payment Status"]
    data = fetch_data('workshop_registration')
    return render_template('workshop_registration.html', form={"headers":headers,"data":data})

@app.route('/general_contact')
def general_contact():
    headers = ["ID", "Full Name", "Email", "Phone Number", "Message"]
    data = fetch_data('general_contact')
    return render_template('general_contact.html', form={"headers":headers,"data":data})

@app.route('/support_ticket')
def support_ticket():
    headers = ["ID", "Full Name", "Email", "Phone Number", "Issue Category", "Description", "Priority"]
    data = fetch_data('support_ticket')
    return render_template('support_ticket.html', form={"headers":headers,"data":data})

@app.route('/customer_inquiry')
def customer_inquiry():
    headers = ["ID", "Full Name", "Email", "Phone Number", "Product/Service", "Message"]
    data = fetch_data('customer_inquiry')
    return render_template('customer_inquiry.html', form={"headers":headers,"data":data})

@app.route('/online_order')
def online_order():
    headers = ["ID", "Full Name", "Email", "Phone Number", "Shipping Address", "Product Name", "Quantity", "Payment Method"]
    data = fetch_data('online_order')
    return render_template('online_order.html', form={"headers":headers,"data":data})

@app.route('/product_checkout')
def product_checkout():
    headers = ["ID", "Full Name", "Email", "Billing Address", "Shipping Address", "Product Details", "Payment Details"]
    data = fetch_data('product_checkout')
    return render_template('product_checkout.html',form={"headers":headers,"data":data})

@app.route('/subscribers')
def subscribers():
    headers = ["Id", "Full Name", "Email", "Subscription Plan","Created At"]
    data = fetch_data('subscribers')
    return render_template('subscription_payment.html', form={"headers":headers,"data":data})

@app.route('/customer_feedback')
def customer_feedback():
    headers = ["ID", "Full Name", "Email", "Phone Number", "Product/Service", "Rating", "Comments"]
    data = fetch_data('customer_feedback')
    return render_template('customer_feedback.html', form={"headers":headers,"data":data})

@app.route('/employee_satisfaction')
def employee_satisfaction():
    headers = ["ID", "Full Name", "Email", "Department", "Job Role", "Satisfaction Rating", "Feedback"]
    data = fetch_data('employee_satisfaction')
    return render_template('employee_satisfaction.html', form={"headers":headers,"data":data})

@app.route('/market_research')
def market_research():
    headers = ["ID", "Full Name", "Email", "Age Group", "Gender", "Preferences", "Feedback"]
    data = fetch_data('market_research')
    return render_template('market_research.html', form={"headers":headers,"data":data})

@app.route('/job_application')
def job_application():
    headers = ["ID", "Full Name", "Email", "Phone Number", "Resume Upload", "Job Position", "Experience", "Cover Letter"]
    data = fetch_data('job_application')
    return render_template('job_application.html', form={"headers":headers,"data":data})

@app.route('/loan_application')
def loan_application():
    headers = ["ID", "Full Name", "Email", "Phone Number", "Loan Amount", "Employment Status"]
    data = fetch_data('loan_application')
    return render_template('loan_application.html', form={"headers":headers,"data":data})

@app.route('/scholarship_application')
def scholarship_application():
    headers = ["ID", "Full Name", "Email", "Phone Number", "Course Name", "University Name", "Academic Achievements", "Personal Statement"]
    data = fetch_data('scholarship_application')
    return render_template('scholarship_application.html', form={"headers":headers,"data":data})


@app.route('/student_registration_form', methods=['GET', 'POST'])
def student_registration_form():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        dob = request.form['dob']
        address = request.form['address']
        course = request.form['course']
        college = request.form['college']

        try:
            cursor = db.cursor()
            sql = "INSERT INTO student_registration (full_name, email, phone_number, date_of_birth, address, course, college_name) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (fullname, email, phone, dob, address, course, college))
            db.commit()
            cursor.close()
            flash("Student registered successfully!", "success")
            return redirect(url_for('student_registration_form'))
        except Exception as e:
            db.rollback()
            flash(f"Error: {str(e)}", "danger")

    return render_template('studentform.html')

@app.route('/event_registration_form', methods=['GET', 'POST'])
def event_registration_form():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        event = request.form['event']
        ticket = request.form['ticket']
        payment = request.form['payment']

        try:
            cursor = db.cursor()
            sql = """INSERT INTO event_registration 
                     (full_name, email, phone_number, event_name, ticket_type, payment_status) 
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (fullname, email, phone, event, ticket, payment))
            db.commit()
            cursor.close()
            flash("Registration successful!", "success")
            return redirect(url_for('event_registration_form'))
        except Exception as e:
            db.rollback()
            flash(f"Error: {str(e)}", "danger")

    return render_template('eventform.html')

@app.route('/employee_registration_form', methods=['GET', 'POST'])
def employee_registration_form():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        employee_id = request.form['employee_id']
        department = request.form['department']
        joining_date = request.form['joining_date']

        try:
            cursor = db.cursor()
            query = "INSERT INTO employee_registration (full_name, email, phone_number, employee_id, department, joining_date) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (fullname, email, phone, employee_id, department, joining_date))
            db.commit()
            flash('Employee Registered Successfully!', 'success')
            return redirect(url_for('employee_registration_form'))
        except Exception as e:
            db.rollback()
            flash(f'Error: {str(e)}', 'danger')

    return render_template('employeeform.html')

@app.route('/workshop_registration_form', methods=['GET', 'POST'])
def workshop_registration_form():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        workshop_name = request.form['workshop_name']
        preferred_date = request.form['preferred_date']
        payment_status = request.form['payment_status']

        try:
            cursor = db.cursor()
            query = """
                INSERT INTO workshop_registration
                (full_name, email, phone_number, workshop_name, preferred_date, payment_status) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (fullname, email, phone, workshop_name, preferred_date, payment_status))
            db.commit()
            flash('Workshop Registered Successfully!', 'success')
            return redirect(url_for('workshop_registration_form'))
        except Exception as e:
            db.rollback()
            flash(f'Error: {str(e)}', 'danger')

    return render_template('workshopform.html')

@app.route('/contact_form', methods=['GET', 'POST'])
def contact_form():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        try:
            cursor = db.cursor()
            query = """
                INSERT INTO general_contact
                (full_name, email, phone_number, message) 
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (fullname, email, phone, message))
            db.commit()
            flash('Contact Registered Successfully!', 'success')
            return redirect(url_for('contact_form'))
        except Exception as e:
            db.rollback()
            flash(f'Error: {str(e)}', 'danger')

    return render_template('generalcontact.html')

@app.route('/support_ticket_form', methods=['GET', 'POST'])
def support_ticket_form():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        issue = request.form['category']
        description = request.form['description']
        priority = request.form['priority']

        try:
            cursor = db.cursor()
            query = """
                INSERT INTO support_ticket
                (full_name, email, phone_number, issue_category, description, priority) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (fullname, email, phone, issue, description, priority))
            db.commit()
            flash('Support Ticket Given Successfully!', 'success')
            return redirect(url_for('support_ticket_form'))
        except Exception as e:
            db.rollback()
            flash(f'Error: {str(e)}', 'danger')

    return render_template('supportform.html')

@app.route('/submit_inquiry', methods=['GET','POST'])
def submit_inquiry():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        product_service = request.form['product_service']
        message = request.form['message']

        try:
            cursor = db.cursor()
            sql = """INSERT INTO customer_inquiry (full_name, email, phone_number, product_service, message) 
                     VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (fullname, email, phone, product_service, message))
            db.commit()
            flash('Your inquiry has been submitted successfully!', 'success')
            return redirect(url_for('submit_inquiry'))

        except Exception as e:
            db.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()

    return render_template('customerEnquiryform.html')

@app.route('/submit_order', methods=['GET','POST'])
def submit_order():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        product = request.form['product']
        quantity = request.form['quantity']
        payment_method = request.form['payment_method']

        try:
            cursor = db.cursor()
            sql = """INSERT INTO online_order (full_name, email, phone_number, shipping_address, product_name, quantity, payment_method) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (fullname, email, phone, address, product, quantity, payment_method))
            db.commit()
            flash('Your order has been placed successfully!', 'success')
            return redirect(url_for('submit_order'))

        except Exception as e:
            db.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()

    return render_template('onlineorderform.html')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        fullname = request.form['full_name']
        email = request.form['email']
        billing_address = request.form['billing_address']
        shipping_address = request.form['shipping_address']
        product_details = request.form['product_details']
        payment_details = request.form['payment_details']

        try:
            cursor = db.cursor()
            sql = """INSERT INTO product_checkout (full_name, email, billing_address , shipping_address, product_details, payment_details) 
                        VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (fullname, email, billing_address, shipping_address, product_details, payment_details))
            db.commit()
            flash('Your product will be delivered successfully!', 'success')
            return redirect(url_for('checkout'))

        except Exception as e:
            db.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()

    return render_template('productcheckoutform.html')


@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        subscription_plan = request.form['subscription_plan']

        try:
            cursor = db.cursor()
            sql = "INSERT INTO subscribers (full_name, email, subscription_plan) VALUES (%s, %s, %s)"
            cursor.execute(sql, (full_name, email, subscription_plan))
            db.commit()
            flash('Your product will be delivered successfully!', 'success')
            return redirect(url_for('subscribe'))

        except Exception as e:
            db.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()

    return render_template('subscriptionpayment.html')


@app.route("/submit_feedback", methods=['GET',"POST"])
def submit_feedback():
    if request.method == "POST":
        full_name = request.form["full_name"]
        email = request.form["email"]
        phone_number = request.form["phone_number"]
        product_service = request.form["product_service"]
        rating = request.form["rating"]
        comments = request.form["comments"]

        sql = """INSERT INTO customer_feedback (full_name, email, phone_number, product_service, rating, comments) 
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (full_name, email, phone_number, product_service, rating, comments)

        try:
            cursor = db.cursor()
            cursor.execute(sql, values)
            db.commit()
            flash('Thankyou for your feedback!', 'success')
            return redirect(url_for('submit_feedback'))

        except Exception as e:
            db.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()

    return render_template('feedback.html')

@app.route("/submit_survey", methods=['GET',"POST"])
def submit_survey():
    if request.method == "POST":
        full_name = request.form["full_name"]
        email = request.form["email"]
        department = request.form["department"]
        job_role = request.form["job_role"]
        satisfaction_rating = request.form["satisfaction_rating"]
        feedback = request.form["feedback"]

        sql = """INSERT INTO employee_satisfaction (full_name, email, department, job_role, satisfaction_rating, feedback) 
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (full_name, email, department, job_role, satisfaction_rating, feedback)

        try:
            cursor = db.cursor()
            cursor.execute(sql, values)
            db.commit()
            flash('Thankyou for your feedback!', 'success')
            return redirect(url_for("submit_survey"))

        except Exception as e:
            db.rollback()
            print("Error:", e)

    return render_template('employeesatisfaction.html')


@app.route("/submit_research", methods=['GET',"POST"])
def submit_research():
    if request.method == "POST":
        full_name = request.form["full_name"]
        email = request.form["email"]
        age_group = request.form["age_group"]
        gender = request.form["gender"]
        preferences = request.form["preferences"]
        feedback = request.form["feedback"]

        sql = """INSERT INTO market_research (full_name, email, age_group, gender, preferences, feedback) 
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (full_name, email, age_group, gender, preferences, feedback)

        try:
            cursor = db.cursor()
            cursor.execute(sql, values)
            db.commit()
            flash('Thankyou for your feedback!', 'success')
            return redirect(url_for('submit_research'))

        except Exception as e:
            db.rollback()
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()

    return render_template('marketresearch.html')

@app.route("/job_application_form", methods=['GET',"POST"])
def job_application_form():
    if request.method == "POST":
        full_name = request.form["full_name"]
        email = request.form["email"]
        phone_number = request.form["phone_number"]
        job_position = request.form["job_position"]
        experience = request.form["experience"]
        cover_letter = request.form["cover_letter"]

        # Handle file upload
        resume_file = request.files["resume_upload"]
        if resume_file:
            UPLOAD_FOLDER = "static/uploads"
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            filename = secure_filename(resume_file.filename)
            resume_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            resume_file.save(resume_path)

            sql = """INSERT INTO job_application 
                     (full_name, email, phone_number, resume_upload, job_position, experience, cover_letter) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            values = (full_name, email, phone_number, filename, job_position, experience, cover_letter)

            try:
                cursor = db.cursor()
                cursor.execute(sql, values)
                db.commit()
                flash('Your Application has been submitted', 'success')
                return redirect(url_for('job_application_form'))

            except Exception as e:
                db.rollback()
                flash(f'Error: {str(e)}', 'danger')
            finally:
                cursor.close()

    return render_template('jobapplication.html')


@app.route("/loan_application_form", methods=["GET", "POST"])
def loan_application_form():
    if request.method == "POST":
        full_name = request.form["full_name"]
        email = request.form["email"]
        phone_number = request.form["phone_number"]
        loan_amount = request.form["loan_amount"]
        employment_status = request.form["employment_status"]

        sql = """INSERT INTO loan_application 
                 (full_name, email, phone_number, loan_amount, employment_status) 
                 VALUES (%s, %s, %s, %s, %s)"""
        values = (full_name, email, phone_number, loan_amount, employment_status)

        try:
            cursor = db.cursor()
            cursor.execute(sql, values)
            db.commit()
            flash("Your Loan Application has been submitted", "success")
            return redirect(url_for("loan_application_form"))
        except Exception as e:
            db.rollback()
            flash(f"Error: {str(e)}", "danger")
        finally:
            cursor.close()

    return render_template("loanapplication.html")

@app.route("/scholarship_application_form", methods=["GET", "POST"])
def scholarship_application_form():
    if request.method == "POST":
        full_name = request.form["full_name"]
        email = request.form["email"]
        phone_number = request.form["phone_number"]
        course_name = request.form["course_name"]
        university_name = request.form["university_name"]
        academic_achievements = request.form["academic_achievements"]
        personal_statement = request.form["personal_statement"]

        sql = """INSERT INTO scholarship_application 
                 (full_name, email, phone_number, course_name, university_name, academic_achievements, personal_statement) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        values = (full_name, email, phone_number, course_name, university_name, academic_achievements, personal_statement)

        try:
            cursor = db.cursor()
            cursor.execute(sql, values)
            db.commit()
            flash("Your Scholarship Application has been submitted", "success")
            return redirect(url_for("scholarship_application_form"))
        except Exception as e:
            db.rollback()
            flash(f"Error: {str(e)}", "danger")
        finally:
            cursor.close()

    return render_template("scolarshipapplication.html")

if __name__ == '__main__':
    app.run(debug=True)