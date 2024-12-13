from flask import Flask,render_template, redirect, request, jsonify, flash, session
import requests
import mysql.connector
import os
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from flask_cors import CORS
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend
import matplotlib.pyplot as plt

app = Flask(__name__)
CORS(app)
app.secret_key=os.urandom(24)

conn =mysql.connector.connect(host="localhost",user="root",password="",database="dietdb")
cursor = conn.cursor()  # Enables dictionary cursor
# cursor = conn.cursor(dictionary=True)  # Enables dictionary cursor

data = pd.read_csv("DietChartPlan.csv")


# Load the trained model and label encoders
with open("ModelFile.pkl", "rb") as model_file:
    classifier, label_encoder_DietName, label_encoder_DietType = pickle.load(model_file)


MEALDB_BASE_URL = "https://www.themealdb.com/api/json/v1/1/search.php"


@app.route('/')  #First page that Load
def image():
    return render_template('index.html')


@app.route('/get_recipe', methods=['GET'])
def get_recipe():
    # Get the food name from query parameters
    food_name = request.args.get('food_name')
    if not food_name:
        return jsonify({"error": "Please provide a food name using the 'food_name' query parameter"}), 400

    # Make a request to the MealDB API
    response = requests.get(MEALDB_BASE_URL, params={"s": food_name})
    
    # Check for errors in the response
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch recipes from the MealDB API"}), response.status_code

    # Parse the API response
    data = response.json()

    # Check if meals were found
    if not data.get('meals'):
        return jsonify({"message": f"No recipes found for '{food_name}'"}), 404

    # Extract relevant recipe details
    recipes = []
    for meal in data['meals']:
        recipes.append({
            "name": meal['strMeal'],
            "category": meal['strCategory'],
            "area": meal['strArea'],
            "instructions": meal['strInstructions'],
            "image": meal['strMealThumb'],
            "youtube": meal['strYoutube']
        })

    # Return recipes as JSON
    return jsonify(recipes)


