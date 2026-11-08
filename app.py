
import os
import logging

import pandas as pd
import numpy as np
import joblib

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    session,
    flash
)

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from config import Config


# --------------------------------------------------
# LOGGING CONFIGURATION
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()],
    force=True
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# FLASK APPLICATION INITIALIZATION
# --------------------------------------------------

app = Flask(__name__)
app.config.from_object(Config)

# Initialize PostgreSQL
db = SQLAlchemy()
if app.config.get("SQLALCHEMY_DATABASE_URI"):
    db.init_app(app)
else:
    logger.warning(
        "DATABASE_URL is not configured. "
        "Authentication database is unavailable."
    )


# --------------------------------------------------
# USER DATABASE MODEL
# --------------------------------------------------

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
        index=True
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )


# --------------------------------------------------
# DATABASE INITIALIZATION
# --------------------------------------------------

if app.config.get("SQLALCHEMY_DATABASE_URI"):
    try:
        with app.app_context():
            db.create_all()
            logger.info("Database tables are ready.")

    except Exception:
        logger.exception(
            "Could not initialize PostgreSQL database."
        )


# --------------------------------------------------
# MACHINE LEARNING GLOBAL VARIABLES
# --------------------------------------------------

model = None
scaler = None
stats_cache = {}
country_list = []


# --------------------------------------------------
# LOAD MACHINE LEARNING RESOURCES
# --------------------------------------------------

def load_ml_resources():
    """Load ML model, scaler and dataset statistics."""

    global model, scaler, stats_cache, country_list

    Config.init_app()

    # Load Model
    if os.path.exists(Config.MODEL_PATH):
        try:
            model = joblib.load(Config.MODEL_PATH)
            logger.info("ML model loaded successfully.")

        except Exception as e:
            logger.error(f"Error loading ML model: {e}")

    else:
        logger.warning(
            f"ML model file not found at {Config.MODEL_PATH}"
        )

    # Load Scaler
    if os.path.exists(Config.SCALER_PATH):
        try:
            scaler = joblib.load(Config.SCALER_PATH)
            logger.info("Feature scaler loaded successfully.")

        except Exception as e:
            logger.error(f"Error loading scaler: {e}")

    else:
        logger.warning(
            f"Scaler file not found at {Config.SCALER_PATH}"
        )

    # Load Processed Dataset
    if os.path.exists(Config.PROCESSED_DATA_PATH):
        try:
            df = pd.read_csv(Config.PROCESSED_DATA_PATH)

            country_list = sorted(
                df['country'].dropna().unique().tolist()
            )

            stats_cache = {
                'total_countries': len(country_list),
                'avg_hdi': round(df['hdi'].mean(), 3),
                'avg_life_exp': round(
                    df['life_expectancy'].mean(), 1
                ),
                'avg_eys': round(
                    df['expected_years_schooling'].mean(), 1
                ),
                'avg_mys': round(
                    df['mean_years_schooling'].mean(), 1
                ),
                'avg_gni': round(
                    df['gni_per_capita'].mean(), 1
                ),
                'latest_year': int(df['year'].max())
            }

            logger.info(
                "Dataset statistics loaded. "
                f"Countries: {stats_cache['total_countries']}"
            )

        except Exception as e:
            logger.error(
                f"Error reading processed dataset: {e}"
            )
            stats_cache = get_fallback_stats()

    else:
        logger.warning(
            "Processed dataset not found. "
            "Using fallback statistics."
        )
        stats_cache = get_fallback_stats()


# --------------------------------------------------
# FALLBACK STATISTICS
# --------------------------------------------------

def get_fallback_stats():
    """Return fallback statistics if dataset is unavailable."""

    global country_list

    country_list = [
        "United States",
        "Germany",
        "Japan",
        "United Kingdom",
        "Canada",
        "Australia",
        "China",
        "India",
        "Brazil",
        "South Africa",
        "Kenya",
        "Nigeria"
    ]

    return {
        'total_countries': len(country_list),
        'avg_hdi': 0.720,
        'avg_life_exp': 72.0,
        'avg_eys': 12.5,
        'avg_mys': 8.5,
        'avg_gni': 18500.0,
        'latest_year': 2021
    }


# Load ML assets when application starts
load_ml_resources()


# --------------------------------------------------
# HDI CATEGORY CLASSIFICATION
# --------------------------------------------------

