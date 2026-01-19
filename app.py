import tkinter as tk
from tkinter import ttk, messagebox

class NutritionCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HEALTHIER!")
        self.geometry("600x800")
        self.create_widgets()

        # Variables to store BMI calculation results
        self.stored_weight = None
        self.stored_height = None
        self.stored_age = None
        self.stored_gender = None
        self.stored_athlete_status = None
        self.stored_activity_level = None
        self.stored_bmi = None
        self.stored_special_status = None

    def create_widgets(self):
        self.main_menu()

    def main_menu(self):
        for widget in self.winfo_children():
            widget.destroy()

        # Introduction Section
        intro_text = (
            "Welcome to HEALTHIER!\n\n"
            "This tool is designed to help you assess your BMI, understand "
            "your daily energy and nutrient requirements, and calculate the "
            "calories burned through various physical activities.\n\n"
            "Choose from the options below to get started."
        )
        tk.Label(self, text=intro_text, font=("Helvetica", 12), wraplength=500, justify="left").pack(pady=20)

        tk.Label(self, text="Healthier", font=("Helvetica", 16)).pack(pady=10)
        
        ttk.Button(self, text="Calculate Your BMI", command=self.calculate_bmi).pack(pady=10)
        ttk.Button(self, text="Average Recommended Number of Serves", command=self.average_serves).pack(pady=10)
        ttk.Button(self, text="Get Moving! Calculator", command=self.get_moving).pack(pady=10)

    def calculate_bmi(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Calculate Your BMI", font=("Helvetica", 16)).pack(pady=20)

        tk.Label(self, text="Gender:").pack()
        self.bmi_gender_var = tk.StringVar()
        ttk.Combobox(self, textvariable=self.bmi_gender_var, values=["Male", "Female"]).pack()

        tk.Label(self, text="Age:").pack()
        self.bmi_age_var = tk.IntVar()
        tk.Entry(self, textvariable=self.bmi_age_var).pack()

        tk.Label(self, text="Weight (kg):").pack()
        self.bmi_weight_var = tk.DoubleVar()
        tk.Entry(self, textvariable=self.bmi_weight_var).pack()

        tk.Label(self, text="Height (cm):").pack()
        self.bmi_height_var = tk.DoubleVar()
        tk.Entry(self, textvariable=self.bmi_height_var).pack()

        tk.Label(self, text="Are you an athlete?").pack()
        self.athlete_status_var = tk.StringVar()
        ttk.Combobox(self, textvariable=self.athlete_status_var, values=["Yes", "No"]).pack()

        tk.Label(self, text="Activity Level:").pack()
        self.activity_level_var = tk.StringVar()
        activity_levels = [
            "1.2 - Very sedentary (bed bound, chair bound)",
            "1.4 - Sedentary work and no strenuous leisure activity (office worker)",
            "1.6 - Mostly sedentary work with little or no strenuous leisure activity (students, lab assistants, drivers)",
            "1.8 - Moderately active work, predominantly standing or walking (waiters, shop assistant, teacher)",
            "2.0 - Heavy activity (trades person, or high performance athletes)",
            "2.2 - Significantly active (with your occupation with additional strenuous activities)"
        ]
        ttk.Combobox(self, textvariable=self.activity_level_var, values=activity_levels).pack()

        ttk.Button(self, text="Submit", command=self.calculate_bmi_result).pack(pady=10)
        ttk.Button(self, text="Back to Main Menu", command=self.main_menu).pack(pady=10)

    def calculate_bmi_result(self):
        gender = self.bmi_gender_var.get().lower()
        age = self.bmi_age_var.get()
        weight = self.bmi_weight_var.get()
        height = self.bmi_height_var.get()
        athlete_status = self.athlete_status_var.get().lower()
        activity_level = float(self.activity_level_var.get().split(" - ")[0]) if self.activity_level_var.get() else None

        if height <= 0 or weight <= 0:
            messagebox.showwarning("Invalid Input", "Invalid input for height or weight")
            return

        if gender and age and weight and height and athlete_status and activity_level:
            height_m = height / 100
            bmi = weight / (height_m ** 2)
            self.stored_bmi = bmi
            category = self.get_bmi_category(bmi, age, gender)

            # Store values for later use
            self.stored_weight = weight
            self.stored_height = height
            self.stored_age = age
            self.stored_gender = gender
            self.stored_athlete_status = athlete_status
            self.stored_activity_level = activity_level

            explanation = (
                f"Based on your inputs:\n"
                f"- Gender: {gender.capitalize()}\n"
                f"- Age: {age} years\n"
                f"- Weight: {weight} kg\n"
                f"- Height: {height} cm\n"
                f"- Athlete: {athlete_status.capitalize()}\n"
                f"- Activity Level: {activity_level}\n\n"
                f"Your Body Mass Index (BMI) is {bmi:.2f}, which falls into the category: {category}."
            )

            messagebox.showinfo("BMI Result", explanation)
            
            # Directly calculate and show the results for daily energy and nutrient requirements
            self.calculate_energy_needs()
            self.nutrient_requirements()
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields")

    def get_bmi_category(self, bmi, age, gender):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        elif 30 <= bmi < 34.9:
            return "Obesity Class I"
        elif 35 <= bmi < 39.9:
            return "Obesity Class II"
        else:
            return "Obesity Class III"

    def calculate_energy_needs(self):
        if self.stored_gender and self.stored_age and self.stored_weight and self.stored_height and self.stored_athlete_status and self.stored_activity_level:
            weight = self.stored_weight
            height = self.stored_height
            age = self.stored_age
            gender = self.stored_gender
            athlete_status = self.stored_athlete_status
            activity_level = self.stored_activity_level

            # Calculate Basal Metabolic Rate (BMR)
            if gender == 'male':
                bmr = 10 * weight + 6.25 * height - 5 * age + 5
                bmr_formula = "10 * weight (kg) + 6.25 * height (cm) - 5 * age (years) + 5"
            else:
                bmr = 10 * weight + 6.25 * height - 5 * age - 161
                bmr_formula = "10 * weight (kg) + 6.25 * height (cm) - 5 * age (years) - 161"

            daily_energy = bmr * activity_level

            # Adjust for special status (e.g., pregnant, breastfeeding)
            if self.stored_special_status == 'pregnant':
                daily_energy += 300  # Example adjustment
            elif self.stored_special_status == 'breastfeeding':
                daily_energy += 500

            explanation = (
                f"Your Basal Metabolic Rate (BMR) was calculated using the formula: {bmr_formula}.\n"
                f"Based on your inputs:\n"
                f"- Weight: {weight} kg\n"
                f"- Height: {height} cm\n"
                f"- Age: {age} years\n"
                f"- Gender: {gender.capitalize()}\n"
                f"- Athlete: {athlete_status.capitalize()}\n"
                f"- Activity Level: {activity_level}\n"
                f"Your BMR is {bmr:.2f} kcal/day.\n\n"
                f"This BMR is then multiplied by your Physical Activity Level (PAL) to estimate your daily energy needs.\n"
                f"Therefore, your estimated daily energy requirement is {daily_energy:.2f} kcal/day."
            )

            messagebox.showinfo("Daily Energy Requirement", explanation)
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields or calculate your BMI first.")

    def nutrient_requirements(self):
        if self.stored_gender and self.stored_age and self.stored_athlete_status:
            gender = self.stored_gender
            age = self.stored_age
            athlete_status = self.stored_athlete_status

            # Define nutrient requirements based on gender, athlete status, and age range
            nutrient_reqs = {
                'non_athlete_male': {
                    (14, 18): {
                        'energy': 2800,
                        'protein': 59,
                        'fat': 70,
                        'carbohydrates': 130,
                        'fiber': 38,
                        'sugar': 50,
                        'sodium': 2300
                    },
                    (19, 30): {
                        'energy': 2600,
                        'protein': 56,
                        'fat': 70,
                        'carbohydrates': 130,
                        'fiber': 38,
                        'sugar': 50,
                        'sodium': 2300
                    },
                    (31, 50): {
                        'energy': 2400,
                        'protein': 56,
                        'fat': 70,
                        'carbohydrates': 130,
                        'fiber': 38,
                        'sugar': 50,
                        'sodium': 2300
                    },
                    (51, float('inf')): {
                        'energy': 2200,
                        'protein': 56,
                        'fat': 70,
                        'carbohydrates': 130,
                        'fiber': 30,
                        'sugar': 50,
                        'sodium': 2300
                    }
                },
                'athlete_male': {
                    (14, 18): {
                        'energy': 3200,
                        'protein': 84,
                        'fat': 100,
                        'carbohydrates': 130,
                        'fiber': 38,
                        'sugar': 75,
                        'sodium': 2300
                    },
                    (19, 30): {
                        'energy': 3000,
                        'protein': 84,
                        'fat': 100,
                        'carbohydrates': 130,
                        'fiber': 38,
                        'sugar': 75,
                        'sodium': 2300
                    },
                    (31, 50): {
                        'energy': 2800,
                        'protein': 84,
                        'fat': 100,
                        'carbohydrates': 130,
                        'fiber': 38,
                        'sugar': 75,
                        'sodium': 2300
                    },
                    (51, float('inf')): {
                        'energy': 2600,
                        'protein': 84,
                        'fat': 100,
                        'carbohydrates': 130,
                        'fiber': 38,
                        'sugar': 75,
                        'sodium': 2300
                    }
                },
                'non_athlete_female': {
                    (14, 18): {
                        'energy': 2200,
                        'protein': 46,
                        'fat': 70,
                        'carbohydrates': 130,
                        'fiber': 26,
                        'sugar': 50,
                        'sodium': 2300
                    },
                    (19, 30): {
                        'energy': 2000,
                        'protein': 46,
                        'fat': 70,
                        'carbohydrates': 130,
                        'fiber': 25,
                        'sugar': 50,
                        'sodium': 2300
                    },
                    (31, 50): {
                        'energy': 1800,
                        'protein': 46,
                        'fat': 70,
                        'carbohydrates': 130,
                        'fiber': 25,
                        'sugar': 50,
                        'sodium': 2300
                    },
                    (51, float('inf')): {
                        'energy': 1600,
                        'protein': 46,
                        'fat': 70,
                        'carbohydrates': 130,
                        'fiber': 21,
                        'sugar': 50,
                        'sodium': 2300
                    }
                },
                'athlete_female': {
                    (14, 18): {
                        'energy': 2800,
                        'protein': 66,
                        'fat': 80,
                        'carbohydrates': 130,
                        'fiber': 26,
                        'sugar': 50,
                        'sodium': 2300
                    },
                    (19, 30): {
                        'energy': 2500,
                        'protein': 66,
                        'fat': 80,
                        'carbohydrates': 130,
                        'fiber': 25,
                        'sugar': 50,
                        'sodium': 2300
                    },
                    (31, 50): {
                        'energy': 2400,
                        'protein': 66,
                        'fat': 80,
                        'carbohydrates': 130,
                        'fiber': 25,
                        'sugar': 50,
                        'sodium': 2300
                    },
                    (51, float('inf')): {
                        'energy': 2200,
                        'protein': 66,
                        'fat': 80,
                        'carbohydrates': 130,
                        'fiber': 21,
                        'sugar': 50,
                        'sodium': 2300
                    }
                }
            }

            # Determine appropriate nutrient requirements
            category = 'athlete' if athlete_status == 'yes' else 'non_athlete'
            key = f'{category}_{gender}'
            age_range = next((range for range in nutrient_reqs[key] if range[0] <= age <= range[1]), None)

            if age_range:
                reqs = nutrient_reqs[key][age_range]
                explanation = (
                    f"Based on your inputs:\n"
                    f"- Gender: {gender.capitalize()}\n"
                    f"- Age: {age} years\n"
                    f"- Athlete: {athlete_status.capitalize()}\n\n"
                    f"Your daily nutrient requirements are approximately:\n"
                    f"- Energy: {reqs['energy']} kcal\n"
                    f"- Protein: {reqs['protein']} g\n"
                    f"- Fat: {reqs['fat']} g\n"
                    f"- Carbohydrates: {reqs['carbohydrates']} g\n"
                    f"- Fiber: {reqs['fiber']} g\n"
                    f"- Sugar: {reqs['sugar']} g\n"
                    f"- Sodium: {reqs['sodium']} mg"
                )
                messagebox.showinfo("Nutrient Requirements", explanation)
            else:
                messagebox.showwarning("Age Error", "Unable to find nutrient requirements for your age group.")
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields or calculate your BMI first.")

    def average_serves(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Average Recommended Number of Serves", font=("Helvetica", 16)).pack(pady=20)

        tk.Label(self, text="Gender:").pack()
        self.serves_gender_var = tk.StringVar()
        ttk.Combobox(self, textvariable=self.serves_gender_var, values=["Male", "Female"]).pack()

        tk.Label(self, text="Age:").pack()
        self.serves_age_var = tk.IntVar()
        tk.Entry(self, textvariable=self.serves_age_var).pack()

        tk.Label(self, text="Special Status:").pack()
        self.special_status_var = tk.StringVar()
        special_statuses = ["Neither", "Breastfeeding", "Pregnant"]
        ttk.Combobox(self, textvariable=self.special_status_var, values=special_statuses).pack()

        tk.Label(self, text="Activity Level:").pack()
        self.serves_activity_level_var = tk.StringVar()
        activity_levels = [
            "Sedentary",
            "Moderate",
            "Active"
        ]
        ttk.Combobox(self, textvariable=self.serves_activity_level_var, values=activity_levels).pack()

        ttk.Button(self, text="Submit", command=self.calculate_average_serves).pack(pady=10)
        ttk.Button(self, text="Back to Main Menu", command=self.main_menu).pack(pady=10)

    def calculate_average_serves(self):
        gender = self.serves_gender_var.get().lower()
        age = self.serves_age_var.get()
        special_status = self.special_status_var.get().lower()
        activity_level = self.serves_activity_level_var.get().lower()

        if gender and age and special_status and activity_level:
            serves = self.get_serves(gender, age, special_status, activity_level)

            explanation = (
                f"Based on your inputs:\n"
                f"- Gender: {gender.capitalize()}\n"
                f"- Age: {age} years\n"
                f"- Special Status: {special_status.capitalize()}\n"
                f"- Activity Level: {activity_level.capitalize()}\n\n"
                f"The average recommended number of serves per day are:\n{serves}"
            )

            messagebox.showinfo("Average Recommended Number of Serves", explanation)
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields")

    def get_serves(self, gender, age, special_status, activity_level):
        serves = {
            "vegetables": 5,
            "fruit": 2,
            "grains": 6,
            "protein": 2.5,
            "dairy": 2.5,
        }

         # Adjust serves based on gender, age, activity level, and special status
        if gender == "male":
            if 2 <= age <= 3:
                serves.update({"vegetables": 2.5, "fruit": 1, "grains": 4, "protein": 1, "dairy": 1.5})
            elif 4 <= age <= 8:
                serves.update({"vegetables": 4.5, "fruit": 1.5, "grains": 4, "protein": 1.5, "dairy": 2})
            elif 9 <= age <= 13:
                serves.update({"vegetables": 5.5, "fruit": 2, "grains": 5, "protein": 2.5, "dairy": 2.5})
            elif 14 <= age <= 18:
                serves.update({"vegetables": 5.5, "fruit": 2, "grains": 7, "protein": 2.5, "dairy": 3.5})
            elif 19 <= age <= 50:
                serves.update({"vegetables": 6, "fruit": 2, "grains": 6, "protein": 3, "dairy": 2.5})
            elif age > 50:
                serves.update({"vegetables": 5.5, "fruit": 2, "grains": 4.5, "protein": 2.5, "dairy": 2.5})
            if activity_level == "active":
                serves["grains"] += 2

        elif gender == "female":
            if special_status == "neither":
                if 2 <= age <= 3:
                    serves.update({"vegetables": 2.5, "fruit": 1, "grains": 4, "protein": 1, "dairy": 1.5})
                elif 4 <= age <= 8:
                    serves.update({"vegetables": 4.5, "fruit": 1.5, "grains": 4, "protein": 1.5, "dairy": 1.5})
                elif 9 <= age <= 13:
                    serves.update({"vegetables": 5, "fruit": 2, "grains": 5, "protein": 2.5, "dairy": 3})
                elif 14 <= age <= 18:
                    serves.update({"vegetables": 5, "fruit": 2, "grains": 7, "protein": 2.5, "dairy": 3.5})
                elif 19 <= age <= 50:
                    serves.update({"vegetables": 5, "fruit": 2, "grains": 6, "protein": 2.5, "dairy": 2.5})
                elif age > 50:
                    serves.update({"vegetables": 5, "fruit": 2, "grains": 4, "protein": 2, "dairy": 4})
                if activity_level == "active":
                    serves["grains"] += 1

            elif special_status == "pregnant":
                if 14 <= age <= 18:
                    serves.update({"vegetables": 5, "fruit": 2, "grains": 8, "protein": 3.5, "dairy": 3.5})
                elif 19 <= age <= 50:
                    serves.update({"vegetables": 5, "fruit": 2, "grains": 8.5, "protein": 3.5, "dairy": 2.5})
                if activity_level == "active":
                    serves["grains"] += 1

            elif special_status == "breastfeeding":
                if 14 <= age <= 18:
                    serves.update({"vegetables": 7.5, "fruit": 2, "grains": 9, "protein": 2.5, "dairy": 3.5})
                elif 19 <= age <= 50:
                    serves.update({"vegetables": 7.5, "fruit": 2, "grains": 9, "protein": 2.5, "dairy": 2.5})
                if activity_level == "active":
                    serves["grains"] += 1

        return "\n".join([f"- {group.capitalize()}: {serves[group]} serves" for group in serves])

    def get_moving(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Get Moving! Calculator", font=("Helvetica", 16)).pack(pady=20)

        tk.Label(self, text="Select Activity:").pack()
        self.activity_var = tk.StringVar()
        activities = [
            "Walking (3.5 METs)",
            "Running (7 METs)",
            "Bicycling (6 METs)",
            "Swimming (6 METs)",
            "Yoga (2.5 METs)",
            "Hiking (6 METs)",
            "Jogging (7 METs)",
            "Gardening (4 METs)",
            "Badminton (4.5 METs)",
            "Tennis (7.3 METs)",
            "Washing Dishes (1.8 METs)",
            "Cleaning House (3.5 METs)"
        ]
        ttk.Combobox(self, textvariable=self.activity_var, values=activities).pack()

        tk.Label(self, text="Duration (minutes):").pack()
        self.duration_var = tk.IntVar()
        tk.Entry(self, textvariable=self.duration_var).pack()

        ttk.Button(self, text="Calculate Calories Burned", command=self.calculate_calories_burned).pack(pady=10)
        ttk.Button(self, text="Back to Main Menu", command=self.main_menu).pack(pady=10)

    def calculate_calories_burned(self):
        if self.stored_weight and self.activity_var.get() and self.duration_var.get():
            weight = self.stored_weight
            activity = self.activity_var.get()
            duration = self.duration_var.get()

            # Default MET value if not found
            met = 1

            if activity == "Walking (3.5 METs)":
                met = 3.5
            elif activity == "Running (7 METs)":
                met = 7.0
            elif activity == "Bicycling (6 METs)":
                met = 6.0
            elif activity == "Swimming (6 METs)":
                met = 6.0
            elif activity == "Yoga (2.5 METs)":
                met = 2.5
            elif activity == "Hiking (6 METs)":
                met = 6.0
            elif activity == "Jogging (7 METs)":
                met = 7.0
            elif activity == "Gardening (4 METs)":
                met = 4.0
            elif activity == "Badminton (4.5 METs)":
                met = 4.5
            elif activity == "Tennis (7.3 METs)":
                met = 7.3
            elif activity == "Washing Dishes (1.8 METs)":
                met = 1.8
            elif activity == "Cleaning House (3.5 METs)":
                met = 3.5

            # Calculate calories burned
            calories_burned = (met * 3.5 * weight / 200) * duration

            explanation = (
                f"Based on your inputs:\n"
                f"- Activity: {activity}\n"
                f"- Duration: {duration} minutes\n"
                f"- Weight: {weight} kg\n\n"
                f"The estimated calories burned are: {calories_burned:.2f} kcal."
            )

            messagebox.showinfo("Calories Burned", explanation)
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields or calculate your BMI first.")

if __name__ == "__main__":
    app = NutritionCalculator()
    app.mainloop()