@app.route('/recipe')
def recipe():
    return render_template('recipe.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

def create_user_table(email):

    create_table_query = """
    CREATE TABLE IF NOT EXISTS `{}` (
        User_Table_id INT AUTO_INCREMENT PRIMARY KEY,
        DietName VARCHAR(255),
        dietType VARCHAR(255),
        image_url VARCHAR(255),
        foodName VARCHAR(255),
        carbs INT(20),
        protein INT(20),
        calories INT(20)
    )
    """.format(email)
    cursor.execute(create_table_query)
    conn.commit()

@app.route('/RegistrationNewUser', methods=["POST"])
def add_user():
    try:
        # Get the data from the form submission
        Name = request.form.get('Name')
        Email = request.form.get('Email')
        Password = request.form.get('Password')
        
        # Validate inputs (optional but recommended)
        if not Name or not Email or not Password:
            return jsonify({'success': False, 'message': 'All fields are required!'}), 400

        # Insert into the database using parameterized queries to prevent SQL injection
        cursor.execute("""
            INSERT INTO `logindetails` (`Name`, `Email`, `Password`) 
            VALUES (%s, %s, %s)
        """, (Name, Email, Password))
        conn.commit()

        # Optionally create a user-specific table or perform other actions
        create_user_table(Email)
        
        # Return a success response
        return jsonify({'success': True, 'message': 'Registered successfully!'}), 201

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': 'Registration failed. Please try again later.'}), 500

@app.route('/UserLogin', methods=['POST'])
def LoginVald():
    try:
        # Get the email and password from the form
        Email = request.form.get('Email')
        Password = request.form.get('Password')

        # Validate input fields
        if not Email or not Password:
            return jsonify({'success': False, 'message': 'Both email and password are required!'}), 400

        # Execute a parameterized query to prevent SQL injection
        query = """SELECT * FROM `logindetails` WHERE `Email` = %s AND `Password` = %s"""
        cursor.execute(query, (Email, Password))
        users = cursor.fetchall()

        if len(users) > 0:
            # Extract the first user's data
            user = users[0]

            # Debugging: Print the user data structure for clarity
            print("User fetched from database:", user)

            # Store email in session
            session['Email'] = user[2]  # Replace with the correct index or key

            # Create a user-specific table if needed
            create_user_table(Email)

            # Prepare user data for response
            user_data = {
                "Id": user[0],        # Replace index if needed
                "Name": user[1],      # Replace index if needed
                "Email": user[2],     # Replace index if needed
                "Password": user[3],  # Replace index if needed
            }
            return jsonify({'success': True, 'message': 'Login successful!', 'user': user_data}), 200
        else:
            return jsonify({'success': False, 'message': 'Invalid email or password. Please try again.'}), 400
    except Exception as e:
        # Enhanced error logging for debugging
        print(f"Error during login validation: {e}")
        return jsonify({'success': False, 'message': 'Login failed. Please try again later.'}), 500



unique_brand_to_image_url = data.drop_duplicates(subset='FoodName').set_index('FoodName')['Image'].to_dict()

@app.route('/BestFoodRecommend', methods=['POST'])
def BestFoodRecommend():
    try:
        DietName = request.form['DietName']
        DietType = request.form['DietType']
        Protein = float(request.form['Protein'])
        Calories = float(request.form['Calories'])
        DietName_encoded = label_encoder_DietName.transform([DietName])[0]
        DietType_encoded = label_encoder_DietType.transform([DietType])[0]
        probabilities = classifier.predict_proba([[DietName_encoded, DietType_encoded, Protein, Calories]])[0]

        food_probabilities = pd.DataFrame({
            'FoodName': classifier.classes_,
            'Probability': probabilities
        })

        # Filtering food names based on DietName and DietType
        filtered_food_names = data[(data['DietName'] == DietName) & (data['DietType'] == DietType)]['FoodName'].unique()

        # Filtering food probabilities to only include food names that match the criteria
        top_10_foods = food_probabilities[food_probabilities['FoodName'].isin(filtered_food_names)]
        top_10_foods = top_10_foods.sort_values(by='Probability', ascending=False).head(10)

        recommended_foods = top_10_foods.to_dict(orient='records')

        # Updating food information with additional details
        for food in recommended_foods:
            food_name = food['FoodName']

            food_protein = data.loc[data['FoodName'] == food_name, 'Protein'].iloc[0]
            food_calories = data.loc[data['FoodName'] == food_name, 'Calories'].iloc[0]
            food_carbs = data.loc[data['FoodName'] == food_name, 'Carbs'].iloc[0]
            food_FoodDescription = data.loc[data['FoodName'] == food_name, 'FoodDescription'].iloc[0]

            food['Protein'] = food_protein
            food['Calories'] = food_calories
            food['Carbs'] = food_carbs
            food['FoodDescription'] = food_FoodDescription

            image_url = unique_brand_to_image_url.get(food_name, 'Image')
            food['image_url'] = image_url

            # Ensure the values are JSON serializable (convert int64 to int)
            food['Protein'] = int(food['Protein'])
            food['Calories'] = int(food['Calories'])
            food['Carbs'] = int(food['Carbs'])

        # Return a JSON response with success, message, and data
        return jsonify({
            'success': True,
            'message': 'Food recommendations retrieved successfully',
            'recommended_foods': recommended_foods  # Correct the key here as 'data' was used
        })

    except Exception as e:
        print(e, "e")
        # Return an error response in case of any issues
        return jsonify({
            'success': False,
            'message': str(e)  # Return the exception message
        })

@app.route('/add_to_log', methods=['POST'])
def add_to_log():
        
        try:
            data = request.json
            dietName = data['dietName']
            dietType = data['dietType']
            image_url = data['image_url']
            foodName = data['foodName']
            carbs = data['carbs']
            protein = data['protein']
            calories = data['calories']
            email = data['email']
            if not email:
                return jsonify({'error': 'User not logged in or session expired'}), 400
            query = "INSERT INTO `{}` (dietName,dietType,image_url,foodName,carbs,protein,calories) VALUES (%s, %s, %s, %s, %s, %s, %s)".format(email)
            cursor.execute(query, (dietName,dietType,image_url,foodName, carbs, protein, calories))
            conn.commit()

            return jsonify({'message': 'Data added to log successfully'}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/userViewLod', methods=['POST'])
def userViewLod():
    try:
        # Extract email from the POST request body
        data = request.json
        email = data.get('email')
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        # Dynamically use email as the table name
        query = "SELECT * FROM `{}`".format(email)
        cursor.execute(query)
        meals = cursor.fetchall()
        
        return jsonify({'meals': meals}), 200
    except Exception as e:
        import traceback
        print("Error:", traceback.format_exc())
        return jsonify({'error': str(e)}), 500


@app.route('/compareFood', methods=['POST'])
def ComparePage():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('Email')  # Get the Email from the request body
        food1 = data.get('food1')
        food2 = data.get('food2')

        if food1 == food2:
            return jsonify({
                'success': False,
                'message': "Please select two different foods for comparison.",
                'data': []
            })

        query = f"SELECT foodName, dietType, image_url, protein, calories, carbs FROM `{email}` WHERE foodName = %s OR foodName = %s"
        cursor.execute(query, (food1, food2))
        food_details = cursor.fetchall()

        if not food_details:
            return jsonify({
                'success': False,
                'message': 'No food details found for the selected items.',
                'data': []
            })

        # Manually map tuple indices to keys
        food_data = []
        for food in food_details:
            food_data.append({
                'foodName': food[0],  # Index 0 corresponds to foodName
                'dietType': food[1],  # Index 1 corresponds to dietType
                'image_url': food[2],  # Index 2 corresponds to image_url
                'protein': food[3],  # Index 3 corresponds to protein
                'calories': food[4],  # Index 4 corresponds to calories
                'carbs': food[5]  # Index 5 corresponds to carbs
            })

        return jsonify({
            'success': True,
            'message': 'Food comparison successful.',
            'data': {
                'food1': food_data[0] if len(food_data) > 0 else None,
                'food2': food_data[1] if len(food_data) > 1 else None
            }
        })

    else:
        email = request.args.get('Email')
        query = f"SELECT DISTINCT foodName FROM `{email}`"
        cursor.execute(query)
        food_detail = [row[0] for row in cursor.fetchall()]  # Extract only the foodName

        return jsonify({
            'success': True,
            'message': 'Food list retrieved successfully.',
            'data': food_detail
        })


@app.route('/delete/<int:food_id>', methods=['POST'])
def delete(food_id):
    try:
        # Extract email from request body
        data = request.json
        email = data.get('email')

        if not email:
            return jsonify({'success': False, 'message': 'Email is required'}), 400
        # Use the email as the table name
        table_user = email

        query = f"DELETE FROM `{table_user}` WHERE User_Table_id = {food_id}"
        cursor.execute(query)

        conn.commit()

        return jsonify({'success': True, 'message': 'Record deleted successfully'}), 200
    except Exception as e:
        import traceback
        print("Error:", traceback.format_exc())
        return jsonify({'success': False, 'message': 'Error deleting record', 'error': str(e)}), 500

@app.route('/updateuser', methods=["POST"])
def update_user():
    # Fetching JSON data from the request body
    data = request.get_json()
    # Extracting fields from the JSON data
    Name = data.get('Name')
    Email = data.get('Email')
    localemail = data.get('PrevEmail')
    Password = data.get('Password')

    # Checking if all fields are provided
    if not all([Name, Email, Password]):
        return jsonify({"status": "error", "message": "All fields are required!"}), 400

    # Updating user details in the database
    try:
        cursor.execute(
            """
            UPDATE logindetails
            SET Name = %s, Password = %s, Email = %s
            WHERE Email = %s
            """,
            (Name, Password, Email, localemail)
        )
        conn.commit()
        return jsonify({"status": "success", "message": "User details updated successfully!"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": f"Error updating user details: {str(e)}"}), 500


if __name__ == '__main__':
    # Ensure the server is running in debug mode
    app.run(debug=True,host='0.0.0.0', port=5000)