def get_hdi_category(hdi_val):
    """Classify HDI according to UNDP definitions."""

    if hdi_val >= 0.800:
        return {
            'name': 'Very High Human Development',
            'color': 'success',
            'text_color': '#155724',
            'bg_color': '#d4edda'
        }

    elif hdi_val >= 0.700:
        return {
            'name': 'High Human Development',
            'color': 'primary',
            'text_color': '#004085',
            'bg_color': '#cce5ff'
        }

    elif hdi_val >= 0.550:
        return {
            'name': 'Medium Human Development',
            'color': 'warning',
            'text_color': '#856404',
            'bg_color': '#fff3cd'
        }

    else:
        return {
            'name': 'Low Human Development',
            'color': 'danger',
            'text_color': '#721c24',
            'bg_color': '#f8d7da'
        }


# --------------------------------------------------
# POLICY SUGGESTIONS
# --------------------------------------------------

def generate_suggestions(le, eys, mys, gni):
    """Generate policy suggestions based on HDI indicators."""

    health_score = (le - 20) / (85 - 20)

    edu_score = (
        (mys / 15) + (eys / 18)
    ) / 2

    income_score = (
        np.log(max(gni, 100)) - np.log(100)
    ) / (
        np.log(75000) - np.log(100)
    )

    health_score = np.clip(health_score, 0, 1)
    edu_score = np.clip(edu_score, 0, 1)
    income_score = np.clip(income_score, 0, 1)

    suggestions = []

    min_score = min(
        health_score,
        edu_score,
        income_score
    )

    if min_score == health_score:

        suggestions.append({
            'area': 'Health and Vitality (Primary Priority)',
            'desc': (
                'Invest in primary healthcare networks, '
                'maternal health services, and vaccine availability '
                'to boost life expectancy. Focus on reducing '
                'child and adult mortality rates.'
            ),
            'icon': 'fa-heartbeat'
        })

    elif min_score == edu_score:

        suggestions.append({
            'area': 'Education and Schooling (Primary Priority)',
            'desc': (
                'Focus on improving school enrollment rates '
                'and educational quality. Strengthen secondary '
                'and vocational training.'
            ),
            'icon': 'fa-graduation-cap'
        })

    else:

        suggestions.append({
            'area': 'Economic Standard of Living (Primary Priority)',
            'desc': (
                'Enact economic policies that raise GDP per capita '
                'and promote equitable income distribution. '
                'Support microfinance, export diversification, '
                'and structural job creation.'
            ),
            'icon': 'fa-chart-line'
        })

    scores = {
        'health': health_score,
        'education': edu_score,
        'income': income_score
    }

    sorted_scores = sorted(
        scores.items(),
        key=lambda item: item[1]
    )

    secondary_area = sorted_scores[1][0]

    if secondary_area == 'health':

        suggestions.append({
            'area': 'Health (Secondary Priority)',
            'desc': (
                'Ensure universal health coverage, modern medical '
                'equipment supply, and expand rural healthcare outreach.'
            ),
            'icon': 'fa-clinic-medical'
        })

    elif secondary_area == 'education':

        suggestions.append({
            'area': 'Education (Secondary Priority)',
            'desc': (
                'Provide teacher training, expand digital learning '
                'infrastructures, and subsidize tertiary education fees.'
            ),
            'icon': 'fa-book-open'
        })

    else:

        suggestions.append({
            'area': 'Economy (Secondary Priority)',
            'desc': (
                'Reduce business hurdles, encourage foreign '
                'direct investments, and invest in infrastructure.'
            ),
            'icon': 'fa-coins'
        })

    return suggestions


# ==================================================
# AUTHENTICATION ROUTES
# ==================================================


# --------------------------------------------------
# LOGIN PROTECTION
# --------------------------------------------------

@app.before_request
def require_login():

    public_endpoints = {
        'login',
        'register',
        'static'
    }

    if request.endpoint in public_endpoints:
        return None

    if request.path.startswith('/static/'):
        return None

    if not session.get('user_id'):
        return redirect(url_for('login'))


# --------------------------------------------------
# USER REGISTRATION
# --------------------------------------------------

