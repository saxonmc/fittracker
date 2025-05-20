from datetime import datetime
import os
import difflib

def main():
    print("Welcome to Fittracker!")
    while True:
        print("\nWhat would you like to do?")
        print("1. Log a new workout")
        print("2. View workout history")
        print("3. View specific exercise history")
        print("4. Exit")

        choice = input('> ')

        if choice == "1":
            log_workout()
        elif choice == "2":
            view_history()
        elif choice == "3":
            search_history_by_exercise()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid. Select a number from 1 to 4.")

def log_workout():
    print("\nWhat type of workout do you want to log?")
    print("1. Lifting")
    print("2. Running")
    workout_type = input("> ").strip()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    if workout_type == "1":
        print("We're logging a lifting session. Enter exercises one at a time.")
        print("Type 'done' when you're finished logging the session.\n")

        session_entries = []

        while True:
            exercise = input("Enter exercise name (or 'done'): ").strip()
            if exercise.lower() == "done":
                break

            weight = input("Weight used: ")
            reps = input("Number of reps completed: ")
            sets = input("Number of sets completed: ")
            rpe = input("RPE on a scale of 1-10: ")

            session_entries.append(f"{exercise} | {weight} | {reps} reps | {sets} sets | {rpe} RPE")

        if session_entries:
            entry_block = f"[{timestamp}] Lifting Workout:\n" + "\n".join(f"  - {e}" for e in session_entries) + "\n\n"
            with open("workouts.txt", "a") as file:
                file.write(entry_block)
            print("✅ Lifting session logged!")
        else:
            print("⚠️ No exercises entered. Nothing saved.")

    elif workout_type == "2":
        distance = input("Distance: ")
        duration = input("Duration: ")
        terrain = input("Terrain (road, trail, treadmill, etc): ")

        entry = f"[{timestamp}] Running | {distance} | {duration} | {terrain} terrain\n"
        with open("workouts.txt", "a") as file:
            file.write(entry)
        print("✅ Run logged!")

    else:
        print("❌ Not an option.")
        input("Press Enter to return to the menu.")
        return

    input("Press Enter to return to the menu.")






def view_history():
    print("\n📓 Workout History\n")

    if not os.path.exists("workouts.txt"):
        print("No workouts logged yet.")
    else:
        with open("workouts.txt", "r") as file:
            content = file.read().strip()

            if not content:
                print("No workouts found.")
            else:
                print(content)
                print("\n" + "-" * 40)

    input("\nPress Enter to return to the menu.")






def search_history_by_exercise():
    print("\n🔍 Search Workout History by Exercise")
    query = input("Enter the exercise you want to see: ").strip().lower()

    if not os.path.exists("workouts.txt"):
        print("No workouts logged yet.")
        return
    
    with open("workouts.txt", "r") as file:
        lines = file.readlines()

    current_timestamp = None
    results = []

    for line in lines:
        line_stripped = line.strip()

         # Detect timestamp line
        if line_stripped.startswith("[") and "Workout" in line_stripped:
            # Extract timestamp portion inside brackets[ ]
            current_timestamp = line_stripped.split("]")[0][1:]
        
        #check for fuzzy match
        if " | " in line_stripped:
            lower_line = line_stripped.lower()
            words = lower_line.split(" | ")[0]
            similarity = difflib.SequenceMatcher(None, query, words).ratio()
            if similarity >= 0.6:
                results.append(f"{current_timestamp} → {line_stripped.strip()}")

    if results:
        print("\n🎯 Matches Found:\n")
        for res in results:
            print(f"- {res}")
        print("\n" + "-" * 40)
    else: 
        print("❌ No matches found for that exercise.")

    input("\nPress Enter to return to the menu.")

if __name__ == "__main__":
    main()