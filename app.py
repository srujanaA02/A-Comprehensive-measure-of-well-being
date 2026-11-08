            'suggestions': suggestions
        }
        
        logger.info(f"Prediction made for {country}: HDI {result_data['predicted_hdi']}")
        return render_template('result.html', result=result_data)
        
    except Exception as e:
        logger.error(f"Exception during prediction: {e}", exc_info=True)
        return render_template('500.html', error=f"Backend computation error: {str(e)}"), 500

@app.route('/about')
def about():
    """Serves information page regarding how HDI is computed and model details."""
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
    
    # Attempt to load coefficients from file
    eval_report_path = os.path.join(Config.MODEL_DIR, 'evaluation_report.txt')
    if os.path.exists(eval_report_path):
        try:
            with open(eval_report_path, 'r') as f:
                lines = f.readlines()
                coeffs = {}
                for line in lines:
                    if "R-squared" in line:
                        model_details['r2_score'] = f"{float(line.split(':')[-1].strip()) * 100:.2f}%"
                    elif "Mean Absolute Error" in line:
                        model_details['mae'] = f"{float(line.split(':')[-1].strip()):.5f}"
                    elif "Root Mean Squared Error" in line:
                        model_details['rmse'] = f"{float(line.split(':')[-1].strip()):.5f}"
                    elif "life_expectancy" in line:
                        coeffs['Life Expectancy'] = float(line.split(':')[-1].strip())
                    elif "expected_years_schooling" in line:
                        coeffs['Expected Years of Schooling'] = float(line.split(':')[-1].strip())
                    elif "mean_years_schooling" in line:
                        coeffs['Mean Years of Schooling'] = float(line.split(':')[-1].strip())
                    elif "gni_per_capita" in line:
                        coeffs['GNI per Capita'] = float(line.split(':')[-1].strip())
                if coeffs:
                    model_details['coefficients'] = coeffs
        except Exception as e:
            logger.warning(f"Error loading evaluation report lines for About page: {e}")
            
    return render_template('about.html', details=model_details)

# --- API ENDPOINTS ---

@app.route('/api/country/<string:country_name>', methods=['GET'])
def get_country_metrics(country_name):
    """API endpoint to fetch the latest metrics of a given country for prefilling."""
    if os.path.exists(Config.PROCESSED_DATA_PATH):
        try:
            df = pd.read_csv(Config.PROCESSED_DATA_PATH)
            country_df = df[df['country'].str.lower() == country_name.lower()]
            if not country_df.empty:
                # Get the latest year record
                latest_record = country_df.sort_values(by='year', ascending=False).iloc[0]
                return jsonify({
                    'success': True,
                    'country': latest_record['country'],
                    'life_expectancy': float(latest_record['life_expectancy']),
                    'expected_years_schooling': float(latest_record['expected_years_schooling']),
                    'mean_years_schooling': float(latest_record['mean_years_schooling']),
                    'gni_per_capita': float(latest_record['gni_per_capita'])
                })
        except Exception as e:
            logger.error(f"Error reading country metrics: {e}")
            
    return jsonify({'success': False, 'message': 'Country not found'}), 404

@app.route('/api/countries', methods=['GET'])
def get_countries():
    """API endpoint to get list of countries."""
    global country_list
    if not country_list:
        load_ml_resources()
    return jsonify({'countries': country_list})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """API endpoint to get overall dataset statistics."""
    global stats_cache
    if not stats_cache:
        load_ml_resources()
    return jsonify(stats_cache)

# --- ERROR HANDLERS ---

@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 handler."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Custom 500 handler."""
    logger.error(f"Internal server error handler triggered: {e}")
    return render_template('500.html', error="An unexpected server error occurred. Please try again later."), 500

if __name__ == '__main__':
    # Ensure folder structure is intact
    Config.init_app()
    # Run the Flask app
    app.run(host='127.0.0.1', port=5000, debug=True)