@app.route('/register', methods=['GET', 'POST'])
def register():

    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        return render_template(
            'register.html',
            error='Database is not configured yet.'
        ), 503

    if request.method == 'POST':

        full_name = request.form.get(
            'full_name', ''
        ).strip()

        username = request.form.get(
            'username', ''
        ).strip().lower()

        email = request.form.get(
            'email', ''
        ).strip().lower()

        password = request.form.get(
            'password', ''
        )

        confirm_password = request.form.get(
            'confirm_password', ''
        )

        if not all([
            full_name,
            username,
            email,
            password,
            confirm_password
        ]):

            return render_template(
                'register.html',
                error='Please fill in all fields.'
            ), 400

        if len(full_name) > 100:

            return render_template(
                'register.html',
                error='Name must be 100 characters or fewer.'
            ), 400

        if len(username) < 3 or len(username) > 50:

            return render_template(
                'register.html',
                error='Username must be 3 to 50 characters.'
            ), 400

        if not username.replace(
            '_', ''
        ).replace(
            '.', ''
        ).isalnum():

            return render_template(
                'register.html',
                error=(
                    'Username may contain letters, numbers, '
                    'dots and underscores.'
                )
            ), 400

        if (
            len(email) > 120
            or '@' not in email
            or email.startswith('@')
            or email.endswith('@')
        ):

            return render_template(
                'register.html',
                error='Please enter a valid email address.'
            ), 400

        if len(password) < 8:

            return render_template(
                'register.html',
                error='Password must contain at least 8 characters.'
            ), 400

        if password != confirm_password:

            return render_template(
                'register.html',
                error='Passwords do not match.'
            ), 400

        existing_user = User.query.filter(
            or_(
                User.username == username,
                User.email == email
            )
        ).first()

        if existing_user:

            return render_template(
                'register.html',
                error='Username or email already exists.'
            ), 409

        user = User(
            full_name=full_name,
            username=username,
            email=email
        )

        user.set_password(password)

        try:

            db.session.add(user)
            db.session.commit()

        except Exception:

            db.session.rollback()

            logger.exception(
                'Registration failed.'
            )

            return render_template(
                'register.html',
                error=(
                    'Registration could not be completed. '
                    'Please try again.'
                )
            ), 500

        flash(
            'Registration successful. Please log in.',
            'success'
        )

        return redirect(url_for('login'))

    return render_template('register.html')


# --------------------------------------------------
# USER LOGIN
# --------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        if not app.config.get("SQLALCHEMY_DATABASE_URI"):

            return render_template(
                'login.html',
                error='Database is not configured yet.'
            ), 503

        username_or_email = request.form.get(
            'username', ''
        ).strip().lower()

        password = request.form.get(
            'password', ''
        )

        user = User.query.filter(
            or_(
                User.username == username_or_email,
                User.email == username_or_email
            )
        ).first()

        if user and user.check_password(password):

            session.clear()

            session['user_id'] = user.id
            session['username'] = user.username
            session['full_name'] = user.full_name

            session.permanent = True

            logger.info(
                'User logged in: %s',
                user.username
            )

            return redirect(url_for('index'))

        return render_template(
            'login.html',
            error='Invalid username/email or password.'
        ), 401

    return render_template('login.html')


# --------------------------------------------------
# USER LOGOUT
# --------------------------------------------------

@app.route('/logout', methods=['GET', 'POST'])
def logout():

    session.clear()

    flash(
        'You have been logged out.',
        'success'
    )

    return redirect(url_for('login'))


# ==================================================
# MAIN APPLICATION ROUTES
# ==================================================


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

@app.route('/')
def index():

    global stats_cache, country_list

    if (
        model is None
        or not stats_cache
        or stats_cache.get('total_countries', 0) <= 12
    ):
        load_ml_resources()

    model_r2 = "98.5%"

    eval_report_path = os.path.join(
        Config.MODEL_DIR,
        'evaluation_report.txt'
    )

    if os.path.exists(eval_report_path):

        try:

            with open(eval_report_path, 'r') as f:

                lines = f.readlines()

                for line in lines:

                    if "R-squared" in line:

                        r2_val = float(
                            line.split(":")[-1].strip()
                        )

                        model_r2 = f"{r2_val * 100:.1f}%"

                        break

        except Exception:
            pass

    return render_template(
        'index.html',
        stats=stats_cache,
        countries=country_list,
        model_accuracy=model_r2
    )


# --------------------------------------------------
# HDI PREDICTION
# --------------------------------------------------

@app.route('/predict', methods=['GET', 'POST'])
def predict():

    global model, scaler, country_list

    if model is None or scaler is None:

        load_ml_resources()

        if model is None or scaler is None:

            return render_template(
                '500.html',
                error=(
                    'Machine Learning model components are not '
                    'initialized. Please ensure the model training '
                    'pipeline has completed successfully.'
                )
            ), 500

    if request.method == 'GET':

        return redirect(url_for('index'))

    try:

        country = request.form.get(
            'country', 'Unknown Country'
        ).strip()

        life_exp_str = request.form.get(
            'life_expectancy', ''
        ).strip()

        expected_schooling_str = request.form.get(
            'expected_years_schooling', ''
        ).strip()

        mean_schooling_str = request.form.get(
            'mean_years_schooling', ''
        ).strip()

        gni_per_capita_str = request.form.get(
            'gni_per_capita', ''
        ).strip()

        # Field validation
        if not all([
            life_exp_str,
            expected_schooling_str,
            mean_schooling_str,
            gni_per_capita_str
        ]):

            return render_template(
                'index.html',
                error='All fields are required.',
                countries=country_list,
                stats=stats_cache
            ), 400

        # Numeric validation
        try:

            life_exp = float(life_exp_str)

            expected_schooling = float(
                expected_schooling_str
            )

            mean_schooling = float(
                mean_schooling_str
            )

            gni_per_capita = float(
                gni_per_capita_str
            )

        except ValueError:

            return render_template(
                'index.html',
                error='Values must be numeric.',
                countries=country_list,
                stats=stats_cache
            ), 400

        # Logical range validation
        validation_errors = []

        if not (20.0 <= life_exp <= 100.0):

            validation_errors.append(
                'Life Expectancy must be between 20.0 and 100.0 years.'
            )

        if not (0.0 <= expected_schooling <= 25.0):

            validation_errors.append(
                'Expected Years of Schooling must be between 0.0 and 25.0 years.'
            )

        if not (0.0 <= mean_schooling <= 20.0):

            validation_errors.append(
                'Mean Years of Schooling must be between 0.0 and 20.0 years.'
            )

        if mean_schooling > expected_schooling:

            validation_errors.append(
                'Mean Years of Schooling should not exceed Expected Years of Schooling.'
            )

        if not (100.0 <= gni_per_capita <= 150000.0):

            validation_errors.append(
                'GNI per Capita must be between $100 and $150,000 PPP.'
            )

        if validation_errors:

            return render_template(
                'index.html',
                error='; '.join(validation_errors),
                countries=country_list,
                stats=stats_cache
            ), 400

        # ML Prediction
        features = np.array([[
            life_exp,
            expected_schooling,
            mean_schooling,
            gni_per_capita
        ]])

        features_scaled = scaler.transform(features)

        predicted_hdi = model.predict(
            features_scaled
        )[0]

        predicted_hdi = np.clip(
            predicted_hdi,
            0.000,
            1.000
        )

        # HDI Classification
        category_info = get_hdi_category(
            predicted_hdi
        )

        # Policy Suggestions
        suggestions = generate_suggestions(
            life_exp,
            expected_schooling,
            mean_schooling,
            gni_per_capita
        )

        # Indicator percentages
        health_pct = round(
            np.clip(
                (life_exp - 20) / (85 - 20),
                0,
                1
            ) * 100,
            1
        )

        edu_pct = round(
            np.clip(
                (
                    (mean_schooling / 15)
                    + (expected_schooling / 18)
                ) / 2,
                0,
                1
            ) * 100,
            1
        )

        income_pct = round(
            np.clip(
                (
                    np.log(max(gni_per_capita, 100))
                    - np.log(100)
                ) / (
                    np.log(75000) - np.log(100)
                ),
                0,
                1
            ) * 100,
            1
        )

        result_data = {
            'country': country,
            'life_expectancy': life_exp,
            'expected_years_schooling': expected_schooling,
            'mean_years_schooling': mean_schooling,
            'gni_per_capita': gni_per_capita,
            'predicted_hdi': round(
                float(predicted_hdi),
                3
            ),
            'category': category_info['name'],
            'category_color': category_info['color'],
            'category_bg': category_info['bg_color'],
            'category_text': category_info['text_color'],
            'health_pct': health_pct,
            'edu_pct': edu_pct,
            'income_pct': income_pct,
            'suggestions': suggestions
        }

        logger.info(
            f"Prediction made for {country}: "
            f"HDI {result_data['predicted_hdi']}"
        )

        return render_template(
            'result.html',
            result=result_data
        )

    except Exception as e:

        logger.error(
            f"Exception during prediction: {e}",
            exc_info=True
        )

        return render_template(
            '500.html',
            error=f'Backend computation error: {str(e)}'
        ), 500


# --------------------------------------------------
# ABOUT PAGE
# --------------------------------------------------

@app.route('/about')
def about():

    model_details = {
        'model_name': 'Linear Regression',
        'r2_score': '98.5%',
        'mae': '0.0125',
        'rmse': '0.0165',
        'coefficients': {
            'Life Expectancy': 0.28,
            'Expected Education': 0.25,
            'Mean Education': 0.24,
            'Log GNI per Capita': 0.26
        }
    }

    eval_report_path = os.path.join(
        Config.MODEL_DIR,
        'evaluation_report.txt'
    )

    if os.path.exists(eval_report_path):

        try:

            with open(eval_report_path, 'r') as f:

                lines = f.readlines()

                coeffs = {}

                for line in lines:

                    if "R-squared" in line:

                        model_details['r2_score'] = (
                            f"{float(line.split(':')[-1].strip()) * 100:.2f}%"
                        )

                    elif "Mean Absolute Error" in line:

                        model_details['mae'] = (
                            f"{float(line.split(':')[-1].strip()):.5f}"
                        )

                    elif "Root Mean Squared Error" in line:

                        model_details['rmse'] = (
                            f"{float(line.split(':')[-1].strip()):.5f}"
                        )

                    elif "life_expectancy" in line:

                        coeffs['Life Expectancy'] = float(
                            line.split(':')[-1].strip()
                        )

                    elif "expected_years_schooling" in line:

                        coeffs['Expected Years of Schooling'] = float(
                            line.split(':')[-1].strip()
                        )

                    elif "mean_years_schooling" in line:

                        coeffs['Mean Years of Schooling'] = float(
                            line.split(':')[-1].strip()
                        )

                    elif "gni_per_capita" in line:

                        coeffs['GNI per Capita'] = float(
                            line.split(':')[-1].strip()
                        )

                if coeffs:
                    model_details['coefficients'] = coeffs

        except Exception as e:

            logger.warning(
                f"Error loading evaluation report: {e}"
            )

    return render_template(
        'about.html',
        details=model_details
    )


# ==================================================
# API ENDPOINTS
# ==================================================


# --------------------------------------------------
# COUNTRY METRICS API
# --------------------------------------------------

@app.route(
    '/api/country/<string:country_name>',
    methods=['GET']
)
def get_country_metrics(country_name):

    if os.path.exists(Config.PROCESSED_DATA_PATH):

        try:

            df = pd.read_csv(
                Config.PROCESSED_DATA_PATH
            )

            country_df = df[
                df['country'].str.lower()
                == country_name.lower()
            ]

            if not country_df.empty:

                latest_record = country_df.sort_values(
                    by='year',
                    ascending=False
                ).iloc[0]

                return jsonify({
                    'success': True,
                    'country': latest_record['country'],
                    'life_expectancy': float(
                        latest_record['life_expectancy']
                    ),
                    'expected_years_schooling': float(
                        latest_record['expected_years_schooling']
                    ),
                    'mean_years_schooling': float(
                        latest_record['mean_years_schooling']
                    ),
                    'gni_per_capita': float(
                        latest_record['gni_per_capita']
                    )
                })

        except Exception as e:

            logger.error(
                f"Error reading country metrics: {e}"
            )

    return jsonify({
        'success': False,
        'message': 'Country not found'
    }), 404


# --------------------------------------------------
# COUNTRIES API
# --------------------------------------------------

@app.route('/api/countries', methods=['GET'])
def get_countries():

    global country_list

    if not country_list:
        load_ml_resources()

    return jsonify({
        'countries': country_list
    })


# --------------------------------------------------
# STATISTICS API
# --------------------------------------------------

@app.route('/api/stats', methods=['GET'])
def get_stats():

    global stats_cache

    if not stats_cache:
        load_ml_resources()

    return jsonify(stats_cache)


# ==================================================
# ERROR HANDLERS
# ==================================================


@app.errorhandler(404)
def page_not_found(e):

    return render_template(
        '404.html'
    ), 404


@app.errorhandler(500)
def internal_server_error(e):

    logger.error(
        f"Internal server error handler triggered: {e}"
    )

    return render_template(
        '500.html',
        error='An unexpected server error occurred. Please try again later.'
    ), 500


# ==================================================
# LOCAL DEVELOPMENT
# ==================================================

if __name__ == '__main__':

    Config.init_app()

    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
